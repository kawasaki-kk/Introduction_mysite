# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_superuser, first_name=None, last_name=None, **extra_fields):
        if not username:
            raise ValueError(u'ユーザー名を入力してください！')
        if User.objects.filter(username=username):
            raise ValueError(u'そのユーザーは登録されています')
        user = self.model(
            username=username, first_name=first_name, last_name=last_name, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _edit_user(self, id, username, is_superuser, first_name=None, last_name=None, **extra_fields):
        if not username:
            raise ValueError(u'ユーザー名を入力してください！')
        if User.objects.filter(username=username):
            raise ValueError(u'そのユーザーは登録されています')
        user = get_object_or_404(User, pk=id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('ユーザーID', max_length=30, unique=True,
                                help_text="This using user ID and use login or logout")
    screenname = models.CharField('表示名', max_length=255,
                                  help_text="")
    first_name = models.CharField('姓', max_length=255, blank=True, null=True,
                                  help_text="")
    last_name = models.CharField('名', max_length=255, blank=True, null=True,
                                 help_text="")
    is_active = models.BooleanField('有効フラグ', default=True)
    is_staff = models.BooleanField('スタッフ', default=True)
    created_date = models.DateTimeField('登録日時', auto_now_add=True)
    modified_date = models.DateTimeField('更新日時', auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = verbose_name

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        else:
            return self.username

    def get_short_name(self):
        return self.first_name
