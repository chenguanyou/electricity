import django_filters
from django.db.models import Q
from goods.models import Goods


# from django_filters import filters

class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    pricemin = django_filters.filters.NumberFilter(name="shop_price", help_text="最小值", lookup_expr='gte')
    pricemax = django_filters.filters.NumberFilter(name="shop_price", help_text="最大值", lookup_expr='lte')
    name = django_filters.CharFilter(name="name", help_text="名称", lookup_expr="icontains")  # 模糊查询名称，不加lookup_expr="icontains"则全部匹配
    top_category = django_filters.NumberFilter(method='top_category_filter', help_text="商品类别")

    def top_category_filter(self, queryset, name, value):
        '''
        商品列表过滤
        :param queryset:
        :param name:
        :param value:
        :return:
        '''
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name', 'is_hot', 'is_new']
