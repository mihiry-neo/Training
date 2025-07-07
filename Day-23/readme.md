# Data Warehousing Concepts

## Data Warehouse
- Centralized system for **structured data** and **analytical processing (OLAP)**.
- **Read-heavy**, uses **denormalized structure**, **columnar storage**, and **parallel processing**.
- Enables **data-driven decisions**, tracks **KPIs**, supports BI.
- Tools: Snowflake, Redshift, Teradata, Exadata.

## Data Lake
- Stores **raw structured, semi-structured, unstructured data**.
- **Schema-on-read**, supports ELT, scalable, low-cost.
- Best for **big data, ML, real-time analytics**.

## Data Mart
- Subset of DW, focused on specific department (Sales, HR, etc.).
- Improves **query speed**, **data security**, and **business autonomy**.
- Types: **Dependent** (from DW), **Independent** (from source systems).

## Layers in DW
- **Staging Layer**: Temporary raw data zone.
  - **Persistent**: Retains data.
  - **Non-Persistent**: Discard after processing.
- **User Access Layer**: Cleaned, structured data for querying.

## Transformations (ETL)
- Standardize, clean, deduplicate data.
- Key for consistent, accurate analytics.
- Techniques: value/type unification, null handling, dropping irrelevant fields.

## Loading
- **Initial Load**: One-time, full ingest.
- **Incremental Load**: Periodic updates (Append, SCD1, Truncate).
- Supports **non-volatility** and **data freshness**.

## Slowly Changing Dimensions (SCD)
- Manage changes in dimension data:
  - **Type 0**: No change allowed.
  - **Type 1**: Overwrite current value.
  - **Type 2**: Keep history (new row per change).
  - **Type 3**: Limited history (new column).
  - **Hybrid**: Combination of types for flexibility.
