"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.static import serve
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.authtoken import views  # 获取TOKEN_URL
from rest_framework.documentation import include_docs_urls  # django_rest_formework的api文档
from rest_framework_jwt.views import obtain_jwt_token  # jwt的认证

import xadmin
from MxShop.settings import MEDIA_ROOT, MEDIA_URL  # , #STATIC_ROOT  # , #STATIC_ROOT, DEBUG#用于生产环境

from trade.views import ShoppingCartViewset, OrderViewset, AliPayViewset
from users.views import SmsCodeViewSite, UserViewset
from user_operation.views import UserFavViewSet, LeavingMessageViewset, AdderssViewset
from goods.views import GoodsListViewset, CategoryViewset, BannerViewset, IndexCategoryViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# 商品列表url页面，分页搜索，过滤，排序
router.register(r'goods', GoodsListViewset, base_name='goods')

# 商品分类的列表url数据
router.register(r'categorys', CategoryViewset, base_name='categorys')

# 短信注册验证码
router.register(r'code', SmsCodeViewSite, base_name='code')

# 短信注册验证码
router.register(r'users', UserViewset, base_name='users')

# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

# 用户留言
router.register(r'messages', LeavingMessageViewset, base_name='messages')

# 用户地址
router.register(r'address', AdderssViewset, base_name='address')

# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 订单信息
router.register(r'orders', OrderViewset, base_name="orders")

# 首页轮播图
router.register(r'banners', BannerViewset, base_name="banners")

# 首页商品分类
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")
urlpatterns = [
                  # url(r'^admin/', admin.site.urls),
                  url(r'^xadmin/', include(xadmin.site.urls)),
                  url(r'api-token-auth/', views.obtain_auth_token),  # Rest自带的认证模式
                  url(r'^login/$', obtain_jwt_token),  # jwt的认证模式
                  url(r'^ueditor/', include('DjangoUeditor.urls')),  # 富文本url
                  url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 配置在生产环境下的图片不能访问的问题
                  # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),  # 配置在生产环境下的静态样式不能访问的问题
                  url(r'^', include(router.urls)),  # url配置
                  # DRF的文档
                  url(r'^docs/', include_docs_urls(title='生鲜小超市')),  # 文档一定不要带$符号，这里是一个坑
                  # DRF登陆的url
                  url(r'^api-auth/', include('rest_framework.urls')),
                  # 支付宝url
                  url(r'^alipay/return/', AliPayViewset.as_view(), name="alipay"),
                  # 支付跳转url
                  url(r'index', TemplateView.as_view(template_name="index.html"), name="index"),

                  url('', include('social_django.urls', namespace='social'))    #第三方登陆
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)  # 图片的url连接
