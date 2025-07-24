-- Create the target database (only if running from psql shell, not inside container entrypoint)
-- CREATE DATABASE ecommerce_warehouse;
-- \c ecommerce_warehouse;

-- SCHEMAS
CREATE SCHEMA IF NOT EXISTS facts;
CREATE SCHEMA IF NOT EXISTS dimensions;

-- ========================
-- DIMENSIONS
-- ========================

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS dimensions.dim_customers (
    customer_sk SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    city VARCHAR(100),
    created_at TIMESTAMP
);

-- Dimension: Products
CREATE TABLE IF NOT EXISTS dimensions.dim_products (
    product_sk SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2),
    created_at TIMESTAMP
);

-- Customer Segments (Gold Output)
CREATE TABLE IF NOT EXISTS dimensions.customer_segments (
    segment_sk SERIAL PRIMARY KEY,
    customer_id INT,
    recency_days INT,
    frequency INT,
    monetary_value DECIMAL(12,2),
    segment VARCHAR(50),
    report_date TIMESTAMP
);

-- ========================
-- FACTS
-- ========================

-- Fact: Orders (from Gold product performance)
CREATE TABLE IF NOT EXISTS facts.fact_orders (
    order_sk SERIAL PRIMARY KEY,
    order_id INT,
    customer_sk INT,
    product_sk INT,
    quantity INT,
    total_price DECIMAL(10,2),
    order_date TIMESTAMP,
    FOREIGN KEY (customer_sk) REFERENCES dimensions.dim_customers(customer_sk),
    FOREIGN KEY (product_sk) REFERENCES dimensions.dim_products(product_sk)
);

-- Fact: Sales Summary (Gold Aggregation)
CREATE TABLE IF NOT EXISTS facts.sales_summary (
    summary_sk SERIAL PRIMARY KEY,
    order_date TIMESTAMP,
    total_orders INT,
    total_sales DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    report_date TIMESTAMP
);
