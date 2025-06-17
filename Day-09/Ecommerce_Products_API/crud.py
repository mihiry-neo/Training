from sqlalchemy.orm import Session
import models, schemas

def create_product_manual(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()

def get_products_by_category(db: Session, category_id: int):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()

def search_products(db: Session, query: str):
    return db.query(models.Product).filter(models.Product.name.like(f"%{query}%")).all()

def get_all_categories(db: Session):
    return db.query(models.Category).all()