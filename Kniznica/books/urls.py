from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('/getBooks', views.get_books, name="getBooks"),
    path('/showBooks', views.show_books, name="showBooks"),
]
