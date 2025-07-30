-- Fully updated init.sql for ecommerce_db

DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- USERS
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(20),
    age INT,
    phone_number VARCHAR(20),
    nationality VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- CATEGORIES
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id)
        ON DELETE SET NULL
);

-- PRODUCTS
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    brand VARCHAR(100),
    attributes JSON,
    category_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE CASCADE
);

-- PRODUCT PRICE HISTORY
CREATE TABLE product_history (
    ph_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    old_price DECIMAL(10, 2) NOT NULL,
    new_price DECIMAL(10, 2) NOT NULL,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(100),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- INVENTORY
CREATE TABLE inventory (
    inv_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL UNIQUE,
    quantity_available INT DEFAULT 0,
    quantity_reserve INT DEFAULT 0,
    reorder_level INT DEFAULT 10,
    reorder_quantity INT DEFAULT 20,
    unit_cost DECIMAL(10, 2),
    last_restocked DATETIME,
    expiry_date DATETIME,
    batch_number VARCHAR(100),
    location VARCHAR(100),
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- CARTS
CREATE TABLE carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- CART ITEMS
CREATE TABLE cart_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE SET NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
        ON DELETE CASCADE
);

-- ORDERS
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    items JSON NOT NULL,
    total_amount FLOAT NOT NULL,
    status ENUM('pending', 'shipped', 'delivered', 'canceled') DEFAULT 'pending',
    payment_method VARCHAR(50),
    shipping_address VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- STOCK MOVEMENTS (patched: renamed `change` to `quantity_change`)
CREATE TABLE stock_movements (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    quantity_change INT NOT NULL,
    reason VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cart_id INT,
    order_id INT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE SET NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
        ON DELETE SET NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE SET NULL
);
