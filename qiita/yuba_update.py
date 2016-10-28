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
    recommender = client.Recommender(SERVER_IP, SERVER_PORT, NAME)

    for file_name in get_all_files(DATA_FILE_DIR):
        data = load_json(DATA_FILE_DIR, file_name)
        print(data["title"])
        d = Datum(
            get_AllNouns(data["body"])
        )

        recommender.update_row(file_name, d)
