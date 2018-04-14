# from django.contrib import admin
import xadmin
from xadmin import views

from users.models import *

#让xadmin后台支持主题选择
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#修改xadmin的头部和底部信息
class GlobalSetting(object):
    site_title = "商店管理系统"
    site_footer = "商店管理系统"
    menu_style = "accordion" #把App收缩起来

# class UserProFileClass(object):
#     list_display = ["name", "birthay", "mobile", "gender", "email", "add_time"]  # 后台显示类型
#     search_fields = ["name", "birthay", "mobile", "gender", "email"]  # 设置搜索
#     list_filter = ["name", "birthay", "mobile", "gender", "email"]  # 搜索过滤器
#     model_icon = "fa fa-envelope"  # 这样可以替换与设置原有的Xadmin的图标


# xadmin.site.unregister(UserProFile)
# xadmin.site.register(UserProFile, UserProFileClass)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(VerifyCode)
xadmin.site.register(views.CommAdminView, GlobalSetting)

