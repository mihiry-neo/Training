# Product API – Day09 - 17/06/2025

This repository contains the backend setup for an **E-commerce Product API**, built using **FastAPI**, **SQLAlchemy**, and **MySQL**. The goal is to create a real-time, scalable product management system, complete with category hierarchies, inventory updates, and dynamic pricing.

---


### 1. Database Models Design
- Designed relational models for:
  - **Products**: Includes name, price, stock, brand, attributes, etc.
  - **Categories**: Supports parent-child category relationships.
  - **Price History**: Logs price changes for audit and analytics.

### 2. Pydantic Schemas
- Created schema classes to validate and serialize API data.
- Incorporated nested relationships like `Product` → `Category` and `PriceHistory`.
- Enabled forward references and automatic ORM data conversion.

### 3. Core CRUD Operations
- Built essential database operations using SQLAlchemy ORM:
  - Create new product entries.
  - Retrieve products (all, by ID, by category, or via search).
  - Fetch all category entries.

### 4. Data Generation Utilities
- Created a **data generator class** using the **Faker** library:
  - Auto-generates product and category data with realistic values.
  - Simulates dynamic price and stock updates.
  - Creates hierarchical global category structures with subcategories.
  - Supports real-time new product generation and historical pricing logs.

### 5. Environment and Database Setup
- Connected the app to a **MySQL database** using SQLAlchemy.
- Secured sensitive DB credentials using environment variables (`.env` file).
- Set up database session handling for dependency injection.

---

## Next Steps (Planned)
- Implement full API endpoints using FastAPI.
- Add pagination, filtering, and sorting to the product listing endpoint.
- Integrate background tasks for real-time stock and price updates.

---

## Tech Stack
- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Data Generation**: Faker as Mimesis has deprecated lots of built in providers
- **Environment Management**: dotenv
