#-*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *
from cmdb import categroy, idc, physicaldevice



urlpatterns = [
    url(r'^physicallist/?$',physicaldevice.physicalListView.as_view(), name='physical_list'),
    url(r'^physicaldetail/(?P<pk>\d+)?/?$',physicaldevice.physicalDetailView.as_view(), name='physical_detail'),

    url(r'^idclist/?$',idc.IdcListView.as_view(), name='idc_list'),
    url(r'^idcdetail/(?P<pk>\d+)?/?$',idc.IdcDetailView.as_view(), name='idc_detail'),

    url(r'^vendorlist/?$',physicaldevice.physicalListView.as_view(), name='vendor_list'),
    url(r'^vendordetail/(?P<pk>\d+)?/?$',physicaldevice.physicalListView.as_view(), name='vendor_detail'),

    url(r'^assetcategorylist/?$',categroy.AssetCategoryListView.as_view(), name='assetcategory_list'),
    url(r'^assetcategorydetail/(?P<pk>\d+)?/?$',categroy.AssetCategoryDetailView.as_view(), name='assetcategory_detail'),

    url(r'^assetcabselect/?$', physicaldevice.AssetCab.as_view()),
]
