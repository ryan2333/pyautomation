# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Myusers(models.Model):
    name = models.CharField(max_length=20)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name