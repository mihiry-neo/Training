from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.orm import joinedload
from typing import Tuple, Dict, Any, Optional, List
import models, schemas
from logger import log

def create_product_manual(db: Session, product: schemas.ProductCreate):
    try:
        db_product = models.Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        log.info(f"Product created manually: ID={db_product.id}, Name={db_product.name}")
        return db_product
    except Exception as e:
        db.rollback()
        log.error(f"Failed to create product: {e}")
        raise

def get_all_products(db: Session):
    products = db.query(models.Product).all()
    log.info(f"Retrieved {len(products)} products")
    return products

def get_product_by_id(db: Session, id: int):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product:
        log.info(f"Found product by ID={id}: {product.name}")
    else:
        log.warning(f"No product found with ID={id}")
    return product

def get_products_by_category(db: Session, category_id: int):
    products = db.query(models.Product).filter(models.Product.category_id == category_id).all()
    log.info(f"Found {len(products)} products for Category ID={category_id}")
    return products

def search_products(db: Session, query: str):
    products = db.query(models.Product).filter(
        func.lower(models.Product.name).like(f"%{query.lower()}%")
    ).all()
    log.info(f"Search for '{query}' returned {len(products)} product(s)")
    return products

def get_all_categories(db: Session):
    categories = db.query(models.Category).all()
    log.info(f"Retrieved {len(categories)} categories")
    return categories

def get_paginated_products(
    db: Session, 
    skip: int, 
    limit: int, 
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    filters: Optional[Dict[str, Any]] = None
) -> Tuple[int, List[models.Product]]:
    try:
        log.info(f"Fetching paginated products | Skip={skip}, Limit={limit}, Search={search}, Sort={sort_by} {sort_dir}, Filters={filters}")
        query = db.query(models.Product).options(joinedload(models.Product.category))
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    models.Product.name.like(search_term),
                    models.Product.brand.like(search_term)
                )
            )
        
        if filters:
            if filters.get('min_price'):
                query = query.filter(models.Product.price >= filters['min_price'])
            if filters.get('max_price'):
                query = query.filter(models.Product.price <= filters['max_price'])
            if filters.get('category_id'):
                query = query.filter(models.Product.category_id == filters['category_id'])
            if filters.get('in_stock_only'):
                query = query.filter(models.Product.stock_quantity > 0)

        total = query.count()

        if hasattr(models.Product, sort_by):
            sort_column = getattr(models.Product, sort_by)
            if sort_dir == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        else:
            log.warning(f"Invalid sort_by column '{sort_by}'")

        products = query.offset(skip).limit(limit).all()
        log.info(f"Returning {len(products)} products out of total {total}")
        return total, products
    
    except Exception as e:
        log.error(f"Error in get_paginated_products: {e}")
        raise
