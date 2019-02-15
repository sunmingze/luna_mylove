#!/usr/bin/env python
# coding=utf8

'''
	join all these data by itemid
	inputs:
		base all features
	return:
		uid: uid stats_feature
		eg: uid_stats_xxx:1#1,2#1
'''

import sys
import os
import json


def parse_samples(line):
	parts = line.strip().split("\t")
	uid = parts[0]
	time = parts[10]
	print "%s\t%s\t%s" % (uid, time, line.strip())


def main():
	for line in sys.stdin:
		parse_samples(line)


if __name__ == "__main__":
	main()
