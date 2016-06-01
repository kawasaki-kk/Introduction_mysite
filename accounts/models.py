from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError(u'ユーザー名を入力してください！')
        user = self.model(username=username, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('ユーザー名', max_length=30, unique=True)
    screenname = models.CharField('ユーザー名（表示用）', max_length=255)
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
        return self.__str__()

    get_short_name = get_full_name