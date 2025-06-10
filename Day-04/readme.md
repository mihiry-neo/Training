# SQL Triggers and Python Pandas -- Day-04 -- 10/06/25

## `Taxi Trips TimeSeries Data `
- Loaded and cleaned taxi trip data from a CSV file
- Processed datetime columns and filtered data for trips from January 2023 onwards
- Added temporal features (year, month, day, hour, weekday) to analyze patterns
- Performed time-based aggregations:
  - Daily trip counts and revenue
  - Weekly statistics (fares, distances, passenger counts)
  - Monthly and yearly aggregations

### `Time Zone Handling`
- Localized timestamps to UTC timezone
- Converted to New York timezone for proper local analysis

### `Time Series Functions and Explode Function`
- Trips by weekday (showing busiest days)
- Created 7-day rolling averages to identify trends
- Examined time between trips
- Categorized trips into time periods (rush hours, business hours, late night)


## SQL Triggers
Created and tested several database triggers:

### Before Insert Trigger
- `prevent_low_salary`: Blocks employee inserts with salary < 50

### After Insert Trigger
- `log_high_salary`: Logs employees with salary > 10,000 to audit table

### Update (Before and After) Triggers
- `track_salary_change`: Logs all salary changes to a tracking table
- `enforce_salary_cap`: Prevents salary increases > 2x current salary

### Delete (Before and After) Triggers
- `prevent_fin_emp_deletion`: Blocks deletion of finance department employees
- `log_deleted_dept`: Logs department deletions and cascades to employees
