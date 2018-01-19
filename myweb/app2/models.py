# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
import django.utils.timezone as timezone

# Create your models here.


class Book1(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField(default=10)
    pub_date = models.DateField(auto_now=True)
    note = models.TextField(default='test')
    title = models.CharField(max_length=32,default='tele')

    def __unicode__(self): #在python3中，用__str__代替__unicode__
        return self.name

    class Meta:
        #abstract = True #抽象类,不产生表，其它表来继承此表
        ordering = ['name'] #排序，反序加-号
        # verbose_name = 'Book'
        abstract = True

class Book2(Book1):
    writer = models.CharField(max_length=32)

    @property
    def priceplus(self):
        return self.price + 1

    @property  #property装方法当成一个属性调用
    def todict(self):  #通过models_to_dict方法获取数据库数据，并返回前端JSON字符串
        exclude = ['id']
        ret = dict()
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self,fieldname)
            if fieldname in exclude:
                continue
            ret[fieldname] = fieldvalue
        return ret

    class Meta:
        verbose_name = 'Book2'