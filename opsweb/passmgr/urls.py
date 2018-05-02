from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'passlist/?', passList.as_view(), name='passlist'),
    url(r'passdetail/(?P<pk>\d*)?/?$',passDetail.as_view(), name='passdetail'),
    url(r'passapi/(?P<pk>\d*)?/?$', passApi.as_view(), name='passapi'),
]