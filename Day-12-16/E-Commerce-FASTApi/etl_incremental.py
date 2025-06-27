import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from Products.models import Product, Inventory, Category, StockMovement


# Ensure models and base are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# 👇 Fix for relationship dependency
from Orders.models import Order  # Required because StockMovement uses relationship("Order")
from Products.models import Product, Inventory

# Load both DB connections from one .env file
load_dotenv()

def load_session(env_var: str):
    url = os.getenv(env_var)
    if not url:
        raise ValueError(f"{env_var} is not set in .env file")
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return engine, Session()

# ✅ Correctly labeled
client_engine, client_db = load_session("DATABASE_URL")
warehouse_engine, warehouse_db = load_session("DATABASE_URL2")


def get_all_warehouse_products(db):
    return {
        p.product_id: (p.updated_at or datetime.min.replace(tzinfo=timezone.utc))
        for p in db.query(Product.product_id, Product.updated_at).all()
    }

def sync_categories():
    print("📁 Syncing categories...")

    client_categories = client_db.query(Category).all()
    existing_category_ids = {c.category_id for c in warehouse_db.query(Category.category_id).all()}

    new_categories = []
    for cat in client_categories:
        if cat.category_id not in existing_category_ids:
            new_cat = Category(
                category_id=cat.category_id,
                name=cat.name,
                parent_id=cat.parent_id,
                created_at=cat.created_at,
                updated_at=cat.updated_at
            )
            new_categories.append(new_cat)

    if new_categories:
        warehouse_db.add_all(new_categories)
        warehouse_db.commit()
        print(f"✅ Synced {len(new_categories)} new categories.")
    else:
        print("✅ No new categories to sync.")

def sync_products():
    try:
        
        print("🔁 Starting incremental sync (new + updated)...")
        sync_categories()
        warehouse_products = get_all_warehouse_products(warehouse_db)

        updated_or_new = client_db.query(Product).filter(
            Product.updated_at != None,
            Product.updated_at > datetime.min.replace(tzinfo=timezone.utc)
        ).all()


        inserted, updated = 0, 0

        for client_product in updated_or_new:
            warehouse_updated_at = warehouse_products.get(client_product.product_id)

            if not warehouse_updated_at:
                action = "insert"
            elif client_product.updated_at and client_product.updated_at > warehouse_updated_at:
                action = "update"
            else:
                continue

            if action == "insert":
                new_product = Product(
                    product_id=client_product.product_id,
                    name=client_product.name,
                    price=client_product.price,
                    category_id=client_product.category_id,
                    brand=client_product.brand,
                    attributes=client_product.attributes,
                    created_at=client_product.created_at,
                    updated_at=client_product.updated_at
                )
                warehouse_db.add(new_product)

                if client_product.inventory:
                    new_inventory = Inventory(
                        product_id=client_product.product_id,
                        quantity_available=client_product.inventory.quantity_available,
                        quantity_reserve=client_product.inventory.quantity_reserve,
                        reorder_level=client_product.inventory.reorder_level,
                        reorder_quantity=client_product.inventory.reorder_quantity,
                        unit_cost=client_product.inventory.unit_cost,
                        last_restocked=client_product.inventory.last_restocked,
                        expiry_date=client_product.inventory.expiry_date,
                        batch_number=client_product.inventory.batch_number,
                        location=client_product.inventory.location
                    )
                    warehouse_db.add(new_inventory)

                inserted += 1

            elif action == "update":
                warehouse_product = warehouse_db.query(Product).get(client_product.product_id)
                if warehouse_product:
                    if client_product.price != warehouse_product.price:
                        from Products.models import PriceHistory

                        price_history = PriceHistory(
                            product_id=client_product.product_id,
                            old_price=warehouse_product.price,
                            new_price=client_product.price,
                            changed_at=datetime.now(timezone.utc),
                            reason="Synced from client DB"
                        )
                        warehouse_db.add(price_history)

                    warehouse_product.name = client_product.name
                    warehouse_product.price = client_product.price
                    warehouse_product.category_id = client_product.category_id
                    warehouse_product.brand = client_product.brand
                    warehouse_product.attributes = client_product.attributes
                    warehouse_product.updated_at = client_product.updated_at

                    if client_product.inventory:
                        inv = warehouse_db.query(Inventory).filter_by(product_id=client_product.product_id).first()
                        if inv:
                            inv.quantity_available = client_product.inventory.quantity_available
                            inv.quantity_reserve = client_product.inventory.quantity_reserve
                            inv.reorder_level = client_product.inventory.reorder_level
                            inv.reorder_quantity = client_product.inventory.reorder_quantity
                            inv.unit_cost = client_product.inventory.unit_cost
                            inv.last_restocked = client_product.inventory.last_restocked
                            inv.expiry_date = client_product.inventory.expiry_date
                            inv.batch_number = client_product.inventory.batch_number
                            inv.location = client_product.inventory.location

                    updated += 1

        warehouse_db.commit()
        print(f"✅ Sync complete: {inserted} inserted, {updated} updated.")

        sync_stock_movements()

    except Exception as e:
        warehouse_db.rollback()
        print(f"❌ Sync failed: {e}")

    finally:
        client_db.close()
        warehouse_db.close()
    

def sync_stock_movements():
    print("📦 Syncing stock movements...")

    latest_synced = warehouse_db.query(func.max(StockMovement.timestamp)).scalar()
    if not latest_synced:
        latest_synced = datetime.min.replace(tzinfo=timezone.utc)

    new_movements = client_db.query(StockMovement).filter(
        StockMovement.timestamp > latest_synced
    ).all()

    print(f"🕒 Found {len(new_movements)} new stock movements since {latest_synced}.")

    for sm in new_movements:
        movement = StockMovement(
            stock_id=sm.stock_id,  # Optional: can omit if autoincrement
            product_id=sm.product_id,
            change=sm.change,
            reason=sm.reason,
            timestamp=sm.timestamp,
            cart_id=sm.cart_id,
            order_id=sm.order_id
        )
        warehouse_db.add(movement)

    warehouse_db.commit()
    print(f"✅ Synced {len(new_movements)} stock movements.")

if __name__ == "__main__":
    sync_products()
