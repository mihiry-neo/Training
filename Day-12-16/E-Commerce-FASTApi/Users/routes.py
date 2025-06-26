from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, Dict, List, Optional
from Products.schemas import ProductListResponse, ProductSummary
from database import get_db
from fastapi import Body
from . import schemas, crud
from auth import create_access_token, verify_password
from utils import get_current_user
from Orders.crud import get_user_cart, create_order, clear_cart
from Orders.schemas import OrderCreate, OrderResponse, CartItemResponse,OrderItem
from Products.crud import get_all_products
from Products import crud as product_crud
from Orders.schemas import OrderResponse, CartItemResponse, CartItemCreate, CartCreate, OrderCreate
from Orders import crud as order_crud
 
router = APIRouter(tags=['Users'])
 
 
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db, user)
    return new_user
 
 
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
 
 
@router.get("/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_users(db)
 
 
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
 
 
@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User {user_id} deleted"}
 
@router.get("/{user_id}/products_recommendations")
def get_recommendations(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return product_crud.generate_recommendations(limit=5, db=db)
 
 
@router.get("/{user_id}/browse_products", response_model=ProductListResponse)
def browse_products(
    user_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    category_id: Optional[int] = Query(None),
    in_stock_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
 
    skip = (page - 1) * per_page
    filters = {
        "min_price": min_price,
        "max_price": max_price,
        "category_id": category_id,
        "in_stock_only": in_stock_only
    }
 
    total, products = product_crud.get_paginated_products(
        db=db,
        skip=skip,
        limit=per_page,
        search=search,
        sort_by=sort_by,
        sort_dir=sort_dir,
        filters=filters
    )
 
    product_summaries = []
    for product in products:
        rating = product.attributes.get("rating") if product.attributes else None
        product_summaries.append(ProductSummary(
            product_id=product.product_id,
            name=product.name,
            price=product.price,
            brand=product.brand,
            category_name=product.category.name if product.category else "Unknown",
            rating=rating
        ))
 
    total_pages = (total + per_page - 1) // per_page
 
    return ProductListResponse(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        products=product_summaries
    )
 
 
@router.post("/{user_id}/addToCart", response_model=CartItemResponse)
def add_to_cart(
    user_id: int,
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart:
        cart = order_crud.create_cart(db, CartCreate(user_id=user_id))
 
    return order_crud.add_item(db=db, cart_id=cart.cart_id, item_in=item)
 
@router.post("/{user_id}/cancel_order/{order_id}")
def cancel_order(
    user_id: int,
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(403, "Unauthorized")
 
    return order_crud.cancel_order(db, order_id)
 
 
@router.delete("/{user_id}/remove_item", response_model=List[CartItemResponse])
def remove_item(
    user_id: int,
    product_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(403, "Unauthorized")
 
    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart:
        raise HTTPException(404, "Cart not found")
 
    item = db.query(order_crud.CartItem).filter_by(cart_id=cart.cart_id, product_id=product_id).first()
    if not item:
        raise HTTPException(404, "Item not found in cart")
 
    order_crud.remove_item(db, item_id=item.item_id)
    return order_crud.list_cart_items(db, cart.cart_id)
 
 
@router.get("/{user_id}/mycart", response_model=List[CartItemResponse])
def my_cart(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart:
        return []

    # Transform to CartItemResponse
    enriched_items = []
    for item in cart.items:
        enriched_items.append(CartItemResponse(
            item_id=item.item_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.price,
            total_price=round(item.quantity * item.price, 2)
        ))

    return enriched_items

 
 
@router.get("/{user_id}/myorders", response_model=List[OrderResponse])
def my_orders(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return order_crud.get_user_orders(db, user_id=user_id)

 
@router.delete("/{user_id}/remove_item", response_model=List[CartItemResponse])
def remove_item(
    user_id: int,
    product_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
 
    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
 
    item = db.query(order_crud.CartItem).filter_by(cart_id=cart.cart_id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
 
    order_crud.remove_item(db, item_id=item.item_id)
    return order_crud.list_cart_items(db, cart.cart_id)
 
 
@router.delete("/{user_id}/clear_cart")
def clear_cart(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
 
    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
 
    order_crud.clear_cart(db, cart.cart_id)
    return {"message": "Cart cleared"}
 
 
@router.post("/{user_id}/checkout", response_model=OrderResponse)
def checkout(
    user_id: int,
    shipping_address: str = Body(..., embed=True),
    payment_method: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(403, "Unauthorized")
 
    cart = db.query(order_crud.Cart).filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        raise HTTPException(400, "Cart is empty")
 
    order_items = [
        OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        for item in cart.items
    ]
 
    order_in = OrderCreate(
        user_id=user_id,
        cart_id=cart.cart_id,
        items=order_items,
        shipping_address=shipping_address,
        payment_method=payment_method
    )
 
    created_order = order_crud.create_order(db, order_in)
    order_crud.clear_cart(db, cart.cart_id)
 
    return created_order