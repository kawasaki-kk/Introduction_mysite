# -*- coding: utf-8 -*-

# yuba_update.pyで作成した学習済みモデルを、外部ファイルに保存する用スクリプト
# 保存先は、/tmp
# ファイル名は${IPADDR}_${PORT}_${TYPE}_${ID}.jubatusで保存される
# 第一引数指定で、${ID}を指定できる。
# 第一引数指定がない場合、、${ID}が"年月日_時分秒"で保存される。

import sys
import time
from jubatus.recommender import client

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9199
NAME = "recommender_qiita"


recommender = client.Recommender(SERVER_IP, SERVER_PORT, NAME)
try:
    recommender.save(sys.argv[1])
except:
    recommender.save(time.strftime("%Y%m%d_%I%M%S", time.localtime()))
