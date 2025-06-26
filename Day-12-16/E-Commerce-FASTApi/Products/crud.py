from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc, asc
from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from typing import Tuple, Dict, Any, Optional, List, Union
from database import get_db
import Products.models, Products.schemas
from Products.models import Product, PriceHistory, StockMovement
from decimal import Decimal, ROUND_HALF_UP
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_product_manual(db: Session, product: Products.schemas.ProductCreate):
    try:
        db_product = Products.models.Product(**product.model_dump(exclude={"inventory"}))
        db.add(db_product)
        db.flush()

        if product.inventory:
            db_inventory = Products.models.Inventory(
                product_id=db_product.product_id,
                **product.inventory.model_dump()
            )
            db.add(db_inventory)

        db.commit()
        db.refresh(db_product)
        return db_product

    except Exception as e:
        db.rollback()
        print(f"Error creating manual product with inventory: {e}")
        raise


def get_all_products(db: Session):
    return db.query(Products.models.Product).all()

def get_product_by_id(db: Session, id: int):
    return db.query(Products.models.Product).filter(Products.models.Product.product_id == id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(Products.models.Product).filter(Products.models.Product.name == name).first()

def get_product_by_brand(db: Session, brand: str):
    return db.query(Products.models.Product).filter(Products.models.Product.brand == brand).first()

def get_products_by_category(db: Session, category_id: int):
    return db.query(Products.models.Product).filter(Products.models.Product.category_id == category_id).all()

def get_all_categories(db: Session):
    return db.query(Products.models.Category).all()

def get_paginated_products(
    db: Session, 
    skip: int, 
    limit: int, 
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    filters: Optional[Dict[str, Any]] = None
) -> Tuple[int, List[Products.models.Product]]:
    try:
        query = db.query(Products.models.Product)\
                 .options(joinedload(Products.models.Product.category),
                          joinedload(Products.models.Product.inventory)) 

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Products.models.Product.name.ilike(search_term),
                    Products.models.Product.brand.ilike(search_term),
                    Products.models.Product.product_id == search if search.isdigit() else False  # NEW
                )
            )

        
        if filters:
            if filters.get('min_price') is not None:
                query = query.filter(Products.models.Product.price >= filters['min_price'])
            if filters.get('max_price') is not None:
                query = query.filter(Products.models.Product.price <= filters['max_price'])
            if filters.get('category_id') is not None:
                query = query.filter(Products.models.Product.category_id == filters['category_id'])
            if filters.get('in_stock_only'):
                query = query.join(Products.models.Inventory)\
                             .filter(Products.models.Inventory.quantity_available > 0)

        total = query.count()

        if hasattr(Products.models.Product, sort_by):
            sort_column = getattr(Products.models.Product, sort_by)
            query = query.order_by(desc(sort_column) if sort_dir == "desc" else asc(sort_column))

        products = query.offset(skip).limit(limit).all()
        return total, products
    except Exception as e:
        raise

def update_product(db: Session, product_id: int, product_update: Products.schemas.ProductUpdate):
    db_product = db.query(Products.models.Product).filter(Products.models.Product.product_id == product_id).first()
    
    if not db_product:
        db_product = db.query(Products.models.Product).filter(Products.models.Product.name == str(product_id)).first()
    
    if not db_product:
        db_product = db.query(Products.models.Product).filter(Products.models.Product.brand == str(product_id)).first()
    
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    
    if 'attributes' in update_data:
        new_attributes = update_data.pop('attributes')
        if new_attributes is not None:
            existing_attributes = db_product.attributes or {}
            if isinstance(new_attributes, dict) and new_attributes:
                merged_attributes = dict(existing_attributes)
                merged_attributes.update(new_attributes)
                db_product.attributes = merged_attributes
            elif new_attributes == {}:
                db_product.attributes = {}
                
    for field, value in update_data.items():
        if hasattr(db_product, field):
            setattr(db_product, field, value)
    
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise e

def get_inventory_by_product_id(db: Session, product_id: int):
    return db.query(Products.models.Inventory).filter(Products.models.Inventory.product_id == product_id).first()

