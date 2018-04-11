#-*- coding: utf-8 -*-

from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'passlist/?', passList.as_view()),
    url(r'passdetail/(?P<pk>\d*)?/?$',passDetail.as_view()),
    url(r'passapi/(?P<pk>\d*)?/?$', passApi.as_view()),
]