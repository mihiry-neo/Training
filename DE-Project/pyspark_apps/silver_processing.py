from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, to_date, split, when, lit, round as spark_round
from pyspark.sql.utils import AnalysisException
import sys
import os


def process_customers_to_silver(spark, bronze_base_path, silver_base_path, processing_date_str):
    """Cleans and transforms raw customers data to the Silver layer."""
    year, month, day = processing_date_str.split('-')
    raw_customers_path = os.path.join(bronze_base_path, "customers", year, month, day)
    silver_customers_path = os.path.join(silver_base_path, f"customers_cleaned/processed_date={processing_date_str}")

    print(f"\n👤 Processing customers from: {raw_customers_path}")
    try:
        df_customers = spark.read.parquet(raw_customers_path)

        df_customers = df_customers.withColumn("name_parts", split(col("name"), " ")) \
                                   .withColumn("first_name", lower(trim(col("name_parts").getItem(0)))) \
                                   .withColumn("last_name", lower(trim(
                                       when(col("name_parts").getItem(1).isNotNull(), col("name_parts").getItem(1))
                                       .otherwise(lit("")))))

        df_customers_cleaned = df_customers.withColumn("email", lower(trim(col("email")))) \
                                           .withColumn("signup_date", to_date(col("created_at"), "yyyy-MM-dd")) \
                                           .fillna({
                                               "email": "unknown@example.com",
                                               "signup_date": "2000-01-01"
                                           })

        df_customers_silver = df_customers_cleaned.select(
            col("customer_id").cast("int"),
            col("first_name"),
            col("last_name"),
            col("email"),
            col("signup_date"),
            col("address").cast("string")
        )

        df_customers_silver.write.mode("overwrite").parquet(silver_customers_path)
        print(f"✅ Customers written to Silver: {silver_customers_path}")

    except AnalysisException:
        print(f"⚠️ No customers data found at: {raw_customers_path} — skipping.")
    except Exception as e:
        print(f"❌ Error processing customers: {e}")
        raise


def process_products_to_silver(spark, bronze_base_path, silver_base_path, processing_date_str):
    year, month, day = processing_date_str.split('-')
    raw_products_path = os.path.join(bronze_base_path, "products", year, month, day)
    silver_products_path = os.path.join(silver_base_path, f"products_cleaned/processed_date={processing_date_str}")

    print(f"\n📦 Processing products from: {raw_products_path}")
    try:
        df = spark.read.parquet(raw_products_path)

        df_cleaned = df.filter(
            (col("product_id").isNotNull()) &
            (col("product_name").isNotNull()) &
            (col("price") > 0) &
            (col("stock_quantity") >= 0)
        )

        df_silver = df_cleaned.select(
            col("product_id").cast("int"),
            col("product_name"),
            col("category"),
            col("price").cast("double"),
            col("stock_quantity").cast("int"),
            to_date(col("created_at")).alias("created_date")
        )

        df_silver.write.mode("overwrite").parquet(silver_products_path)
        print(f"✅ Products written to Silver: {silver_products_path}")

    except AnalysisException:
        print(f"⚠️ No products data found at: {raw_products_path} — skipping.")
    except Exception as e:
        print(f"❌ Error processing products: {e}")
        raise


def process_orders_to_silver(spark, bronze_base_path, silver_base_path, processing_date_str):
    year, month, day = processing_date_str.split('-')
    raw_orders_path = os.path.join(bronze_base_path, "orders", year, month, day)
    silver_orders_path = os.path.join(silver_base_path, f"orders_cleaned/processed_date={processing_date_str}")
    silver_customers_path = os.path.join(silver_base_path, f"customers_cleaned/processed_date={processing_date_str}")
    silver_products_path = os.path.join(silver_base_path, f"products_cleaned/processed_date={processing_date_str}")

    print(f"\n🧾 Processing orders from: {raw_orders_path}")
    try:
        orders_df = spark.read.parquet(raw_orders_path)
        customers_df = spark.read.parquet(silver_customers_path)
        products_df = spark.read.parquet(silver_products_path)

        df = orders_df.join(customers_df.select("customer_id"), on="customer_id", how="inner") \
                      .join(products_df.select("product_id", "price"), on="product_id", how="inner") \
                      .filter(col("quantity") > 0)

        df = df.withColumn("expected_price", spark_round(col("price") * col("quantity"), 2)) \
               .withColumn("total_price", col("expected_price")) \
               .drop("expected_price")

        df_silver = df.select(
            col("order_id").cast("int"),
            col("customer_id").cast("int"),
            col("product_id").cast("int"),
            col("quantity").cast("int"),
            col("total_price").cast("double"),
            to_date(col("order_date")).alias("order_date")
        )

        df_silver.write.mode("overwrite").parquet(silver_orders_path)
        print(f"✅ Orders written to Silver: {silver_orders_path}")

    except AnalysisException:
        print(f"⚠️ Missing orders or reference data. Skipping orders transformation.")
    except Exception as e:
        print(f"❌ Error processing orders: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\n❌ Usage: python silver_processing.py <bronze_base_path> <silver_base_path> <processing_date YYYY-MM-DD>\n")
        sys.exit(1)

    bronze_path = sys.argv[1]   # Expects: /opt/ecommerce_data_lake/bronze/mysql
    silver_path = sys.argv[2]   # Expects: /opt/ecommerce_data_lake/silver
    processing_date = sys.argv[3]

    spark = SparkSession.builder.appName("SilverProcessingEcommerce").getOrCreate()

    process_customers_to_silver(spark, bronze_path, silver_path, processing_date)
    process_products_to_silver(spark, bronze_path, silver_path, processing_date)
    process_orders_to_silver(spark, bronze_path, silver_path, processing_date)

    spark.stop()
