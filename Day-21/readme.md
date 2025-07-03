# GitHub Issues Incremental Ingestion Pipeline (PySpark + Delta Lake on Databricks) - 3/7/25 - Day-21


## Objective
Build a robust, incremental ingestion pipeline in Databricks using PySpark to fetch data from a paginated public API (GitHub Issues API) and store it in a Delta Lake table with proper error handling, schema validation, and load verification.

---

## Key Features

### 1. **Secure Token-Based API Access**
- GitHub Personal Access Token securely retrieved from a Databricks secret scope (`my_scope`).
- Used for authenticated API calls to increase rate limit from 60 to 5000 requests/hour.

### 2. **Pagination Handling**
- Dynamically loops through multiple pages using `?page` and `per_page` parameters.
- Stops automatically when the last page is reached (`< per_page` items returned).

### 3. **Structured Schema Definition**
- Defined a nested PySpark schema to align with the JSON structure of GitHub issues.
- Includes nested `user.login` field for flattening later.

### 4. **Incremental Load Support**
- Uses `updated_at` field from Delta table to identify the most recent ingestion timestamp.
- Fetches only records updated after `since_ts`, ensuring incremental ingestion.
- Includes an `ingest_ts` column for observability and audit.

### 5. **Serverless-Compatible Ingestion**
- Avoids `sc.parallelize()` (unsupported in serverless) by using `spark.createDataFrame()` directly on the list of dictionaries.

### 6. **Robust Error Handling**
- Detects and raises errors for:
  - API failures (`!= 200`)
  - Malformed or unexpected responses (non-list data)
  - JSON parsing errors

### 7. **Delta Table Write**
- Data is appended to a Delta Lake table (`github_issues_bronze`) in Databricks.
- Ensures compatibility with ACID operations and future upserts.

### 8. **Validation Test Case**
- Asserts that the number of records fetched from the API matches the number of ingested rows.
- Ensures data consistency and ingestion reliability.

---

## Final Output
- Total records fetched: **150**
- Records successfully ingested: **150**
- Row count validation: **Passed ✅**
