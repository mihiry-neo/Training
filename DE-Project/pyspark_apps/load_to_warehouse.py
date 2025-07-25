from pyspark.sql import SparkSession
import os
import sys
import traceback
from dotenv import load_dotenv

# Load from .env for local testing (no effect inside Docker)
load_dotenv()

def load_gold_table_to_postgres(spark, gold_table_path, pg_jdbc_url, connection_properties, target_table_name):
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
    if len(sys.argv) != 3:
        print("Usage: load_to_warehouse.py <gold_base_path> <processing_date YYYY-MM-DD>")
        sys.exit(1)

    gold_base_path = sys.argv[1]
    processing_date = sys.argv[2]

    print(f"\n[INFO] Starting warehouse load for date: {processing_date}")
    spark = SparkSession.builder.appName("LoadGoldToWarehouse").getOrCreate()

    # Load credentials and DB config from env
    pg_user = os.getenv("POSTGRES_USER")
    pg_password = os.getenv("POSTGRES_PASSWORD")
    pg_host = os.getenv("POSTGRES_HOST", "postgres_dw")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_db = os.getenv("POSTGRES_DB", "airflow")

    if not pg_user or not pg_password:
        print("❌ Missing PostgreSQL credentials in environment.")
        sys.exit(1)

    # Construct JDBC URL
    pg_jdbc_url = f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}"

    connection_props = {
        "user": pg_user,
        "password": pg_password,
        "driver": "org.postgresql.Driver"
    }

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
