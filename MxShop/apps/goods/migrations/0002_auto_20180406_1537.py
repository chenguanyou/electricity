# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 15:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品信息管理', 'verbose_name_plural': '商品信息管理'},
        ),
    ]