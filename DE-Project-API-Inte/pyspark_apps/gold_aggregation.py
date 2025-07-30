from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum as _sum, count as _count, max as _max, datediff,
    date_format, lit, when, to_date
)
from pyspark.sql.utils import AnalysisException
import sys
import os


def create_product_performance_summary(spark, silver_path, gold_path, processing_date):
    silver_orders_path = os.path.join(silver_path, f"orders_cleaned/processed_date={processing_date}")
    output_path = os.path.join(gold_path, f"product_daily_performance/report_date={processing_date}")

    print(f"\n📊 Generating product performance from: {silver_orders_path}")
    try:
        df = spark.read.parquet(silver_orders_path)

        df_summary = df.groupBy(
            col("product_id"),
            date_format(col("order_date"), "yyyy-MM-dd").alias("sale_date")
        ).agg(
            _count("order_id").alias("orders_count"),
            _sum("total_price").alias("total_sales")
        ).withColumn("report_date", lit(processing_date))

        df_summary.write.mode("overwrite").parquet(output_path)
        print(f"✅ Product performance written to: {output_path}")
    except AnalysisException:
        print(f"⚠️ No silver orders found for product performance.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def create_sales_daily_summary(spark, silver_path, gold_path, processing_date):
    silver_orders_path = os.path.join(silver_path, f"orders_cleaned/processed_date={processing_date}")
    output_path = os.path.join(gold_path, f"sales_daily_summary/report_date={processing_date}")

    print(f"\n📈 Generating daily sales summary from: {silver_orders_path}")
    try:
        df = spark.read.parquet(silver_orders_path)

        df_summary = df.groupBy("order_date").agg(
            _count("order_id").alias("total_orders"),
            _sum("total_price").alias("total_sales")
        ).withColumn("avg_order_value", col("total_sales") / col("total_orders")) \
        .withColumn("report_date", lit(processing_date))


        df_summary.write.mode("overwrite").parquet(output_path)
        print(f"✅ Sales summary written to: {output_path}")
    except AnalysisException:
        print(f"⚠️ No silver orders found for sales summary.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def create_customer_segments(spark, silver_path, gold_path, processing_date):
    silver_orders_path = os.path.join(silver_path, f"orders_cleaned/processed_date={processing_date}")
    output_path = os.path.join(gold_path, f"customer_segments/report_date={processing_date}")

    print(f"\n👥 Generating customer segments from: {silver_orders_path}")
    try:
        df = spark.read.parquet(silver_orders_path)

        df_rfm = df.groupBy("customer_id").agg(
            _max("order_date").alias("last_order_date"),
            _count("order_id").alias("frequency"),
            _sum("total_price").alias("monetary_value")
        )

        df_rfm = df_rfm.withColumn("recency_days", datediff(
            to_date(lit(processing_date)), col("last_order_date"))
        )

        df_segmented = df_rfm.withColumn("segment", when(
            (col("recency_days") <= 30) & (col("frequency") >= 5) & (col("monetary_value") >= 5000), "Platinum"
        ).when(
            (col("recency_days") <= 60) & (col("frequency") >= 3), "Gold"
        ).when(
            (col("recency_days") <= 90) & (col("frequency") >= 2), "Silver"
        ).otherwise("Bronze"))

        df_segmented = df_segmented.withColumn("report_date", lit(processing_date))

        df_segmented.write.mode("overwrite").parquet(output_path)
        print(f"✅ Customer segments written to: {output_path}")
    except AnalysisException:
        print(f"⚠️ No silver orders found for customer segmentation.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\n❌ Usage: python gold_aggregation.py <silver_base_path> <gold_base_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    silver_path = sys.argv[1]
    gold_path = sys.argv[2]
    processing_date = sys.argv[3]

    spark = SparkSession.builder.appName("GoldAggregationEcommerce").getOrCreate()

    create_product_performance_summary(spark, silver_path, gold_path, processing_date)
    create_sales_daily_summary(spark, silver_path, gold_path, processing_date)
    create_customer_segments(spark, silver_path, gold_path, processing_date)

    spark.stop()
