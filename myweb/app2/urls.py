#-*- coding:utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^hello',hello),
    url(r'users/(\d+)',helloNumber), #隐式参数
    url(r'add/(\d{1,3})/(\d{1,3})', add) , #两个隐式参数
    url(r'add1/(?P<n1>\d+)/(?P<n2>\d+)', add1), #显示参数
    url(r'argstest',argstest), #http://10.13.3.18:9000/app1/argstest/?n1=122&n2=233
    # url(r'index', index1)
    url(r'book',bookQuery)
]