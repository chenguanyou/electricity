from random import choice
from django.db.models import Q
from rest_framework import mixins
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from users.models import VerifyCode
from MxShop.settings import API_KEY
from utils.yunpian import YunPian_Sms
from users.serializers import SmaSerializer, UserRegSerializer, UserDetailSerializer

User = get_user_model()


# Create your views here.

class CustomBackend(ModelBackend):
    '''
    自定义用户的认证
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        重写authenticate函数
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        '''
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSite(CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码：
    '''
    serializer_class = SmaSerializer

    def generate_code(self):
        '''
        生成验证码
        :return:
        '''
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian_Sms(API_KEY)
        code = self.generate_code()
        sms_status = yun_pian.sendout_sms(mobile=mobile, code=code)
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(mobile=mobile, code=code)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    用户注册, 修改，获取
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    # permissions_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # 认证

    def get_serializer_class(self):
        '''
        动态获取:serializer
        :return:
        '''
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        '''
        动态获取认证
        :return:
        '''
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        '''
        获取id
        :return:
        '''
        return self.request.user

    def perform_create(self, serializer):
        '''
        :param serializer:
        :return:
        '''
        return serializer.save()
