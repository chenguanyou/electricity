import time
from random import Random
from rest_framework import serializers
# from rest_framework.fields import

from utils.alipay import AliPay
from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods

from MxShop.settings import PUBLIC_KEY, PRIVATE_KEY, ALIPAY_APPID, ALIPAY_URL


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCatSerializer(serializers.Serializer):
    '''
    购物车serializer
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods_num = serializers.IntegerField(required=True, min_value=1, label="数量",
                                         error_messages={
                                             "min_value": "商品数量不能少于1",
                                             "required": "请选着购买数量"
                                         })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        ''''
        重写create方法，并且加入自己的判断逻辑
        :param validated_data:
        :return:
        '''
        user = self.context["request"].user
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        goods_num = validated_data["goods_num"]

        if existed:
            existed = existed[0]
            existed.goods_num += goods_num
            existed.save()
        else:
            ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    '''
    订单serializer
    '''
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    '''
    订单serializer
    '''
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=ALIPAY_URL,
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=ALIPAY_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    '''
    订单serializer
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    order_sn = serializers.CharField(read_only=True)  # 设置订单编号只读
    trade_no = serializers.CharField(read_only=True)  # 设置支付编号只读
    pay_status = serializers.CharField(read_only=True)  # 设置支付状态只读
    pay_time = serializers.CharField(read_only=True)  # 设置支付时间状态只读
    add_time = serializers.CharField(read_only=True)  # 设置提交时间只读
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=ALIPAY_URL,
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=ALIPAY_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        # 生成低订单号：当前时间+ userid+ 随机数
        randon_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=randon_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
