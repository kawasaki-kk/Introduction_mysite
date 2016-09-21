# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from accounts import models


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', )
    list_filter = ('username', )
    search_fields = ('username', )
    ordering = ('username', )
    filter_horizontal = ()

admin.site.register(models.User, UserAdmin)
