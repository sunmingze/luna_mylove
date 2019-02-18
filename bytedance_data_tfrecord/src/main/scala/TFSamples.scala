
import java.util

import org.apache.hadoop.io.{BytesWritable, NullWritable}
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}
import org.tensorflow.example._
import org.tensorflow.hadoop.io.TFRecordFileOutputFormat

import scala.collection.Map
import scala.collection.mutable.ArrayBuffer

/**
  * Created by sunmingze on 2018/3/16.
  */

object TFSamples {

  def setFeatureFloat(input: Array[Double]) = {
    val builder = FloatList.newBuilder()
    if (input.size == 0) {
      for( i <- 0 until 128 )
        builder.addValue(0.0.toFloat)
    }
    else {
      input.map { v =>
        builder.addValue(v.toFloat)
      }
    }
    builder
  }

  def setFeatureId(input: Array[String], map: Map[String, Long]) = {
    val builder = Int64List.newBuilder()
    if (input.size == 0 || map == null)
      builder.addValue(0)
    else {
      input.map { v =>
        val value: Long = map.getOrElse(v, 0L)
        builder.addValue(value)
      }
    }
    builder
  }

  // features:
  // 	uid, city, item_id, author_id, item_city, channel, finish, like, music_id, device, time, duration_time, title, gender,beauty,video
  def initFeatureGroupIds(sc: SparkContext, path: String): Map[String, Map[String, Long]] = {
    val featureGroupMap = sc.textFile(path).flatMap { line => {
      val parts = line.split("\t")
      val end = new ArrayBuffer[(String, String)]()
      end.append(("uid", parts(0)))
      end.append(("city", parts(1)))
      end.append(("item_id", parts(2)))
      end.append(("author_id", parts(3)))
      end.append(("item_city", parts(4)))
      end.append(("channel", parts(5)))
      end.append(("music_id", parts(8)))
      end.append(("device", parts(9)))
      end.append(("duration_time", parts(11)))

      for (key <- parts(12).split(",")) {
        end.append(("title", key))
      }

      for (key <- parts(13).split(",")) {
        end.append(("gender", key))
      }

      for (key <- parts(14).split(",")) {
        end.append(("beauty", key))
      }



      end
    }
    }.map(x => (x._1, Set(x._2))).reduceByKey(_ ++ _).repartition(20).map {
      case (feaType, feaList) =>
        (feaType, feaList.zipWithIndex.map(a => (a._1, (a._2 + 1).toLong)).toMap)
    }.filter(_._2 != null).collectAsMap()
    featureGroupMap
  }

  def parseSampleTFRecord(sc: SparkContext, path: String, output_path: String, featureId: Map[String, Map[String, Long]]): Unit = {

    val features = sc.textFile(path).flatMap{ line => {
      val parts = line.split("\t")

      var featuresList = collection.mutable.Map[String, Int64List.Builder]()
      var valueList = collection.mutable.Map[String, FloatList.Builder]()

      // sparse embedding feature
      featuresList += ("uid" -> setFeatureId(parts(0).split(","), featureId("uid")))
      featuresList += ("city" -> setFeatureId(parts(1).split(","), featureId("city")))
      featuresList += ("item_id" -> setFeatureId(parts(2).split(","), featureId("item_id")))
      featuresList += ("author_id" -> setFeatureId(parts(3).split(","), featureId("author_id")))
      featuresList += ("item_city" -> setFeatureId(parts(4).split(","), featureId("item_city")))
      featuresList += ("channel" -> setFeatureId(parts(5).split(","), featureId("channel")))
      featuresList += ("music_id" -> setFeatureId(parts(8).split(","), featureId("music_id")))
      featuresList += ("device" -> setFeatureId(parts(9).split(","), featureId("device")))
      featuresList += ("duration_time" -> setFeatureId(parts(11).split(","), featureId("duration_time")))
      featuresList += ("title" -> setFeatureId(parts(12).split(","), featureId("title")))
      featuresList += ("gender" -> setFeatureId(parts(13).split(","), featureId("gender")))
      featuresList += ("beauty" -> setFeatureId(parts(14).split(","), featureId("beauty")))
      // dense feature
      valueList += ("video_embedding" -> setFeatureFloat(parts(15).split(",").map(line => line.toFloat)))

      val featureTF = Features.newBuilder()
      featuresList.map { fea =>
        featureTF.putFeature(fea._1, Feature.newBuilder().setInt64List(fea._2.build()).build())
      }
      valueList.map { fea =>
        featureTF.putFeature(fea._1, Feature.newBuilder().setFloatList(fea._2.build()).build())
      }

      val fininshed_label_list = Int64List.newBuilder().addValue(parts(6).toInt)
      val liked_label_list = Int64List.newBuilder().addValue(parts(7).toInt)

      featureTF.putFeature("finished_label", Feature.newBuilder().setInt64List(fininshed_label_list).build())
      featureTF.putFeature("liked_label", Feature.newBuilder().setInt64List(liked_label_list).build())
      val example = Example.newBuilder().setFeatures(featureTF).build()
      Some(new BytesWritable(example.toByteArray), NullWritable.get())

    }
    }
    features.coalesce(1000).saveAsNewAPIHadoopFile[TFRecordFileOutputFormat](output_path)

  }

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("DnnRecalFeatureExtractsPipeline").set("spark.executor.extraJavaOptions", "-Djava.util.Arrays.useLegacyMergeSort=true");
    val sc = new SparkContext(conf)
    val input_path = "/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/trunk1_output"
    val output_path = "/user/s_feeds/sunmingze/deep_learning/dnn_gsf_ffm_sample/tf_output"
    val featureGroupMap = initFeatureGroupIds(sc,input_path)
    parseSampleTFRecord(sc,input_path,output_path,featureGroupMap)

  }

}