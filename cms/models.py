from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from Introduction_mysite import settings


class Book(models.Model):
    """書籍"""
    name = models.CharField('書籍名', max_length=255)
    publisher = models.CharField('出版社', max_length=255, blank=True)
    page = models.IntegerField('ページ数', blank=True, default=0)

    def __str__(self):
        return self.name


class Impression(models.Model):
    """感想"""
    book = models.ForeignKey(Book, verbose_name='書籍', related_name='impressions')
    comment = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.comment


class Daily(models.Model):
    """日報"""
    #daily_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='daily')
    title = models.CharField('タイトル', max_length=255)
    report = models.TextField('日報', blank=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def __report__(self):
        return self.report


class Comment(models.Model):
    """コメント"""
    #comment_id = models.AutoField(primary_key=True)
    daily = models.ForeignKey(Daily, verbose_name='投稿内容', related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='comment')
    comment = models.TextField('コメント', blank=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
