# data_generation_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append("/opt/airflow/data_generation")

from generate_all_data import generate_all_data_pipeline as run_generate_all_data

default_args = {
    'owner': 'airflow',
    'email_on_failure': False,
    'email_on_retry': False,
    'email_on_success': False,
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='generate_ecommerce_sample_data',
    default_args=default_args,
    schedule_interval='@daily',   # or change to None for manual-only
    catchup=False,
    tags=['ecommerce', 'data_generation'],
) as dag:

    generate_data_task = PythonOperator(
        task_id="generate_all_data",
        python_callable=run_generate_all_data
    )

    generate_data_task
