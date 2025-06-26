import time
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datagen import DataGenerator
from database import Base
import sys

# Load .env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env file")

# Setup DB session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def main(product_count: int = 1500):
    db = SessionLocal()
    generator = DataGenerator()

    print("🚀 Generating categories...")
    categories = generator.create_categories(db)
    if not categories:
        print("❌ Failed to generate categories. Aborting product generation.")
        return

    print(f"🚀 Generating {product_count} products...")
    start = time.time()
    products = generator.create_products(db, categories, product_count)
    duration = time.time() - start

    print(f"✅ Successfully generated {len(products)} products.")
    print(f"🕒 Total time: {duration:.2f} seconds")
    print(f"📦 Avg time per product: {(duration / len(products)):.4f} seconds" if products else "No products generated")

if __name__ == "__main__":
    main(product_count=15000)