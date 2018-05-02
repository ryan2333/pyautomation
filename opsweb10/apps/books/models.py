# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Publish(models.Model):
    name = models.CharField(max_length=32, verbose_name='出版社名称')
    address = models.CharField(max_length=64, verbose_name='出版社地址')
    city = models.CharField(max_length=32, verbose_name='出版社城市')

    class Meta:
        verbose_name = '出版社信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name='作者名称')
    email = models.EmailField(verbose_name='作者邮箱')
    phone = models.CharField(max_length=16, verbose_name='作者电话', null=True, blank=True)

    class Meta:
        verbose_name = '作者信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Book(models.Model):
    name = models.CharField('书名',max_length=96)
    authors = models.ManyToManyField(Author, verbose_name='作者')
    publisher = models.ForeignKey(Publish,verbose_name='出版社')
    publication_date = models.DateField("出版时间")

    class Meta:
        verbose_name = '图书信息'
        verbose_name_plural = verbose_name
        ordering = ['-publication_date']

    def __unicode__(self):
        return self.name