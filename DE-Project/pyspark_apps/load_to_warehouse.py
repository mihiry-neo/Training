from pyspark.sql import SparkSession
import sys
import os
import traceback

def load_gold_table_to_postgres(spark, gold_table_path, pg_jdbc_url, connection_properties, target_table_name):
    """Loads a Gold Parquet table to a PostgreSQL table."""
    print(f"\n[INFO] Reading Gold data from: {gold_table_path}")
    try:
        df_gold = spark.read.parquet(gold_table_path)

        if df_gold.rdd.isEmpty():
            print(f"[WARNING] Skipped {target_table_name} – DataFrame is empty.")
            return

        print(f"[INFO] Writing to PostgreSQL table: {target_table_name}")
        df_gold.write \
            .mode("overwrite") \
            .jdbc(url=pg_jdbc_url, table=target_table_name, properties=connection_properties)

        print(f"[SUCCESS] Loaded data to PostgreSQL: {target_table_name}")

    except Exception as e:
        print(f"[ERROR] Failed to load {target_table_name} from path {gold_table_path}: {str(e)}")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: load_to_warehouse.py <gold_base_path> <pg_jdbc_url> <user> <password> <processing_date YYYY-MM-DD>")
        sys.exit(1)

    gold_base_path = sys.argv[1]      # e.g. /opt/data_lake/gold
    pg_jdbc_url = sys.argv[2]
    pg_user = sys.argv[3]
    pg_password = sys.argv[4]
    processing_date = sys.argv[5]

    print(f"\n[INFO] Starting warehouse load for date: {processing_date}")
    spark = SparkSession.builder.appName("LoadGoldToWarehouse").getOrCreate()

    connection_props = {
        "user": pg_user,
        "password": pg_password,
        "driver": "org.postgresql.Driver"
    }

    # Gold tables and their target PostgreSQL warehouse destinations
    gold_targets = {
        "product_daily_performance": "facts.fact_orders",
        "sales_daily_summary": "facts.sales_summary",
        "customer_segments": "dimensions.customer_segments"
    }

    for gold_folder, target_table in gold_targets.items():
        full_gold_path = os.path.join(gold_base_path, f"{gold_folder}/report_date={processing_date}")
        print(f"\n[INFO] Processing: {gold_folder} → {target_table}")
        load_gold_table_to_postgres(
            spark,
            full_gold_path,
            pg_jdbc_url,
            connection_props,
            target_table
        )

    print("\n[SUCCESS] All gold tables processed successfully.\n")
    spark.stop()
