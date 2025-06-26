#  E-Commerce FastAPI
 
**A modular, secure, and full-featured e-commerce backend built with FastAPI, SQLAlchemy, JWT auth, and MySQL.**
 
---
 
##  Key Features
 
- **User Management**: Register, login with JWT, get/list/delete users . See what you've ordered and what is in cart
- **Product Catalog**: CRUD, pagination, inventory management, stock movements, and recommendations  
- **Cart & Checkout**: Add/remove items, reserve and release stock, clear cart  
- **Order Processing**: Checkout from cart, list orders, cancel orders  
- **Security**: Bcrypt-hashed passwords and secure JWT-based authentication  
- **Modular Design**: Separate modules for Users, Products, and Orders
 
---
 
##  Project Structure
```
.
├── main.py
├── database.py
├── auth.py
├── utils.py
│
├── Users/
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ └── routes.py
│
├── Products/
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ └── routes.py
│
└── Orders/
├── models.py
├── schemas.py
├── crud.py
└── routes.py
 
```
 
---
 
##  Setup Instructions
 
### Requirements
 
- Python 3.9+  
- MySQL  
- Install dependencies:
```bash
  pip install -r requirements.txt
```
## Environment Variables
Create a .env file in the root:
 
.env
edit
```bash
DATABASE_URL=mysql+mysqlconnector://<USER>:<PASS>@<HOST>/<DB>
JWT_SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
## Database
Use SQLAlchemy prep scripts to initialize tables.
Run the Server
```bash
 
uvicorn main:app --reload
```
Visit the documentation at http://localhost:8000/docs.
 
## API Endpoints
- Users
    - POST users/register
 
    - POST users/token
 
    - GET /users/{id}
 
    - GET /users/
 
    - DELETE /users/{id}
 
    - POST /users/{id}/addToCart
 
    - GET /users/{id}/mycart
 
    - DELETE /users/{id}/remove_item
 
    - DELETE /users/{id}/clear_cart
 
    - POST /users/{id}/checkout
 
    - GET /users/{id}/myorders
 
- Products
    - GET /products/
 
    - POST /products/
 
    - GET /products/{product_id}
 
    - POST /products/
 
    - PATCH /products/{product_id}
 
    - GET /products/{id}/inventory
   
    - POST /products/auto-generate
 
    - GET /products/{product_id}/inventory
 
    - PATCH /products/{product_id}/inventory/settings
 
    - GET /products/{product_id}/stock-movements
 
 
 
Inventory operations: /reserve, /release, /finalize, /stock-movements
 
- Cart & Orders (User-specific)
    - GET /orders/
 
    - POST /orders/
 
    - GET /orders/{order_id}
 
    - DELETE /orders/{order_id}
 
    - PATCH /orders/{order_id}/status
 
    - GET /cart/{user_id}
 
    - POST /cart/
 
    - GET /cart/{cart_id}/details
 
    - POST /cart/{cart_id}/items
 
    - PUT /cart/{cart_id}/items/{product_id}
 
    - DELETE /cart/{cart_id}/items/{item_id}
 
    - DELETE /cart/{cart_id}/clear
       
## Workflow Example
1. Register → POST /register
 
2. Login → POST /token → store JWT
 
3. Browse products → GET /products/
 
4. Add to cart → POST /users/{id}/addToCart
 
5. View cart → GET /users/{id}/mycart
 
6. Checkout → POST /users/{id}/checkout
 
7. View orders → GET /users/{id}/myorders
 
8. Cancel order → DELETE /users/{id}/orders/{order_id}/cancel