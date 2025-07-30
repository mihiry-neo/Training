# E-commerce Data Pipeline Project

## Overview

This project implements a comprehensive end-to-end data engineering pipeline for an e-commerce platform using modern data stack technologies. The pipeline follows the medallion architecture (Bronze, Silver, Gold) and includes real-time streaming capabilities, automated orchestration, and business intelligence dashboards.

## Architecture

The system is built using a microservices architecture with Docker containerization, featuring:

- **Source System**: MySQL database containing transactional e-commerce data
- **Data Lake**: Organized in medallion architecture with Bronze, Silver, and Gold layers
- **Data Warehouse**: PostgreSQL for analytical workloads
- **Orchestration**: Apache Airflow for workflow management
- **Processing Engine**: Apache Spark for batch and stream processing
- **Streaming Platform**: Apache Kafka for real-time event processing
- **Visualization**: Apache Superset for business intelligence dashboards
- **Event Analytics**: PostHog integration for customer behavior tracking

## Key Features

### Data Pipeline Architecture
- **Bronze Layer**: Raw data ingestion from MySQL transactional database
- **Silver Layer**: Data cleaning, validation, and standardization
- **Gold Layer**: Business-ready aggregated data and analytics
- **Real-time Processing**: Kafka streaming for event-driven data processing

### Data Sources
- **Users**: Customer information and profiles
- **Products**: Product catalog with categories and inventory
- **Orders**: Transaction data with order items and pricing
- **Categories**: Product categorization hierarchy
- **Inventory**: Stock levels and warehouse management
- **Events**: Real-time customer behavior and interaction data

### Automated Workflows
- Daily batch processing of transactional data
- Automated data quality checks and validation
- Incremental data loading with date partitioning
- Data archival and retention management
- Real-time event streaming and processing

## Technology Stack

### Core Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Apache Airflow**: Workflow orchestration and scheduling
- **Apache Spark**: Distributed data processing engine
- **Apache Kafka**: Event streaming platform
- **Zookeeper**: Kafka cluster coordination

### Databases
- **MySQL**: Source transactional database
- **PostgreSQL**: Data warehouse for analytics

### Analytics & Visualization
- **Apache Superset**: Business intelligence and dashboards
- **PostHog**: Customer analytics and event tracking

### Monitoring & Management
- **Kafka UI**: Streaming data monitoring
- **Airflow Web UI**: Pipeline monitoring and management
- **Spark UI**: Job monitoring and performance tracking

## Data Processing Layers

### Bronze Layer (Raw Data)
- Direct ingestion from MySQL source systems
- Data stored in native format with minimal transformation
- Partitioned by date for efficient querying
- Full historical data preservation

### Silver Layer (Cleaned Data)
- Data quality validation and cleansing
- Schema standardization and type conversion
- Business rule application
- Deduplication and error handling
- Structured for downstream consumption

### Gold Layer (Business Data)
- Aggregated business metrics and KPIs
- Customer segmentation analysis
- Product performance analytics
- Sales reporting and forecasting
- Ready for business intelligence tools

## Key Pipelines

### Daily Batch Processing
- Automated extraction from MySQL source
- Multi-table processing with dependency management
- Incremental loading with change data capture
- Data validation and quality checks
- Loading to data warehouse

### Real-time Streaming
- Kafka event ingestion from multiple sources
- Real-time data processing with Spark Streaming
- Event-driven analytics and alerting
- Customer behavior tracking
- Inventory updates and notifications

### Data Archival
- Automated data lifecycle management
- Historical data archival based on retention policies
- Storage optimization and cost management
- Compliance and governance requirements

## Business Intelligence

### Customer Analytics
- Customer segmentation using RFM analysis
- Lifetime value calculations
- Churn prediction and retention analysis
- Behavioral pattern identification

### Product Analytics
- Product performance metrics
- Inventory optimization
- Category analysis
- Pricing strategy insights

### Sales Analytics
- Daily, weekly, and monthly sales reporting
- Revenue trend analysis
- Order pattern analysis
- Geographic sales distribution

## Data Quality & Governance

### Data Validation
- Schema validation and type checking
- Business rule enforcement
- Duplicate detection and handling
- Completeness and accuracy checks

### Monitoring & Alerting
- Pipeline health monitoring
- Data quality metrics tracking
- Performance monitoring and optimization
- Error handling and notification

## Deployment & Operations

### Container Orchestration
- Multi-container deployment with Docker Compose
- Service dependency management
- Health checks and auto-restart capabilities
- Resource allocation and scaling

### Configuration Management
- Environment-based configuration
- Secrets management
- Database connection pooling
- Service discovery and networking

