# Apache Spark, PySpark & Databricks - Day07 - 13/06/2025

## 1. Apache Spark
Apache Spark is a distributed data processing engine designed for speed and scalability. It performs in-memory computations and supports large-scale analytics, machine learning, and stream processing.

### Key Concepts:
- In-memory execution for faster performance  
- Multi-language support: PySpark (Python), Scala, Java, R  
- Unified engine for batch, streaming, ML, and graph processing  
- Compatible with Hadoop ecosystem and modern data lakes  

---

## 2. Spark Architecture 
Spark uses a **Driver-Executor** model:
- **Driver**: Manages the application and distributes tasks.
- **Executors**: Perform computations and store data on worker nodes.

Jobs are broken into **stages** and **tasks**, executed in parallel using a **DAG (Directed Acyclic Graph)**. The DAG scheduler optimizes task execution before running.

---

## 3. Key Spark Concepts

- **RDD (Resilient Distributed Dataset)**: Core data structure, fault-tolerant, lazily evaluated.
- **Transformations & Actions**: Transformations (e.g., `map`, `filter`) build computation plans; actions (e.g., `collect`, `count`) trigger execution.
- **Lazy Evaluation**: Delays computation until results are actually needed.
- **Partitioning**: Data is divided across nodes for parallelism and efficiency.
- **Memory Management**: Execution and storage memory are carefully managed across executors to avoid OOM errors.
- **Logging**: Standard output and error logs per worker for monitoring.
- **Query Optimizer**: Catalyst, a query optimizer helps in Predicate pushdown, Projection Pushdown, constant folding, filter combination
- **Join Optimization**: Broadcast Join for Small tables, Hash join for medium tables and Merge-Sort Join for Large tables 

---

## 4. SparkSession & SparkContext  
- **SparkSession**: Entry point for working with structured and semi-structured data.
- **SparkContext**: Lower-level interface for managing resources; now mostly managed by SparkSession.

---

## 5. PySpark Data Formats – Interaction Overview  
PySpark natively supports a wide range of file formats:

### Supported Formats:
- **CSV & JSON**: Standard text-based formats  
- **Parquet & Avro**: Efficient columnar formats. Avro is like JSON with defined schema.  
- **Excel**: Requires extra libraries  
- **Delta Tables**: ACID-compliant, supports schema evolution  
- **SQL Tables**: Interacts with external RDBMSs 

---

## 6. Databricks  
Databricks is a cloud-based platform built on Apache Spark, offering collaborative notebooks, scalable clusters, and ML integration.

### Highlights:
- **Fully Managed Spark**: No setup required  
- **Delta Lake Support**: Enables versioned, reliable data lakes  
- **Built-in ML Tools**: Supports MLflow and AutoML  
- **Interactive Workspaces**: Code in Python, SQL, Scala, R  
- **Multi-cloud Support**: Available on AWS, Azure, and GCP  

---

## 7. Working with Databricks

- **Uploaded CSV files** to Unity Catalog Volumes
- Also **Uploaded CSV files** and registered them as **tables** directly from the UI  
- Performed basic transformations (e.g., filter out cancelled flights)

---

## 8. Use Case: Cluster Planning Example  
To process ~70GB of data efficiently:
- Estimate number of **executors**, **cores**, and **memory per node**
- Use Spark’s caching and partitioning wisely
- Monitor executor logs for shuffle, GC, and storage issue
- After parsing, transformation, shuffling, and caching, it might temporarily expand 2–3x or more.
- So 200GB of disk would be required per node with driver needing 16GB RAM and 4 cores.
- A cluster would need 4 worker nodes each having 48-64 GB RAM, 3 Executors and 12 Cores
