from django.forms import ModelForm
from accounts.models import UserManager, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from . import models


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User


class UserForm(ModelForm):
    """ユーザーのフォーム"""
    class Meta:
        model = User
        fields = ('username', 'password', 'screenname', )

