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
    note = models.TextField(default='')
    title = models.CharField(max_length=32,default='')

    def __unicode__(self): #在python3中，用__str__代替__unicode__
        return self.name

    class Meta:
        abstract = True #抽象类，不产生表，用作其它表继承
        ordering = ['name'] #排序，反序加-号
        verbose_name = '表名'
        permissions = ()