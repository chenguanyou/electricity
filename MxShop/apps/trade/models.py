from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    '''
    购物车：
    user = 用户，关联用户
    goods = 商品，关联商品
    goods_num = 购买商品数量
    add_time = 添加时间
    '''
    user = models.ForeignKey(User, verbose_name="用户", help_text="商品")
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品")
    goods_num = models.IntegerField(default=0, verbose_name="商品数量", help_text="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "购物车信息"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 联合唯一

    def __str__(self):
        return "%s(%d)" % (self.goods.name, self.goods_num)


class OrderInfo(models.Model):
    '''
    订单：
    user = 用户，关联用户
    order_sn = 订单编号，unique = True
    trade_no = 支付订单号，unique = True
    pay_status = 支付状态, ORDER_STATUS((success,成功),(cancel,取消),(cancel,待支付))
    order_mount = 订单金额
    pay_time = 支付时间

    配送信息：
    address = 地址
    singer_name = 签收人的姓名
    singer_mobile = 签收人电话
    add_time = 添加时间
    '''
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(User, verbose_name="用户", help_text="用户")
    order_sn = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name="订单编号", help_text="订单编号")
    trade_no = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name="支付编号",
                                help_text="支付编号")
    pay_status = models.CharField(max_length=30, choices=ORDER_STATUS, default="paying", verbose_name="支付状态",
                                  help_text="支付状态")
    order_mount = models.FloatField(default=0.0, verbose_name="支付金额", help_text="支付金额")
    pay_time = models.DateTimeField(default=datetime.now, verbose_name="支付时间", help_text="支付时间")
    # 配送信息
    address = models.CharField(default="", max_length=200, verbose_name="订单地址", help_text="订单地址")
    signer_name = models.CharField(default="", max_length=100, verbose_name="签收人姓名", help_text="签收人姓名")
    signer_mobile = models.CharField(default="", max_length=11, verbose_name="收货人电话", help_text="收货人电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{name}({pay_status})".format(name=self.user.name, pay_status=self.pay_status)


class OrderGoods(models.Model):
    '''
    订单的商品详情：
    order = 订单
    goods = 商品
    goods_num = 商品的数量
    add_time = 订单的时间
    '''
    order = models.ForeignKey(OrderInfo, verbose_name="订单", help_text="订单", related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品")
    goods_num = models.IntegerField(default=0, verbose_name="商品数量", help_text="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="订单的时间", help_text="订单的时间")

    class Meta:
        verbose_name = "订单商品详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
