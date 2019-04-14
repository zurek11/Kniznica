from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from register.models import Borrow, Type, StatisticsProductUse, Category
import json
from django.core.serializers.json import DjangoJSONEncoder


def return_book(request):
    products = []
    identification = request.GET.get('id')

    if request.user.is_authenticated:
        logged = True
        user_name = request.user

        user_borrows = Borrow.objects.filter(user=user_name)

        if identification:
            borrow = user_borrows.get(pk=int(identification))
            borrow.deleted_at = timezone.now()
            borrow.copy_book.borrowed = False
            borrow.save()

            for borrow in user_borrows:
                products.append(borrow.copy_book.book.product)

            return render(
                request,
                'user_borrow.html',
                {'logged': logged, 'user_name': user_name, 'products': zip(products, user_borrows)}
            )
        else:
            for borrow in user_borrows:
                products.append(borrow.copy_book.book.product)

            return render(
                request,
                'user_borrow.html',
                {'logged': logged, 'user_name': user_name, 'products': zip(products, user_borrows)}
            )
    else:
        raise Http404('Stránka neexistuje')


def statistics(request):
    if request.user.is_authenticated:
        logged = True
        user_name = request.user

        types = Type.objects.all().values_list('name').exclude(name='news')
        statistics = StatisticsProductUse.objects.filter(user=user_name)
        borrows = Borrow.objects.filter(user=user_name)

        statistics_types_count = []
        statistics_book_category_count = []
        statistics_game_category_count = []
        statistics_video_category_count = []
        statistics_song_category_count = []
        statistics_book_borrow_count = []

        categories_books = Category.objects.filter(products__type__name='book').values_list('name').distinct()
        categories_games = Category.objects.filter(products__type__name='game').values_list('name').distinct()
        categories_videos = Category.objects.filter(products__type__name='video').values_list('name').distinct()
        categories_songs = Category.objects.filter(products__type__name='song').values_list('name').distinct()
        categories_borrow_books = Category.objects.filter(products__type__name='book').values_list('name').distinct()

        for type in types:
            count = statistics.filter(product__type__name=type[0]).aggregate(Count('counter'))
            if count.get('counter__count') > 0:
                statistics_types_count.append(count)
            else:
                types = types.exclude(name=type[0])

        for category in categories_books:
            count = statistics.filter(product__category__name=category[0]).aggregate(Count('counter'))
            if count.get('counter__count') > 0:
                statistics_book_category_count.append(count)
            else:
                categories_books = categories_books.exclude(name=category[0])

        for category in categories_games:
            count = statistics.filter(product__category__name=category[0]).aggregate(Count('counter'))
            if count.get('counter__count') > 0:
                statistics_game_category_count.append(count)
            else:
                categories_games = categories_games.exclude(name=category[0])

        for category in categories_videos:
            count = statistics.filter(product__category__name=category[0]).aggregate(Count('counter'))
            if count.get('counter__count') > 0:
                statistics_video_category_count.append(count)
            else:
                categories_videos = categories_videos.exclude(name=category[0])

        for category in categories_songs:
            count = statistics.filter(product__category__name=category[0]).aggregate(Count('counter'))
            if count.get('counter__count') > 0:
                statistics_song_category_count.append(count)
            else:
                categories_songs = categories_songs.exclude(name=category[0])

        for category in categories_borrow_books:
            count = borrows.filter(copy_book__book__product__category__name=category[0]).count()
            if count > 0:
                statistics_book_borrow_count.append(count)
            else:
                categories_borrow_books = categories_borrow_books.exclude(name=category[0])

        types_json = json.dumps(list(types), cls=DjangoJSONEncoder)
        categories_books_json = json.dumps(list(categories_books), cls=DjangoJSONEncoder)
        categories_games_json = json.dumps(list(categories_games), cls=DjangoJSONEncoder)
        categories_videos_json = json.dumps(list(categories_videos), cls=DjangoJSONEncoder)
        categories_songs_json = json.dumps(list(categories_songs), cls=DjangoJSONEncoder)
        categories__borrow_books_json = json.dumps(list(categories_borrow_books), cls=DjangoJSONEncoder)

        statistics_types = json.dumps([index['counter__count'] for index in statistics_types_count],
                                      cls=DjangoJSONEncoder)
        statistics_book_category = json.dumps([index['counter__count'] for index in statistics_book_category_count],
                                              cls=DjangoJSONEncoder)
        statistics_game_category = json.dumps([index['counter__count'] for index in statistics_game_category_count],
                                              cls=DjangoJSONEncoder)
        statistics_video_category = json.dumps([index['counter__count'] for index in statistics_video_category_count],
                                              cls=DjangoJSONEncoder)
        statistics_song_category = json.dumps([index['counter__count'] for index in statistics_song_category_count],
                                              cls=DjangoJSONEncoder)
        statistics_book_borrow = json.dumps(statistics_book_borrow_count, cls=DjangoJSONEncoder)

        return render(
            request,
            'statistics.html',
            {
                'logged': logged,
                'user_name': user_name,
                'types': types_json,
                'categories_books': categories_books_json,
                'categories_games': categories_games_json,
                'categories_videos': categories_videos_json,
                'categories_songs': categories_songs_json,
                'categories_borrow_books': categories__borrow_books_json,
                'statistics_types': statistics_types,
                'statistics_book_category': statistics_book_category,
                'statistics_game_category': statistics_game_category,
                'statistics_video_category': statistics_video_category,
                'statistics_song_category': statistics_song_category,
                'statistics_book_borrow': statistics_book_borrow
            }
        )
    else:
        raise Http404('Stránka neexistuje')
