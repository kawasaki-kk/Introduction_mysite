# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from cms.models import Daily, Comment, Task
from cms.forms import SearchForm, DateForm, TaskFormSet, TaskSearchForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from . import services
from django.utils import timezone
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

u"""views.py
    各関数は、辞書型で引数をまとめ、renderにhtmlファイルの指定とともに渡します
    本ファイル中で、直接モデルにアクセスする処理は書かないようにしています
        services.pyで行います

    各関数ではservices.init_form()を呼んでいます
    init_form()は、検索フォームなど共通の情報を初期情報として登録するためのものです
    daily_list()において軽く触れますが、以降の関数では触れませんのでご了承ください

    NAME最後の()内は対応するCRUDの属性です
        ex) 日報詳細(R)
            RはReadの頭文字であり、日報詳細はCRUDのRに対応する関数である
        なお、すべてのモデルに対して、すべてのCRUDを実装しているわけではありません
"""


# 日報の一覧
@login_required
def daily_list(request):
    u"""日報一覧
        日報の一覧を取得し、レンダリングを指示します

        lists:
            init:キーワード検索フォーム
            init:日付絞込みフォーム
            公開済みの全日報のクエリセット
            当日分のタスク一覧(フォーム形式)
            明日以降分のタスク一覧(フォーム形式)
    :param request: 関数が呼ばれたときにhtmlから送られてきた情報。ここでは使用しない。
    :return:レンダリング対象のhtmlファイル'cms/daily_list.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    lists = services.init_form(request=request)

    lists.update(pages=services.create_pagination(request, services.get_all_daily_list(True)))
    lists.update(dailys=lists['pages'].object_list)
    lists.update(is_paginated=True)
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))

    return render_to_response('cms/daily_list.html', lists, context_instance=RequestContext(request))


@login_required
def daily_detail(request, daily_id):
    u"""日報詳細(R)
        日報の詳細を取得し、レンダリングを指示します
        表示対象は以下の通り
            ある日報のレコード
            日報の作成日に実施されたタスク
            日報の作成日に作成されたタスク
        lists:
            日報
            日報の作成日に実施されたタスク(implement_date)
            日報の作成日に作成されたタスク(create_date)
            日報に紐付けられたコメント一覧
            コメント入力フォーム
            当日分のタスク一覧(フォーム形式)
            明日以降分のタスク一覧(フォーム形式)
    :param request: ユーザー情報の取得
    :param daily_id: 表示対象の日報取得
    :return: レンダリング対象のhtmlファイル'cms/daily_detail.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    lists = services.init_form(request=request, daily_id=daily_id)
    lists.update(daily=services.get_or_create_daily(daily_id=daily_id))
    lists.update(comments=services.get_comments_from_daily(lists['daily']))
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))
    lists.update(implement_task=services.get_task_from_implement(
        user=lists['daily'].user, date=lists['daily'].create_date))
    lists.update(create_task=services.get_task_from_create(
        user=lists['daily'].user, date=lists['daily'].create_date))
    flag, lists['comment_form'] = services.edit_comment(
        request=request, daily=lists['daily'],  comment=services.get_or_create_comment(request.user))

    return render_to_response('cms/daily_detail.html', lists, context_instance=RequestContext(request))


# 日報の編集
def daily_edit(request, daily_id=None):
    u"""日報編集(U)
        日報を編集し、編集後の日報詳細を表示する
        表示対象は以下の通り
            日報
            日報の作成日または当日(新規作成時)に実施されたタスク
            日報の作成日または当日(新規作成時)に作成されたタスク
        なお、日報編集ページではタスクの編集は行わない
            トップページなどの画面中に表示されているタスク編集フォームを利用して逐次更新が行われているものとする
        lists:
            日報
            日報編集用フォーム
                idが指定されている場合は日報を取得後、フォームとする
                idが未指定の場合には、新規日報のインスタンスを作成し、フォームとする
            日報の作成日または当日(新規作成時)に実施されたタスク(implement_date)
            日報の作成日または当日(新規作成時)に作成されたタスク(create_date)
    :param request: ユーザー情報の取得
    :param daily_id: 編集対象の日報id(未指定の場合新規作成と判断)
    :return: レンダリング対象のhtmlファイル'cms/daily_edit.html'、およびhtmlファイル中で利用するフォーム・クエリリスト
    """
    lists = services.init_form(request=request, daily_id=daily_id)
    lists.update(daily=services.get_or_create_daily(user=request.user, daily_id=daily_id))
    if request.user != lists['daily'].user:
        return redirect('login')
    flag, lists['report_form'] = services.edit_daily(request=request, daily=lists['daily'])
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))

    if daily_id:
        lists.update(implement_task=services.get_task_from_implement(lists['daily'].user, lists['daily'].create_date))
        lists.update(create_task=services.get_task_from_create(lists['daily'].user, lists['daily'].create_date))
    else:
        lists.update(implement_task=services.get_task_from_implement(request.user, timezone.now().date()))
        lists.update(create_task=services.get_task_from_create(request.user, timezone.now().date()))

    if request.method == 'POST' and flag:
        return redirect('cms:daily_detail', daily_id=lists['report_form'].id)
    elif flag is False:
        lists.update(comment="必須項目が入力されていません")

    return render_to_response('cms/daily_edit.html', lists, context_instance=RequestContext(request))


