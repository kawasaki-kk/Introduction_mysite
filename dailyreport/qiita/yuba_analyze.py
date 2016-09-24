#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from jubatus.recommender import client
from jubatus.recommender import types
from jubatus.common import Datum
from services import load_json
from mecab import get_AllNouns

NAME = "recommender_qiita";


def recommend_Qiita(title, content, recommend_num = 4):
	recommender = client.Recommender("127.0.0.1", 9199, NAME)
	recommender.load('1018')

	d = Datum(get_AllNouns(content))
	recommender.update_row(title, d)
	similars = recommender.similar_row_from_id(title , recommend_num)
	print(similars)

	data = []
	for similar in similars[1:]:
		print("i:",similar)
		#temp = recommender.decode_row(sr[i].id).string_values
		#print(temp)
		item = load_json("./data/item", similar.id)
		#data.append({"id":sr[i].id, "score":sr[i].score, "url":_get_url_or_tags(temp, "url"), "tags":_get_url_or_tags(temp, "tags").split(",")})
		data.append({"id":item["title"], "score":similar[i].score, "url":item["url"], "tags":item["tags"]})
	print(data)
	return data

def _get_url_or_tags(data_list, name):
	if data_list:
		return 	list(filter(lambda taple: taple[0]==name, data_list))[0][1]
	else:
		return []

if __name__ == '__main__':
	from pprint import pprint
	recommender = client.Recommender("127.0.0.1", 9199, NAME)
	recommender.load('1018')

	with open('./data/nippo/20161013.txt') as f:
		nippo = f.read().split('\n')

	sr = recommend_Qiita(nippo[0], nippo[1])
	print(sr)

	print ("nippo ", nippo[0],  " is similar to :")
	for data in sr:
		pprint([data["id"], data["score"], data["url"], data["tags"]] )

	#datam = recommender.decode_row(sr[1].id)
	#print(datam.string_values[0][1])
	#print(sr[1].id, recommender.decode_row(sr[1].id))
