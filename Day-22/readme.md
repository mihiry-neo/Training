## Netflix Titles & Credits Analysis with PySpark - 4/7/25

This notebook applies PySpark to explore, transform, validate, and analyze Netflix Titles and Credits datasets using real-world data engineering practices. Below is a structured summary of each stage implemented in code.

---

### 1. Schema Definition and File Reading
- Defined strict `StructType` schemas for `titles.csv` and `credits.csv`.
- Loaded both files as Spark DataFrames using `.read.format("csv")` with schema enforcement.
- Wrote the DataFrames to Delta tables for future querying and ingestion consistency.

---

### 2. Data Loading from Delta Tables
- Read the Delta tables `titles_df` and `credits_df` for further transformations.

---

### 3. JSON Field Fix (Array Columns)
- Fixed the stringified array fields:
  - `genres` → `genres_array`
  - `production_countries` → `countries_array`
- Used `from_json()` with `ArrayType(StringType())`.

---

### 4. Display and Initial Data Inspection
- Used `display()` and `limit()` to inspect records visually.
- Verified `dtypes` of DataFrames for correctness.

---

### 5. Null Value Audit
- Computed null count for every column in both datasets.
- Used `isnull()` and `when()` wrapped in `count()` for complete null profiling.

---

### 6. Handling Missing Character Fields
- Replaced missing values in `character` column for actors:
  - If `role == ACTOR` and `character is null` → `'Unknown Character'`
  - If `character is null` in general → `'N/A'`

---

### 7. Handling Missing IMDB Votes
- Filled `null` in `imdb_votes` using logic:
  - If `imdb_score` is not null → default `100`
  - Otherwise → `0`

---

### 8. Critical Column Selection (Preparation for Joins/Aggregations)
- Selected a subset of important columns like `id`, `title`, `release_year` for further focused processing.

---

### 9. Joins Between Titles and Credits
- Merged `titles_df` with `credits_df` on `id` for enriched views.
- Prepared the base for actor-title relationships.

---

### 10. Preliminary Transformation and Filtering
- Applied simple filters and `display()` on joined dataset to explore actor and title combinations.
- Explored conditional and column-based filtering using `where()` and `col()`.

---

### 11. Cleanup and Null Management Recap
- Recapped missing value handling, display outputs, and column replacement logic.

---

### Key Practices Followed
- Strict schema enforcement for reliability.
- Delta format used for transaction-safe data storage.
- Proper null handling logic for critical fields.
- JSON parsing for stringified arrays.
- Modular, readable, and extendable code structure.
