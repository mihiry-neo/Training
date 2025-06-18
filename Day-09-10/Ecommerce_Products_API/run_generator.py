from database import SessionLocal, engine, Base
from data_generator import DataGenerator
import math

# Create all tables
Base.metadata.create_all(bind=engine)

def main(total_products: int = 50000, batch_size: int = 1000):
    generator = DataGenerator()

    # Use context manager to handle DB session cleanly
    with SessionLocal() as db:
        # 1. Create categories
        categories = generator.create_categories(db)
        print(f"✅ Created {len(categories)} categories")

        # 2. Generate products in batches
        num_batches = math.ceil(total_products / batch_size)
        all_products = []
        for batch_num in range(num_batches):
            print(f"🚀 Batch {batch_num + 1}/{num_batches}: Generating {batch_size} products...")
            products = generator.create_products(db, categories, count=batch_size)
            all_products.extend(products)
        print(f"✅ Created {len(all_products)} total products")

        # 3. Simulate price and stock changes on a sample set
        print("🔁 Simulating price and stock updates for first 50 products...")
        for product in all_products[:50]:
            generator.update_product_price(db, product, reason="initial_simulation")
            generator.update_stock_quantity(db, product)
        print("✅ Simulated price/stock updates")

if __name__ == "__main__":
    main()
