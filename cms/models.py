from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from Introduction_mysite import settings


class Daily(models.Model):
    """日報"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='daily',
                             help_text="This is the user who posted the daily report")
    title = models.CharField('タイトル', max_length=255,
                             help_text="This is daily report title about [0801部会参加と記事執筆]")
    report_y = models.TextField('やったこと', blank=True,
                                help_text="This is y:やったこと of daily report's comment")
    report_w = models.TextField('わかったこと', blank=True,
                                help_text="This is w:わかったこと of daily report")
    report_t = models.TextField('つぎにやること', blank=True,
                                help_text="This is t:つぎにやること of daily report's comment")
    create_date = models.DateField('作成日', default=now,
                                   help_text="This is post or create date about [YYYY-MM-DD]")
    update_date = models.DateTimeField('更新日時', auto_now=True,
                                       help_text="This is date of update daily report about date plus time, second")
    release = models.BooleanField('公開状態', default=False,
                                  help_text="This flag is publish or not of daily report in True or False")

    def __str__(self):
        return self.title


class Task(models.Model):
    """タスク"""
    daily = models.ForeignKey(Daily, verbose_name='登録日報', related_name='task', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='登録者', related_name='task')
    name = models.CharField('タスク名', max_length=255,
                            help_text="This is task name about [Bookモデルに対するCRUD機能の実装]")
    goal = models.CharField('目標', max_length=255, blank=True,
                            help_text="This is goal of a task about [時間内に終わらせる]")
    time_plan = models.IntegerField('予定時間', blank=False,
                                    help_text="This is time for planning")
    time_real = models.IntegerField('実務時間', default=0,
                                    help_text="This is time for real practice time")
    create_date = models.DateField('登録日', default=now)
    update_date = models.DateTimeField('更新日時', auto_now=True)
    implement_date = models.DateField('実施日', blank=False,
                                      help_text="This is date for task implement")
    complete_task = models.BooleanField(default=False,
                                        help_text="This is flag for task completed or not")
    complete_goal = models.BooleanField(default=False,
                                        help_text="This is flag for goal completed or not")

    def __str__(self):
        return self.name


class Comment(models.Model):
    """コメント"""
    daily = models.ForeignKey(Daily, verbose_name='投稿内容', related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', related_name='comment')
    comment = models.TextField('コメント', blank=False,
                               help_text="This is comment on the daily report aboout [がんばってください]")
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
