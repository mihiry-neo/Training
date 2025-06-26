from pydantic import BaseModel, PositiveInt
from typing import List, Optional
from datetime import datetime
 
# ---------------------- CART ITEM ----------------------
 
class CartItemCreate(BaseModel):
    user_id: PositiveInt
    product_id: PositiveInt
    quantity: PositiveInt
 
 
class CartItemResponse(BaseModel):
    item_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
 
    class Config:
        from_attributes = True
 
# ---------------------- CART ----------------------
 
class CartCreate(BaseModel):
    user_id: PositiveInt
 
class CartResponse(CartCreate):
    cart_id: int
    created_at: datetime
    items: List[CartItemResponse] = []
 
    class Config:
        from_attributes = True
 
# ---------------------- ORDER ITEM ----------------------
 
class OrderItem(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt
 
# ---------------------- ORDER ----------------------
 
class OrderCreate(BaseModel):
    user_id: PositiveInt
    cart_id: Optional[int] = None
    items: List[OrderItem]
    shipping_address: str
    payment_method: str
 
class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_amount: float
    status: str
    order_date: datetime
    shipping_address: str
    payment_method: str
 
    class Config:
        from_attributes = True
 
class OrderStatusUpdate(BaseModel):
    status: str
 
class OrderCancelResponse(BaseModel):
    detail: str