# E-Commerce FastAPI Platform

## Project Overview

A full-featured e-commerce backend API built with FastAPI and MySQL. This project handles everything you need to run an online store - user accounts, product management, shopping carts, and order processing.

The backend is split into three main parts: user management, product catalog, and order handling. Each part works independently but connects smoothly with the others. Users can browse products, add items to their cart, and complete purchases while the system automatically manages inventory levels.

Built for developers who need a solid e-commerce foundation without the complexity. Whether you're building a new online store or replacing an existing backend, this API provides the core functionality with room to customize and extend.

## Database Architecture

![Database Schema](schema.png)

The platform utilizes a well-structured relational database design that ensures data integrity and optimal performance:

- **User Management**: Comprehensive user profiles with authentication and activity tracking
- **Product Catalog**: Hierarchical category system with detailed product attributes and pricing history
- **Inventory Control**: Real-time stock tracking with movement logging and automated reorder management
- **Shopping Cart**: Persistent cart functionality with session management
- **Order Processing**: Complete order lifecycle management from creation to fulfillment

## Core Features

### User Authentication & Security
- JWT-based authentication with secure token management
- Bcrypt password hashing for enhanced security
- Role-based access control for administrative functions
- Session management and user activity tracking

### Product and Inventory Management
- Comprehensive product catalog with category organization
- Advanced inventory management with stock reservations
- Product pricing history and promotional capabilities
- Automated stock movement logging and analytics

### Customer Experience
- Persistent shopping cart functionality
- Real-time stock validation and reservation
- Seamless checkout process with inventory management
- Order tracking and status updates

### Analytics and Reporting
- Stock movement tracking and reporting
- Order analytics and sales metrics
- User behavior insights and recommendations
- Inventory optimization suggestions

## Technical Architecture

### Backend Framework
- **FastAPI**: High-performance async framework with automatic API documentation
- **SQLAlchemy ORM**: Database abstraction with relationship management
- **MySQL**: Robust relational database for data persistence
- **Pydantic**: Data validation and serialization

### Security Implementation
- **JWT Tokens**: Stateless authentication with configurable expiration
- **Password Hashing**: Bcrypt algorithm for secure credential storage
- **Input Validation**: Comprehensive request validation and sanitization

### Development Standards
- **Modular Architecture**: Separated concerns with dedicated modules
- **RESTful API Design**: Intuitive endpoints following REST principles
- **Documentation**: Auto-generated OpenAPI/Swagger documentation

## Getting Started

### Prerequisites
- Python 3.9 or higher
- MySQL 8.0 or compatible database
- Virtual environment (recommended)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-fastapi
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file in the project root:
   ```
   DATABASE_URL=mysql+mysqlconnector://username:password@localhost/database_name
   JWT_SECRET_KEY=your-secure-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Initialize Database**
   Run the database initialization scripts to create required tables and relationships.

6. **Launch Application**
   ```bash
   uvicorn main:app --reload
   ```

7. **Access Documentation**
   Navigate to `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints Overview

### Authentication
- User registration and login
- JWT token management
- Password reset functionality

### User Management
- Profile creation and updates
- User preferences and settings
- Account activity tracking

### Product Operations
- Product catalog browsing
- Category-based filtering
- Inventory status checking
- Product recommendations

### Shopping Cart
- Add/remove items
- Quantity adjustments
- Cart persistence
- Stock validation

### Order Management
- Checkout processing
- Order status tracking
- Order history retrieval
- Cancellation handling

### Inventory Control
- Stock reservations
- Movement tracking
- Automatic restocking
- Low-stock alerts

## Project Structure

The codebase follows a modular architecture pattern:

```
├── main.py                 # Application entry point
├── database.py            # Database configuration
├── auth.py               # Authentication utilities
├── utils.py              # Common utilities
├── Users/                # User management module
├── Products/             # Product catalog module
└── Orders/               # Order processing module
```

Each module contains:
- **models.py**: Database models and relationships
- **schemas.py**: Request/response data models
- **crud.py**: Database operations
- **routes.py**: API endpoint definitions

## Business Workflow

1. **User Onboarding**: Registration and profile setup
2. **Product Discovery**: Browse catalog and categories
3. **Shopping Experience**: Add items to cart with real-time validation
4. **Secure Checkout**: Process orders with inventory management
5. **Order Fulfillment**: Track orders from processing to delivery
6. **Customer Support**: Order management and issue resolution
