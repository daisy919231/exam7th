from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _

from user.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name=models.CharField(max_length=255, blank=True, default='')
    username=models.CharField(blank=True, null=True, max_length=100)

    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    date_joined=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(blank=True, null=True)

    objects=CustomUserManager()

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=[]


    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
