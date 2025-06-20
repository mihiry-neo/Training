from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    stock_quantity = Column(Integer, default=0)
    brand = Column(String(100), index=True)
    attributes = Column(JSON)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates='products')
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="product", uselist=False)

class PriceHistory(Base):
    __tablename__ = "product_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(String(100))

    product = relationship("Product", back_populates="price_history")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key = True, index = True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_available = Column(Integer, default=0)
    quantity_reserve = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)
    product = relationship("Product", back_populates="inventory")
