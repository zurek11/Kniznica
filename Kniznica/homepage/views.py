import logging
from django.core.paginator import Paginator
from django.shortcuts import render
from register.models import Type, Product


def index(request):
    logged = False
    user_name = ''
    news_list = None
    news = None

    try:
        news_type = Type.objects.get(name='news')
        news_list = Product.objects.filter(type=news_type).order_by('pk')
    except Type.DoesNotExist:
        logging.error('Game category does not exist!')

    if news_list:
        paginator = Paginator(news_list, 8)
        page = request.GET.get('page')
        news = paginator.get_page(page)

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

    return render(request, 'homepage.html', {'logged': logged, 'user_name': user_name, 'news': news})
