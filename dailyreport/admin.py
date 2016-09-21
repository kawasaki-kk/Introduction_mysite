# -*- coding: utf-8 -*-
from django.contrib import admin

from dailyreport.models import Daily, Comment, Task


class DailyAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_w',)
    list_display_links = ('title', )
admin.site.register(Daily, DailyAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('daily', 'name',)
    list_display_links = ('name', )
admin.site.register(Task, TaskAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('daily', 'comment',)
    list_display_links = ('comment',)
admin.site.register(Comment, CommentAdmin)
