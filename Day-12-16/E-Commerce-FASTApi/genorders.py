import random
from datetime import datetime
from faker import Faker
 
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
 
from main import app
from database import SessionLocal
from Users.models import User
from Products.models import Product, Inventory
from Products.crud import reserve_products, finalize_products
 
fake = Faker()
client = TestClient(app)
 
# Config
NUM_CARTS_TO_CREATE = 200
NUM_ORDERS_TO_GENERATE = 200
 
used_product_ids = set()
created_cart_ids = []
 
def get_random_users(db: Session, limit=50):
    return db.query(User).filter(User.is_active == True).limit(limit).all()
 
def get_products_with_stock(db: Session):
    return (
        db.query(Product)
        .join(Inventory)
        .filter(Inventory.quantity_available > 0)
        .all()
    )
 
def create_cart(db: Session, user_id: int):
    response = client.post("/cart/", json={"user_id": user_id})
    if response.status_code == 201:
        cart_id = response.json()["cart_id"]
        created_cart_ids.append(cart_id)
        return cart_id
    return None
 
def create_cart_items(db: Session, user_id: int, cart_id: int, max_items=5):
    products = get_products_with_stock(db)
    items = []
    count = 0
    for product in products:
        if product.product_id in used_product_ids:
            continue
        qty = min(5, product.inventory.quantity_available)
        if qty <= 0:
            continue
        item = {
            "user_id": user_id,
            "product_id": product.product_id,
            "quantity": random.randint(1, qty),
            "price": float(product.price),
            "cart_id": cart_id
        }
        items.append(item)
        used_product_ids.add(product.product_id)
        count += 1
        if count >= max_items:
            break
 
    # Call reserve directly (not via client.post)
    reserve_products(reservations=items, cart_id=cart_id, db=db)
 
    return items
 
def create_order_from_products(db: Session, user_id: int, products: list):
    items = []
    for product in products:
        if product.inventory.quantity_available <= 0:
            continue
        qty = random.randint(1, min(5, product.inventory.quantity_available))
        items.append({
            "product_id": product.product_id,
            "quantity": qty,
            "price": float(product.price)
        })
 
    if not items:
        print(f"No valid products for user {user_id}")
        return
 
    # Reserve first
    reserve_products(reservations=items, db=db)
 
    payload = {
        "user_id": user_id,
        "items": items,
        "payment_method": random.choice(["Credit Card", "PayPal", "Cash"]),
        "shipping_address": fake.address().replace("\n", ", ")
    }
 
    order_resp = client.post("/orders/", json=payload)
    if order_resp.status_code in [200, 201]:
        order_data = order_resp.json()
        order_id = order_data.get("order_id")
 
        try:
            finalize_products(reservations=items, order_id=order_id, db=db)
            print(f"Order created and finalized for user {user_id}")
        except Exception as e:
            print(f"Finalize failed: {e}")
    else:
        print(f"Order failed: {order_resp.json()}")
 
def main():
    db = SessionLocal()
    try:
        users = get_random_users(db)
        if not users:
            print("No users found.")
            return
 
        products = get_products_with_stock(db)
        if not products:
            print("No products with stock.")
            return
 
        print(f"Creating {NUM_CARTS_TO_CREATE} carts...")
        for i in range(NUM_CARTS_TO_CREATE):
            user = random.choice(users)
            cart_id = create_cart(db, user.user_id)
            if not cart_id:
                continue
            num_items = random.randint(1, 5)
            create_cart_items(db, user.user_id, cart_id, max_items=num_items)
            print(f"Cart {cart_id} created for user {user.user_id} with {num_items} items.")
 
        print(f"\nGenerating {NUM_ORDERS_TO_GENERATE} orders...")
        for _ in range(NUM_ORDERS_TO_GENERATE):
            user = random.choice(users)
            products = [
                p for p in get_products_with_stock(db)
                if p.product_id not in used_product_ids
            ]
            if len(products) < 3:
                break
            selected = random.sample(products, min(5, len(products)))
            create_order_from_products(db, user.user_id, selected)
 
        print("Script execution complete.")
        print("Created cart IDs:", created_cart_ids)
 
    finally:
        db.close()
 
if __name__ == "__main__":
    main()
 
 