import pymysql
import os
import random
import json
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
fake = Faker()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

NUM_CARTS_TO_CREATE = 200
NUM_ORDERS_TO_GENERATE = 200

def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=True
    )

def get_random_users(cursor, limit=100):
    cursor.execute("SELECT user_id FROM users WHERE is_active=1 LIMIT %s", (limit,))
    return [row[0] for row in cursor.fetchall()]

def get_products_with_stock(cursor):
    cursor.execute("""
        SELECT p.product_id, p.price, i.quantity_available
        FROM products p
        JOIN inventory i ON p.product_id = i.product_id
        WHERE i.quantity_available > 0
    """)
    return cursor.fetchall()

def log_stock_movement(cursor, product_id, change_amount, reason, cart_id=None, order_id=None):
    cursor.execute("""
        INSERT INTO stock_movements (product_id, quantity_change, reason, timestamp, cart_id, order_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        product_id,
        change_amount,
        reason,
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        cart_id,
        order_id
    ))

def reserve_product_stock(cursor, product_id, quantity, cart_id=None):
    cursor.execute("SELECT quantity_available FROM inventory WHERE product_id=%s", (product_id,))
    result = cursor.fetchone()
    if not result or result[0] < quantity:
        return False

    cursor.execute("""
        UPDATE inventory
        SET quantity_available = quantity_available - %s,
            quantity_reserve = quantity_reserve + %s
        WHERE product_id = %s
    """, (quantity, quantity, product_id))

    log_stock_movement(cursor, product_id, -quantity, "cart reserve", cart_id=cart_id)
    return True

def create_cart(cursor, user_id):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO carts (user_id, created_at) VALUES (%s, %s)", (user_id, now))
    return cursor.lastrowid

def create_cart_items(cursor, cart_id, products, used_product_ids, max_items=5):
    items = []
    count = 0
    for product_id, price, qty in products:
        if product_id in used_product_ids or qty <= 0:
            continue

        quantity = random.randint(1, min(5, qty))
        if not reserve_product_stock(cursor, product_id, quantity, cart_id):
            continue

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, quantity, price, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cart_id, product_id, quantity, float(price), now, now))

        items.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": float(price)
        })
        used_product_ids.add(product_id)
        count += 1

        if count >= max_items:
            break
    return items

def create_order(cursor, user_id, items):
    total_amount = sum(item["price"] * item["quantity"] for item in items)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    shipping_address = fake.address().replace("\n", ", ")
    status = "pending"
    payment_method = random.choice(["Credit Card", "PayPal", "Cash"])

    cursor.execute("""
        INSERT INTO orders (user_id, order_date, items, total_amount, status, payment_method, shipping_address, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        now,
        json.dumps(items),
        total_amount,
        status,
        payment_method,
        shipping_address,
        now,
        now
    ))
    return cursor.lastrowid

def main():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        users = get_random_users(cursor)
        if not users:
            print("No active users found.")
            return

        print(f"Creating {NUM_CARTS_TO_CREATE} carts...")
        used_product_ids = set()

        for _ in range(NUM_CARTS_TO_CREATE):
            try:
                user_id = random.choice(users)
                products = get_products_with_stock(cursor)
                if not products:
                    continue
                cart_id = create_cart(cursor, user_id)
                items = create_cart_items(cursor, cart_id, products, used_product_ids)
                print(f"Cart {cart_id} created for user {user_id} with {len(items)} items.")
            except Exception as e:
                print("Cart creation failed:", e)
                conn.rollback()

        print(f"\nGenerating {NUM_ORDERS_TO_GENERATE} orders...")
        for _ in range(NUM_ORDERS_TO_GENERATE):
            try:
                user_id = random.choice(users)
                products = get_products_with_stock(cursor)
                selected = random.sample(products, min(5, len(products)))
                items = []

                for product_id, price, qty in selected:
                    if qty <= 0:
                        continue
                    quantity = random.randint(1, min(5, qty))
                    if reserve_product_stock(cursor, product_id, quantity):
                        items.append({
                            "product_id": product_id,
                            "quantity": quantity,
                            "price": float(price)
                        })

                if not items:
                    continue

                order_id = create_order(cursor, user_id, items)
                for item in items:
                    log_stock_movement(cursor, item["product_id"], -item["quantity"], "order placed", order_id=order_id)
                print(f"Order {order_id} created for user {user_id} with {len(items)} items.")
            except Exception as e:
                print("Order creation failed:", e)
                conn.rollback()

        print("Order generation complete.")

    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
