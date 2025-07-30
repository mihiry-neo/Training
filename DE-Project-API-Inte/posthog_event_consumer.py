# === Enhanced PostHog Event Consumer (Handles stock_change events) ===

import json
import time
import logging
import os
from kafka import KafkaConsumer
import posthog
from dotenv import load_dotenv

# === Load .env ===
load_dotenv()

# === CONFIG ===
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "ecommerce_events")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://us.posthog.com")

if not POSTHOG_API_KEY:
    raise EnvironmentError("❌ POSTHOG_API_KEY not set in environment")

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PostHogConsumer")

# === Init PostHog ===
posthog.project_api_key = POSTHOG_API_KEY
posthog.host = POSTHOG_HOST

# === Send Event to PostHog ===
def send_to_posthog(event_data):
    try:
        distinct_id = event_data.get("user_id", "anonymous")
        event_name = event_data.get("event", "unknown_event")
        properties = event_data.get("properties", {})

        # Optional enrichment or mapping
        if event_name == "stock_change":
            properties["$group"] = "inventory"
            logger.info(f"📦 Handling stock change: Product {properties.get('product_id')} | Qty: {properties.get('quantity_change')}")

        posthog.capture(distinct_id=distinct_id, event=event_name, properties=properties)
        logger.info(f"✅ Sent event '{event_name}' for user '{distinct_id}'")

    except Exception as e:
        logger.error(f"❌ Failed to send to PostHog: {e}")

# === Kafka Consumer Loop ===
def consume_events():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="posthog-consumer-group"
    )

    logger.info(f"📡 Listening to Kafka topic: {KAFKA_TOPIC}")
    for message in consumer:
        event_data = message.value
        logger.info(f"📥 Received event: {event_data}")
        send_to_posthog(event_data)

# === Main ===
if __name__ == "__main__":
    while True:
        try:
            consume_events()
        except Exception as err:
            logger.error(f"💥 Error in consumer: {err}")
            time.sleep(5)