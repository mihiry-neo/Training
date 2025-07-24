from pyspark.sql import SparkSession
import sys
import os

def bronze_ingest(spark, jdbc_url, props, table, bronze_path, processing_date):
    print(f"\n🔄 Starting Bronze Ingestion for table: {table}")

    try:
        # Read from MySQL using JDBC
        df = spark.read.jdbc(url=jdbc_url, table=table, properties=props)

        # Parse date from CLI
        year, month, day = processing_date.split("-")

        # Define HDFS/Local output path
        output_path = os.path.join(bronze_path, "mysql", table, year, month, day)
        print(f"📁 Writing output to: {output_path}")

        # Write as Parquet
        df.write.mode("overwrite").parquet(output_path)
        print(f"✅ Successfully ingested '{table}' to Bronze at {output_path}\n")

    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("\n❌ Usage: python bronze_ingestion.py <jdbc_url> <user> <password> <table> <bronze_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    jdbc_url = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]
    table_name = sys.argv[4]
    bronze_path = sys.argv[5]
    processing_date = sys.argv[6]  # Expects format: YYYY-MM-DD

    spark = SparkSession.builder \
        .appName(f"BronzeIngest_{table_name}") \
        .getOrCreate()

    conn_props = {
        "user": user,
        "password": pwd,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    bronze_ingest(spark, jdbc_url, conn_props, table_name, bronze_path, processing_date)

    spark.stop()
