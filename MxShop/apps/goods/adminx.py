# from django.contrib import admin
# Register your models here.

import xadmin

from goods.models import *

class GoodsAdmins(object):
    list_display = ["category","goods_sn","name","click_num","sold_num"]
    search_fields = ["name"]
    list_filter = ["category","goods_sn","name","click_num","sold_num"]
    ordering = ["-add_time"] #按照点击人数最多的进行排序
    style_fields = {"goods_desc":"ueditor"} #使用富文本编辑器


xadmin.site.register(GoodsCategory)     #商品类别
xadmin.site.register(GoodsCategoryBrand)       #商品品牌管理
xadmin.site.register(Goods, GoodsAdmins)     #商品信息
xadmin.site.register(GoodsImage)    #商品轮播图管理
xadmin.site.register(Banner)    #首页轮播图管理
xadmin.site.register(IndexAD)   #首页商品广告
