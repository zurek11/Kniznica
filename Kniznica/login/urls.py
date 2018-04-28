from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/logUser', views.log_user),
    path('/logOut', views.log_out_user),
]
