from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="video_categories"),
    url(r'^/search$', views.search, name='search_videos'),
    url(r'/(?P<index>\d+)$', views.play, name='play_video'),
]
