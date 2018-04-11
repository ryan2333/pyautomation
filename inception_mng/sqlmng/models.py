# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    """基础表（抽象类）"""
    name = models.CharField(max_length=64, verbose_name="名字")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    note = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['-id']

class DBConf(BaseModel):
    GENDER_CHOICES = (
        ('1', u'生产'),
        ('2', u'测试'),
    )
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    host = models.CharField(max_length=16)
    port = models.CharField(max_length=5)
    env = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)

class InceptSql(BaseModel):
    SQL_STATUS = (
        (-3, u'已回滚'),
        (-2, u'已暂停'),
        (-1, u'待执行'),
        (0, u'已执行'),
        (1, u'已放弃'),
        (2, u'执行失败'),
    )

    ENV = (
        (1, u'生产环境'),
        (2, u'测试环境')
    )

    sqluser = models.ManyToManyField(User)
    commiter = models.CharField(max_length=32) #提交人
    sqlcontent = models.TextField(blank=True, null=True) #sql内容
    env = models.IntegerField(choices=ENV) #环境
    dbname = models.CharField(max_length=50) #目标数据库
    treater = models.CharField(max_length=20) #挂靠人
    # treater = models.ManyToManyField(User)  # 挂靠人
    status = models.IntegerField(default=-1, choices=SQL_STATUS) #sql执行状态
    executerz = models.TextField(default='', null=True, blank=True) #sql执行结果
    exe_affected_rows = models.CharField(max_length=10) # 执行影响的行数
    roll_affected_rows = models.CharField(max_length=10) #回滚影响的行数
    rollbackopid = models.TextField(blank=True, null=True) #回滚的id
    rollbackdb = models.CharField(max_length=100) # 回滚的数据库