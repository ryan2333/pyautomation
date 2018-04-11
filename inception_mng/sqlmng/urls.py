#-*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'inception_commit',InceptionCommit.as_view()),
    url(r'dbconfig/(?P<pk>\d)?/?$', DBConfig.as_view()),
    url(r'autoselect/?$', AutoSelect.as_view()),
    url(r'^inception_result/(?P<pk>\d+)?/?(?P<actiontype>\w+)?/?$', inception_result.as_view(), name='inception_result'),
]

