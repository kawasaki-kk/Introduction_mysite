# -*- coding: utf-8 -*-
import traceback

from django.shortcuts import get_object_or_404

from dailyreport.models import Daily
from dailyreport.forms import DailyForm, DateForm, DailySearchForm

u"""services_daily.py
    views.pyから切り離した、モデルへのアクセスを行うメソッドをまとめたファイルです
    Dailyモデルへのアクセスを行います

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
def get_all_daily_list(request, release):
    u"""日報の取得(全ユーザー)
        ユーザーにかかわらず、日報を取得し、クエリセットとして返します
    :param request:表示クエリの取得
    :param release: 日報の公開状態(True:公開/False:非公開)
    :return: 指定したrelease状態の日報の一覧
    """
    if request.method is 'GET':
        # リクエストを取得しながら検索フォームを生成
        form = DateForm(request.GET)
        if form.is_valid():
            form = DateForm(request.GET)
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
        form = DailySearchForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['cond'] == '1':
                return Daily.objects.filter(user=user, release=True).order_by('-update_date')
            elif form.cleaned_data['cond'] == '2':
                return Daily.objects.filter(user=user, release=False).order_by('-update_date')
            else:
                return Daily.objects.filter(user=user).order_by('-update_date')
    if int(request.user.id) == int(user):
        return Daily.objects.filter(user=user).order_by('-update_date')
    else:
        return Daily.objects.filter(user=user, release=True).order_by('-update_date')


@exception
def get_or_create_daily(user=None, daily_id=None):
    if daily_id:
        daily = get_object_or_404(Daily, pk=daily_id)
    elif user:
        daily = Daily(user=user)
    else:
        return False
    return daily


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
            new_daily.save()
            return True, new_daily
        else:
            return False, form
    else:
        form = DailyForm(instance=daily)
    return True, form


def delete_daily_record(request, daily):
    u"""日報の削除

    :param request: リクエスト情報(リクエストユーザー)
    :param daily: 削除対象日報
    :return: 成否
    """
    if daily.user != request.user:
        return False
    daily.delete()
    return True
