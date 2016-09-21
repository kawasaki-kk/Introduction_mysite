# -*- coding: utf-8 -*-
import traceback
from django.shortcuts import get_object_or_404
from pure_pagination import Paginator, PageNotAnInteger
from cms.models import Daily, Comment, Task
from cms.forms import DailyForm, CommentForm, SearchForm, TaskFormSet, DateForm, TaskSearchForm, DailySearchForm

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
def get_all_daily_list(request, release):
    u"""日報の取得(全ユーザー)
        ユーザーにかかわらず、日報を取得し、クエリセットとして返します
    :param request:表示クエリの取得
    :param release: 日報の公開状態(True:公開/False:非公開)
    :return: 指定したrelease状態の日報の一覧
    """
    if request.method == 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = DateForm(request.GET)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
        if form.is_valid():
            # リクエストを取得しながら検索フォームを生成
            form = DateForm(request.GET)
            # フォームの中身が存在する場合=検索キーワードが入力されている場合
            if form.is_valid():
                return Daily.objects.filter(
                    create_date=form.cleaned_data['date'], release=release).order_by('-update_date')
            else:
                return Daily.objects.filter(release=release).order_by('-update_date')
        else:
            return Daily.objects.filter(release=release).order_by('-update_date')

    return Daily.objects.filter(release=release).order_by('-update_date')


@exception
def get_user_daily_list(request, user):
    u"""日報の取得(ユーザー指定)
        ユーザーを指定して、日報を取得し、クエリセットとして返します
    :param request: 検索のクエリ
    :param user: 取得対象のユーザー
    :return: 指定したユーザーの日報の一覧
    """
    if request.method == 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = DailySearchForm(request.GET)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
        if form.is_valid():
            if form.cleaned_data['cond'] == '1':
                return Daily.objects.filter(user=user, release=True).order_by('-update_date')
            elif form.cleaned_data['cond'] == '2':
                return Daily.objects.filter(user=user, release=False).order_by('-update_date')
            else:
                return Daily.objects.filter(user=user).order_by('-update_date')
    return Daily.objects.filter(user=user, release=True).order_by('-update_date')


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
    elif user:           # new create
        daily = Daily(user=user)
    else:
        return False
    return daily


@exception
def get_or_create_comment(user=None, comment_id=None):
    if comment_id:  # edit
        comment = get_object_or_404(Comment, pk=comment_id)
    elif user:  # new create
        comment = Comment(user=user)
    else:
        return False
    return comment


@exception
def edit_comment(request, daily, comment):
    u"""コメントの編集

    :param request: リクエスト情報
    :param daily: 投稿対象の日報
    :param comment: 編集対象のコメント
    :return: 成否、及びコメントフォーム
    """
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.daily = daily
            comment.save()
            return True, CommentForm()
        else:
            return False, CommentForm(request.POST, instance=comment)
    return True, CommentForm(instance=comment)


@exception
def edit_daily(request, daily):
    u"""日報の編集

    :param request: リクエスト情報
    :param daily: 編集対象の日報
    :return: 成否、及び成功時は日報レコード、失敗時はフォーム
    """
    if request.method == 'POST':
        form = DailyForm(request.POST, instance=daily)
        if form.is_valid():
            new_daily = form.save(commit=False)
            if 'release' in request.POST:
                new_daily.release = True
            new_daily.save()  # 日報の登録
            return True, new_daily
        else:
            return False, form
    else:  # GET の時
        form = DailyForm(instance=daily)
    return True, form


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
def create_pagination(request, query):
    u"""ページネーションの作成
        pure_paginationモジュールを利用して、クエリを分割し、ページ情報を付加する

    :param request: リクエスト情報
    :param query: ページ分割対象のクエリ
    :return: ページ情報を付加し、指定ページ向けに分割したクエリ
    """
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(query, per_page=5, request=request)
    return p.page(page)


@exception
def get_search_task(request):
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
    if request.method == 'GET' and 'tasks' in request.GET:
        # リクエストを取得しながら検索フォームを生成
        form = TaskSearchForm(request.GET)
        print(request.path)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
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


def delete_daily(request, daily):
    u"""日報の削除

    :param request: リクエスト情報(リクエストユーザー)
    :param daily: 削除対象日報
    :return: 成否
    """
    if daily.user != request.user:  # 投稿者とログインユーザが異なる場合
        return False
    daily.delete()  # 日報の削除
    return True


def delete_comment(request, comment):
    u"""コメントの削除

    :param request: リクエスト情報(リクエストユーザー)
    :param comment: 削除対象コメント
    :return: 成否
    """
    if comment.user != request.user:
        return False
    comment.delete()
    return True
