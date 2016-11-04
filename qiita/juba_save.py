# -*- coding: utf-8 -*-

# yuba_update.pyで作成した学習済みモデルを、外部ファイルに保存する用スクリプト
# 保存先は、/tmp
# ファイル名は${IPADDR}_${PORT}_${TYPE}_${ID}.jubatusで保存される
# 第一引数指定で、${ID}を指定できる。
# 第一引数指定がない場合、、${ID}が"年月日_時分秒"で保存される。

import sys
import time
from juba_abstract import QiitaRecommender


recommender = QiitaRecommender()

try:
    recommender.save(sys.argv[1])
except:
    recommender.save(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
