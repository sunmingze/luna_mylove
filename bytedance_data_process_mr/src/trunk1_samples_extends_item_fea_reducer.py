#!/usr/bin/env python
# coding=utf8

'''
	return:
		extends all features
		uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time, title,
		gender,beauty,video (eg: 1,2,3)

'''

import sys
import os
import random

pre_key = ""
title_feature = "None"
gender_feature = "None"
beauty_feature = "None"
video_feature = "None"

for line in sys.stdin:
	parts = line.strip().split("\t")
	key = parts[0]
	tag = parts[1]

	if key != pre_key:
		title_feature = "None"
		gender_feature = "None"
		beauty_feature = "None"
		video_feature = "None"
	if tag == "1":
		title_feature = parts[2]
	elif tag == "2":
		gender_feature = parts[2]
		beauty_feature = parts[3]
	elif tag == "3":
		video_feature = parts[2]
	else:
		basic_feature = "\t".join(parts[2:])
		print "%s\t%s\t%s\t%s\t%s" % (basic_feature, title_feature, gender_feature, beauty_feature, video_feature)
	pre_key = key
