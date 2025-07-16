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

