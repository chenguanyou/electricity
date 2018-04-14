from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser     #继承Django_AbstractUser用来扩展models

# Create your models here.
class UserProFile(AbstractUser):
    '''
    用户信息models
    name = 姓名
    birthay = 出生日期
    mobile = 手机号
    gender = 性别
    email = 邮箱
    add_time = 注册时间
    '''
    name = models.CharField(max_length=20, default="新注册用户", null=True, blank=True, verbose_name="用户名" )
    birthay = models.DateField(null=True, blank=True, verbose_name="出生日期")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    gender = models.CharField(max_length=10, choices=(("female", "女"), ("male", "男")), default="female", verbose_name="性别")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class VerifyCode(models.Model):
    '''
    短信验证码
    mobile = 手机
    code = 验证码
    add_time = 注册时间
    '''
    mobile = models.CharField(max_length=11, verbose_name="手机号", help_text="手机号")
    code = models.CharField(max_length=10, verbose_name="验证码")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile

