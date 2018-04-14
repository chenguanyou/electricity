from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend  # 精确过滤
from rest_framework.authentication import TokenAuthentication  # rest自带的认证
from rest_framework_extensions.cache.mixins import CacheResponseMixin #res缓存
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexGoodsSerializer


# Create your views here.
class GoodsPagination(PageNumberPagination):
    '''
    自定义django_rest_fromework的页面参数
    '''
    page_size = 12  # 最少10条
    page_size_query_param = "page_size"  # 像后台声明要多少条
    page_query_param = "page"  # 要多少页
    max_page_size = 30  # 最多30条


class GoodsListViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):  # viewsets.ReadOnlyModelViewSet
    '''
    商品列表页面，分页搜索，过滤，排序
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle) #drf的限速，防止爬虫请求过快
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )  #REST自带的认证
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 精确过滤
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price', 'add_time')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    '''
    list:
        商品分类的列表数据序列化
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin
                           , viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品","酒水饮料"])
    serializer_class = IndexGoodsSerializer