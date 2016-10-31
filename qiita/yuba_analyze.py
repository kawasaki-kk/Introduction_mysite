#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jubatus.recommender import client
# from jubatus.recommender import types
from jubatus.common import Datum

# デバッグにシェルから読んだ時用と、Djangoから読んだ時用。
if __name__ == '__main__':
    from services import load_json
    from mecab import get_AllNouns
else:
    from qiita.services import load_json
    from qiita.mecab import get_AllNouns

NAME = "recommender_qiita"


def recommend_Qiita(content, recommend_num=4, learned_file_name=""):
    # 日報本文を受け取り、出現する名詞とその出現回数のDatumをクエリとして、
    # Jubatus recomenderから類似記事を取得する。

    # content: 日報本文
    # recommend_num: おすすめする記事数
    # learned_file_name: 事前に保存しておいた学習モデルのファイル名

    # return 類似記事のタイトル、類似度スコア、url、tag情報

    # Jubatus recommenderサーバに接続
    recommender = client.Recommender("127.0.0.1", 9199, NAME)
    if learned_file_name:
        recommender.load(learned_file_name)  # 保存した学習モデルを読み込む

    # 日報本文からDatum作成
    d = Datum(get_AllNouns(content))
    # recommend_numで指定した数、類似記事の情報を取得
    similars = recommender.similar_row_from_datum(d, recommend_num)

    data = []
    for similar in similars:
        # 類似記事のid＝ファイル名から、類似記事のデータをロード
        print("similar:", similar)
        item = load_json(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "data/items"),
            similar.id)
        # データから、各情報をappend
        data.append({
            "q_title": item["title"],
            "score": similar.score,
            "url": item["url"],
            "tags": item["tags"]
        })
    return data


if __name__ == '__main__':
    # デバッグ用。

    from pprint import pprint
    recommender = client.Recommender("127.0.0.1", 9199, NAME)

    # with open('') as f:
    # nippo = f.read().split('\n')
    nippo = ["日報テスト", "Pythonが好きだ。" * 100]

    data = recommend_Qiita(nippo[1])
    # print(sr)

    print("nippo ", nippo[0],  " is similar to :")
    for item in data:
        pprint([item["q_title"], item["score"], item["url"], item["tags"]])
