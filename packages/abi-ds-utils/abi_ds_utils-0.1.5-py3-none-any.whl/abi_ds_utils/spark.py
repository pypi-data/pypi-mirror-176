import os
import multiprocessing
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


def getSpark() -> SparkSession:
    # Memory/CPU calculations based on:
    # https://spoddutur.github.io/spark-notes/distribution_of_executors_cores_and_memory_for_spark_application.html
    cpu_cores = multiprocessing.cpu_count()
    num_executors = cpu_cores - 2
    executor_cores = num_executors // 4

    spark = (
        SparkSession.builder
        # General
        .master('local[*]')
        .config("spark.driver.maxResultSize", 0)

        # Get 80% of free memory (this might be a bad idea)
        .config("spark.driver.memory", "10g")
        .config("spark.executor.memory", "10g")
        .config("spark.executor.cores", executor_cores)
        .config("spark.dynamicAllocation.enabled", "true")
        .config("spark.dynamicAllocation.minExecutors", "1")
        .config("spark.dynamicAllocation.maxExecutors", "5")


        # PyArrow for dtypes conversions
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")

        # Jars compatible with the base-notebook image (Python 3.8.8, PySpark 3.1.1)
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.1.1,io.delta:delta-core_2.12:1.0.1')

        # Delta Lake setup
        .config("spark.hadoop.fs.s3a.connection.maximum", 128)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    )
    if os.environ.get('AWS_SESSION_TOKEN') is not None:
        spark = spark.config(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider"
        )
    return spark.getOrCreate()


