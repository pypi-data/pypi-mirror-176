import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from django.utils.deconstruct import deconstructible

from dvadmin.utils.models import CoreModel

User = get_user_model()
KEY_CHARACTERS = string.ascii_letters + string.digits


@deconstructible
class SecretKeyGenerator(object):
    """
    Helper to give default values to Client.secret and Client.key
    """

    def __init__(self, field):
        self.field = field

    def default_gen_secret_key(self, length=40):
        return ''.join([random.choice(KEY_CHARACTERS) for _ in range(length)])

    def gen_secret_key(self, length=40):
        generator = getattr(settings, 'SIMPLE_￿SSO_KEYGENERATOR', self.default_gen_secret_key)
        return generator(length)

    def __call__(self):
        key = self.gen_secret_key(32)
        while self.get_model().objects.filter(**{self.field: key}).exists():
            key = self.gen_secret_key(32)
        return key


class ConsumerSecretKeyGenerator(SecretKeyGenerator):
    def get_model(self):
        return AkSkManage


class AkSkManage(CoreModel):
    """
    管理 access_key 和 access_secret
    """

    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    access_key = models.CharField(max_length=64, unique=True, default=ConsumerSecretKeyGenerator('access_key'),
                                  verbose_name='access_key')
    access_secret = models.CharField(max_length=64, unique=True, default=ConsumerSecretKeyGenerator('access_secret'),
                                     verbose_name='access_secret')
    status = models.IntegerField(default=0, choices=STATUS_CHOICES, verbose_name="状态", help_text="状态")
    user = models.ForeignKey(User, related_name='ak_sk_manage_user', on_delete=CASCADE, verbose_name='关联用户',
                             null=True, blank=True, help_text='关联用户')

    class Meta:
        verbose_name = "ak/sk管理"
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)
