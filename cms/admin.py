from django.contrib import admin
from cms.models import Daily, Comment, Task


class DailyAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_w',)  # 一覧に出したい項目
    list_display_links = ('title', )  # 修正リンクでクリックできる項目
admin.site.register(Daily, DailyAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('daily', 'name',)  # 一覧に出したい項目
    list_display_links = ('name', )  # 修正リンクでクリックできる項目
admin.site.register(Task, TaskAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('daily', 'comment',)  # 一覧に出したい項目
    list_display_links = ('comment',)  # 修正リンクでクリックできる項目
admin.site.register(Comment, CommentAdmin)