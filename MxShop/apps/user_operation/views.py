from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated  # 收藏权限
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # Token验证
from rest_framework.authentication import SessionAuthentication  # Token验证

from goods.models import Goods
from user_operation.models import UserFav, UserLeavingMesage, UserAddress
from utils.permissions import IsOwnerOrReadOnly
from user_operation.serializers import UserFavSerializer, UserFavDetaialSerializer, LeavingMessageSerializer, \
    AddressSerializer


# Create your views here.


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    '''
    list:
        获取用户收藏
    create:
        商品收藏
    retrieve:
        判断某个商品是否已经收藏
    update:
        更新
    partial_update:
        更新
    delete:
        删除
    '''

    # queryset = UserFav.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)  # Token验证
    # serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 登陆验证
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    def get_serializer_class(self):
        '''
        动态获取收藏的：serializer
        :return:
        '''
        if self.action == "list":
            return UserFavDetaialSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    create:
        修改留言
    delete:
        删除留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 验证登陆
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 验证登陆
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMesage.objects.filter(user=self.request.user)


class AdderssViewset(viewsets.ModelViewSet):
    '''
    收获地址管理
    list:
        获取地址
    create:
        添加地址
    update:
        更新地址
    delete:
        删除地址
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 验证登陆
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 验证登陆
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
