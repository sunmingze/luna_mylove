#!/usr/bin/env python
# coding=utf8

'''
	join all these data by uid
	inputs:
		base all features
	return:
		uid: uid stats_feature
'''

import sys
import os
import json


def parse_user_stats_fea(parts):
	uid = parts[0]
	tag = '1'
	end = parts[1:]
	print "%s\t%s\t%s" % (uid, tag,"\t".join(end))


def parse_samples(parts):
	uid = parts[0]
	tag = '2'
	print "%s\t%s\t%s" % (uid, tag, "\t".join(parts))


def main():
	for line in sys.stdin:
		parts = line.strip().split("\t")
		if len(parts) == 16:
			parse_user_stats_fea(parts)
		else:
			parse_samples(parts)

if __name__ == "__main__":
	main()
