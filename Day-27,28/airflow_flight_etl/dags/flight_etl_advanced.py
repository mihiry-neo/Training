from airflow import DAG, Dataset
from airflow.utils.dates import days_ago
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable
from include.hooks.flight_api_hook import FlightAPIHook
from include.operators.flight_status_operator import FlightStatusOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "sla": timedelta(minutes=4),
    "depends_on_past": False,
}

airport_dataset = Dataset("airport_data_ready")

with DAG(
    dag_id="flight_etl_advanced",
    description="Flight status ETL with all airflow features",
    schedule="*/5 * * * *",
    start_date=days_ago(1),
    catchup=False,
    default_args=default_args,
    params={"airport": "VABB"},
    tags=["flight", "ETL"],
):

    start = EmptyOperator(task_id="start", trigger_rule=TriggerRule.ALL_SUCCESS)

    wait_for_api = HttpSensor(
        task_id="wait_for_flight_api",
        http_conn_id="opensky_api",
        endpoint="states/all",
        timeout=10,
        poke_interval=60,
        mode="reschedule"
    )

    get_flight_data = FlightStatusOperator(
        task_id="fetch_flight_data",
        airport="{{ params.airport }}"
    )

    @task
    def transform_flights(data):
        from airflow.models import XCom
        # simulate cleansing
        return [f"{d['icao24']} - {d['callsign']}" for d in data]

    @task
    def conditional_branch():
        # simulate conditional logic
        from random import choice
        return "load_to_postgres" if choice([True, False]) else "skip_loading"

    load_to_postgres = PythonOperator(
        task_id="load_to_postgres",
        python_callable=lambda: print("Loaded into DB (simulate PostgresHook)")
    )

    skip_loading = BashOperator(
        task_id="skip_loading",
        bash_command="echo 'Skipping load step...'"
    )

    notify = BashOperator(
        task_id="notify",
        bash_command="echo 'Send Slack/Email here'",
        trigger_rule=TriggerRule.ALL_DONE
    )

    downstream_trigger = TriggerDagRunOperator(
        task_id="trigger_reporting_dag",
        trigger_dag_id="flight_reporting_dag",
        wait_for_completion=False,
        reset_dag_run=True
    )

    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)

    start >> wait_for_api >> get_flight_data >> transform_flights() >> conditional_branch() >> [load_to_postgres, skip_loading] >> notify >> downstream_trigger >> end
