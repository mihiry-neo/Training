from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"mysql+pymysql://{os.getenv('DB_User')}:{os.getenv('DB_Password')}@{os.getenv('DB_Host')}:{os.getenv('DB_Port')}/{os.getenv('DB_Name')}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()