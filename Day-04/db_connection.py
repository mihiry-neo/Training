import pymysql
import pandas as pd
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("db_logs.log"),
        logging.StreamHandler()
    ]
)

try:
    conn = pymysql.connect(
        host=os.getenv("DB_Host"),
        user=os.getenv("DB_User"),
        password=os.getenv("DB_Password"),
        database=os.getenv("DB_Name"),
        autocommit=True
    )
    logging.info("🔗 Persistent DB connection established")
except pymysql.MySQLError as e:
    logging.error(f"Failed to connect: {e}")
    raise

def run_ddl_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        logging.info("DDL executed (e.g., trigger/table created or dropped)")
    except pymysql.MySQLError as e:
        logging.error(f"Error executing DDL: {e}")

def run_dml_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        logging.info("DML query executed (insert/update/delete)")
    except pymysql.MySQLError as e:
        logging.error(f"Error executing DML: {e}")

def run_select_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            logging.info("SELECT query executed")
            return pd.DataFrame(rows, columns=columns)
    except pymysql.MySQLError as e:
        logging.error(f"Error executing SELECT: {e}")
