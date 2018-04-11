#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'authorlist/$', AuthorList.as_view()),
    url(r'authordetail/(?P<pk>\d*)?/?$', AuthorDetail.as_view()),
    url(r'authorapi/(?P<pk>\d*)?/?$', AuthorApi.as_view()),
]
