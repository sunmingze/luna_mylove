#!/usr/bin/env python
# coding=utf8

'''
	join all these data by itemid
	base data:
		eg: uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time
	title data:
		eg: itemid, title_word_ids
	face data:
		eg:
	video features:
		eg:

	return:
		extends features
		eg: uid,time,title_feature
'''

import sys
import os
import json


def parse_title_json(line):
	fea = json.loads(line.strip())
	tag = "1"
	itemid = str(fea["item_id"])
	title_features = "title_fea:" + ",".join(fea["title_features"].keys())
	print "%s\t%s\t%s" % (itemid, tag, title_features)


def parse_face_attrs_json(line):
	fea = json.loads(line.strip())
	tag = "2"
	itemid = str(fea["item_id"])
	attrs_list = fea["face_attrs"]
	gender_list = []
	beauty_list = []
	for attrs in attrs_list:
		if not len(attrs) == 0:
			gender_list.append(str(attrs["gender"]))
			beauty_list.append(str(attrs["beauty"]))
	print "%s\t%s\t%s\t%s" % (itemid, tag, "gender:" + ",".join(gender_list), "beauty:" + ",".join(beauty_list))


def parse_video_embedding_json(line):
	fea = json.loads(line.strip())
	tag = "3"
	itemid = str(fea["item_id"])
	video_embedding = map(lambda x: str(x), fea["video_feature_dim_128"])
	print "%s\t%s\t%s" % (itemid, tag, "video_feature:" + ",".join(video_embedding))


def parse_basic_samples(line):
	parts = line.strip().split("\t")
	tag = "9"
	itemid = parts[2]
	print "%s\t%s\t%s" % (itemid, tag, line.strip())


def main():
	for line in sys.stdin:
		if not line.find("title_features") == -1:
			parse_title_json(line)
		elif not line.find("face_attrs") == -1:
			parse_face_attrs_json(line)
		elif not line.find("video_feature_dim_128") == -1:
			parse_video_embedding_json(line)
		else:
			parse_basic_samples(line)


if __name__ == "__main__":
	main()
