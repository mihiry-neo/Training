# dags/config/spark_job_config.py

SPARK_MASTER = "spark://spark-master:7077"
SPARK_CONF = {"spark.master": SPARK_MASTER}
SPARK_PACKAGES = {
    "mysql": "mysql:mysql-connector-java:8.0.33",
    "postgres": "org.postgresql:postgresql:42.6.0",
}
JDBC_URLS = {
    "mysql": "jdbc:mysql://mysql_source:3306/ecommerce_daily_db",
    "postgres": "jdbc:postgresql://postgres_dwh:5432/ecommerce_dwh",
}
CREDENTIALS = {
    "mysql": {
        "user": "ecomuser",
        "password": "ecompassword",
    },
    "postgres": {
        "user": "airflow",
        "password": "airflow",
    }
}
