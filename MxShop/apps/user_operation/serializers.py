from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav, UserLeavingMesage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetaialSerializer(serializers.ModelSerializer):
    '''
    显示用户收藏：
    '''
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    '''
    用户收藏
    '''
    # 自动获取user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [  # 自定义重复收藏的提示消息
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "goods"),
                message="已收藏"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    '''
    用户留言：
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format=("%Y-%m-%d"))

    class Meta:
        model = UserLeavingMesage
        fields = ("user", "msg_type", "message", "file", "subject", "add_time", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    '''
    用户地址：
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "id")
