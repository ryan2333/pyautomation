# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20180419_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetidc',
            name='contract_id',
            field=models.CharField(default='', max_length=32, verbose_name='\u5408\u540c\u7f16\u53f7'),
        ),
    ]
