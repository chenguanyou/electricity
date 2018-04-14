from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
    密码加密
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    '''
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        Token.objects.create(user=instance)