import re

import unidecode
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from register.models import Category, Type, Product, StatisticsProductUse


def index(request):
    logged = False
    user_name = ''

    categories_list = Category.objects.filter(products__type__name='song').distinct()

    if not categories_list:
        raise Http404('Stránka neexistuje!')
    else:
        paginator = Paginator(categories_list, 8)
        page = request.GET.get('page')
        categories = paginator.get_page(page)

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    return render(
        request,
        'songs_select.html',
        {'logged': logged, 'user_name': user_name, 'categories': categories, 'categories_list': categories_list}
    )


def play(request, index):
    logged = False
    user_name = ''

    try:
        product = Product.objects.get(id=index)
    except Category.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    categories_list = Category.objects.filter(products__type__name='song').distinct()

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

        try:
            statistic = StatisticsProductUse.objects.get(user=user_name, product=product)
            statistic.counter += 1
            statistic.save()
        except StatisticsProductUse.DoesNotExist:
            StatisticsProductUse.objects.create(
                user=user_name,
                product=product,
                counter=1
            )

    return render(
        request,
        'song.html',
        {'logged': logged, 'user_name': user_name, 'product': product, 'categories_list': categories_list}
    )


def search(request):
    logged = False
    user_name = ''

    input_text = request.GET.get('input')
    input_voice = request.GET.get('input_voice')
    input_type = request.GET.get('input_type')
    categories = request.GET.getlist('categories')

    try:
        type_obj = Type.objects.get(name='song')
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    products = Product.objects.filter(type=type_obj).order_by('pk')
    categories_list = Category.objects.filter(products__type__name='song').distinct()

    if input_text:
        if input_type == 'title':
            products = products.filter(title__icontains=input_text)
        elif input_type == 'author':
            products = products.filter(author__icontains=input_text)
        elif input_type == 'publisher':
            products = products.filter(publlisher__icontains=input_text)

    elif input_voice:
        input_voice = input_voice.lower()
        input_voice = re.findall(r"[\w']+", input_voice)
        for voice_word in input_voice:
            products = products.filter(category__name__icontains=unidecode.unidecode(voice_word))

    if categories:
        products = products.filter(category__name__in=categories)

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    return render(
        request,
        'songs.html',
        {'logged': logged, 'user_name': user_name, 'products': products, 'categories_list': categories_list}
    )
