import json
import random
import time
import logging
import os
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv
import pymysql

load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
PRODUCER_MODE = os.getenv("PRODUCER_MODE", "both")  # fake | real | both

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PostHogProducer")

USERS = [f"user_{i:03d}" for i in range(1, 11)]
PRODUCTS = [f"product_{i:03d}" for i in range(100, 110)]
EVENTS = ["product_viewed", "product_wishlisted", "checkout_initiated"]

def wait_for_kafka(server, retries=10, delay=5):
    for i in range(retries):
        try:
            logger.info(f"\u23f3 Attempt {i+1}/{retries} - Connecting to Kafka at {server}")
            producer = KafkaProducer(
                bootstrap_servers=server,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            logger.info("\u2705 Connected to Kafka successfully")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"\u274c Kafka not ready. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("\ud83d\udea8 Kafka connection failed after retries.")

def generate_fake_event():
    user = random.choice(USERS)
    product = random.choice(PRODUCTS)
    event_type = random.choice(EVENTS)
    timestamp = datetime.utcnow().isoformat()
    return {
        "user_id": user,
        "event": event_type,
        "properties": {
            "product_id": product,
            "timestamp": timestamp,
            "source": "posthog_event_producer"
        }
    }

def fetch_stock_events(last_id=0):
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stock_id, product_id, quantity_change, reason, timestamp, cart_id, order_id
        FROM stock_movements
        WHERE stock_id > %s
        ORDER BY stock_id ASC
        LIMIT 10;
    """, (last_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_user_from_cart_or_order(cart_id, order_id):
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    user_id = None
    if cart_id:
        cursor.execute("SELECT user_id FROM carts WHERE cart_id = %s", (cart_id,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]

    if not user_id and order_id:
        cursor.execute("SELECT user_id FROM orders WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]

    conn.close()
    return f"user_{user_id}" if user_id else "system"

def format_stock_event(row):
    stock_id, product_id, quantity_change, reason, timestamp, cart_id, order_id = row
    user = fetch_user_from_cart_or_order(cart_id, order_id)

    return {
        "user_id": user,
        "event": "stock_change",
        "properties": {
            "stock_id": stock_id,
            "product_id": f"product_{product_id:03d}",
            "quantity_change": quantity_change,
            "reason": reason,
            "timestamp": timestamp.isoformat(),
            "cart_id": cart_id,
            "order_id": order_id,
            "source": "stock_movement"
        }
    }

if __name__ == "__main__":
    logger.info("\ud83d\udce4 Starting PostHog Event Producer (Kafka + MySQL)")
    producer = wait_for_kafka(KAFKA_BOOTSTRAP_SERVERS)
    last_stock_id = 0

    try:
        while True:
            if PRODUCER_MODE in ["fake", "both"]:
                fake_event = generate_fake_event()
                producer.send(KAFKA_TOPIC, value=fake_event)
                logger.info(f"\ud83d\udce8 Sent FAKE event: {fake_event}")

            if PRODUCER_MODE in ["real", "both"]:
                stock_rows = fetch_stock_events(last_stock_id)
                for row in stock_rows:
                    stock_event = format_stock_event(row)
                    producer.send(KAFKA_TOPIC, value=stock_event)
                    logger.info(f"\ud83d\udce8 Sent STOCK event: {stock_event}")
                    last_stock_id = row[0]

            time.sleep(random.uniform(2, 20))
    except KeyboardInterrupt:
        logger.info("\ud83d\ude93 Producer stopped manually")
    finally:
        producer.flush()
        producer.close()
        logger.info("\u2705 Kafka producer closed cleanly")

