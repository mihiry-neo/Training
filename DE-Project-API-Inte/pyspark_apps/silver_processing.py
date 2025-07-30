from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, to_date, round as spark_round, explode, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, ArrayType
import sys
import os

def path_exists(spark, path):
    hadoop_conf = spark._jsc.hadoopConfiguration()
    fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)
    return fs.exists(spark._jvm.org.apache.hadoop.fs.Path(path))

def process_users_to_silver(spark, bronze_path, silver_path, processing_date):
    year, month, day = processing_date.split('-')
    raw_users_path = os.path.join(bronze_path, "mysql", "users", year, month, day)
    silver_users_path = os.path.join(silver_path, f"users_cleaned/processed_date={processing_date}")

    if not path_exists(spark, raw_users_path):
        print(f"⚠️ Skipping users processing — no data found at {raw_users_path}")
        return

    print(f"\n👤 Processing users from: {raw_users_path}")
    try:
        df = spark.read.parquet(raw_users_path)

        df = df.withColumn("email", lower(trim(col("email")))) \
               .withColumn("signup_date", to_date(col("created_at"))) \
               .fillna({
                   "email": "unknown@example.com",
                   "signup_date": "2000-01-01"
               })

        df_silver = df.select(
            col("user_id").cast("int").alias("customer_id"),
            col("username").alias("name"),
            col("email"),
            col("phone_number").alias("phone"),
            col("signup_date")
        )

        df_silver.write.mode("overwrite").parquet(silver_users_path)
        print(f"✅ Users written to Silver: {silver_users_path}")

    except Exception as e:
        print(f"❌ Failed to process users: {e}")
        raise

def process_products_to_silver(spark, bronze_path, silver_path, processing_date):
    year, month, day = processing_date.split('-')
    raw_products_path = os.path.join(bronze_path, "mysql", "products", year, month, day)
    silver_products_path = os.path.join(silver_path, f"products_cleaned/processed_date={processing_date}")

    if not path_exists(spark, raw_products_path):
        print(f"⚠️ Skipping products processing — no data found at {raw_products_path}")
        return

    print(f"\n📦 Processing products from: {raw_products_path}")
    try:
        df_products = spark.read.parquet(raw_products_path)

        df_cleaned = df_products.filter(
            (col("product_id").isNotNull()) &
            (col("name").isNotNull()) &
            (col("price") > 0)
        )

        df_silver = df_cleaned.select(
            col("product_id").cast("int"),
            col("name").alias("product_name"),
            col("brand"),
            col("price").cast("double"),
            col("category_id").cast("int"),
            to_date(col("created_at")).alias("created_date")
        )

        df_silver.write.mode("overwrite").parquet(silver_products_path)
        print(f"✅ Products written to Silver: {silver_products_path}")

    except Exception as e:
        print(f"❌ Failed to process products: {e}")
        raise

def process_orders_to_silver(spark, bronze_path, silver_path, processing_date):
    year, month, day = processing_date.split('-')
    raw_orders_path = os.path.join(bronze_path, "mysql", "orders", year, month, day)
    silver_orders_path = os.path.join(silver_path, f"orders_cleaned/processed_date={processing_date}")
    silver_users_path = os.path.join(silver_path, f"users_cleaned/processed_date={processing_date}")
    silver_products_path = os.path.join(silver_path, f"products_cleaned/processed_date={processing_date}")

    for path in [raw_orders_path, silver_users_path, silver_products_path]:
        if not path_exists(spark, path):
            print(f"⚠️ Skipping orders processing — required data missing at: {path}")
            return

    print(f"\n🧾 Processing orders from: {raw_orders_path}")
    try:
        orders_df = spark.read.parquet(raw_orders_path)
        users_df = spark.read.parquet(silver_users_path)
        products_df = spark.read.parquet(silver_products_path)

        df_orders = orders_df.select("order_id", "user_id", "items", "order_date") \
                             .withColumnRenamed("user_id", "customer_id")

        # SOLUTION 1: Parse JSON string to array and then explode
        # Define the schema for items array
        item_schema = ArrayType(
            StructType([
                StructField("product_id", IntegerType(), True),
                StructField("quantity", IntegerType(), True),
                StructField("price", DoubleType(), True)
            ])
        )
        
        # Parse JSON string and then explode
        df_orders = df_orders.withColumn("items_parsed", from_json(col("items"), item_schema)) \
                             .withColumn("item", explode(col("items_parsed")))

        df_orders = df_orders.select(
            col("order_id").cast("int"),
            col("customer_id").cast("int"),
            col("item.product_id").cast("int").alias("product_id"),
            col("item.quantity").cast("int").alias("quantity"),
            col("item.price").cast("double").alias("item_price"),
            col("order_date")
        )

        # Join with users and products
        df = df_orders.join(users_df, on="customer_id", how="inner") \
                      .join(products_df.select("product_id", "price").alias("prod"), 
                           on="product_id", how="inner")

        # Calculate total price using product price and quantity
        df = df.withColumn("total_price", spark_round(col("price") * col("quantity"), 2))

        df_silver = df.select(
            col("order_id"),
            col("customer_id"),
            col("product_id"),
            col("quantity"),
            col("total_price"),
            to_date(col("order_date")).alias("order_date")
        )

        df_silver.write.mode("overwrite").parquet(silver_orders_path)
        print(f"✅ Orders written to Silver: {silver_orders_path}")

    except Exception as e:
        print(f"❌ Failed to process orders: {e}")
        raise

