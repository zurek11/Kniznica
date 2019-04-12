from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    url(r'^/search$', views.search, name='search_books'),
    url(r'^/borrow$', views.borrow, name='borrow_book'),
    url(r'/(?P<index>\d+)$', views.play, name='play_book')
]
