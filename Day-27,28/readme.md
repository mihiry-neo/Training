# Airflow Crypto ETL Pipeline with PostgreSQL – Project Summary

This project sets up a **complete ETL pipeline** using **Apache Airflow**, which extracts live cryptocurrency market data from the CoinGecko API and stores it in a **PostgreSQL database** every 5 minutes. The entire setup is **containerized with Docker**, making it reproducible and easy to deploy.

---

## Project Structure

- **DAG file**: `crypto_etl_pg.py` (inside `./dags/`)
- **Docker Compose**: Defines three services – `postgres`, `airflow-webserver`, and `airflow-scheduler`
- **Requirements**: Python dependencies like `requests` and the Postgres provider
- **`.env` file**: Contains the shared `SECRET_KEY` used by both webserver and scheduler for session consistency

---

## DAG Breakdown (`crypto_etl_pg.py`)

- **Schedule**: Every 5 minutes (`*/5 * * * *`)
- **Tasks**:
  1. **Extract**: Fetches market data (price, cap, volume, last_updated) for Bitcoin, Ethereum, and Dogecoin from CoinGecko.
  2. **Transform**: Structures the JSON response into a list of tuples.
  3. **Load**: Connects to the Postgres DB using `PostgresHook`, creates a table `crypto_market` if it doesn’t exist, and inserts the data.

- **Connection**:
  Uses `conn_id = postgres_default`, which must be configured in the Airflow UI (Admin → Connections) with the same credentials and DB used in the Postgres container.

---

## Docker Compose Setup

- **PostgreSQL**:
  - Runs on port `5432`
  - Uses database name `crypto_db` with user `airflow` and password `airflow`

- **Airflow Webserver**:
  - Installs requirements
  - Initializes the metadata DB
  - Creates the admin user
  - Starts the webserver on port `8080`
  - Shares the secret key using environment variable `${SECRET_KEY}`

- **Airflow Scheduler**:
  - Runs the scheduler after DB migration
  - Uses the same `SECRET_KEY` to maintain session security and avoid log access issues

- **Volumes**:
  - `./dags:/opt/airflow/dags`: Mounts your DAG code
  - `postgres_data`: Persists PostgreSQL data

---

## Secret Key Handling

Both the Airflow webserver and scheduler must **share the same secret key**, which is passed using a `.env` file. Without this, you’ll face issues like:
- `403 Forbidden` errors when accessing logs
- Session mismatch or CSRF issues



# Advanced Apache Airflow Notes – Data Engineering Focus

This repository provides a **deep dive into Apache Airflow** with a focus on **real-world orchestration, ETL pipelines, dynamic DAGs, PySpark integration, error handling, and deployment strategies**. Perfect for those targeting **production-grade workflow orchestration** and **data engineering roles**.

---

## 1. Introduction to Apache Airflow
- What is Airflow, and why use it for workflow orchestration
- History, architecture, use cases in modern data pipelines

## 2. Installation & Setup
- Install via `pip`, constraints, Airflow Docker setup
- Folder structure & initializing metadata DB

## 3. Airflow Core Concepts
- DAGs, Tasks, Operators, Schedulers, Executors
- The DAG bag, Directed Acyclic Graph principles

## 4. DAG Lifecycle & Execution Flow
- From code parsing to task instance execution
- Trigger rules, task dependencies, and retries

## 5. Advanced Task Orchestration
- Branching, ShortCircuit, Dummy, TriggerDagRun
- Setup/teardown tasks, conditional flows, SLA miss callbacks

## 6. Custom Operators, Hooks & Plugins
- Extending `BaseOperator` and writing custom logic
- Creating reusable code with custom hooks and plugins

## 7. Variables, Connections, Pools & XComs
- Using `airflow.models.Variable`, `XCom.push()`, `XComArg`
- Managing secrets and credentials via Connections UI

## 8. Monitoring, Logging & Alerting
- Airflow logging, alerting via email/Slack
- Task failure notifications, log retention

## 9. Airflow UI Deep Dive
- Graph View, Tree View, Gantt View, Task Duration
- Navigating logs, retries, and task states via UI

## 10. Datasets & Data-Aware Scheduling
- Using `Dataset` for cross-DAG dependencies
- Data-aware triggering and scheduling examples

## 11. TaskFlow API (Functional DAGs)
- Writing Pythonic DAGs using `@task` decorators
- Automatic XComs and parameter passing

## 12. Airflow Configuration & Custom Plugins
- Key airflow.cfg settings
- Writing and loading custom plugins dynamically

## 13. CLI & REST API
- Using `airflow dags list`, `tasks run`, etc.
- Airflow 2+ REST API for triggering DAGs programmatically

## 14. Scheduler & Executors
- How the scheduler parses DAGs and queues tasks
- CeleryExecutor, LocalExecutor, KubernetesExecutor

## 15. Sensors & Deferrable Operators
- FileSensor, HttpSensor, S3Sensor
- Async sensors for scalable and efficient waits

## 16. Incremental ETL Handling
- Using timestamps, checkpoints, Watermarks
- SCD handling and idempotent pipelines

## 17. Airflow with PySpark Jobs
- Submitting PySpark via BashOperator, Livy, or SparkSubmitOperator
- PySpark on Databricks, handling Spark logs
