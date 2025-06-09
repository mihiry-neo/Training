import os
import pymysql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def load_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_Host"),
        user=os.getenv("DB_User"),
        password=os.getenv("DB_Password"),
        database=os.getenv("DB_Name")
    )

def run_query(query):
    conn = load_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            if cur.description:  # it's a SELECT
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return pd.DataFrame(rows, columns=columns)
            else:
                conn.commit()
                print("Query executed successfully.")
    except pymysql.MySQLError as e:
        print("Error:", e)
    finally:
        conn.close()