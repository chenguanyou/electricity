# from django.contrib import admin
import xadmin

from user_operation.models import *
# Register your models here.
xadmin.site.register(UserFav)   #用户收藏
xadmin.site.register(UserLeavingMesage)     #用户留言
xadmin.site.register(UserAddress)   #用户收获地址