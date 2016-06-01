from django.contrib import admin
from cms.models import Book, Impression, Daily, Comment

# admin.site.register(Book)
# admin.site.register(Impression)


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'page',)  # 一覧に出したい項目
    list_display_links = ('id', 'name',)  # 修正リンクでクリックできる項目
admin.site.register(Book, BookAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
admin.site.register(Impression, ImpressionAdmin)


class DailyAdmin(admin.ModelAdmin):
    list_display = ('title', 'report',)  # 一覧に出したい項目
    list_display_links = ('title', 'report',)  # 修正リンクでクリックできる項目
admin.site.register(Daily, DailyAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('daily', 'comment',)  # 一覧に出したい項目
    list_display_links = ('comment',)  # 修正リンクでクリックできる項目
admin.site.register(Comment, CommentAdmin)