from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count, date_format, lit, max as _max, datediff, when
import sys
import os

def create_product_performance_summary(spark, silver_base_path, gold_base_path, processing_date_str):
    silver_orders_path = os.path.join(silver_base_path, f"orders_cleaned/processed_date={processing_date_str}")
    gold_product_summary_path = os.path.join(gold_base_path, f"product_daily_performance/report_date={processing_date_str}")

    print(f"\n🔍 Reading cleaned orders from: {silver_orders_path}")
    try:
        df_orders_silver = spark.read.parquet(silver_orders_path)

        df_product_summary = (
            df_orders_silver.groupBy(
                col("product_id"),
                date_format(col("order_date"), "yyyy-MM-dd").alias("sale_date")
            )
            .agg(
                _count("order_id").alias("orders_count"),
                _sum("total_price").alias("total_sales")
            )
            .withColumn("report_date", lit(processing_date_str))
        )

        print(f"📁 Writing product performance summary to: {gold_product_summary_path}")
        df_product_summary.write.mode("overwrite").parquet(gold_product_summary_path)

        print(f"✅ Successfully created product performance summary: {gold_product_summary_path}\n")
    except Exception as e:
        print(f"❌ Error during product performance summary: {e}")
        raise

def create_sales_daily_summary(spark, silver_base_path, gold_base_path, processing_date_str):
    silver_orders_path = os.path.join(silver_base_path, f"orders_cleaned/processed_date={processing_date_str}")
    gold_summary_path = os.path.join(gold_base_path, f"sales_daily_summary/report_date={processing_date_str}")

    df_orders = spark.read.parquet(silver_orders_path)
    df_summary = df_orders.groupBy("order_date").agg(
        _count("order_id").alias("orders_count"),
        _sum("total_price").alias("total_sales")
    ).withColumn("report_date", lit(processing_date_str))

    df_summary.write.mode("overwrite").parquet(gold_summary_path)

def create_customer_segments(spark, silver_path, gold_path, processing_date):
    df = spark.read.parquet(os.path.join(silver_path, f"orders_cleaned/processed_date={processing_date}"))

    df_rfm = df.groupBy("customer_id").agg(
        _max("order_date").alias("last_order_date"),
        _count("order_id").alias("frequency"),
        _sum("total_price").alias("monetary_value")
    )

    df_rfm = df_rfm.withColumn("recency_days", datediff(lit(processing_date), col("last_order_date")))

    df_segmented = df_rfm.withColumn("segment", when(
        (col("recency_days") <= 30) & (col("frequency") >= 5) & (col("monetary_value") >= 5000), "Platinum"
    ).when(
        (col("recency_days") <= 60) & (col("frequency") >= 3), "Gold"
    ).when(
        (col("recency_days") <= 90) & (col("frequency") >= 2), "Silver"
    ).otherwise("Bronze"))

    df_segmented = df_segmented.withColumn("report_date", lit(processing_date))

    output_path = os.path.join(gold_path, f"customer_segments/report_date={processing_date}")
    df_segmented.write.mode("overwrite").parquet(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\n❌ Usage: python gold_aggregation_cleaned.py <silver_base_path> <gold_base_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    silver_path_arg = sys.argv[1]
    gold_path_arg = sys.argv[2]
    date_arg = sys.argv[3]

    spark_session = SparkSession.builder.appName("GoldAggregationCleaned").getOrCreate()

    create_product_performance_summary(spark_session, silver_path_arg, gold_path_arg, date_arg)
    create_sales_daily_summary(spark_session, silver_path_arg, gold_path_arg, date_arg)
    create_customer_segments(spark_session, silver_path_arg, gold_path_arg, date_arg)

    spark_session.stop()
