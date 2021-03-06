# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-10 23:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0003_auto_20180408_2144'),
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(help_text='订单', on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='trade.OrderInfo', verbose_name='订单'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('TRADE_SUCCESS', '成功'), ('TRADE_CLOSED', '超时关闭'), ('WAIT_BUYER_PAY', '交易创建'), ('TRADE_FINISHED', '交易结束'), ('paying', '待支付')], default='paying', help_text='支付状态', max_length=15, verbose_name='支付状态'),
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set([('user', 'goods')]),
        ),
    ]
