# Day-06 - 12/6/25

## Data Engineering Terminologies Learned

### 1. Data Types & Sources

**Structured Data**
- Learned: Tabular data organized in rows and columns
- Examples: SQL databases, Excel spreadsheets

**Semi-Structured Data**
- Learned: Data with some organizational structure but flexible schema
- Formats: JSON, XML, Avro, Parquet

**Unstructured Data**
- Learned: Data without predefined structure
- Examples: Text files, images, videos, log files

**Data Lake vs Data Warehouse**
- **Data Lake**: Centralized repository storing raw data in native format
  - Supports all data types (structured, semi-structured, unstructured)
  - Schema-on-read approach
- **Data Warehouse**: Optimized for structured, processed, queryable data
  - Schema-on-write approach
  - Better performance for analytics

**OLTP vs OLAP**
- **OLTP (Online Transaction Processing)**: Handles day-to-day operational transactions
  - Fast, simple queries
  - High concurrency
- **OLAP (Online Analytical Processing)**: Supports complex analytical queries
  - Complex aggregations
  - Historical data analysis

### 2. Data Processing Approaches

**ETL vs ELT**
- **ETL (Extract, Transform, Load)**: Traditional approach
  - Transform data before loading
  - Better for structured data
- **ELT (Extract, Load, Transform)**: Modern cloud approach
  - Load raw data first, transform later
  - Leverages cloud computing power

**Batch vs Stream Processing**
- **Batch Processing**: Processes data in large chunks at scheduled intervals
  - Tools: Apache Spark, Hadoop MapReduce
  - Better for large volumes, non-time-sensitive data
- **Stream Processing**: Real-time data processing
  - Tools: Apache Kafka, Apache Flink
  - Better for time-sensitive applications

**Data Ingestion & Orchestration**
- **Data Ingestion**: Process of pulling data from various sources
- **Data Orchestration**: Managing workflows and scheduling
  - Tool: Apache Airflow

### 3. Storage & Formats

**Columnar vs Row-based Storage**
- **Columnar**: Stores data by columns (Parquet, ORC)
  - Better for analytics and aggregations
  - Higher compression ratios
- **Row-based**: Stores data by rows (CSV, JSON)
  - Better for transactional operations

**Distributed Storage**
- **Distributed File System**: HDFS, Amazon S3, Azure Blob
- **Data Partitioning**: Dividing data for parallel processing
- **Data Sharding**: Splitting databases to improve performance

### 4. Query Engines & Cloud Services

**Key Query Engines Learned:**
- **Presto/Trino**: Distributed SQL query engine
- **Hive**: Data warehouse system on Hadoop
- **BigQuery, Athena, Dremio**: Serverless query engines

**Cloud Services:**
- **ETL Tools**: AWS Glue, Azure Data Factory, Google Dataflow
- **Data Warehouses**: Redshift, Snowflake, BigQuery, Synapse
- **Lakehouse**: Databricks Delta Lake (combines lake + warehouse benefits)

### 5. Data Governance & Quality

**Key Concepts:**
- **Data Catalog**: Metadata repository for data discovery
- **Data Lineage**: Tracking data origin and transformation flow
- **Data Profiling**: Understanding data characteristics and patterns
- **Data Quality**: Ensuring validity, accuracy, completeness, and timeliness
- **Schema Evolution**: Managing changes in data structure over time

---

## Data Engineering Architectures Understood

### 1. Traditional ETL Architecture
**Learning**: Sequential processing, data transformed before storage

### 2. Modern ELT Architecture
**Learning**: Leverages cloud computing power for transformation

### 3. Lambda Architecture
**Learning**: Combines batch and real-time processing for comprehensive data handling

### 4. Kappa Architecture
**Learning**: Purely stream-based, simpler than Lambda but requires all data as streams

### 5. Data Lakehouse Architecture
**Learning**: Best of both worlds - flexibility of lakes with performance of warehouses

### 6. Event-Driven Architecture
**Learning**: Based on event triggers, often uses Kafka for real-time responsiveness

