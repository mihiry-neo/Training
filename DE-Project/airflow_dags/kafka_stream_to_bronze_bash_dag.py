from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 24),
}

with DAG('kafka_stream_to_bronze_bash_dag',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    stream_kafka_to_bronze = BashOperator(
        task_id='stream_kafka_to_bronze',
        bash_command="""
        spark-submit \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
        /opt/bitnami/spark/apps/spark_streaming_kafka_to_bronze.py \
        kafka:9092 \
        ecommerce_events \
        /opt/data_lake/bronze/events
        """
    )
