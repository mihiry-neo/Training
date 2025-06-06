import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def load_db_connection():
    return pymysql.connect(
        host = os.getenv("DB_Host"),
        user = os.getenv("DB_User"),
        password = os.getenv("DB_Password"),
        database = os.getenv("DB_Name")
    )