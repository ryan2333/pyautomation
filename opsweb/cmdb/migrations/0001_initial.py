# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 03:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u5206\u7c7b\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u5206\u7c7b',
                'verbose_name_plural': '\u8d44\u4ea7\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='AssetIDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('address', models.CharField(max_length=128, verbose_name='\u673a\u623f\u5730\u5740')),
                ('sales_name', models.CharField(max_length=16, verbose_name='\u9500\u552e\u59d3\u540d')),
                ('sales_phone', models.CharField(max_length=16, verbose_name='\u9500\u552e\u7535\u8bdd')),
                ('customer_name', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u5ba2\u670d\u540d\u79f0')),
                ('customer_phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u5ba2\u670d\u7535\u8bdd')),
                ('rental_pods', models.CharField(max_length=128, verbose_name='\u79df\u7528\u673a\u67dc')),
                ('bandwidth', models.CharField(max_length=16, verbose_name='\u79df\u7528\u5e26\u5bbd')),
                ('contract_id', models.CharField(max_length=32, verbose_name='\u5408\u540c\u7f16\u53f7')),
            ],
            options={
                'verbose_name': 'IDC\u4fe1\u606f',
                'verbose_name_plural': 'IDC\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='AssetVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='\u5382\u5546\u540d\u79f0')),
                ('sales_name', models.CharField(max_length=16, verbose_name='\u9500\u552e\u59d3\u540d')),
                ('sales_phone', models.CharField(max_length=16, verbose_name='\u9500\u552e\u7535\u8bdd')),
                ('tech_name', models.CharField(max_length=16, verbose_name='\u6280\u672f\u59d3\u540d')),
                ('tech_phone', models.CharField(max_length=16, verbose_name='\u6280\u672f\u7535\u8bdd')),
            ],
            options={
                'verbose_name': '\u5382\u5546\u4fe1\u606f',
                'verbose_name_plural': '\u5382\u5546\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='PhysicalDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='\u8bbe\u5907\u540d\u79f0')),
                ('brand', models.CharField(max_length=16, verbose_name='\u8bbe\u5907\u54c1\u724c')),
                ('model', models.CharField(max_length=64, verbose_name='\u8bbe\u5907\u578b\u53f7')),
                ('operation_system', models.CharField(max_length=64, verbose_name='\u64cd\u4f5c\u7cfb\u7edf')),
                ('mgrip', models.CharField(max_length=16, verbose_name='\u7ba1\u7406IP\u5730\u5740')),
                ('ip1', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u7f51\u53611IP')),
                ('ip2', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u7f51\u53612IP')),
                ('ip3', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u7f51\u53613IP')),
                ('ip4', models.CharField(blank=True, max_length=16, null=True, verbose_name='\u7f51\u53614IP')),
                ('mac1', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u7f51\u53611MAC')),
                ('mac2', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u7f51\u53612MAC')),
                ('mac3', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u7f51\u53613MAC')),
                ('mac4', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u7f51\u53614MAC')),
                ('sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u8bbe\u5907\u5e8f\u5217\u53f7')),
                ('asset_number', models.CharField(blank=True, max_length=32, null=True, verbose_name='\u8d44\u4ea7\u7f16\u53f7')),
                ('asset_cab', models.CharField(max_length=16, verbose_name='\u8bbe\u5907\u6240\u5728\u673a\u67dc')),
                ('asset_cab_location', models.CharField(max_length=16, verbose_name='\u8bbe\u5907\u6240\u5728\u673a\u67dc\u4f4d\u7f6e')),
                ('asset_owner_dep', models.CharField(max_length=32, verbose_name='\u8bbe\u5907\u6240\u6709\u90e8\u95e8')),
                ('asset_manage_dep', models.CharField(max_length=32, verbose_name='\u8bbe\u5907\u7ba1\u7406\u90e8\u95e8')),
                ('asset_use_dep', models.CharField(max_length=32, verbose_name='\u8bbe\u5907\u4f7f\u7528\u90e8\u95e8')),
                ('purchase_date', models.DateField(verbose_name='\u91c7\u8d2d\u65e5\u671f')),
                ('decription', models.TextField(max_length=255, verbose_name='\u8bbe\u5907\u63cf\u8ff0')),
                ('asset_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u8bbe\u5907\u7ba1\u7406\u5458')),
                ('asset_idc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.AssetIDC', verbose_name='\u8bbe\u5907\u6240\u5728IDC')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.AssetCategory', verbose_name='\u8d44\u4ea7\u5206\u7c7b')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.AssetVendor', verbose_name='\u91c7\u8d2d\u5382\u5546')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u7269\u7406\u8d44\u4ea7\u4fe1\u606f',
                'verbose_name_plural': '\u7269\u7406\u8d44\u4ea7\u4fe1\u606f',
            },
        ),
    ]
