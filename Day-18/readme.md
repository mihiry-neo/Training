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