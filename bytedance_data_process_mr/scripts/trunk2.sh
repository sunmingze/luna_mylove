#!/usr/bin/env bash
source scripts/common.sh

input_path="/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/branch1_output,/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/trunk1_output"
output_path="/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/trunck2_output"
JOB_NAME="feeds-model-pipeline-gsf-stats-trunck2"


$HDFS -rm -r $output_path
$HADOOP jar $HADOOP_STREAMING \
    -files src/trunk2_join_user_stats_mapper.py,src/trunk2_join_user_stats_reducer.py \
    -D mapred.job.queue.name=${JOB_QUEUE} \
    -D mapred.job.name=${JOB_NAME}  \
    -D mapred.reduce.tasks=200 \
    -D mapred.map.tasks=1000 \
    -D mapred.job.priority=VERY_HIGH \
    -D mapreduce.reduce.memory.mb=10000 \
    -input $input_path \
    -output $output_path \
    -mapper trunk2_join_user_stats_mapper.py \
    -reducer trunk2_join_user_stats_reducer.py



