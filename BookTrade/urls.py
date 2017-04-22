from django.conf.urls import url
from django.contrib import admin

from . import book
from . import data

urlpatterns = [
    url(r'^sale/$', book.add),
    url(r'^newest_data/$', data.ajax_newest),
    url(r'^details.*/$', book.details),
    url(r'^submit_trade/$', data.ajax_trade),
    url(r'^account_booksell/$', data.account_booksell),
    url(r'^account_bookbuy/$', data.account_bookbuy),
    url(r'^search_data/$', data.search_data),
]