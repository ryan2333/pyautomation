#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'index/$', index.as_view()),
    # url(r'^testapi/(?P<pk>\d+)?$', testapi.as_view()),
]