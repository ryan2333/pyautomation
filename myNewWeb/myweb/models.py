# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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

class Publish(models.Model):
    name = models.CharField(max_length=32, default=u'')
    note = models.TextField(default='test')
    title = models.CharField(max_length=32, default='tele')
    city = models.CharField(max_length=32, default=u'北京市')

    def __unicode__(self): #在python3中，用__str__代替__unicode__
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=16,default='')
    address = models.CharField(max_length=64, null=True,blank=True)
    phone = models.CharField(max_length=16,default='')
    fans = models.IntegerField(default=0)
    income = models.IntegerField(default=0)

    @property  # property装方法当成一个属性调用
    def todict(self):  # 通过models_to_dict方法获取数据库数据，并返回前端JSON字符串
        # exclude = ['id']
        include = ['name', 'address', 'phone']
        ret = dict()
        ret['books'] = [{'id':i.id,'bookname':i.name,'Publish':i.publish.name,'price':i.price} for i in self.book2_set.all()]

        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self, fieldname)
            if fieldname not in include:continue
            if fieldname == 'phone':
                if fieldvalue and len(fieldvalue) ==11:
                    fieldvalue = fieldvalue[0:3]+'****'+fieldvalue[8:] #隐藏中间四位手机号
            ret[fieldname] = fieldvalue
        return ret


    def __unicode__(self): #在python3中，用__str__代替__unicode__
        return self.name

class Book2(Book1):
    publish = models.ForeignKey(Publish,null=True,blank=True)
    author = models.ManyToManyField("Author",null=True,blank=True)

    @property
    def priceplus(self):
        return self.price + 1

    @property  #property装方法当成一个属性调用
    def todict(self):  #通过models_to_dict方法获取数据库数据，并返回前端JSON字符串
        # exclude = ['id']
        include = ['name','price','title']
        ret = dict()
        ret['author'] = [{'Author': i.name} for i in self.author.all()] #多对多链表查询返回
        ret['publish'] = self.publish.name
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self,fieldname)
            if fieldname in include:
                ret[fieldname] = fieldvalue
        return ret

    class Meta:
        verbose_name = 'Book2'