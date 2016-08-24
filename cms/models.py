from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from Introduction_mysite import settings


class Daily(models.Model):
    """日報"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='daily')
    title = models.CharField('タイトル', max_length=255)
    report = models.TextField('日報', blank=False)
    date = models.DateTimeField(default=now)
    release = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def __report__(self):
        return self.report


class Comment(models.Model):
    """コメント"""
    daily = models.ForeignKey(Daily, verbose_name='投稿内容', related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='comment')
    comment = models.TextField('コメント', blank=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
