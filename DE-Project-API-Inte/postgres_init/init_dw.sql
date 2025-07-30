-- ========================
-- SCHEMAS
-- ========================

CREATE SCHEMA IF NOT EXISTS facts;
CREATE SCHEMA IF NOT EXISTS dimensions;

-- ========================
-- DIMENSIONS
-- ========================

-- Dimension: Customers
CREATE TABLE dimensions.dim_users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(20),
    age INT,
    phone_number VARCHAR(20),
    nationality VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Categories (Optional but useful for rollups)
CREATE TABLE IF NOT EXISTS dimensions.dim_categories (
    category_sk SERIAL PRIMARY KEY,
    category_id INT UNIQUE,
    name VARCHAR(100),
    parent_id INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Dimension: Products
CREATE TABLE IF NOT EXISTS dimensions.dim_products (
    product_sk SERIAL PRIMARY KEY,
    product_id INT UNIQUE,
    name VARCHAR(255),
    brand VARCHAR(100),
    category_id INT,
    category_name VARCHAR(255),
    attributes JSONB,
    price DECIMAL(10,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Dimension: Customer Segments (Gold Output)
CREATE TABLE IF NOT EXISTS dimensions.customer_segments (
    segment_sk SERIAL PRIMARY KEY,
    customer_id INT,
    recency_days INT,
    frequency INT,
    monetary_value DECIMAL(12,2),
    segment_label VARCHAR(50),
    report_date TIMESTAMP
);

-- ========================
-- FACTS
-- ========================

-- Fact: Orders (flattened from JSON items in Bronze/Gold)
CREATE TABLE IF NOT EXISTS facts.fact_orders (
    order_sk SERIAL PRIMARY KEY,
    order_id INT,
    customer_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    order_date TIMESTAMP,
    status VARCHAR(20),
    payment_method VARCHAR(50),
    shipping_city VARCHAR(100),
    created_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES dimensions.dim_customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES dimensions.dim_products(product_id)
);

-- Fact: Daily Sales Summary
CREATE TABLE IF NOT EXISTS facts.sales_summary (
    summary_sk SERIAL PRIMARY KEY,
    order_date DATE,
    total_orders INT,
    total_items_sold INT,
    total_sales DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    report_date TIMESTAMP
);
