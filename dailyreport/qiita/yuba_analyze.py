#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum

if __name__ == '__main__':
	from services import load_json
	from mecab import get_AllNouns
else:
	from dailyreport.qiita.services import load_json
	from dailyreport.qiita.mecab import get_AllNouns

NAME = "recommender_qiita";


def recommend_Qiita(title, content, recommend_num = 4):
	recommender = client.Recommender("127.0.0.1", 9199, NAME)
	#recommender.load('1018')

	d = Datum(get_AllNouns(content))
	similars = recommender.similar_row_from_datum(d , recommend_num)
	print(similars)

	data = []
	for similar in similars:
		print("similar:",similar)
		item = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/items"), similar.id)
		#data.append({"id":sr[i].id, "score":sr[i].score, "url":_get_url_or_tags(temp, "url"), "tags":_get_url_or_tags(temp, "tags").split(",")})
		data.append({"title":item["title"], "score":similar.score, "url":item["url"], "tags":item["tags"]})
	return data

def _get_url_or_tags(data_list, name):
	if data_list:
		return 	list(filter(lambda taple: taple[0]==name, data_list))[0][1]
	else:
		return []

if __name__ == '__main__':
	from pprint import pprint
	recommender = client.Recommender("127.0.0.1", 9199, NAME)

	with open('./data/nippo/20161013.txt') as f:
		nippo = f.read().split('\n')

	sr = recommend_Qiita(nippo[0], nippo[1])
	#print(sr)

	print ("nippo ", nippo[0],  " is similar to :")
	for data in sr:
		pprint([data["title"], data["score"], data["url"], data["tags"]] )

