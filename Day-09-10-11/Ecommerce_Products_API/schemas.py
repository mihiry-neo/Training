from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

# =================== Category Schemas ===================

class CategoryBase(BaseModel):
    name: str
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


class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int
    brand: Optional[str] = None
    stock_quantity: int = 0
    attributes: Optional[Dict[str, Any]] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0, description="Price must be positive")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID must be positive")
    brand: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0, description="Stock cannot be negative")
    attributes: Optional[Dict[str, Any]] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip() if v else v
    
    @field_validator('brand')
    @classmethod
    def validate_brand(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Brand cannot be empty or just whitespace')
        return v.strip() if v else v

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