def task_edit(request):
    u"""タスク一覧(CRU)
        タスク一覧をフォームとして表示します
        表示対象のタスクはユーザーそれぞれのタスクのみです
        R属性は仮です
            タスク単独を詳しく編集するフォームを実装する可能性があります
        lists:
        タスクフォーム
    :param request:ユーザー情報の取得
    :return:レンダリング対象のhtmlファイル'cms/task_list.html'、およびhtmlファイル中で利用するフォーム
    """
    # タスク一覧
    lists = services.init_form(request=request)
    services.edit_task(request)
    lists.update(tasks=services.create_pagination(request, services.get_all_task(request.user)))
    lists.update(task_form=services.create_task_form_in_queryset(lists['tasks'].object_list))
    return render_to_response('cms/task_list.html', lists, context_instance=RequestContext(request))


def task_edit_daily(request):
        u"""タスク一覧(CRU)
            日報表示部分を持つページにおいてタスクを更新するためのメソッドです
            通常のものと比べ、返るページが異なります
            表示対象のタスクはユーザーそれぞれのタスクのみです
            R属性は仮です
                タスク単独を詳しく編集するフォームを実装する可能性があります
            lists:
            タスクフォーム
        :param request:ユーザー情報の取得
        :return:レンダリング対象のhtmlファイル'cms/task_list.html'、およびhtmlファイル中で利用するフォーム
        """
        services.edit_task(request)

        return redirect('cms:daily_list')


# def search_for_task_in_date
def task_date_search(request):
    u"""タスク日付絞込み
        タスクの一覧を日付で絞り込みます
        表示対象のタスクはtask_editと同じくユーザーそれぞれのタスクのみです
        DateFormフォームより送られてきた日付情報をもとに、タスクフォームセットに表示する情報を絞り込みます
            絞り込む対象は実施日(implement_date)です
            タスクの作成日(create_date)ではありません
    :param request: dateform(日付をカレンダーによって指定するフォーム)からのリクエスト、及びユーザー情報の取得
    :return: レンダリング対象のhtmlファイル'cms/task_list.html'、およびhtmlファイル中で利用する日付で絞り込んだフォーム
    """
    lists = services.init_form(request=request)
    if request.method == 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = TaskSearchForm(request.GET)
        lists.update(task_search_form=form)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
        if form.is_valid():
            if form.cleaned_data['cond'] == '0':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date']
                ).order_by('-id'))
            elif form.cleaned_data['cond'] == '1':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date'],
                    complete_task=True
                ).order_by('-id'))
            elif form.cleaned_data['cond'] == '2':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                    implement_date=form.cleaned_data['date'],
                    complete_task=False
                ).order_by('-id'))
        elif form.cleaned_data['cond']:
            if form.cleaned_data['cond'] == '0':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                ).order_by('-id'))
            elif form.cleaned_data['cond'] == '1':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                    complete_task=True
                ).order_by('-id'))
            elif form.cleaned_data['cond'] == '2':
                form = TaskFormSet(queryset=Task.objects.filter(
                    user=request.user,
                    complete_task=False
                ).order_by('-id'))
        else:
            form = TaskSearchForm()

        lists.update(task_form=form)
        return render_to_response('cms/task_list.html', lists, context_instance=RequestContext(request))


# def search_for_daily_in_date
def daily_date_search(request):
    u"""日報日付絞込み
        日報の一覧を日付で絞り込みます
        絞り込み対象は全日報です
        以下、基本的な手順はtask_date_search()と同様です
    :param request: dateform(日付をカレンダーによって指定するフォーム)からのリクエスト、及びユーザー情報の取得に使用
    :return: レンダリング対象のhtmlファイル'cms/daily_list.html'、およびhtmlファイル中で利用する日付で絞り込んだクエリリスト
    """
    lists = services.init_form(request=request)
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))

    if request.method == 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = DateForm(request.GET)
        lists.update(date_form=form)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
        if form.is_valid():
            lists.update(dailys=Daily.objects.all().filter(create_date=form.cleaned_data['date']))
            lists.update(is_paginated=False)
            return render_to_response('cms/daily_list.html', lists, context_instance=RequestContext(request))

    return redirect('cms:daily_list')