def update_inventory_quantity(db: Session, product_id: int, quantity_delta: int, reason: str = None, order_id: int = None):
    inventory = get_inventory_by_product_id(db, product_id)
    if not inventory:
        raise Exception("Inventory record not found for product_id")

    inventory.quantity_available += quantity_delta
    inventory.quantity_available = max(0, inventory.quantity_available)

    movement = Products.models.StockMovement(
        product_id=product_id,
        order_id=order_id,
        change=quantity_delta,
        reason=reason
    )
    db.add(movement)
    db.commit()
    db.refresh(inventory)
    return inventory

def create_or_update_inventory(db: Session, product_id: int, data: Products.schemas.InventoryBase):
    inventory = get_inventory_by_product_id(db, product_id)
    if not inventory:
        inventory = Products.models.Inventory(product_id=product_id, **data.model_dump())
        db.add(inventory)
    else:
        for key, value in data.model_dump().items():
            setattr(inventory, key, value)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_stock_movements_for_product(db: Session, product_id: int):
    return db.query(Products.models.StockMovement)\
        .filter(Products.models.StockMovement.product_id == product_id)\
        .order_by(Products.models.StockMovement.timestamp.desc()).all()

def update_inventory_settings(db: Session, product_id: int, update_data: Products.schemas.InventoryUpdate):
    inventory = db.query(Products.models.Inventory).filter(Products.models.Inventory.product_id == product_id).first()
    if not inventory:
        raise Exception("Inventory not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(inventory, key, value)

    db.commit()
    db.refresh(inventory)
    return inventory

def generate_recommendations(limit: int, db: Session) -> List[dict]:
    affordable = db.query(Products.models.Product)\
        .join(Products.models.Inventory)\
        .filter(
            Products.models.Inventory.quantity_available > 0,
            Products.models.Product.price < 300,
            Products.models.Product.attributes["rating"].as_float() >= 3
        )\
        .order_by(func.random())\
        .limit(limit // 2).all()

    premium = db.query(Products.models.Product)\
        .join(Products.models.Inventory)\
        .filter(
            Products.models.Inventory.quantity_available > 0,
            Products.models.Product.price > 1500,
            Products.models.Product.attributes["rating"].as_float() >= 3
        )\
        .order_by(func.random())\
        .limit(limit - len(affordable)).all()

    combined = affordable + premium
    random.shuffle(combined)

    return [
        {
            "id": p.product_id,
            "name": p.name,
            "price": float(p.price),
            "brand": p.brand,
            "category_name": p.category.name if p.category else "Unknown",
            "rating": p.attributes.get("rating") if p.attributes else None,
            "stock_quantity": p.inventory.quantity_available if p.inventory else 0
        }
        for p in combined
    ]


def reserve_products(
    reservations: Union[List[dict], dict],
    cart_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if isinstance(reservations, dict):
        reservations = [reservations]

    try:
        reserved_items = []

        for item in reservations:
            inventory = Products.crud.get_inventory_by_product_id(db, item["product_id"])
            if not inventory or inventory.quantity_available < item["quantity"]:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {item['product_id']} (requested: {item['quantity']}, available: {inventory.quantity_available if inventory else 0})"
                )

        for item in reservations:
            inventory = Products.crud.get_inventory_by_product_id(db, item["product_id"])
            inventory.quantity_available -= item["quantity"]
            inventory.quantity_reserve += item["quantity"]

            movement = Products.models.StockMovement(
                product_id=item["product_id"],
                cart_id=item.get("cart_id", cart_id),
                change=-item["quantity"],
                reason=f"reserve_cart_{item.get('cart_id', cart_id)}"
            )
            db.add(movement)

            reserved_items.append({
                **item,
                "remaining_available": inventory.quantity_available
            })

        db.commit()

        return {
            "success": True,
            "reserved_items": reserved_items,
            "total_items": len(reserved_items),
            "cart_id": cart_id,
            "message": f"Successfully reserved {len(reserved_items)} product(s)"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def release_products(
    reservations: Union[List[dict], dict],
    cart_id: Optional[int] = None,
    order_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if isinstance(reservations, dict):
        reservations = [reservations]

    try:
        released_items = []

        for item in reservations:
            product_id = item["product_id"]
            quantity = item["quantity"]

            inventory = Products.crud.get_inventory_by_product_id(db, product_id)
            if inventory and inventory.quantity_reserve >= quantity:
                inventory.quantity_reserve -= quantity
                inventory.quantity_available += quantity

                movement_cart_id = item.get("cart_id") if isinstance(item.get("cart_id"), int) else cart_id
                movement_order_id = item.get("order_id") if isinstance(item.get("order_id"), int) else order_id

                reason_parts = ["release"]
                if movement_cart_id is not None:
                    reason_parts.append(f"cart_{movement_cart_id}")
                if movement_order_id is not None:
                    reason_parts.append(f"order_{movement_order_id}")
                reason = "_".join(reason_parts)

                movement = Products.models.StockMovement(
                    product_id=product_id,
                    cart_id=movement_cart_id,
                    order_id=movement_order_id,
                    change=quantity,
                    reason=reason
                )
                db.add(movement)

                released_items.append({
                    **item,
                    "new_available": inventory.quantity_available
                })

        db.commit()
        return {
            "success": True,
            "released_items": released_items,
            "total_items": len(released_items),
            "cart_id": cart_id,
            "order_id": order_id,
            "message": f"Successfully released {len(released_items)} product(s)"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def finalize_products(
    reservations: Union[List[dict], dict],
    order_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if isinstance(reservations, dict):
        reservations = [reservations]

    try:
        finalized_items = []

        for item in reservations:
            product_id = item["product_id"]
            quantity = item["quantity"]

            inventory = Products.crud.get_inventory_by_product_id(db, product_id)
            if not inventory:
                raise HTTPException(status_code=404, detail=f"Inventory not found for product {product_id}")

            print(
                f"[DEBUG][BEFORE] Product {product_id} -> "
                f"Available: {inventory.quantity_available}, Reserved: {inventory.quantity_reserve}"
            )

            if inventory.quantity_reserve < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough reserved stock for product {product_id}"
                )

            if inventory.quantity_available < quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough available stock for product {product_id}"
                )

            inventory.quantity_reserve -= quantity
            inventory.quantity_available -= quantity
            db.add(inventory)

            movement = Products.models.StockMovement(
                product_id=product_id,
                order_id=item.get("order_id", order_id),
                cart_id=item.get("cart_id"),
                change=-quantity,
                reason=f"finalize_order_{item.get('order_id', order_id)}"
            )
            db.add(movement)

            print(
                f"[DEBUG][AFTER] Product {product_id} -> "
                f"Available: {inventory.quantity_available}, Reserved: {inventory.quantity_reserve}"
            )

            finalized_items.append({
                **item,
                "remaining_reserved": inventory.quantity_reserve,
                "remaining_stock": inventory.quantity_available
            })

        db.flush()
        db.commit()

        return {
            "success": True,
            "finalized_items": finalized_items,
            "total_items": len(finalized_items),
            "order_id": order_id,
            "message": f"Successfully finalized {len(finalized_items)} product(s)"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Finalization failed: {str(e)}")


def randomly_update_prices(
    db: Session,
    products: List[Product],
    batch_size: int = 50,
    reason: str = "auto_scheduler"
) -> None:
    try:
        selected = random.sample(products, min(batch_size, len(products)))

        for product in selected:
            old_price = product.price
            change_percent = Decimal(str(random.uniform(-0.2, 0.2)))
            new_price = (old_price * (Decimal("1.0") + change_percent)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            new_price = max(new_price, Decimal("1.00"))

            product.price = new_price
            db.add(product)

            price_history = PriceHistory(
                product_id=product.product_id,
                old_price=old_price,
                new_price=new_price,
                reason=reason
            )
            db.add(price_history)

        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def log_stock_movement(
    db: Session,
    product_id: int,
    change: int,
    reason: str,
    order_id: Optional[int] = None,
    cart_id: Optional[int] = None
):
    try:
        movement = StockMovement(
            product_id=product_id,
            change=change,
            reason=reason,
            order_id=order_id,
            cart_id=cart_id
        )
        db.add(movement)
        db.commit()
        print(f"[STOCK LOGGED] Product {product_id} | Change: {change} | Reason: {reason}")
        return movement
    except Exception as e:
        db.rollback()
        print(f"[STOCK LOGGING ERROR] Failed to log stock movement for product {product_id}: {e}")
        return None

