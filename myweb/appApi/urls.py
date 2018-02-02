#-*- coding:utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^testapi/(?P<pk>\d+)?$', testapi.as_view()),
    url(r'^testapiPage/(?P<pk>\d+)?$', testapi1.as_view()),
]