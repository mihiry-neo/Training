from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# =================== Category Schemas ===================

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['Category'] = []

    class Config:
        from_attribute = True

# =================== Price History Schemas ===================

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

# =================== Product Schemas ===================

class ProductAttributes(BaseModel):
    color: str
    weight: str
    material: str
    rating: float

class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int
    brand: Optional[str] = None
    stock_quantity: int = 0
    attributes: ProductAttributes

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    stock_quantity: Optional[int] = None
    attributes: Optional[Dict[str, Any]] = None

class ProductSummary(BaseModel):
    id: int
    name: str
    price: float
    brand: Optional[str] = None
    stock_quantity: int
    category_name: str
    rating: Optional[float] = None
    
    class Config:
        from_attributes = True
        
class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    price_history: List[ProductPriceHistory] = []
    
    class Config:
        from_attributes = True

# =================== Response Schemas ===================

class ProductListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    products: List[ProductSummary]

# Update forward references
Category.model_rebuild()