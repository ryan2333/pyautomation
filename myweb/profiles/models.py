# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('0', u'无'),
        ('1', u'总监'),
        ('2', u'经理'),
        ('3', u'研发'),
    )
    user = models.OneToOneField(User, primary_key= True)
    phone = models.CharField(max_length=11, default='', blank=True)
    role = models.CharField(max_length=1,default='0',blank=True, choices=GENDER_CHOICES)
    note = models.CharField(max_length=128,default='',blank=True)

    def __unicode__(self):
        return self.role

@receiver(post_save, sender=User)
def create_save_user(sender, **kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if instance.is_superuser:
        return True
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
