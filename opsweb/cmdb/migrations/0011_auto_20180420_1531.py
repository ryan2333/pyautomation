# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-20 07:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0010_auto_20180420_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='physicaldevice',
            options={'ordering': ['status', '-category'], 'verbose_name': '\u7269\u7406\u8d44\u4ea7\u4fe1\u606f', 'verbose_name_plural': '\u7269\u7406\u8d44\u4ea7\u4fe1\u606f'},
        ),
    ]