---

## 🐘 Deep Dive: Hadoop Ecosystem

### What is Hadoop & How Does It Work?

**Hadoop Overview:**
- Open-source framework for distributed storage and processing of big data
- Designed to scale from single servers to thousands of machines
- Built on the principle of bringing computation to data rather than data to computation

**Core Components:**
1. **HDFS (Hadoop Distributed File System)**
   - Distributed file storage across multiple machines
   - Fault-tolerant through data replication
   - Optimized for large files and sequential access

2. **YARN (Yet Another Resource Negotiator)**
   - Resource management and job scheduling
   - Manages cluster resources and application lifecycle

3. **MapReduce**
   - Programming model for processing large datasets
   - Splits work into smaller tasks across multiple nodes

**How Hadoop Works:**
1. Data is split into blocks (typically 128MB or 256MB)
2. Blocks are distributed across multiple nodes in the cluster
3. Each block is replicated (default: 3 copies) for fault tolerance
4. Processing happens on nodes where data resides
5. Results are aggregated and returned

### MapReduce: Processing Large Amounts of Data

**MapReduce Concept:**
- Programming paradigm for processing large datasets in parallel
- Divides work into two phases: Map and Reduce

**How MapReduce Works:**

1. **Input Split**: Large dataset divided into smaller chunks
2. **Map Phase**: 
   - Each chunk processed independently by mapper functions
   - Produces key-value pairs as intermediate output
3. **Shuffle & Sort**: 
   - Intermediate data grouped by keys
   - Data moved to appropriate reducers
4. **Reduce Phase**: 
   - Aggregates intermediate results by key
   - Produces final output

**Example Process (Word Count):**
```
Input: "Hello World Hello"
Map: (Hello,1), (World,1), (Hello,1)
Shuffle: Group by key → Hello:[1,1], World:[1]
Reduce: Hello:2, World:1
```

**Key Benefits of MapReduce:**
- Automatic parallelization and distribution
- Fault tolerance through task re-execution
- Data locality optimization
- Scalability across thousands of nodes

### Why Spark is Better Than MapReduce

**Problems with MapReduce:**

1. **Disk I/O Intensive**: 
   - Writes intermediate results to disk after each Map phase
   - Slow due to frequent disk reads/writes

2. **Not Suitable for Iterative Algorithms**:
   - Machine learning algorithms require multiple passes
   - Each iteration requires full data reload from disk

3. **Complex Programming Model**:
   - Everything must fit into Map-Reduce paradigm
   - Difficult to express complex multi-step algorithms

4. **Batch Processing Only**:
   - No support for real-time or interactive processing
   - High latency for results

5. **Limited Caching**:
   - No way to keep frequently accessed data in memory
   - Repeated disk access for commonly used datasets

**How Spark Solves These Problems:**

1. **In-Memory Computing**:
   - Keeps data in RAM between operations
   - 100x faster for iterative algorithms
   - Significantly reduces I/O overhead

2. **Rich API and Abstractions**:
   - RDDs (Resilient Distributed Datasets)
   - DataFrames and Datasets for structured data
   - Multiple programming languages support (Scala, Python, Java, R)

3. **Multiple Processing Models**:
   - Batch processing (like MapReduce)
   - Real-time streaming (Spark Streaming)
   - Interactive queries (Spark SQL)
   - Machine learning (MLlib)
   - Graph processing (GraphX)

4. **Optimized Execution Engine**:
   - Catalyst optimizer for SQL queries
   - Tungsten execution engine for performance
   - Lazy evaluation and query optimization

5. **Better Fault Tolerance**:
   - RDD lineage for recovery
   - Checkpointing for long-running applications

6. **Easier Development**:
   - More intuitive APIs
   - Interactive shells for development
   - Better debugging and monitoring tools

**Performance Comparison:**
- **Spark**: In-memory processing, suitable for iterative workloads
- **MapReduce**: Disk-based processing, better for simple batch ETL jobs
