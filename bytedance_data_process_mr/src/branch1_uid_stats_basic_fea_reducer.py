#!/usr/bin/env python
# coding=utf8

'''
	all features:
		eg: uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time
			title_word_ids, gender, beauty,
	return:
		feature columns:
			 'finish_authorid',
			 'finish_beauty',
			 'finish_channel',
			 'finish_gender',
			 'finish_itemcity',
			 'finish_itemid',
			 'finish_music_id',
			 'finish_title_id',
			 'liked_authorid',
			 'liked_beauty',
			 'liked_channel',
			 'liked_gender',
			 'liked_itemcity',
			 'liked_itemid',
			 'liked_music_id',
			 'liked_title_id'
'''

import sys
import os
import random


def init_features():
	return {'liked_itemid': {}, 'liked_authorid': {}, 'liked_itemcity': {},
	        'liked_channel': {}, 'liked_music_id': {}, 'liked_gender': {},
	        'liked_beauty': {}, 'liked_title_id': {},
	        'finish_itemid': {}, 'finish_authorid': {}, 'finish_itemcity': {},
	        'finish_channel': {}, 'finish_music_id': {}, 'finish_gender': {},
	        'finish_beauty': {}, 'finish_title_id': {}}


def append_dict(fea_dict, feature_type, feature_ids):
	if not feature_ids == "":
		for id in feature_ids.split(","):
			if id in fea_dict[feature_type]:
				fea_dict[feature_type][id] = fea_dict[feature_type][id] + 1
			else:
				fea_dict[feature_type][id] = 1


def output_merged_ins(uid, features):
	parts = []
	for fea in sorted(features):
		fea_values = features[fea]
		tmp = []
		for k in fea_values:
			tmp.append(k + "#" + fea_values[k])
		parts.append(",".join(tmp))
	print "%s\t%s" % (uid, "\t".join(parts))


pre_key = ""
features = init_features()

for line in sys.stdin:
	parts = line.strip().split("\t")
	key = parts[0]
	time = parts[1]

	liked = parts[9]
	fininshed = parts[8]
	item_id = parts[4]
	author_id = parts[5]
	item_city = parts[6]
	channel = parts[7]
	music_id = parts[10]
	title_fea = parts[11]
	gender_fea = parts[12]
	beauty_fea = parts[13]

	if key != pre_key:
		output_merged_ins(key, features)
		features = init_features()
	if liked == "1":
		append_dict(features, 'liked_itemid', item_id)
		append_dict(features, 'liked_authorid', author_id)
		append_dict(features, 'liked_itemcity', item_city)
		append_dict(features, 'liked_channel', channel)
		append_dict(features, 'liked_music', music_id)
		if not title_fea == "":
			append_dict(features, 'liked_title', title_fea)
		if not gender_fea == "":
			append_dict(features, 'liked_gender', gender_fea)
		if not beauty_fea == "":
			append_dict(features, 'liked_beauty', beauty_fea)

	if fininshed == "1":
		append_dict(features, 'finish_itemid', item_id)
		append_dict(features, 'finish_authorid', author_id)
		append_dict(features, 'finish_itemcity', item_city)
		append_dict(features, 'finish_channel', channel)
		append_dict(features, 'finish_music', music_id)
		if not title_fea == "":
			append_dict(features, 'finish_title', title_fea)
		if not gender_fea == "":
			append_dict(features, 'finish_gender', gender_fea)
		if not beauty_fea == "":
			append_dict(features, 'finish_beauty', beauty_fea)

	output_merged_ins(pre_key, features)
	pre_key = key
