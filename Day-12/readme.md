# Product API Day4 and Advanced PySpark on Flight Data - Day12 - 20/06/2025

## Summary of Changes in API code

This update focuses on internal improvements to enhance maintainability, clarity, and control in the Product API. No core functionality was removed; the changes are fully backward-compatible and intended to support future extensibility and better development experience.

### Data Generator Optimization
- Merged `generate_product()` into `create_products()` to streamline logic and reduce indirection.
- Simplified product generation flow while maintaining dynamic attribute assignment.
- Retained ability to generate random product data based on category semantics (e.g., weight, material).

### Batch Update Flexibility for Price & Stock
- Merged single product `update_product_price()` and `update_stock_quantity()` into their respective batch methods for simplicity.
- Introduced a unified structure in `randomly_update_prices()` and `randomly_update_stocks()` to handle batch updates with logging and error handling.
- Preserved optional control over batch size for update operations.

### API Endpoint Enhancements
- Added optional `count` query parameter to `/update-prices` and `/update-stock` endpoints for controlling how many products to update per call.
- Default batch size remains `50`, with validation limits applied for safety.

### Schemas Cleanup & Reorganization
- Reorganized `schemas.py` for improved readability:
  - Grouped related models (Category, Product, PriceHistory)
  - Ordered base, create, update, and response schemas logically

### Lifespan & Scheduler Cleanup
- Added safe check: scheduler is shut down only if it was started (`scheduler.running`).
- Used `scheduler.shutdown(wait=False)` to avoid `CancelledError` during termination.

### Inventory System
- Started with the creation of Inventory Models and Routers

## PySpark

### Revisited the Basics and Filtering and Sorting part of PySpark

### Netflix Dataset
- Read both the csv's of Netflix Dataset
- Cleaned the datasets

