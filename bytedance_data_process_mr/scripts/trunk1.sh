#!/usr/bin/env bash
source scripts/common.sh


input_path="/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/trunk1_input"
output_path="/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/trunk1_output"
JOB_NAME="feeds-model-pipeline-gsf-stats-trunck1"


$HDFS -rm -r $output_path
$HADOOP jar $HADOOP_STREAMING \
    -files src/trunk1_samples_extends_item_fea_mapper.py,src/trunk1_samples_extends_item_fea_reducer.py \
    -D mapred.job.queue.name=${JOB_QUEUE} \
    -D mapred.job.name=${JOB_NAME}  \
    -D mapred.reduce.tasks=200 \
    -D mapred.map.tasks=100 \
    -D stream.map.input.field.seperator="\n" \
    -D mapred.job.priority=NORMAL \
    -D mapreduce.map.memory.mb=1000 \
    -D mapreduce.reduce.memory.mb=1000 \
    -input $input_path \
    -output $output_path \
    -mapper trunk1_samples_extends_item_fea_mapper.py \
    -reducer trunk1_samples_extends_item_fea_reducer.py



