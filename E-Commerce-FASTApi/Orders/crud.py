from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from decimal import Decimal

from Orders.models import Cart, CartItem, Order, OrderStatus
from Orders.schemas import (
    CartCreate,
    CartItemCreate,
    OrderCreate,
    CartItemResponse,
    CartResponse
)
from Products import crud as Products_crud


# ---------------------- CART OPERATIONS ----------------------
def create_cart(db: Session, cart_in: CartCreate) -> Cart:
    cart = Cart(user_id=cart_in.user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def get_cart(db: Session, cart_id: int) -> CartResponse:
    cart = db.query(Cart).filter_by(cart_id=cart_id).first()
    if not cart:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Cart {cart_id} not found")

    enriched_items = []
    for item in cart.items:
        inventory = Products_crud.get_inventory_by_product_id(db, item.product_id)
        product = Products_crud.get_product_by_id(db, item.product_id)

        enriched_items.append(CartItemResponse(
            item_id=item.item_id,
            product_id=item.product_id,
            quantity=item.quantity,
            remaining_available=inventory.quantity_available if inventory else None,
            unit_price=item.price,
            total_price=round(item.quantity * item.price, 2),
            product_name=product.name if product else None
        ))

    return CartResponse(
        cart_id=cart.cart_id,
        user_id=cart.user_id,
        created_at=cart.created_at,
        items=enriched_items
    )

def get_user_cart(user_id: int) -> List[CartItem]:
    from database import SessionLocal
    db = SessionLocal()
    cart = db.query(Cart).filter_by(user_id=user_id).first()
    if not cart:
        return []
    return cart.items

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter_by(user_id=user_id).all()

def add_item(db: Session, cart_id: int, item_in: CartItemCreate) -> CartItemResponse:
    reservation_response = Products_crud.reserve_products(
        reservations={
            "product_id": item_in.product_id,
            "quantity": item_in.quantity,
            "cart_id": cart_id
        },
        cart_id=f"cart_{cart_id}",
        db=db
    )

    item = db.query(CartItem).filter_by(cart_id=cart_id, product_id=item_in.product_id).first()
    if item:
        item.quantity += item_in.quantity
    else:
        product = Products_crud.get_product_by_id(db, item_in.product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

        item = CartItem(
            cart_id=cart_id,
            user_id=item_in.user_id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            price=product.price
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    remaining_info = next(
        (r for r in reservation_response.get("reserved_items", []) if r["product_id"] == item.product_id),
        None
    )
    item.remaining_available = remaining_info.get("remaining_available") if remaining_info else None

    return CartItemResponse(
        item_id=item.item_id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=item.price,
        total_price=round(item.quantity * item.price, 2)
    )

def list_cart_items(db: Session, cart_id: int) -> List[CartItemResponse]:
    cart = db.query(Cart).filter_by(cart_id=cart_id).first()
    if not cart:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Cart {cart_id} not found")

    enriched_items = []
    for item in cart.items:
        inventory = Products_crud.get_inventory_by_product_id(db, item.product_id)
        product = Products_crud.get_product_by_id(db, item.product_id)

        enriched_items.append(CartItemResponse(
            item_id=item.item_id,
            product_id=item.product_id,
            quantity=item.quantity,
            remaining_available=inventory.quantity_available if inventory else None,
            unit_price=item.price,
            total_price=round(item.quantity * item.price, 2),
            product_name=product.name if product else None
        ))

    return enriched_items


def update_item_quantity(db: Session, cart_id: int, product_id: int, quantity: int) -> CartItemResponse:
    if quantity < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Quantity must be >= 0")

    item = db.query(CartItem).filter_by(cart_id=cart_id, product_id=product_id).first()
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found in cart")

    quantity_diff = quantity - item.quantity
    cart_key = f"cart_{cart_id}"

    if quantity_diff > 0:
        Products_crud.reserve_products(
            reservations={"product_id": product_id, "quantity": quantity_diff, "cart_id": cart_id},
            cart_id=cart_key,
            db=db
        )
    elif quantity_diff < 0:
        Products_crud.release_products(
            reservations={"product_id": product_id, "quantity": abs(quantity_diff), "cart_id": cart_id},
            cart_id=cart_key,
            db=db
        )

    if quantity == 0:
        db.delete(item)
        db.commit()
        raise HTTPException(status.HTTP_200_OK, detail="Item removed from cart")

    item.quantity = quantity
    db.commit()
    db.refresh(item)

    return CartItemResponse(
        item_id=item.item_id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=item.price,
        total_price=round(item.quantity * item.price, 2)
    )

def remove_item(db: Session, item_id: int):
    item = db.query(CartItem).filter_by(item_id=item_id).first()
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cart item not found")

    Products_crud.release_products(
        reservations={
            "product_id": item.product_id,
            "quantity": item.quantity,
            "cart_id": item.cart_id
        },
        cart_id=f"cart_{item.cart_id}",
        db=db
    )

    db.delete(item)
    db.commit()

def clear_cart(db: Session, cart_id: int):
    items = db.query(CartItem).filter_by(cart_id=cart_id).all()

    for item in items:
        Products_crud.release_products(
            reservations={
                "product_id": item.product_id,
                "quantity": item.quantity,
                "cart_id": cart_id
            },
            cart_id=cart_id,
            db=db
        )
        db.delete(item)

    cart = db.query(Cart).filter_by(cart_id=cart_id).first()
    if cart:
        db.delete(cart)

    db.commit()


# ---------------------- ORDER OPERATIONS ----------------------
def create_order(db: Session, order_in: OrderCreate) -> Order:
    order_items_with_price = []
    total = Decimal("0.0")

    for item in order_in.items:
        product = Products_crud.get_product_by_id(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        price = product.price
        total += item.quantity * price

        order_items_with_price.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": float(price)
        })

    db_order = Order(
        user_id=order_in.user_id,
        items=order_items_with_price,
        total_amount=total,
        payment_method=order_in.payment_method,
        shipping_address=order_in.shipping_address
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    try:
        reservations = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
            }
            for item in order_in.items
        ]
        Products_crud.finalize_products(
            reservations=reservations,
            order_id=str(db_order.order_id),
            db=db
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Order created but stock finalization failed: {str(e)}")

    return db_order

def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found")
    return order

def list_orders(db: Session) -> List[Order]:
    return db.query(Order).all()

def update_order_status(db: Session, order_id: int, status_str: str) -> Order:
    order = get_order(db, order_id)
    try:
        order.status = OrderStatus(status_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status: {status_str}")
    db.commit()
    db.refresh(order)
    return order

def cancel_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order.status == OrderStatus.canceled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Order already cancelled")

    order.status = OrderStatus.canceled

    try:
        reservations = [
            {
                "product_id": item.get("product_id"),
                "quantity": item.get("quantity", 0),
                "order_id": order_id
            }
            for item in order.items
        ]
        Products_crud.release_products(
            reservations=reservations,
            cart_id=None,
            order_id=order_id,
            db=db
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Order cancelled but releasing stock failed: {str(e)}")

    db.commit()
