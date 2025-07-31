from pyspark.sql import SparkSession
import os
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()

def load_parquet_to_postgres(spark, parquet_path, jdbc_url, props, target_table):
    print(f"\n Reading data from: {parquet_path}")
    try:
        df = spark.read.parquet(parquet_path)

        if df.rdd.isEmpty():
            print(f" Skipping {target_table} — DataFrame is empty.")
            return

        print(f" Writing to PostgreSQL table: {target_table}")
        df.write \
            .mode("overwrite") \
            .jdbc(url=jdbc_url, table=target_table, properties=props)

        print(f" Success — Loaded to warehouse: {target_table}")
    except Exception as e:
        print(f" Failed to load {target_table}: {e}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\n Usage: python load_silver_to_warehouse.py <base_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)
        
    base_path = sys.argv[1]
    processing_date = sys.argv[2]

    silver_base_path = "/opt/data_lake/silver"

    print(f"\n Starting SILVER layer load for processed date: {processing_date}")

    spark = SparkSession.builder.appName("LoadSilverToPostgres").getOrCreate()

    pg_user = os.getenv("POSTGRES_USER")
    pg_password = os.getenv("POSTGRES_PASSWORD")
    pg_host = os.getenv("POSTGRES_HOST")
    pg_port = os.getenv("POSTGRES_PORT")
    pg_db = os.getenv("POSTGRES_DB")

    if not pg_user or not pg_password:
        print(" Missing PostgreSQL credentials.")
        sys.exit(1)

    jdbc_url = f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}"
    conn_props = {
        "user": pg_user,
        "password": pg_password,
        "driver": "org.postgresql.Driver"
    }

    silver_targets = {
        "categories_cleaned": "dimensions.dim_categories",
        "products_cleaned": "dimensions.dim_products",
        "users_cleaned": "dimensions.dim_users"
    }

    for silver_folder, target_table in silver_targets.items():
        path = os.path.join(silver_base_path, f"{silver_folder}/processed_date={processing_date}")
        print(f"\n Loading {silver_folder} → {target_table}")
        load_parquet_to_postgres(spark, path, jdbc_url, conn_props, target_table)

    print("\n SILVER layer successfully loaded!\n")
    spark.stop()
