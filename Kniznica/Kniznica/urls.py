from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from Kniznica import views

urlpatterns = [
    path('detska-kniznica', include('homepage.urls'), name='news'),
    path('detska-kniznica/games', include('games.urls'), name='games'),
    path('detska-kniznica/books', include('books.urls'), name='books'),
    path('detska-kniznica/videos', include('video.urls'), name='videos'),
    path('detska-kniznica/songs', include('songs.urls'), name='songs'),

    path('detska-kniznica/register', include('register.urls'), name='register'),
    path('detska-kniznica/login', include('login.urls'), name='login'),

    url(r'^detska-kniznica/return$', views.return_book, name='return_books'),
    url(r'^detska-kniznica/statistics$', views.statistics, name='statistics'),

    path('detska-kniznica/admin', admin.site.urls, name='admin'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
]
