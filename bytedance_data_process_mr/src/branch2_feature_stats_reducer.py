#!/usr/bin/env python
# coding=utf8

'''
	base data:
		eg: uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time
	title data:
		eg: itemid, title_word_ids
	return:
		all 'time' user status
		eg: uid, viewed_itemids, viewed_authorids, viewed_itemcity
'''

import sys
import os
import random


def init_features():
	return {'liked_itemid': [], 'liked_authorid': [], 'liked_itemcity': []}


def output_merged_ins(uid, features):
	parts = []
	for k in features:
		tmp_fea = k + ":" + ",".join(features[k])
		parts.append(tmp_fea)
	print "%s\t%s" % (uid, "\t".join(parts))


pre_key = ""
features = init_features()

for line in sys.stdin:
	parts = line.strip().split("\t")
	key = parts[0]
	liked = parts[8]
	fininshed = parts[7]
	item_id = parts[3]
	author_id = parts[4]
	item_city = parts[5]
	channel = parts[6]
	music_id = parts[9]
	if key != pre_key:
		output_merged_ins(key, features)
		features = init_features()
	if liked == "1":
		features['liked_itemid'].append(item_id)
		features['liked_authorid'].append(author_id)
		features['liked_itemcity'].append(item_city)
		features['liked_channel'].append(channel)
		features['liked_music'].append(music_id)
	if fininshed == "1":
		features['finished_itemid'].append(item_id)
		features['finished_authorid'].append(author_id)
		features['finished_itemcity'].append(item_city)
		features['finished_channel'].append(channel)
		features['finished_music'].append(music_id)
	pre_key = key
output_merged_ins(pre_key, features)
