from django.contrib import admin
from cms.models import Daily, Comment


class DailyAdmin(admin.ModelAdmin):
    list_display = ('title', 'report',)  # 一覧に出したい項目
    list_display_links = ('title', 'report',)  # 修正リンクでクリックできる項目
admin.site.register(Daily, DailyAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('daily', 'comment',)  # 一覧に出したい項目
    list_display_links = ('comment',)  # 修正リンクでクリックできる項目
admin.site.register(Comment, CommentAdmin)