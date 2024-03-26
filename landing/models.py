from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .manager import CustomUserManager


class AUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True,blank=True,null=True)
    firstLogin = models.CharField(default="No", max_length=3)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ()

    objects = CustomUserManager()

    def __str__(self):
        return self.email