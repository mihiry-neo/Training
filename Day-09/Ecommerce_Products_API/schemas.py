from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['Category'] = []

    class Config:
        orm_mode = True

class ProductPriceHistoryBase(BaseModel):
    old_price: float
    new_price: float
    reason: Optional[str] = None

class ProductPriceHistory(ProductPriceHistoryBase):
    id: int
    product_id: int
    changed_at: datetime
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    brand: Optional[str] = None
    stock_quantity: int = 0
    attributes: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    stock_quantity: Optional[int] = None
    attributes: Optional[Dict[str, Any]] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    price_history: List[ProductPriceHistory] = []
    
    class Config:
        from_attributes = True

# Response Schemas
class ProductListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    products: List[Product]

class CategoryListResponse(BaseModel):
    total: int
    categories: List[Category]

# Update forward references
Category.model_rebuild()
