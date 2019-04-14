import logging
import re

import unidecode
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from register.models import Type, Product, Category, StatisticsProductUse


def index(request):
    logged = False
    user_name = ''
    products_list = None
    products = None

    try:
        game_type = Type.objects.get(name='game')
        products_list = Product.objects.filter(type=game_type).order_by('pk')
    except Type.DoesNotExist:
        logging.error('Game category does not exist!')

    categories_list = Category.objects.filter(products__type__name='game').distinct()

    if products_list:
        paginator = Paginator(products_list, 8)
        page = request.GET.get('page')
        products = paginator.get_page(page)

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    return render(
        request,
        'games.html',
        {'logged': logged, 'user_name': user_name, 'products': products, 'categories_list': categories_list}
    )


def play(request, index):
    logged = False
    user_name = ''

    try:
        product = Product.objects.get(id=index)
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    categories_list = Category.objects.filter(products__type__name='game').distinct()

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
        'game.html',
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
        type_obj = Type.objects.get(name='game')
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    products = Product.objects.filter(type=type_obj).order_by('pk')
    categories_list = Category.objects.filter(products__type__name='game').distinct()

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
        'games.html',
        {'logged': logged, 'user_name': user_name, 'products': products, 'categories_list': categories_list}
    )
