# coding=utf-8
import re
from datetime import datetime
from datetime import timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from users.models import UserProFile
from users.models import VerifyCode
from MxShop.settings import REGEX_MOBILE

User = get_user_model()


class SmaSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''
        # 手机号是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=1)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile):
            raise serializers.ValidationError("验证码发送频率超速了")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户信息详情序列化类
    '''
    class Meta:
        model = User
        fields = ("name", "birthay", "mobile", "gender", "email")


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册验证
    '''
    code = serializers.CharField(required=True, max_length=4, min_length=4, label="验证码", write_only=True,
                                 error_messages={"blank": "请输入验证码", "required": "请输入验证码", "max_length": "验证码格式错误",
                                                 "min_length": "验证码格式错误"}, help_text="验证码")
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="不能使用名称")],
                                     help_text="用户名")
    mobile = serializers.CharField(label="手机号", allow_null=True, max_length=11, help_text="手机号")
    password = serializers.CharField(required=True, label="密码", write_only=True,
                                     style={'input_type': 'password'}, help_text="密码"
                                     )

    # 密码加密密文
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=1)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
