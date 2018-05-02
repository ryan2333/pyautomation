# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from dashboard.models import UserProfile

# Create your models here.

class AssetCategory(models.Model):
    '''
    资产分类
    '''
    name = models.CharField(max_length=32, verbose_name='分类名称')

    class Meta:
        verbose_name = '资产分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AssetIDC(models.Model):
    '''
    IDC信息
    '''
    name = models.CharField(max_length=32, verbose_name='机房名称')
    address = models.CharField(max_length=128, verbose_name='机房地址')
    sales_name = models.CharField(max_length=16, verbose_name='销售姓名')
    sales_phone = models.CharField(max_length=16, verbose_name='销售电话')
    customer_phone = models.CharField(max_length=16, verbose_name='客服电话', null=True, blank=True)
    rental_pods = models.CharField(max_length=128, verbose_name='租用机柜')
    bandwidth = models.CharField(max_length=16, verbose_name='租用带宽')
    pod_cost = models.IntegerField(verbose_name="机柜费用", null=True,blank=True)
    bandwidth_cost = models.IntegerField(verbose_name="带宽费用", null=True,blank=True)
    contract_id = models.CharField(max_length=32, verbose_name='合同编号', default='', null=True, blank=True)

    class Meta:
        verbose_name = 'IDC信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AssetVendor(models.Model):
    name = models.CharField(max_length=16, verbose_name='厂商名称')
    sales_name = models.CharField(max_length=16, verbose_name='销售姓名')
    sales_phone = models.CharField(max_length=16, verbose_name='销售电话')
    tech_name = models.CharField(max_length=16, verbose_name='技术姓名')
    tech_phone = models.CharField(max_length=16, verbose_name='技术电话')

    class Meta:
        verbose_name = '厂商信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class PhysicalDevice(models.Model):
    '''
    设备信息
    '''
    DEVICE_STATUS = (
        (0,'正常'),
        (1, '已报废')
    )

    name = models.CharField(max_length=16, verbose_name='设备名称')
    vendor = models.CharField(max_length=16, verbose_name='设备厂商')
    model = models.CharField(max_length=64, verbose_name='设备型号')
    category = models.ForeignKey(AssetCategory, verbose_name='资产分类')
    operation_system = models.CharField(max_length=64, verbose_name='操作系统')
    mgrip = models.CharField(max_length=16, verbose_name='管理IP地址')
    ip1 = models.CharField(max_length=16, null=True, blank=True, verbose_name='网卡1IP')
    ip2 = models.CharField(max_length=16, null=True, blank=True, verbose_name='网卡2IP')
    ip3 = models.CharField(max_length=16, null=True, blank=True, verbose_name='网卡3IP')
    ip4 = models.CharField(max_length=16, null=True, blank=True, verbose_name='网卡4IP')
    mac1 = models.CharField(max_length=32, null=True, blank=True, verbose_name='网卡1MAC')
    mac2 = models.CharField(max_length=32, null=True, blank=True, verbose_name='网卡2MAC')
    mac3 = models.CharField(max_length=32, null=True, blank=True, verbose_name='网卡3MAC')
    mac4 = models.CharField(max_length=32, null=True, blank=True, verbose_name='网卡4MAC')
    sn = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备序列号', unique=True)
    asset_number = models.CharField(max_length=32, null=True, blank=True, verbose_name='资产编号')
    asset_idc = models.ForeignKey(AssetIDC, null=True, blank=True, verbose_name='设备所在IDC')
    asset_cab = models.CharField(max_length=16, null=True, blank=True, verbose_name='设备所在机柜')
    asset_cab_location = models.CharField(max_length=16, null=True, blank=True, verbose_name='设备所在机柜位置')
    asset_owner_dep = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备所有部门')
    asset_manage_dep = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备管理部门')
    asset_use_dep = models.CharField(max_length=32, null=True, blank=True, verbose_name='设备使用部门')
    asset_admin = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='设备管理员')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='采购日期')
    decription = models.TextField(max_length=255, null=True, blank=True, verbose_name='设备描述')
    status = models.IntegerField(choices=DEVICE_STATUS, default=0, verbose_name='设备状态')

    class Meta:
        verbose_name = '物理资产信息'
        verbose_name_plural = verbose_name
        ordering = [ 'status','name']

    def __unicode__(self):
        return self.name