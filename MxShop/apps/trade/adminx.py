# from django.contrib import admin
import xadmin

from trade.models import *
# Register your models here.

xadmin.site.register(ShoppingCart)  #购物车
xadmin.site.register(OrderInfo)     #订单
xadmin.site.register(OrderGoods)    #订单详情
