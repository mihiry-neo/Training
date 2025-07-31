from pyspark.sql import SparkSession
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def bronze_ingest(spark, jdbc_url, props, table, bronze_path, processing_date):
    print(f"\n Starting Bronze Ingestion for table: {table}")

    try:
        df = spark.read.jdbc(url=jdbc_url, table=table, properties=props)

        year, month, day = processing_date.split("-")

        output_path = os.path.join(bronze_path, "mysql", table, year, month, day)
        print(f"Writing output to: {output_path}")

        df.write.mode("overwrite").parquet(output_path)
        print(f"Successfully ingested '{table}' to Bronze at {output_path}\n")

    except Exception as e:
        print(f"Error during ingestion of table '{table}': {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\nUsage: python bronze_ingestion.py <table> <bronze_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    table_name = sys.argv[1]
    bronze_path = sys.argv[2]
    processing_date = sys.argv[3]

    mysql_host = os.getenv("MYSQL_HOST")
    mysql_port = os.getenv("MYSQL_PORT")
    mysql_db   = os.getenv("MYSQL_DATABASE")
    mysql_user = os.getenv("MYSQL_USER")
    mysql_pwd  = os.getenv("MYSQL_PASSWORD")

    if not all([mysql_user, mysql_pwd]):
        print("MYSQL_USER or MYSQL_PASSWORD not set in environment.")
        sys.exit(1)

    jdbc_url = f"jdbc:mysql://{mysql_host}:{mysql_port}/{mysql_db}"

    conn_props = {
        "user": mysql_user,
        "password": mysql_pwd,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    spark = SparkSession.builder \
        .appName(f"BronzeIngest_{table_name}") \
        .getOrCreate()

    bronze_ingest(spark, jdbc_url, conn_props, table_name, bronze_path, processing_date)

    spark.stop()
