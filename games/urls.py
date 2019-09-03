from django.conf.urls import url
from . import views

app_name = 'games'

urlpatterns = [
    # Handle new and existing games
    url(r'^$', views.Games.as_view()),
    url(r'^(?P<game_id>[0-9]+)/$', views.GameDetails.as_view()),

    # Handle the block endpoints
    url(r'^blocks/(?P<block_id>[0-9]+)/$', views.BlockDetails.as_view()),
]