def process_categories_to_silver(spark, bronze_path, silver_path, processing_date):
    year, month, day = processing_date.split('-')
    raw_path = os.path.join(bronze_path, "mysql", "categories", year, month, day)
    silver_output_path = os.path.join(silver_path, f"categories_cleaned/processed_date={processing_date}")

    if not path_exists(spark, raw_path):
        print(f"⚠️ Skipping categories processing — no data found at {raw_path}")
        return

    print(f"\n📁 Processing categories from: {raw_path}")
    try:
        df = spark.read.parquet(raw_path)

        df_cleaned = df.select(
            col("category_id").cast("int"),
            trim(col("name")).alias("category_name"),
            col("parent_id").cast("int"),
            to_timestamp("created_at").alias("created_at"),
            to_timestamp("updated_at").alias("updated_at")
        )


        df_cleaned.write.mode("overwrite").parquet(silver_output_path)
        print(f"✅ Categories written to Silver: {silver_output_path}")

    except Exception as e:
        print(f"❌ Failed to process categories: {e}")
        raise

# === ✅ Inventory ===
def process_inventory_to_silver(spark, bronze_path, silver_path, processing_date):
    year, month, day = processing_date.split('-')
    raw_path = os.path.join(bronze_path, "mysql", "inventory", year, month, day)
    silver_output_path = os.path.join(silver_path, f"inventory_cleaned/processed_date={processing_date}")

    if not path_exists(spark, raw_path):
        print(f"⚠️ Skipping inventory processing — no data found at {raw_path}")
        return

    print(f"\n📦 Processing inventory from: {raw_path}")
    try:
        df = spark.read.parquet(raw_path)

        df_cleaned = df.select(
            col("inv_id").cast("int").alias("inventory_id"),
            col("product_id").cast("int"),
            col("quantity_available").cast("int"),
            col("quantity_reserve").cast("int"),
            col("reorder_level").cast("int"),
            col("reorder_quantity").cast("int"),
            col("unit_cost").cast("decimal(10,2)"),
            to_timestamp("last_restocked").alias("last_restocked"),
            to_timestamp("expiry_date").alias("expiry_date"),
            trim(col("batch_number")).alias("batch_number"),
            trim(col("location")).alias("location"),
            to_timestamp("last_updated").alias("last_updated")
        ).dropna(subset=["product_id", "quantity_available"])


        df_cleaned.write.mode("overwrite").parquet(silver_output_path)
        print(f"✅ Inventory written to Silver: {silver_output_path}")

    except Exception as e:
        print(f"❌ Failed to process inventory: {e}")
        raise


def debug_items_structure(spark, bronze_path, processing_date):
    """
    Helper function to inspect the structure of items column
    """
    year, month, day = processing_date.split('-')
    raw_orders_path = os.path.join(bronze_path, "mysql", "orders", year, month, day)
    
    if not path_exists(spark, raw_orders_path):
        print(f"⚠️ No data found at {raw_orders_path}")
        return
    
    orders_df = spark.read.parquet(raw_orders_path)
    
    # Show schema
    print("📋 Orders DataFrame Schema:")
    orders_df.printSchema()
    
    # Show sample data
    print("\n📄 Sample items data:")
    orders_df.select("order_id", "items").show(5, truncate=False)
    
    # Show data types
    print(f"\n🔍 Items column type: {dict(orders_df.dtypes)['items']}")

if __name__ == "__main__":
    if len(sys.argv) not in [4, 5]:
        print("\n❌ Usage: python silver_processing.py <bronze_path> <silver_path> <processing_date YYYY-MM-DD> [debug]")
        sys.exit(1)

    bronze_path = sys.argv[1]
    silver_path = sys.argv[2]
    processing_date = sys.argv[3]

    spark = SparkSession.builder.appName("SilverProcessingEcommerce").getOrCreate()

    if len(sys.argv) == 5 and sys.argv[4] == "debug":
        debug_items_structure(spark, bronze_path, processing_date)
        spark.stop()
        sys.exit(0)

    process_users_to_silver(spark, bronze_path, silver_path, processing_date)
    process_products_to_silver(spark, bronze_path, silver_path, processing_date)
    process_orders_to_silver(spark, bronze_path, silver_path, processing_date)
    process_categories_to_silver(spark, bronze_path, silver_path, processing_date)
    process_inventory_to_silver(spark, bronze_path, silver_path, processing_date)

    spark.stop()
