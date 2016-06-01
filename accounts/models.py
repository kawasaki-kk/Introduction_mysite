from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """ユーザー"""
    group_name = models.CharField('所属', max_length=255, blank=True)