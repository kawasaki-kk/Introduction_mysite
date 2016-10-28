#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jubatus.recommender import client
# from jubatus.recommender import types
from jubatus.common import Datum

if __name__ == '__main__':
    from services import load_json
    from mecab import get_AllNouns
else:
    from qiita.services import load_json
    from qiita.mecab import get_AllNouns

NAME = "recommender_qiita"


def recommend_Qiita(title, content, recommend_num=4, learned_file_name=""):
    recommender = client.Recommender("127.0.0.1", 9199, NAME)
    if learned_file_name:
        recommender.load(learned_file_name)  # 保存した学習モデルを読み込む

    d = Datum(get_AllNouns(content))
    similars = recommender.similar_row_from_datum(d, recommend_num)

    data = []
    for similar in similars:
        print("similar:", similar)
        item = load_json(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "data/items"),
            similar.id)
        data.append({
            "q_title": item["title"],
            "score": similar.score,
            "url": item["url"],
            "tags": item["tags"]
        })
    return data


if __name__ == '__main__':
    from pprint import pprint
    recommender = client.Recommender("127.0.0.1", 9199, NAME)

    # with open('') as f:
    # nippo = f.read().split('\n')
    nippo = ["日報テスト", "Pythonが好きだ。" * 100]

    data = recommend_Qiita(nippo[0], nippo[1])
    # print(sr)

    print("nippo ", nippo[0],  " is similar to :")
    for item in data:
        pprint([item["q_title"], item["score"], item["url"], item["tags"]])
