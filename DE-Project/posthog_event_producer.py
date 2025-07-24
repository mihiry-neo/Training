import json
import random
import time
import logging
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# === CONFIG ===
KAFKA_TOPIC = "ecommerce_events"
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"  # Correct for Docker Compose networking

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PostHogProducer")

# === Sample Users and Events ===
USERS = [f"user_{i:03d}" for i in range(1, 11)]
PRODUCTS = [f"product_{i:03d}" for i in range(100, 110)]
EVENTS = ["product_viewed", "add_to_cart", "checkout_initiated"]

# === Wait for Kafka to Be Available ===
def wait_for_kafka(server, retries=10, delay=5):
    for i in range(retries):
        try:
            logger.info(f"⏳ Attempt {i+1}/{retries} - Connecting to Kafka at {server}")
            producer = KafkaProducer(
                bootstrap_servers=server,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            logger.info("✅ Connected to Kafka successfully")
            return producer
        except NoBrokersAvailable:
            logger.warning(f"❌ Kafka not ready. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("🚨 Kafka connection failed after retries.")

# === Event Generator ===
def generate_event():
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

# === Main Producer Logic ===
if __name__ == "__main__":
    logger.info("📤 Starting PostHog Event Producer (Kafka)")
    producer = wait_for_kafka(KAFKA_BOOTSTRAP_SERVERS)

    try:
        while True:
            event = generate_event()
            producer.send(KAFKA_TOPIC, value=event)
            logger.info(f"📨 Sent event: {event}")
            time.sleep(random.uniform(60, 180))  # Simulate traffic
    except KeyboardInterrupt:
        logger.info("🛑 Producer stopped manually")
    finally:
        producer.flush()
        producer.close()
        logger.info("✅ Kafka producer closed cleanly")
