# ✅ genusers.py

import os
import random
import pymysql
from dotenv import load_dotenv
from faker import Faker
from datetime import datetime

load_dotenv()
fake = Faker()

# MySQL env
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql_source")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "ecomuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ecompassword")
MYSQL_DB = os.getenv("MYSQL_DATABASE", "ecommerce_db")

def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

GENDERS = ["male", "female", "other"]
NATIONALITIES = ["Indian", "American", "British", "German", "French", "Japanese", "Canadian"]

def generate_user():
    suffix = random.randint(1000, 99999)
    email = f"{fake.user_name()}{suffix}@{fake.free_email_domain()}"
    phone = fake.phone_number()[:20]
    created_at = updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return (
        fake.user_name(),
        email,
        "SecurePass123",
        random.choice(GENDERS),
        random.randint(18, 60),
        phone,
        random.choice(NATIONALITIES),
        True,
        created_at,
        updated_at
    )

def main(total=500):
    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0
    for _ in range(total):
        try:
            cursor.execute("""
                INSERT IGNORE INTO users 
                (username, email, password, gender, age, phone_number, nationality, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, generate_user())
            inserted += cursor.rowcount
        except Exception as e:
            conn.rollback()
            print("Insert error:", e)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {inserted} users into MySQL (ecommerce_db)")

if __name__ == "__main__":
    main()
