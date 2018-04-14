from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "会员信息管理"

    def ready(self):
        '''
        信号量密码加密
        :return:
        '''
        import users.signals
