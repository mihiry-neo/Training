FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Convert Windows line endings in Python scripts (esp. if created on Windows)
RUN find . -type f -name "*.py" -exec sed -i 's/\r$//' {} \;

# Add a startup script inline (no external sh files)
CMD bash -c '\
  echo "⏳ Waiting for MySQL to be ready..." && \
  until python -c "import pymysql; \
    import os; \
    pymysql.connect( \
      host=os.getenv(\"DB_HOST\", \"db\"), \
      user=os.getenv(\"MYSQL_USER\"), \
      password=os.getenv(\"MYSQL_PASSWORD\"), \
      database=os.getenv(\"MYSQL_DATABASE\") \
    )"; do \
    echo "❌ DB not ready yet... retrying in 2s"; \
    sleep 2; \
  done && \
  echo "✅ DB is up. Seeding data..." && \
  python genusers.py && \
  python genpro.py && \
  python genorders.py && \
  echo "🚀 Starting Uvicorn..." && \
  uvicorn main:app --host 0.0.0.0 --port 8000'
