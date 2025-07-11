# FastAPI E-Commerce Backend (Dockerized)

This is a fully containerized FastAPI E-Commerce backend with modular apps for Users, Products, and Orders. The backend uses a Dockerized MySQL database.
---

## Features

- FastAPI backend with Swagger UI
- Modular architecture: `Users`, `Products`, `Orders`
- MySQL 8 as backend DB (Dockerized)
- Automatic table creation and seed data generation
- Docker + Docker Compose setup
- JWT-based Authentication

---

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- MySQL 8
- Docker, Docker Compose
- Uvicorn
- Faker (for seed data)


---

## Build & Push (One-Time Setup by Author)

Before publishing this for public use, I:

1. Built the image locally using:
   ```bash
   docker build -t ecommerce-fastapi-backend .
   ```

2. Tagged and pushed it to Docker Hub:
   ```bash
   docker tag ecommerce-fastapi-backend mihir283/ecom
   docker push mihir283/ecom
   ```

Now others can pull and use the image directly.

---

## Setup & Run (via Prebuilt Docker Image)

### 1. Pull the prebuilt image

```bash
docker pull mihir283/ecom
```

### 2. Create a `.env` file

```env
MYSQL_USER=ecom_user
MYSQL_PASSWORD=ecom_pass
MYSQL_DATABASE=ecom_db
DB_HOST=db
DATABASE_URL=mysql+pymysql://ecom_user:ecom_pass@db/ecom_db
JWT_SECRET_KEY=secretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start the application

```bash
docker-compose up
```

This will:
- Use `mihir283/ecom` to run your FastAPI app
- Launch the MySQL container and initialize the DB
- Auto-create tables and seed fake data

---

## API Access (Swagger & ReDoc)

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Access MySQL Inside the Container

```bash
docker exec -it ecommerce-db bash
mysql -u ecom_user -p
# Enter password: ecom_pass
USE ecom_db;
SHOW TABLES;
```

---

## Deployment Checklist Summary

- [x] Modular FastAPI project with routers (`Users`, `Products`, `Orders`)
- [x] SQLAlchemy + Pydantic models
- [x] JWT-based authentication setup
- [x] Database auto-migration on container start
- [x] Sample data via Faker
- [x] Dockerfile + docker-compose support
- [x] Prebuilt image on DockerHub: `mihir283/ecom`

---

## Folder Structure (in image)

```
app/
├── main.py
├── database.py
├── datagen.py
├── genpro.py
├── genorders.py
├── genusers.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Users/
├── Products/
└── Orders/
```

---

## Final Notes

- Runs fully on Docker using a prebuilt image
- Fast startup with `.env` and `docker-compose up`
- Great base for a full-stack e-commerce app with integrated JWT auth

---
