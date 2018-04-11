# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pymkAes import prpcrypt

# Create your models here.
class passmgr(models.Model):
    account = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    bpasswd1 = models.CharField(max_length=64, default='')
    bpasswd2 = models.CharField(max_length=64, default='')
    bpasswd3 = models.CharField(max_length=64, default='')
    host = models.CharField(max_length=64, default='')
    descript = models.CharField(max_length=255, default='')

    @property
    def todict(self):
        ret = dict()
        for attr in self._meta.fields:
            fieldname = attr.name
            fieldvalue = getattr(self,fieldname)
            ret[fieldname] = fieldvalue
        return ret

    def __unicode__(self):
        return self.account