# 日報の削除
# アラート表示などは未実装
def daily_del(request, daily_id):
    u"""日報削除(D)
        日報の削除を行います
        日報の投稿ユーザーでないユーザーがアクセスした場合、ログインページにリダイレクトされます
        正常に削除できた場合は（ユーザーの）日報一覧画面へリダイレクトされます
    :param request:ユーザー情報の取得
    :param daily_id:削除対象日報id
    :return:日報一覧ページへリダイレクト
    """
    daily = get_object_or_404(Daily, pk=daily_id)
    if daily.user != request.user:  # 投稿者とログインユーザが異なる場合
        return redirect('login')
    daily.delete()  # 日報の削除
    return redirect('cms:user_info', user_id=request.user.id)   # 一覧画面にリダイレクト


# 日報の検索
# def search_for_daily_in_keyword
def daily_search(request):
    u"""日報検索
        日報をキーワードによって検索します
        検索条件
        ・キーワード数：1(複数キーワードのor対応,and未対応)
        ・検索対象：ユーザー名/日報タイトル/日報本文(y/w/t)
    :param request: 検索キーワードの取得
    :return: 絞り込んだ日報の一覧をdaily_list.htmlを利用してレンダリングする
    """
    # リクエストが送られてきている場合
    lists = services.init_form(request=request)
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))

    if request.method == 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = SearchForm(request.GET)
        # フォームの中身が存在する場合=検索キーワードが入力されている場合
        if form.is_valid():
            queries = [Q(user__username__contains=word) |
                       Q(title__contains=word) |
                       Q(report_y__contains=word) |
                       Q(report_w__contains=word) |
                       Q(report_t__contains=word) for word in form.cleaned_data['keyword']]
            query = queries.pop()
            for item in queries:
                query |= item
            lists.update(dailys=Daily.objects.all().filter(query).order_by('-create_date'))
            lists.update(search_form=form)
            lists.update(keyword=form.cleaned_data['keyword'])
            lists.update(is_paginated=False)
            return render_to_response('cms/daily_list.html', lists, context_instance=RequestContext(request))

        return redirect('cms:daily_list')


def user_info(request, user_id):
    u"""ユーザー情報
        ユーザーごとの投稿情報を表示します
        表示対象：
            各ユーザーが投稿した日報
            (自分のページの場合)非公開状態の日報
        その他の表示内容は日報一覧と同様です
    :param request: ユーザー情報の取得
    :param user_id: 表示対象ユーザーid
    :return: ユーザーで絞り込んだ日報のリストを日報一覧と同様のhtmlファイルを使用してレンダリングします
    """
    lists = services.init_form(request=request)
    lists.update(pages=services.create_pagination(
        request, services.get_user_daily_list(user=user_id)))
    lists.update(dailys=lists['pages'].object_list)
    lists.update(is_paginated=True)
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))
    lists.update(userinfo=get_object_or_404(auth.get_user_model(), pk=user_id))

    return render_to_response('cms/daily_list.html', lists, context_instance=RequestContext(request))


# コメントの編集
def comment_edit(request, daily_id, comment_id=None):
    u"""コメント編集
        コメントの編集/新規作成を行います
    :param request:
    :param daily_id:
    :param comment_id:
    :return:
    """
    lists = services.init_form(request=request)
    lists.update(task_form=services.create_task_form_in_queryset(
        services.get_task_from_implement(request.user, timezone.now().date())
    ))
    lists.update(task_form_next=services.create_task_form_in_queryset(
        services.get_next_task(request.user, timezone.now().date())
    ))
    lists.update(daily=services.get_or_create_daily(daily_id=daily_id))
    lists.update(comment=services.get_or_create_comment(user=request.user, comment_id=comment_id))
    if request.user != lists['comment'].user:
        return redirect('login')
    flag, lists['comment_form'] = services.edit_comment(request, lists['daily'], lists['comment'])

    if request.method == 'POST' and flag:
        return redirect('cms:daily_detail', daily_id=lists['daily'].id)
    elif flag is False:
        lists.update(comment="必須項目が入力されていません")

    return render_to_response('cms/comment_edit.html', lists, context_instance=RequestContext(request))


def comment_del(request, daily_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('cms:daily_detail', daily_id=daily_id)