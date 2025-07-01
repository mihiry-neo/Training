# Apache Spark Concepts -  Day18 - 30/6/25

## Introduction

- **Spark** is a fast, distributed computing engine for large-scale data processing.
- Common **Hadoop Misconceptions**:
  - Hadoop is *not* a database.
  - Spark isn't just 100x faster—it's optimized for *in-memory* and *streaming* use cases.
  - Hadoop relies on disk; Spark mostly uses memory.

---

## Spark vs Hadoop

| Aspect | Hadoop | Spark |
|-------|--------|-------|
| Processing | Batch-only | Batch + Streaming |
| I/O | Disk-based | In-memory |
| Language | Complex (MapReduce, HiveQL) | Easy (Scala, Python, SQL) |
| Security | Kerberos, ACL | Depends on underlying HDFS/YARN |
| Fault Tolerance | Replication (HDFS blocks) | DAG lineage recovery |

---

## Spark Ecosystem

- **High-Level APIs**: DataFrames, Spark SQL, MLlib, GraphX, Streaming.
- **Low-Level APIs**: RDDs via Scala, Python, Java.
- **Execution Flow**: APIs → Spark Engine → Cluster Manager → Worker Nodes.

---

## Spark Architecture

- Master-Slave architecture.
- Spark driver (JVM) coordinates tasks and talks to executors.
- In PySpark, Python Driver talks to JVM Driver ⇒ Overhead risk with UDFs.

---

## Transformations & Actions

- **Transformations**: Lazy ops like `map`, `filter`. Can be:
  - Narrow (no shuffling)
  - Wide (requires shuffling)
- **Actions**: `count()`, `collect()` → triggers execution and brings data to driver.

---

## DAG & Lazy Evaluation

- Spark builds a **DAG** of transformations.
- Optimized using the **Catalyst Optimizer** (pushdowns, constant folding).
- Execution only starts on an **Action**.

---

## Spark SQL & Catalyst Optimizer

- **4 Phases**:
  1. Analysis (Metadata via Catalog)
  2. Logical Optimization
  3. Physical Planning
  4. Code Generation (Bytecode)
- Errors like `AnalysisException` happen in the Analysis phase.

---

## Joins in Spark

- **Shuffle Hash Join** (default): Shuffle → Hash table → Merge.
- **Sort-Merge Join**: Sort both sides, then merge.
- **Broadcast Join**: Small table sent to all executors to avoid shuffle.
  - Default limit: `10MB` (`spark.sql.autoBroadcastJoinThreshold`)
- **Cartesian Join** & **Broadcast Nested Loop Join** also available.

---

## SparkSession vs SparkContext

- Use **SparkSession** in modern apps—it includes `SparkContext`, `SQLContext`, `HiveContext`.

---

## Partitioning

- **Repartition(n)**: Evenly reshuffles data across `n` partitions.
- **Coalesce(n)**: Reduces partitions by unevenly merging.
- **spark.sql.shuffle.partitions**: Controls number of partitions post-shuffle (default: 200).

---

## Jobs, Stages, Tasks

- Each **Action** = Job
- Job → Stages (based on wide transformations) → Tasks (run on executors)

---

## OOM Error in Driver

- `collect()` and `show()` may cause **DriverOutOfMemory**.
- `spark.driver.memory` vs `spark.driver.memoryOverhead`

---

## OOM Error in Executor

**Understanding Executor Out of Memory Exceptions**  
- Out of Memory exceptions can occur in Spark even when data processing appears feasible, mainly due to insufficient storage capacity.  
- Executors handle multiple tasks, and if the combined data exceeds the configured memory limits, exceptions arise.  

**Memory Management in Spark**  
- Spark uses two types of memory management: Static and Unified.  
- Unified memory manager allows dynamic allocation between storage and execution memory.  

**Executor Memory Configuration**  
- Executors have a fixed memory limit (e.g., 10GB), plus overhead memory (around 10%).  
- Excessive data processing or concurrent tasks can exceed these limits, causing failure.  

**Factors Leading to Exceptions**  
- Large joins, aggregations, or data spills.  
- Overloaded executors.  

**Strategies for Optimal Memory Use**  
- Partitioning, caching, and monitoring memory usage.  
- Tuning executor memory and retrying failed tasks.

---

## Cache and Persist in PySpark

**Caching in Spark**  
- Stores intermediate results in memory to avoid recomputation.  
- Best used for iterative or multi-action workflows.

**Persisting in Spark**  
- Same as caching, but allows custom storage levels: MEMORY_ONLY, DISK_ONLY, etc.  
- Used when data is too large for memory or needed in multiple stages.

**Differences**  
- `cache()` = `persist()` with MEMORY_AND_DISK  
- `persist()` = flexible

**Memory and Eviction**  
- Cached data may be evicted if memory fills.  
- Monitor memory carefully.

---

## Dynamic Resource Allocation

**Overview**  
- Adjusts executors based on workload.  
- Optimizes cluster usage and reduces idle time.

**Key Concepts**  
- Executors added/removed dynamically.  
- Requires `spark.dynamicAllocation.enabled = true`.  

**Challenges**  
- Idle executor delays.  
- Resource contention and tuning complexity.

**When to Avoid**  
- For production or predictable loads, static allocation is better.

**Effective Configuration**  
- Set min/max executors, timeout settings, enable Spark listener for tracking.

---

## Dynamic Partition Pruning

**Introduction**  
- DPP improves performance by skipping irrelevant partitions at runtime.  
- Effective during joins with partitioned tables.

**How It Works**  
- Filters are applied dynamically based on join keys.  
- Enabled by default in Spark 3.0+.

**When It Works Best**  
- One table partitioned, one small enough to broadcast.  
- Both sides must support DPP for optimal effect.

**Use Cases**  
- ETL and analytical jobs with large fact tables and partition filters.

---

## Salting in Spark

**Understanding Skewness**  
- Data skew happens when one key gets too much data (e.g., single ID dominating join).

**How to Fix with Salting**  
- Add a random suffix to keys (e.g., `user_1`, `user_2`)  
- Join using salted keys on both sides.

**Post-Processing**  
- After join, de-salt by removing randomness if needed.

**When to Use**  
- Severe skew causing one partition to lag or fail.

**Pros & Cons**  
- Reduces execution time but adds complexity.  
- Requires changes to logic and additional columns.

---

## Storage Formats

- **Parquet**:
  - Uses **row groups**, **columnar storage**, and **metadata** for efficient read.
- **Avro**:
  - Compact, row-based format, useful for data serialization.

---

## Broadcast vs Accumulator Variables

- **Broadcast Variables**: Read-only, shared across executors to avoid repeated data shipping.
- **Accumulator Variables**: Write-only (from executors), used for aggregation/logging.

---

## HDFS Replication Strategy

With replication factor = 3:
- Block 1 → local rack,
- Block 2 → same rack, different node,
- Block 3 → different rack.


## Netflix Data

- Started working with Netflix data consisting of credits.csv and titles.csv