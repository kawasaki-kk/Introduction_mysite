# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

from accounts.models import User


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserForm(ModelForm):
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

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            username = cleaned_data['username']
        except:
            raise forms.ValidationError('ユーザー名を入力してください')
        if len(username.strip()) < 1:
            raise forms.ValidationError('ユーザー名には、空白や改行を除き、1文字以上入力してください')
        try:
            first_name = cleaned_data['first_name']
        except:
            raise forms.ValidationError('姓を入力してください')
        if len(first_name.strip()) < 1:
            raise forms.ValidationError('姓には、空白や改行を除き、1文字以上入力してください')
        try:
            last_name = cleaned_data['last_name']
        except:
            raise forms.ValidationError('名を入力してください')
        if len(last_name.strip()) < 1:
            raise forms.ValidationError('名には、空白や改行を除き、1文字以上入力してください')
        try:
            password1 = cleaned_data['password1']
        except:
            raise forms.ValidationError('パスワード1を入力してください')
        if len(password1) < 1:
            raise forms.ValidationError('パスワード1を入力してください')
        try:
            password2 = cleaned_data['password2']
        except:
            raise forms.ValidationError('パスワード2を入力してください')
        if len(password2) < 1:
            raise forms.ValidationError('パスワード2を入力してください')
        if password1 != password2:
            raise forms.ValidationError('パスワードが異なります')
        return cleaned_data


class UserEditFrom(forms.Form):
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

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            username = cleaned_data['username']
        except:
            raise forms.ValidationError('ユーザー名を入力してください')
        if len(username.strip()) < 1:
            raise forms.ValidationError('ユーザー名には、空白や改行を除き、1文字以上入力してください')
        try:
            first_name = cleaned_data['first_name']
        except:
            raise forms.ValidationError('姓を入力してください')
        if len(first_name.strip()) < 1:
            raise forms.ValidationError('姓には、空白や改行を除き、1文字以上入力してください')
        try:
            last_name = cleaned_data['last_name']
        except:
            raise forms.ValidationError('名を入力してください')
        if len(last_name.strip()) < 1:
            raise forms.ValidationError('名には、空白や改行を除き、1文字以上入力してください')
        return cleaned_data
