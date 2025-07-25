from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load .env variables for local debugging (no effect inside container)
load_dotenv()

# === DAG DEFAULTS ===
default_args = {
    'owner': 'airflow',
    'email_on_failure': False,
    'email_on_retry': False,
    'email_on_success': False,
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='ecommerce_medallion_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['ecommerce', 'medallion', 'spark']
) as dag:

    bronze_customers = BashOperator(
        task_id='bronze_ingest_customers',
        bash_command="""
            spark-submit --jars /opt/spark/jars/mysql-connector-java-8.0.28.jar \
            /opt/bitnami/spark/apps/bronze_ingestion.py \
            customers /opt/data_lake/bronze {{ ds }}
        """
    )

    bronze_products = BashOperator(
        task_id='bronze_ingest_products',
        bash_command="""
            spark-submit --jars /opt/spark/jars/mysql-connector-java-8.0.28.jar \
            /opt/bitnami/spark/apps/bronze_ingestion.py \
            products /opt/data_lake/bronze {{ ds }}
        """
    )

    bronze_orders = BashOperator(
        task_id='bronze_ingest_orders',
        bash_command="""
            spark-submit --jars /opt/spark/jars/mysql-connector-java-8.0.28.jar \
            /opt/bitnami/spark/apps/bronze_ingestion.py \
            orders /opt/data_lake/bronze {{ ds }}
        """
    )

    silver_processing = BashOperator(
        task_id='silver_processing',
        bash_command="""
            spark-submit /opt/bitnami/spark/apps/silver_processing.py \
            /opt/data_lake/bronze/mysql /opt/data_lake/silver {{ ds }}
        """
    )

    gold_aggregation = BashOperator(
        task_id='gold_aggregation',
        bash_command="""
            spark-submit /opt/bitnami/spark/apps/gold_aggregation.py \
            /opt/data_lake/silver /opt/data_lake/gold {{ ds }}
        """
    )

    load_to_warehouse = BashOperator(
        task_id='load_to_warehouse',
        bash_command="""
            spark-submit --jars /opt/spark/jars/postgresql-42.7.3.jar \
            /opt/bitnami/spark/apps/load_to_warehouse.py \
            /opt/data_lake/gold {{ ds }}
        """
    )

    [bronze_orders, bronze_products, bronze_customers] >> silver_processing >> gold_aggregation >> load_to_warehouse
