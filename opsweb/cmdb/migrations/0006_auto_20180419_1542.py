# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_auto_20180419_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetidc',
            name='contract_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='\u5408\u540c\u7f16\u53f7'),
        ),
    ]
