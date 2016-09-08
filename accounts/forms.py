from django.forms import ModelForm
from django import forms
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
        fields = ('username', 'first_name', 'last_name', 'password', )


class UserResisterFrom(forms.Form):
    username = forms.CharField(label='ユーザーID', max_length=100, required=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'ユーザーID'}))
    first_name = forms.CharField(label='姓', max_length=100, required=False,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'first name'}))
    last_name = forms.CharField(label='名', max_length=100, required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'last name'}))
    password1 = forms.CharField(label='パスワード', max_length=100, required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'パスワードを入力してください',
                                    'type': 'password'}))
    password2 = forms.CharField(label='', max_length=100, required=False,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'もう一度パスワードを入力してください',
                                    'type': 'password'}))
