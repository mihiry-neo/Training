from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import os
import shutil
import logging

# === Paths & Configuration ===
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_LAKE_PATH = os.path.join(PROJECT_ROOT, '..', 'data_lake')
BRONZE_BASE_PATH = os.path.join(DATA_LAKE_PATH, 'bronze')
ARCHIVE_BASE_PATH = os.path.join(DATA_LAKE_PATH, 'archive', 'bronze')
RETENTION_DAYS_BRONZE = 1  # Archive data older than 1 year
BRONZE_TABLES = ['orders', 'customers', 'products']  # Add more tables here if needed

def archive_old_bronze_data(base_bronze_path, archive_bronze_path, retention_days, table_name):
    """Archives bronze data older than retention_days."""
    log = logging.getLogger("airflow.task")
    source_table_path = os.path.join(base_bronze_path, "mysql", table_name)
    archive_table_path = os.path.join(archive_bronze_path, "mysql", table_name)
    os.makedirs(archive_table_path, exist_ok=True)

    cutoff_date = datetime.now() - timedelta(days=retention_days)
    archived_count = 0

    for year_dir in os.listdir(source_table_path):
        year_path = os.path.join(source_table_path, year_dir)
        if not os.path.isdir(year_path) or not year_dir.isdigit():
            continue
        for month_dir in os.listdir(year_path):
            month_path = os.path.join(year_path, month_dir)
            if not os.path.isdir(month_path) or not month_dir.isdigit():
                continue
            for day_dir in os.listdir(month_path):
                day_path = os.path.join(month_path, day_dir)
                if not os.path.isdir(day_path) or not day_dir.isdigit():
                    continue
                try:
                    current_date = datetime(int(year_dir), int(month_dir), int(day_dir))
                except ValueError:
                    continue
                if current_date < cutoff_date:
                    versioned_day = f"{day_dir}_archived_on={datetime.today().date()}"
                    dest_path = os.path.join(archive_table_path, year_dir, month_dir, versioned_day)

                    if os.path.exists(dest_path):
                        log.warning(f"[SKIPPED] Already archived: {dest_path}")
                        continue

                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(day_path, dest_path)
                    log.info(f"[ARCHIVED] {day_path} → {dest_path}")
                    archived_count += 1

    if archived_count == 0:
        log.info(f"[NO DATA] Nothing to archive for table '{table_name}'.")
    else:
        log.info(f"[SUMMARY] Archived {archived_count} partition(s) for '{table_name}'.")

# === Airflow DAG definition ===
default_args_archive = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='data_archival_pipeline',
    default_args=default_args_archive,
    description='Monthly Data Archival for Bronze Tier',
    schedule_interval='@monthly',
    catchup=False,
    tags=['ecommerce', 'archive'],
) as dag:

    start = EmptyOperator(task_id='start_archival')

    with TaskGroup(group_id="archive_bronze_tables") as archive_tasks:
        for table in BRONZE_TABLES:
            PythonOperator(
                task_id=f'archive_{table}',
                python_callable=archive_old_bronze_data,
                op_kwargs={
                    'base_bronze_path': BRONZE_BASE_PATH,
                    'archive_bronze_path': ARCHIVE_BASE_PATH,
                    'retention_days': RETENTION_DAYS_BRONZE,
                    'table_name': table
                }
            )

    end = EmptyOperator(task_id='end_archival')

    start >> archive_tasks >> end
