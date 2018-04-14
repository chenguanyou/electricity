from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    '''
    用户收藏:
    user = 用户
    goods = 商品
    add_time = 收藏时间
    '''
    user = models.ForeignKey(User, verbose_name="用户", help_text="用户")
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间", help_text="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 字段联合唯一，避免重复

    def __str__(self):
        return self.user.name


class UserLeavingMesage(models.Model):
    '''
    用户留言：
    user = 用户
    msg_type = 留言类型：1.留言，2.投诉，3.询问，4.售后，5.求购
    message = 留言内容
    file = 上传文件
    subject = 主题
    add_time = 留言时间
    '''
    MSSG_TYPES = (
        (0, "留言"),
        (1, "投诉"),
        (2, "询问"),
        (3, "售后"),
        (4, "求购")
    )
    user = models.ForeignKey(User, verbose_name="用户", help_text="用户")
    msg_type = models.IntegerField(choices=MSSG_TYPES, verbose_name="留言类型", help_text="留言类型")
    message = models.CharField(default="", max_length=100, verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(max_length=200, upload_to="UserLeavingMesage/%Y/%m", verbose_name="上传文件", help_text="上传文件")
    subject = models.CharField(default="", max_length=100, verbose_name="留言标题", help_text="留言标题")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "用户留言管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserAddress(models.Model):
    '''
    用户收获地址：
    user = 用户
    district = 收获区域
    address = 收获详细地址
    signer_name = 收货人姓名
    signer_mobile = 签收人电话
    add_time = 添加时间
    '''
    user = models.ForeignKey(User, verbose_name="用户", help_text="用户")
    province = models.CharField(max_length=100, default="", verbose_name="省份", help_text="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市", help_text="城市")
    district = models.CharField(default="", max_length=50, verbose_name="售后区域", help_text="售后区域")
    address = models.CharField(default="", max_length=200, verbose_name="详细地址", help_text="详细地址")
    signer_name = models.CharField(default="", max_length=100, verbose_name="签收人姓名", help_text="签收人姓名")
    signer_mobile = models.CharField(default="", max_length=11, verbose_name="收货人电话", help_text="收货人电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "用户售后地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name