### Monitoring & Maintenance
- Centralized logging and monitoring
- Performance metrics collection
- Automated backup procedures
- Disaster recovery planning

## Development Workflow

### Data Generation
- Synthetic data generation for testing
- Realistic e-commerce transaction simulation
- User behavior pattern simulation
- Product catalog generation

### Testing & Validation
- Unit testing for data transformations
- Integration testing for end-to-end pipelines
- Data quality validation tests
- Performance benchmarking

### Deployment Strategy
- Environment-specific configurations
- Rolling deployments with zero downtime
- Database migration management
- Rollback procedures

## Scalability & Performance

### Horizontal Scaling
- Spark cluster scaling for processing workloads
- Kafka partition scaling for streaming throughput
- Database read replica configuration
- Load balancing and distribution























# eCommerce Analytics Dashboards (Apache Superset)

This project provides end-to-end **interactive dashboards** for an eCommerce business built using **Apache Superset** and PostgreSQL. The dashboards offer deep insights into **sales trends**, **product performance**, **customer segments**, and **category-level analytics**, leveraging a dimensional model with `fact` and `dimension` schemas.

---

## Database Schema Overview

### facts schema
- `fact_orders`: Daily order count and sales by product
- `sales_summary`: Aggregated daily sales, order volume, and average order value

### dimensions schema
- `dim_products`: Product details (brand, price, category)
- `dim_categories`: Hierarchical category structure
- `dim_users`: Customer information
- `customer_segments`: RFM-based customer segments

---

## Dashboards Overview

### 1. Sales Performance Dashboard
| Chart | Type | SQL | Notes |
|-------|------|-----|-------|
| Total Sales Over Time | Line | Uses `sales_summary` | X: `order_date`, Y: `total_sales` |
| Total Orders Over Time | Line | Uses `sales_summary` | X: `order_date`, Y: `total_orders` |
| Avg Order Value Over Time | Line | Uses `sales_summary` | X: `order_date`, Y: `avg_order_value` |
| Total Sales KPI | Big Number | SUM on `total_sales` | Filter: last 30 days |
| Sales by Category | Pie | JOIN `fact_orders` + `dim_products` + `dim_categories` | Group by `category_name` |
| Daily Sales Heatmap | Calendar Heatmap | Uses `sales_summary` | Metric: `total_sales`, Time Col: `order_date` |

---

### 2. Product Performance Dashboard
| Chart | Type | SQL | Notes |
|-------|------|-----|-------|
| Top Products by Sales | Bar | JOIN `fact_orders` + `dim_products` | Group by `product_name`, SUM(`total_sales`) |
| Top Brands by Sales | Bar | Group by `brand` | JOIN with `dim_products` |
| Price vs Sales | Scatter Plot | `dim_products` + `fact_orders` | X: `price`, Y: `total_sales` |
| Product Sales Table | Table | Show `product_name`, `brand`, `total_sales` |

---

### 3. Customer Segmentation Dashboard
| Chart | Type | SQL | Notes |
|-------|------|-----|-------|
| Customers per Segment | Pie | `customer_segments` | Group by `segment` |
| Frequency vs Monetary | Scatter | X: `frequency`, Y: `monetary_value` | Group by `segment` |
| RFM Table | Table | Show RFM values + `segment` | Use filters |
| Top Customers | Bar/Table | JOIN `customer_segments` + `dim_users` | Order by `monetary_value` DESC |

---

### 4. Category Analysis Dashboard
| Chart | Type | SQL | Notes |
|-------|------|-----|-------|
| Sales by Category | Bar | JOIN `fact_orders` + `dim_products` + `dim_categories` | Group by `category_name` |
| Category Drilldown | Treemap | Same as above | Hierarchy: `parent_id`, `category_name` |
| Sales Trend by Category | Line | Filterable by category |
| Category Table | Table | Show `category_id`, `category_name`, `created_at` |

---

### 5. Daily Operations Dashboard
| Chart | Type | SQL | Notes |
|-------|------|-----|-------|
| Today’s Total Sales | Big Number | Filter: `order_date = CURRENT_DATE` |
| Today’s Orders per Product | Bar | Filter `fact_orders.sale_date = CURRENT_DATE` |
| Unique Customers Today | Big Number | JOIN with `dim_users` and `fact_orders` |

---

## How to Use

1. **Connect your Postgres DB** to Superset.
2. Open **SQL Lab**, paste each query, and click **Explore**.
3. Choose the suggested **chart type** and set:
   - X-axis
   - Metrics
   - Dimensions (Group by)
4. Add filters where needed (`report_date`, `category`, `segment`, etc.).
5. Save charts and arrange them into relevant **dashboards**.
6. Set up auto-refresh intervals (e.g., every 1 hour).

---