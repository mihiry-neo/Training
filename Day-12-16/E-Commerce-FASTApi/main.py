from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import sys, os

# Path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load env vars
load_dotenv()

# DB and Routers
from database import engine, Base, get_db, create_engine_from_url
from Products.routes import router as products_router
from Orders.routes import order_router, cart_router
from Users.routes import router as users_router

# Models & Generator
from datagen import DataGenerator
from Users.models import User
from Products.models import Product, Category
from sqlalchemy.exc import SQLAlchemyError


# ✅ Drop & recreate warehouse DB tables
Base.metadata.create_all(bind=engine)
print("✅ Warehouse DB tables created.")

# ✅ Create client DB tables if not already present
client_url = os.getenv("DATABASE_URL2")
if client_url:
    try:
        client_engine = create_engine_from_url(client_url)
        Base.metadata.create_all(bind=client_engine)
        print("✅ Client DB tables created (if not existing).")
    except SQLAlchemyError as e:
        print(f"❌ Failed to create client DB tables: {e}")
else:
    print("⚠️ DATABASE_URL2 (client) not set in .env")

# App setup
generator = DataGenerator()
app = FastAPI(description="FastAPI E-commerce Project")

# Routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, tags=["Products"])
app.include_router(order_router, tags=["Orders"])
app.include_router(cart_router, tags=["Cart"])
