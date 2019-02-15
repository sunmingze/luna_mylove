#!/bin/bash

path=`dirname $0`

master="yarn-cluster"
num_executor=100
queue="root.production.cloud_group.feeds"
cluster="zjyprc-hadoop"

export INFRA_CLIENT_HOME="/home/work/tools/infra-client/bin"
class="TFSamples"

${INFRA_CLIENT_HOME}/spark-submit \
    --cluster "$cluster" \
    --class "$class" \
    --master "$master" \
    --queue "$queue" \
    --conf spark.yarn.job.owners="sunmingze1" \
    --conf spark.driver.maxResultSize=10G \
    --conf spark.sql.shuffle.partitions=1000 \
    --conf spark.default.parallelism=3000 \
    --conf spark.yarn.executor.memoryOverhead=2048 \
    --conf spark.executor.extraJavaOptions="-XX:MaxDirectMemorySize=2048" \
    --conf spark.speculation=true \
    --conf "spark.memory.useLegacyMode=true" \
    --conf "spark.shuffle.memoryFraction=0.8" \
    --conf "spark.storage.memoryFraction=0.2" \
    --conf "spark.rpc.message.maxSize=256" \
    --num-executors "$num_executor" \
    --driver-memory 8g \
    --executor-memory 8g \
    ./target/bytedance-0.1-SNAPSHOT.jar

