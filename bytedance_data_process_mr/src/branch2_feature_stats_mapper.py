#!/usr/bin/env python
# coding=utf8

'''
	base data:
		eg: uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time
	return:

'''

import sys
import os
import random


def parse_basic_samples(line):
	parts = line.split("\t")
	is_finish = parts[6]
	is_liked = parts[7]
	fea_group = ["city,item_id","author_id","channel",]
	for fea in parts:
		for k in fea.split(","):
			fea_name =  k
			print "%s\t%s\t%s" % (k, is_finish, is_liked)


def main():
	for line in sys.stdin:
		parse_basic_samples(line.strip())


if __name__ == "__main__":
	main()
