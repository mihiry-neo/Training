# PySpark and Product API (Day3) - Day11 - 19/06/2025

---
## Product API (FastAPI + SQLAlchemy)

### Key Features Added

- **Update Product Endpoint**
  - Implemented PATCH functionality to update a product using:
    - Product ID
    - Name
    - Brand

- **Created Update Product Function and pydantic models to support the endpoint**

- **Response Schema Optimization**
  - Refactored and optimized response schemas for consistency, minimalism, and clarity
  - Ensured schema includes only necessary fields for frontend consumption

## Key Tasks Performed in PySpark

### 1. User Defined Functions (UDFs)

- Created multiple UDFs to classify data:
  - **Arrival Delay Status** (On Time / Delayed)
  - **Security Risk Level** based on delay duration
  - **Flight Duration Category** (Short, Medium, Long, Very Long)
  - **Red-Eye Flight Detection** based on night departure and early morning arrival
  - **Early Departure Detection** to compare scheduled and actual departure times

### 2. Column Engineering

- Created new fields by combining existing columns:
  - **Route Code** using origin and destination airports
  - **Unique Flight Code** combining airline and flight number

### 3. Filtering and Pattern Matching

- Filtered flights based on pattern matching on flight codes
- Identified red-eye flights from a specific airport

### 4. Airport & City Mapping

- Mapped airport codes to city names by joining with an airports dataset
- Created enriched flight data with origin and destination cities

### 5. Window Functions & Aggregations

- Used groupBy with aggregation functions (`count`, `min`, `max`, `avg`) to:
  - Identify city pairs with average distances
  - Determine airports with the least number of departing flights

### 6. Data Transformation Design Patterns

- Applied clean design principles:
  - Modular UDFs
  - Function-based renaming of columns using a configuration dictionary
  - Joins with multiple DataFrames for enriching flight data


