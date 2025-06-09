# SQL – Day-03 - 09 June 2025

---

### 1. ✅ Window Functions

Window functions perform calculations across a set of rows related to the current row — without collapsing the result into a single row (unlike aggregate functions).


Practiced various analytical functions with `OVER` clause:
- `ROW_NUMBER()`
- `RANK()` and `DENSE_RANK()`
- `LEAD()` and `LAG()`
- `FIRST_VALUE()` and `LAST_VALUE()`
- `SUM()`, `AVG()`, and `COUNT()` with partitioning
- ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING for `LAST_VALUE()`

**Use Cases:**
- Ranking employees by salary (within department and globally)
- Identifying top-N salaries per department
- Cumulative and average salary computations
- Lag/lead comparisons across salaries

---

### 2. ✅ Stored Procedures

A **Stored Procedure** is a saved block of SQL code that can be executed repeatedly. They improve modularity and reusability in database systems.

#### ➤ **Parameterized Stored Procedures (2 examples):**
- Increasing Salary by Percentage for a particular department
- Particular Department Stats

#### ➤ **Non-Parameterized Stored Procedures (3 examples):**
- Employees with Salary Above Department Average
- Department with Highest Average Salary
- Finding Employees with duplicate salaries

**Implemented in MySQL using `CREATE PROCEDURE`, `IN` parameters, and `CALL` statements.**


---

### 3. ✅ Views

A **View** is a virtual table based on the result set of an SQL query. It simplifies data access and hides complex logic. Views types that are non-updatable are views with aggregation, group by or having clause, distinct, joins, set operations, sub-queries, window functions, calculated columns and limit/offset/fetch.

Created and managed SQL views using Python + SQL:
- `emp_basic_view` – Basic employee info
- `emp_dept_view` – Joined view of employees with department names
- `avg_salary_dept` – Average salary by department

**Operations Performed:**
- View creation and selection
- Data updates via updatable view (`emp_basic_view`)
- Renaming views (`emp_dept_view` → `join_view`)
- Dropping views
- Listing views using `SHOW TABLES`

