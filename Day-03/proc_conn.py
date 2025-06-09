import pymysql
import pandas as pd
import os
from dotenv import load_dotenv
import logging

load_dotenv() 

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler("db_logs.log"),
        logging.StreamHandler()
        ]
)

def load_db_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_Host"),
            user=os.getenv("DB_User"),
            password=os.getenv("DB_Password"),
            database=os.getenv("DB_Name")
        )
        logging.info("Connected to the database successfully")   
        return conn
    except pymysql.MySQLError as e:
        logging.error(f"Database connection failed: {e}")
        raise

def run_query(query, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        logging.info("Query executed successfully.")
    except pymysql.MySQLError as e:
        logging.error(f"Faced an Error executing query: {e}")




def call_procedure(proc_name, conn, param = None):
    try:
        with conn.cursor() as cur:
            if param:
                cur.callproc(proc_name, param)
                logging.info(f"Called Stored Procedure `{proc_name}` with params {param}")
            else:
                cur.callproc(proc_name)
                logging.info(f"Called Stored Procedure `{proc_name}` without parameters")

            conn.commit()

            result = cur.fetchall()
            if result:
                columns = [desc[0] for desc in cur.description]
                logging.info(f"Stored Procedure `{proc_name}` returned a result set")
                return pd.DataFrame(result, columns=columns)
            else:
                logging.info(f"Stored Procedure `{proc_name}` executed successfully but returned no result set")
                rows_affected = cur.rowcount
                logging.info(f"{rows_affected} rows affected by Stored Procedure `{proc_name}`")
                return pd.DataFrame()

    except pymysql.MySQLError as e:
        logging.error(f"Faced error while calling Stored Procedure `{proc_name}`: {e}")


def db_main(proc_query, proc_name, param=None):
    conn = None
    try:
        conn = load_db_connection()
        run_query(proc_query, conn)
        result_df = call_procedure(proc_name, conn, param)
        return result_df
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


