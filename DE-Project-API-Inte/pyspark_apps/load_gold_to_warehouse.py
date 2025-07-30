from pyspark.sql import SparkSession
import os
import sys
import traceback
from dotenv import load_dotenv

# Load .env vars
load_dotenv()

def load_parquet_to_postgres(spark, parquet_path, jdbc_url, props, target_table):
    print(f"\n📂 Reading data from: {parquet_path}")
    try:
        df = spark.read.parquet(parquet_path)

        if df.rdd.isEmpty():
            print(f"⚠️ Skipping {target_table} — DataFrame is empty.")
            return

        print(f"🛠️ Writing to PostgreSQL table: {target_table}")
        df.write \
            .mode("overwrite") \
            .jdbc(url=jdbc_url, table=target_table, properties=props)

        print(f"✅ Success — Loaded to warehouse: {target_table}")
    except Exception as e:
        print(f"❌ Failed to load {target_table}: {e}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\n❌ Usage: python load_gold_to_postgres.py <base_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    base_path = sys.argv[1]
    processing_date = sys.argv[2]

    print(f"\n🚀 Starting GOLD layer load for processing date: {processing_date}")

    spark = SparkSession.builder.appName("LoadGoldToPostgres").getOrCreate()

    pg_user = os.getenv("POSTGRES_USER")
    pg_password = os.getenv("POSTGRES_PASSWORD")
    pg_host = os.getenv("POSTGRES_HOST", "postgres_dw")
    pg_port = os.getenv("POSTGRES_PORT", "5432")
    pg_db = os.getenv("POSTGRES_DB", "airflow")

    if not pg_user or not pg_password:
        print("❌ Missing PostgreSQL credentials.")
        sys.exit(1)

    jdbc_url = f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}"
    conn_props = {
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
        path = os.path.join(base_path, f"{gold_folder}/report_date={processing_date}")
        print(f"\n📌 Loading {gold_folder} → {target_table}")
        load_parquet_to_postgres(spark, path, jdbc_url, conn_props, target_table)

    print("\n🎉 GOLD layer successfully loaded!\n")
    spark.stop()
