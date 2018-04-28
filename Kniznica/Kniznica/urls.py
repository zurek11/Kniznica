from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('detska-kniznica', include('homepage.urls')),
    path('detska-kniznica/admin', admin.site.urls),
    path('detska-kniznica/games', include('games.urls')),
    path('detska-kniznica/books', include('books.urls')),
    path('detska-kniznica/register', include('register.urls')),
    path('detska-kniznica/login', include('login.urls')),
]
