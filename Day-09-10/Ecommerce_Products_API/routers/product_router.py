from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db
from data_generator import DataGenerator
from logger import log

router = APIRouter(prefix="/products", tags=["Products"])
generator = DataGenerator()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    log.info(f"Creating product: {product.name}")
    return crud.create_product_manual(db, product)

@router.get("/", response_model=schemas.ProductListResponse)
def get_all_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search products"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_dir: str = Query("desc", regex="^(asc|desc)$", description="Sort direction"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    in_stock_only: bool = Query(False, description="Show only in-stock items")
):
    log.info(f"Fetching products | page={page}, per_page={per_page}, search='{search}', sort_by='{sort_by}', sort_dir='{sort_dir}'")
    
    skip = (page - 1) * per_page
    filters = {
        'min_price': min_price,
        'max_price': max_price,
        'category_id': category_id,
        'in_stock_only': in_stock_only
    }
    
    total, products = crud.get_paginated_products(
        db, skip, per_page, search, sort_by, sort_dir, filters
    )
    
    clean_products = []
    for product in products:
        rating = None
        if product.attributes and 'rating' in product.attributes:
            rating = product.attributes['rating']
        
        clean_products.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "brand": product.brand,
            "stock_quantity": product.stock_quantity,
            "category_name": product.category.name if product.category else "Unknown",
            "rating": rating
        })
    
    total_pages = (total + per_page - 1) // per_page
    log.info(f"Found {len(products)} products (Total: {total}, Total Pages: {total_pages})")
    
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "products": clean_products
    }

@router.get("/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    log.info(f"Fetching product by ID: {product_id}")
    product = crud.get_product_by_id(db, product_id)
    if not product:
        log.warning(f"Product not found: ID {product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/auto-generate", response_model=List[schemas.Product])
def auto_generate_products(count: int = 1, db: Session = Depends(get_db)):
    log.info(f"Auto-generating {count} products")
    categories = crud.get_all_categories(db)
    return generator.create_products(db, categories, count)

@router.post("/update-prices")
def update_all_prices(db: Session = Depends(get_db)):
    log.info("Updating all product prices")
    products = crud.get_all_products(db)
    if not products:
        log.warning("No products found to update prices")
        return {"message": "No products found to update"}
    generator.randomly_update_prices(db, products)
    log.info("Product prices updated")
    return {"message": f"Price updated for products"}

@router.post("/update-stock")
def update_all_stocks(db: Session = Depends(get_db)):
    log.info("Updating all product stock quantities")
    products = crud.get_all_products(db)
    if not products:
        log.warning("No products found to update stock")
        return {"message": "No products found to update"}
    generator.randomly_update_stocks(db, products)
    log.info("Product stock updated")
    return {"message": f"Stock updated for products"}
