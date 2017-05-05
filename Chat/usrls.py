from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^chat/$', views.chat_view),
    url(r'^getchat/$', views.chat_data),
    url(r'^postchat/$', views.chat_post),
]