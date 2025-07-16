from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="flight_reporting_dag",
    start_date=days_ago(1),
    schedule=None,
    catchup=False,
    tags=["reporting"]
) as dag:
    start = EmptyOperator(task_id="start")
