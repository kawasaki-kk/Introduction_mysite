# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from cms.models import Daily, Comment, Task
from cms.forms import DailyForm, CommentForm, SearchForm, TaskFormSet, DateForm, TaskSearchForm
import traceback
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

u"""services.py
    views.pyから切り離した、モデルへのアクセスを行うメソッドをまとめたファイルです
    Daily,Task,Commentモデルへのアクセスを行います
        Userへのアクセスはアプリ"accounts"で行います

"""


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            #raiseしない
            print("--------------------------------------------")
            print(traceback.print_exc())
            print("--------------------------------------------")
    return wrapper


@exception
def init_form(request=None, daily_id=None):
    lists = dict(search_form=SearchForm())
    lists.update(request=request)
    lists.update(daily_id=daily_id)
    lists.update(date_form=DateForm())
    lists.update(task_search_form=TaskSearchForm())

    return lists


@exception
def create_task_form_in_queryset(queryset):
    u"""タスクフォーム作成
        クエリセットを指定してタスクフォームセットを作成します
    :param queryset: フォーム化する対象となるクエリセット
    :return: フォーム化したクエリセット
    """
    return TaskFormSet(queryset=queryset)


@exception
def get_task_from_implement(user, date):
    u"""タスク一覧の取得(実施日版)
        実施日からタスクを絞り込み、クエリセットとして返します
        基本的には日報のY:やったことに相当する情報の取得を行うことができます
    :param user: タスクの登録ユーザー
    :param date: タスクの実施日
    :return: ユーザーと実施日で絞り込んだタスクの一覧
    """
    return Task.objects.filter(user=user, implement_date=date).order_by('id')


@exception
def get_task_from_create(user, date):
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
def get_all_daily_list(release):
    u"""日報の取得(全ユーザー)
        ユーザーにかかわらず、日報を取得し、クエリセットとして返します
    :param release: 日報の公開状態(True:公開/False:非公開)
    :return: 指定したrelease状態の日報の一覧
    """
    return Daily.objects.filter(release=release).order_by('-create_date')


@exception
def get_user_daily_list(user):
    u"""日報の取得(ユーザー指定)
        ユーザーを指定して、日報を取得し、クエリセットとして返します
    :param user: 取得対象のユーザー
    :return: 指定したユーザーの日報の一覧
    """
    return Daily.objects.filter(user=user).order_by('-create_date')


@exception
def get_comments_from_daily(daily):
    u"""コメント一覧の取得
        指定の日報に紐付けられたコメントの一覧を取得します
    :param daily: Dailyモデル型のレコード
    :return: dailyに紐付くコメントの一覧
    """
    return daily.comment.all().order_by('create_date')


@exception
def get_or_create_daily(user=None, daily_id=None):
    if daily_id:    # edit or detail view
        daily = get_object_or_404(Daily, pk=daily_id)
    else:           # new create
        daily = Daily(user=user)
    return daily


@exception
def get_or_create_comment(user=None, comment_id=None):
    if comment_id:  # edit
        comment = get_object_or_404(Comment, pk=comment_id)
    else:  # new create
        comment = Comment(user=user)
    return comment


@exception
def edit_comment(request, daily, comment):
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.daily = daily
            comment.save()
    form = CommentForm()
    return form


@exception
def edit_daily(request, daily):
    if request.method == 'POST':
        form = DailyForm(request.POST, instance=daily)
        if form.is_valid():
            new_daily = form.save(commit=False)
            if 'release' in request.POST:
                new_daily.release = True
            new_daily.save()  # 日報の登録
            return True, new_daily
        else:
            return False, DailyForm(instance=daily)
    else:  # GET の時
        form = DailyForm(instance=daily)
    return True, form


@exception
def edit_task(request, daily_id=None):
    if daily_id:
        daily = get_object_or_404(Daily, pk=daily_id)
    else:
        pass

    if request.method == 'POST':
        formset = TaskFormSet(request.POST or None)
        if formset.is_valid():
            if 'edit' in request.POST:
                formset.save()
            elif 'add' in request.POST:
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
        pass
    return True


@exception
def create_pagination(request, query):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(query, per_page=5, request=request)
    return p.page(page)
