from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from rest_framework.authtoken.models import Token

from user_operation.models import UserFav

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    '''
    用户收藏信号量
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    '''
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=True, **kwargs):
    '''
    用户取消收藏信号量
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    '''
    if created:
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()