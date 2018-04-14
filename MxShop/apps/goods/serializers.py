# coding=utf-8
from django.db.models import Q
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAD


class CategorySerializer(serializers.ModelSerializer):
    '''
    商品列表页面，分页搜索，过滤，排序&商品分类列表页序列化
    '''

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer1(serializers.ModelSerializer):
    '''
    商品分类列表页序列化
    '''
    sub_cat = CategorySerializer(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    '''
    商品分类列表页序列化
    '''
    sub_cat = CategorySerializer1(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    '''
    商品详情页图片
    '''

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    '''
    商品列表页面，分页搜索，过滤，排序
    '''
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class GoodsCategorySerializer(CategorySerializer):
    '''
    商品分类列表数据序列化
    '''
    sub_cat = CategorySerializer2(many=True)
    pass


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexGoodsSerializer(serializers.ModelSerializer):
    brandss = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAD.objects.filter(category_id=obj.id, )
        if ad_goods:
            goods_ins = ad_goods[0].Goods
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request':self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
