from django.conf.urls import url
from . import views

app_name = 'games'

urlpatterns = [

    # User authentication
    url(r'^$', views.Games.as_view()),
    # url(r'^login/$', controller.CustomObtainAuthToken.as_view()),
]
