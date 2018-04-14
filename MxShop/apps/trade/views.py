import datetime
from django.shortcuts import redirect

from rest_framework import views
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from trade.models import ShoppingCart, OrderGoods, OrderInfo
from trade.serlizers import ShopCatSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer

from MxShop.settings import PUBLIC_KEY, PRIVATE_KEY, ALIPAY_APPID, ALIPAY_URL


# Create your views here.

class ShoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    lise:
        获取购物车商品详情
    create:
        商品加入购物车
    delete:
        删除购物车商品
    update:
        更新购物车
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCatSerializer
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.goods_num
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.goods_num
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.goods_num
        saved_record = serializer.save()
        nums = saved_record.goods_num - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCatSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取订单列表
    delete:
        删除订单
    create:
        新增加订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.goods_num
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


class AliPayViewset(views.APIView):
    '''
    支付宝支付
    '''

    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=ALIPAY_URL,
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=ALIPAY_URL
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', "TRADE_SUCCESS")

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        '''
        处理支付宝的notify_url
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid=ALIPAY_APPID,
            app_notify_url=ALIPAY_URL,
            app_private_key_path=PRIVATE_KEY,
            alipay_public_key_path=PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=ALIPAY_URL
        )

        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            order_sn = processed_dict.get("out_trade_no", None)
            trade_no = processed_dict.get("trade_no", None)
            trade_status = processed_dict.get("trade_status", "TRADE_SUCCESS")

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()

            return Response("success")
