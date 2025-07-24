from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StringType, StructField, TimestampType
import sys

def main(bootstrap_servers, topic, bronze_path):
    spark = SparkSession.builder \
        .appName("KafkaToBronze") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    event_schema = StructType([
        StructField("user_id", StringType()),
        StructField("event", StringType()),
        StructField("properties", StructType([
            StructField("product_id", StringType()),
            StructField("timestamp", StringType()),
            StructField("source", StringType())
        ]))
    ])

    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

    df_parsed = df_kafka.selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), event_schema).alias("data")) \
        .select(
            col("data.user_id"),
            col("data.event").alias("event_type"),
            col("data.properties.product_id"),
            col("data.properties.timestamp").alias("event_ts"),
            col("data.properties.source")
        ) \
        .withColumn("ingestion_time", current_timestamp())

    query = df_parsed.writeStream \
        .format("parquet") \
        .option("checkpointLocation", f"{bronze_path}/_checkpoints/") \
        .option("path", bronze_path) \
        .partitionBy("event_type") \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: spark_streaming_kafka_to_bronze.py <bootstrap_servers> <topic> <bronze_output_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
