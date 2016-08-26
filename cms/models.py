from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from Introduction_mysite import settings


class Daily(models.Model):
    """日報"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='daily')
    title = models.CharField('タイトル', max_length=255)
    report_y = models.TextField('やったこと', blank=True)
    report_w = models.TextField('わかったこと', blank=True)
    report_t = models.TextField('つぎにやること', blank=True)
    create_date = models.DateField('作成日', default=now)
    update_date = models.DateTimeField('更新日時', auto_now=True)
    release = models.BooleanField('公開状態', default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    """タスク"""
    daily = models.ForeignKey(Daily, verbose_name='登録日報', related_name='task')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='登録者', related_name='task')
    name = models.CharField('タスク名', max_length=255)
    goal = models.CharField('目標', max_length=255, blank=True)
    time_plan = models.IntegerField('予定時間', blank=False)
    time_real = models.IntegerField('実務時間', default=0)
    create_date = models.DateField('登録日', default=now)
    update_date = models.DateTimeField('更新日時', auto_now=True)
    implement_date = models.DateField('実施日', blank=False)
    complete_task = models.BooleanField(default=False)
    complete_goal = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """コメント"""
    daily = models.ForeignKey(Daily, verbose_name='投稿内容', related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='comment')
    comment = models.TextField('コメント', blank=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
