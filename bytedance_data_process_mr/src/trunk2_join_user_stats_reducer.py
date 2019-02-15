#!/usr/bin/env python
# coding=utf8

'''
	join user stats to basic samples
	return:
		extends all features

'''

import sys
import os
import random

pre_key = ""
user_stats_features = ""

for line in sys.stdin:
	parts = line.strip().split("\t")
	key = parts[0]
	tag = parts[1]

	if key != pre_key:
		user_stats_features = ""
	if tag == "1":
		user_stats_features = "\t".join(parts[2:])
	else:
		print "%s\t%s" % (line.strip(), user_stats_features)
	pre_key = key
