// Databricks notebook source
//import spark.implicits._

val columns = Seq("c1", "c2")
val data = Seq(("a", "b"), ("c", "d"))
val df = spark.createDataFrame(data).toDF(columns:_*)

df.show