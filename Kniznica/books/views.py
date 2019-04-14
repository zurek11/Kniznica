import datetime
import logging
import re

import unidecode
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from register.models import Type, Product, Category, CopyBook, Book, Borrow, StatisticsProductUse


def index(request):
    logged = False
    user_name = ''
    products_list = None
    products = None

    try:
        book_type = Type.objects.get(name='book')
        products_list = Product.objects.filter(type=book_type).order_by('pk')
    except Type.DoesNotExist:
        logging.error('Game category does not exist!')

    categories_list = Category.objects.filter(products__type__name='book').distinct()

    if products_list:
        paginator = Paginator(products_list, 8)
        page = request.GET.get('page')
        products = paginator.get_page(page)

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    return render(request, 'books.html', {'logged': logged, 'user_name': user_name, 'products': products, 'categories_list': categories_list})


def play(request, index):
    logged = False
    user_name = ''

    try:
        product = Product.objects.get(id=index)
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    try:
        book = Book.objects.get(product=product)
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    all_copy_books = CopyBook.objects.filter(book=book)
    available_copy_books = all_copy_books.filter(borrowed=False)
    categories_list = Category.objects.filter(products__type__name='book').distinct()

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
        'book.html',
        {
            'logged': logged,
            'user_name': user_name,
            'product': product,
            'book': book,
            'available_copies': available_copy_books.count(),
            'copies': all_copy_books.count(),
            'categories_list': categories_list
        }
    )


def search(request):
    logged = False
    user_name = ''

    input_text = request.GET.get('input')
    input_voice = request.GET.get('input_voice')
    input_type = request.GET.get('input_type')
    categories = request.GET.getlist('categories')

    try:
        type_obj = Type.objects.get(name='book')
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    products = Product.objects.filter(type=type_obj).order_by('pk')
    categories_list = Category.objects.filter(products__type__name='book').distinct()

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
        'books.html',
        {'logged': logged, 'user_name': user_name, 'products': products, 'categories_list': categories_list}
    )


def borrow(request):
    logged = False
    user_name = ''

    input_borrow_date = None
    input_expire_date = None

    borrow_date_error = None
    expire_date_error = None

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    input_book = request.GET.get('input_book')

    if 'borrow_date' in request.GET:
        input_borrow_date = request.GET.get('borrow_date')
        if not input_borrow_date:
            borrow_date_error = 'Nie je uvedený čas objednania výpožičky.'

    if 'expire_date' in request.GET:
        input_expire_date = request.GET.get('expire_date')
        if not input_expire_date:
            expire_date_error = 'Nie je uvedený čas ukončenia výpožičky.'

    try:
        product = Product.objects.get(id=input_book)
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    try:
        book = Book.objects.get(product=product)
    except Type.DoesNotExist:
        raise Http404('Stránka neexistuje!')

    all_copy_books = CopyBook.objects.filter(book=book)
    available_copy_books = all_copy_books.filter(borrowed=False)
    categories_list = Category.objects.filter(products__type__name='book').distinct()

    if input_borrow_date and input_expire_date:
        borrow_copy_book = available_copy_books.first()

        borrow_day = input_borrow_date[3:5]
        borrow_month = input_borrow_date[0:2]
        borrow_year = input_borrow_date[6:10]
        borrow_hours = input_borrow_date[11:13]
        borrow_minutes = input_borrow_date[14:16]

        expire_day = input_expire_date[3:5]
        expire_month = input_expire_date[0:2]
        expire_year = input_expire_date[6:10]
        expire_hours = input_expire_date[11:13]
        expire_minutes = input_expire_date[14:16]

        Borrow.objects.create(
            user=request.user,
            copy_book=borrow_copy_book,
            borrow_at=datetime.datetime(int(borrow_year), int(borrow_month), int(borrow_day), int(borrow_hours), int(borrow_minutes)),
            expires_at=datetime.datetime(int(expire_year), int(expire_month), int(expire_day), int(expire_hours), int(expire_minutes))
        )
        borrow_copy_book.borrowed = True
        borrow_copy_book.save()

        return render(
            request,
            'book.html',
            {
                'logged': logged,
                'user_name': user_name,
                'product': product,
                'book': book,
                'available_copies': available_copy_books.count(),
                'copies': all_copy_books.count(),
                'categories_list': categories_list,
                'borrow_completed': True
            }
        )

    if borrow_date_error or expire_date_error:
        return render(
            request,
            'borrow.html',
            {
                'logged': logged,
                'user_name': user_name,
                'product': product,
                'book': book,
                'available_copies': available_copy_books.count(),
                'copies': all_copy_books.count(),
                'categories_list': categories_list,
                'borrow_date_error': borrow_date_error,
                'expire_date_error': expire_date_error
            }
        )

    if not available_copy_books:
        return render(
            request,
            'book.html',
            {
                'logged': logged,
                'user_name': user_name,
                'product': product,
                'book': book,
                'available_copies': available_copy_books.count(),
                'copies': all_copy_books.count(),
                'categories_list': categories_list,
                'copy_check': True
            }
        )

    return render(request, 'borrow.html', {'logged': logged, 'user_name': user_name, 'product': product, 'categories_list': categories_list})
