# -*- coding: utf-8 -*-
import traceback
from django.shortcuts import get_object_or_404
from pure_pagination import Paginator, PageNotAnInteger
from dailyreport.models import Daily, Comment, Task
from dailyreport.forms import DailyForm, CommentForm, SearchForm, TaskFormSet, DateForm, TaskSearchForm, DailySearchForm

u"""comment_services.py
    views.pyから切り離した、モデルへのアクセスを行うメソッドをまとめたファイルです
    Commentモデルへのアクセスを行います

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
def get_comments_from_daily(daily):
    u"""コメント一覧の取得
        指定の日報に紐付けられたコメントの一覧を取得します
    :param daily: Dailyモデル型のレコード
    :return: dailyに紐付くコメントの一覧
    """
    return daily.comment.all().order_by('create_date')


@exception
def get_or_create_comment(user=None, comment_id=None):
    if comment_id:
        comment = get_object_or_404(Comment, pk=comment_id)
    elif user:
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
