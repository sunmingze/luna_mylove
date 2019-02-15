#!/usr/bin/env bash

HDFS="/home/work/tools/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
HADOOP="/home/work/tools/infra-client/bin/hadoop --cluster zjyprc-hadoop"
HADOOP_STREAMING="/home/work/hadoop/hadoop-2.6.0/share/hadoop/tools/lib/hadoop-streaming-2.6.0-mdh3.12-jre8-SNAPSHOT.jar"
JOB_QUEUE="root.production.cloud_group.feeds.pipeline"