# -*- coding: utf-8 -*-
import traceback

from pure_pagination import Paginator, PageNotAnInteger

from dailyreport.forms import SearchForm, TaskSearchForm

u"""services_utility.py
    views.pyから切り離した、繰り返し行われる処理をメソッド化したファイルです

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
def init_dictionary(request=None, daily_id=None):
    u"""辞書型初期化メソッド
    テンプレートに送る情報を初期化します
    本メソッド中で追加するのはbase.htmlやtaskbar.htmlで使用される共通データ部分です

    :param request: リクエスト情報
    :param daily_id: 日報情報
    :return: 初期情報を登録した辞書型
    """
    dictionary = dict(search_form=SearchForm())
    dictionary.update(request=request)
    dictionary.update(daily_id=daily_id)
    dictionary.update(task_search_form=TaskSearchForm())

    return dictionary


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
