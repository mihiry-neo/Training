from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests

CRYPTO_IDS = "bitcoin,ethereum,dogecoin"
POSTGRES_CONN_ID = "postgres_default"

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

with DAG(
    dag_id="crypto_etl_postgres_pipeline",
    default_args=default_args,
    schedule_interval="*/5 * * * *",  # Every 5 minutes
    catchup=False,
    tags=["crypto", "postgres", "etl"]
) as dag:

    @task()
    def extract():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": CRYPTO_IDS
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @task()
    def transform(raw_data):
        records = []
        for coin in raw_data:
            records.append((
                coin['id'],
                coin['symbol'],
                coin['current_price'],
                coin['market_cap'],
                coin['total_volume'],
                coin['last_updated']
            ))
        return records

    @task()
    def load(data):
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_market (
                coin_id TEXT,
                symbol TEXT,
                current_price NUMERIC,
                market_cap NUMERIC,
                volume NUMERIC,
                last_updated TIMESTAMPTZ
            );
        """)

        insert_query = """
            INSERT INTO crypto_market (coin_id, symbol, current_price, market_cap, volume, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)

        conn.commit()
        cursor.close()

    # ETL Flow
    raw = extract()
    transformed = transform(raw)
    load(transformed)
