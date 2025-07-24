CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers (name, email, phone, address)
VALUES 
('Riya Sharma', 'riya@gmail.com', '9876543210', 'Delhi'),
('Simran Kaur', 'simran@outlook.com', '9998887771', 'Chandigarh'),
('Raj Mehta', 'raj.mehta@gmail.com', '8887776662', 'Ahmedabad'),
('Anjali Rao', 'anjali_rao@gmail.com', '7776665553', 'Hyderabad'),
('Yash Jain', 'yash_jain@ymail.com', '6665554444', 'Bengaluru'),
('Tanya Kapoor', 'tanya.kapoor@gmail.com', '9551234567', 'Pune'),
('Aman Verma', 'aman@yahoo.com', '9123456789', 'Mumbai');

INSERT INTO products (product_name, category, price, stock_quantity)
VALUES 
('iPhone 14', 'Electronics', 99999.99, 25),
('Samsung Galaxy S23', 'Electronics', 74999.99, 50),
('AirPods Pro', 'Electronics', 24999.99, 200),
('Nike Backpack', 'Accessories', 1499.00, 150),
('Gaming Chair', 'Furniture', 17999.99, 30),
('Kindle Paperwhite', 'Electronics', 13999.99, 40),
('Running Shoes', 'Footwear', 2999.99, 100);
        
INSERT INTO orders (customer_id, product_id, quantity, total_price)
VALUES 
(1, 1, 1, 99999.99),
(3, 3, 1, 2999.99),
(4, 5, 2, 49999.98),
(5, 4, 1, 17999.99),
(2, 6, 1, 74999.99),
(1, 7, 3, 4497.00),
(3, 6, 1, 13999.99),
(4, 2, 1, 24999.99),
(5, 1, 1, 17999.99),
(1, 5, 2, 49999.98),
(2, 2, 2, 5999.98);