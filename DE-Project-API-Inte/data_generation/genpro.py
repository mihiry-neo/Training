import pymysql
import os
import random
import json
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
fake = Faker()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

BRANDS = ["Astra", "Zenex", "Nova", "UrbanMode", "GearPro", "CraftHaus", "NextEra", "Skyline", "PureEssence", "Flytek"]

CATEGORY_STRUCTURE = {
    "Fashion": ["Clothing", "Footwear", "Accessories"],
    "Electronics": ["Mobiles", "Laptops", "Appliances"],
    "Home & Garden": ["Decor", "Plants", "Kitchen"],
    "Food & Beverage": ["Snacks", "Drinks", "Groceries"],
    "Health & Beauty": ["Skincare", "Supplements", "Makeup"],
}

def insert_categories(cursor):
    category_id_map = {}
    for main, subs in CATEGORY_STRUCTURE.items():
        cursor.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s)", (main, None))
        main_id = cursor.lastrowid
        category_id_map[main] = main_id
        for sub in subs:
            full_name = f"{main} - {sub}"
            cursor.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s)", (full_name, main_id))
            category_id_map[full_name] = cursor.lastrowid
    return category_id_map

def generate_product_data(category_map, count=1000):
    products = []
    used_names = set()

    while len(products) < count:
        category_name = random.choice(list(category_map.keys()))
        category_id = category_map[category_name]

        name = f"{fake.unique.word().capitalize()} {fake.unique.word().capitalize()}"
        if name in used_names:
            continue
        used_names.add(name)

        price = round(random.uniform(100.0, 1500.0), 2)
        brand = random.choice(BRANDS)
        attributes = {
            "color": fake.color_name(),
            "weight": f"{round(random.uniform(1.0, 5.0), 2)} kg",
            "material": random.choice(["Cotton", "Plastic", "Metal", "Wood", "Glass"]),
            "rating": round(random.uniform(3.0, 5.0), 1)
        }
        created_at = updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        products.append({
            "name": name,
            "price": price,
            "brand": brand,
            "attributes": json.dumps(attributes),
            "category_id": category_id,
            "created_at": created_at,
            "updated_at": updated_at
        })

    return products

def insert_products_and_inventory(cursor, products):
    for p in products:
        cursor.execute("""
            INSERT INTO products (name, price, brand, attributes, category_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (p["name"], p["price"], p["brand"], p["attributes"], p["category_id"], p["created_at"], p["updated_at"]))

        product_id = cursor.lastrowid
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        expiry = (datetime.utcnow() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO inventory (product_id, quantity_available, quantity_reserve, reorder_level,
                                   reorder_quantity, unit_cost, last_restocked, expiry_date,
                                   batch_number, location, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product_id,
            random.randint(10, 500),
            random.randint(0, 20),
            10,
            50,
            round(p["price"] * random.uniform(0.3, 0.7), 2),
            now,
            expiry,
            fake.uuid4(),
            fake.city(),
            now
        ))

def main(total=1000):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        print("Inserting categories...")
        category_map = insert_categories(cursor)
        print(f"Generating {total} products...")
        products = generate_product_data(category_map, count=total)
        insert_products_and_inventory(cursor, products)
        print(f"Inserted {len(products)} products with inventory.")
    except Exception as e:
        print("Error during product generation:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
