# -*- coding: utf-8 -*-

from jubatus.recommender import client
# from jubatus.recommender import types
from jubatus.common import Datum

from services import load_json, get_all_files
from mecab import get_AllNouns

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9199
NAME = "recommender_qiita"
DATA_FILE_DIR = "./data/items/"

if __name__ == '__main__':
    # Jubatus recommenderサーバに接続して、
    # DATA_FILE_DIRで指定したディレクトリ内の全ファイル.jsonから
    # keyをファイル名、特徴量をファイルのbodyに出現する名詞とその出現回数の辞書
    # として、サーバにアップロードする

    # サーバに接続
    recommender = client.Recommender(SERVER_IP, SERVER_PORT, NAME)

    for file_name in get_all_files(DATA_FILE_DIR):
        # 指定したディレクトリ内の全ファイルを読み込んで、
        data = load_json(DATA_FILE_DIR, file_name)
        print(data["title"])
        datum = Datum(
            get_AllNouns(data["body"])  # body内に出現する名詞と、その出現回数の辞書をDatumとして作成
        )

        # サーバにアップロード
        recommender.update_row(file_name, datum)
