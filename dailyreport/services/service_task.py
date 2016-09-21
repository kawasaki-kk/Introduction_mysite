# -*- coding: utf-8 -*-
import traceback
from django.shortcuts import get_object_or_404
from pure_pagination import Paginator, PageNotAnInteger
from dailyreport.models import Daily, Comment, Task
from dailyreport.forms import DailyForm, CommentForm, SearchForm, TaskFormSet, DateForm, TaskSearchForm, DailySearchForm

u"""task_services.py
    views.pyから切り離した、モデルへのアクセスを行うメソッドをまとめたファイルです
    Taskモデルへのアクセスを行います

"""


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print("--------------------------------------------")
            print(traceback.print_exc())
            print("--------------------------------------------")
    return wrapper


@exception
def create_task_form_in_queryset(queryset):
    u"""タスクフォーム作成
        クエリセットを指定してタスクフォームセットを作成します
    :param queryset: フォーム化する対象となるクエリセット
    :return: フォーム化したクエリセット
    """
    return TaskFormSet(queryset=queryset)


@exception
def get_task_from_implement_date(user, date):
    u"""タスク一覧の取得(実施日版)
        実施日からタスクを絞り込み、クエリセットとして返します
        基本的には日報のY:やったことに相当する情報の取得を行うことができます
    :param user: タスクの登録ユーザー
    :param date: タスクの実施日
    :return: ユーザーと実施日で絞り込んだタスクの一覧
    """
    return Task.objects.filter(user=user, implement_date=date).order_by('id')


@exception
def get_task_from_create_date(user, date):
    u"""タスク一覧の取得(作成日版)
        作成日からタスクを絞り込み、クエリセットとして返します
        基本的には日報のT:つぎにやることに相当する情報の取得を行うことができます
    :param user: タスクの登録ユーザー
    :param date: タスクの作成日
    :return: ユーザーと作成日で絞り込んだタスクの一覧
    """
    return Task.objects.filter(user=user, create_date=date, implement_date__gt=date).order_by('id')


@exception
def get_next_task(user, date):
    u"""タスク一覧の取得(指定日以降実施分)
        実施日からタスクを絞り込み、クエリセットとして返します
        指定日以降に行うことになっているタスクすべてを取得します
    :param user: タスクの登録ユーザー
    :param date: 以降のタスクを取得したい日
    :return: ユーザーと指定日で絞り込んだタスクの一覧
    """
    return Task.objects.filter(user=user, implement_date__gt=date).order_by('id')


@exception
def get_all_task(user):
    u"""タスク一覧の取得(すべてのタスク)
        実施日からタスクを絞り込み、クエリセットとして返します
        指定日以降に行うことになっているタスクすべてを取得します
    :param user: タスクの登録ユーザー
    :return: ユーザーで絞り込んだタスクの一覧
    """
    return Task.objects.filter(user=user).order_by('-id')


@exception
def edit_task(request, daily_id=None):
    u"""タスクの一括編集
        addボタンからリクエストが来た場合にはタスクの新規登録を行う
        その他のボタンからリクエストが来た場合にはフォームセットの保存を行う

    :param request: リクエスト情報
    :param daily_id: 日報id(ある場合)
    :return: 成否
    """
    if daily_id:
        daily = get_object_or_404(Daily, pk=daily_id)
    else:
        pass

    if request.method == 'POST':
        formset = TaskFormSet(request.POST or None)
        if formset.is_valid():
            if 'add' in request.POST:
                if daily_id:
                    task = Task(daily=daily, user=request.user,
                                complete_task=formset.forms[-1].cleaned_data['complete_task'],
                                name=formset.forms[-1].cleaned_data['name'],
                                time_plan=formset.forms[-1].cleaned_data['time_plan'],
                                time_real=formset.forms[-1].cleaned_data['time_real'],
                                implement_date=formset.forms[-1].cleaned_data['implement_date'], )
                else:
                    task = Task(user=request.user,
                                complete_task=formset.forms[-1].cleaned_data['complete_task'],
                                name=formset.forms[-1].cleaned_data['name'],
                                time_plan=formset.forms[-1].cleaned_data['time_plan'],
                                time_real=formset.forms[-1].cleaned_data['time_real'],
                                implement_date=formset.forms[-1].cleaned_data['implement_date'], )
                task.save()
            else:
                formset.save()
    else:
        pass
    return True


@exception
def get_narrowing_task(request):
    u"""タスクの絞り込み
        リクエスト要素
            "GET"であり、"tasks"という名称のボタンからリクエストが送られた場合に動作する
            通常のリンクによるページ移動が"GET"で処理されるため、切り分けるためにボタンに名称を与えている
        絞り込み要素
            date:日付
            cond:完了状態
        その他
            フォーム要素がバリデーションを突破していない場合でもフォームの要素を取得しようとするため、上記のような条件で動作する。
            一応、現状の仕様で、通常使用する分にはエラーはあり得ない。

    :param request: リクエスト
    :return: 条件に従ってフィルタリングを行ったクエリ
    """
    if request.method == 'GET':
        form = TaskSearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['cond'] == '0':
                task = Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date']
                ).order_by('-id')
            elif form.cleaned_data['cond'] == '1':
                task = Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date'],
                    complete_task=True
                ).order_by('-id')
            elif form.cleaned_data['cond'] == '2':
                task = Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date'],
                    complete_task=False
                ).order_by('-id')
            else:
                task = Task.objects.filter(user=request.user).order_by('-id')
        elif form.cleaned_data['cond']:
            if form.cleaned_data['cond'] == '0':
                task = Task.objects.filter(
                    user=request.user,
                ).order_by('-id')
            elif form.cleaned_data['cond'] == '1':
                task = Task.objects.filter(
                    user=request.user,
                    complete_task=True
                ).order_by('-id')
            elif form.cleaned_data['cond'] == '2':
                task = Task.objects.filter(
                    user=request.user,
                    complete_task=False
                ).order_by('-id')
            else:
                task = Task.objects.filter(user=request.user).order_by('-id')
        else:
            task = Task.objects.filter(user=request.user).order_by('-id')
    else:
        task = Task.objects.filter(user=request.user).order_by('-id')

    return task
