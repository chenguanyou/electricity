# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-14 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180414_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscategorybrand',
            name='goodscate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategory', verbose_name='商品类别'),
        ),
    ]