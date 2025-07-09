# Data Warehousing Concepts

## Data Warehouse
- Centralized system for **structured data** and **analytical processing (OLAP)**.
- **Read-heavy**, uses **denormalized structure**, **columnar storage**, and **parallel processing**.
- Enables **data-driven decisions**, tracks **KPIs**, supports BI.
- Tools: Snowflake, Redshift, Teradata, Exadata.

## Data Lake
- Stores **raw structured, semi-structured, unstructured data**.
- **Schema-on-read**, supports ELT, scalable, low-cost.
- Best for **big data, ML, real-time analytics**.

## Data Mart
- Subset of DW, focused on specific department (Sales, HR, etc.).
- Improves **query speed**, **data security**, and **business autonomy**.
- Types: **Dependent** (from DW), **Independent** (from source systems).

## Layers in DW
- **Staging Layer**: Temporary raw data zone.
  - **Persistent**: Retains data.
  - **Non-Persistent**: Discard after processing.
- **User Access Layer**: Cleaned, structured data for querying.

## Transformations (ETL)
- Standardize, clean, deduplicate data.
- Key for consistent, accurate analytics.
- Techniques: value/type unification, null handling, dropping irrelevant fields.

## Loading
- **Initial Load**: One-time, full ingest.
- **Incremental Load**: Periodic updates (Append, SCD1, Truncate).
- Supports **non-volatility** and **data freshness**.

## Slowly Changing Dimensions (SCD)
- Manage changes in dimension data:
  - **Type 0**: No change allowed.
  - **Type 1**: Overwrite current value.
  - **Type 2**: Keep history (new row per change).
  - **Type 3**: Limited history (new column).
  - **Hybrid**: Combination of types for flexibility.

## Fact and Dimension Tables

### Fact Tables
- Store measurable, quantitative data (sales, transactions).
- Linked to multiple dimension tables via foreign keys.
- Categorized as:
  - **Additive**: Can be summed across all dimensions.
  - **Semi-additive**: Summed across some dimensions, not time (e.g., inventory).
  - **Non-additive**: Cannot be summed (e.g., ratios).

### Types of Fact Tables
- **Transaction Fact Table**: Logs individual events (e.g., each sale).
- **Periodic Snapshot Fact Table**: Captures data state at intervals.
- **Accumulating Snapshot Fact Table**: Tracks process lifecycle (e.g., order-to-delivery).

### Factless Fact Table
- Contains no measurable facts.
- Captures event participation (e.g., attendance, promotions).
- Useful for indirect analysis like "what didn't happen?"

## Dimension Tables
- Contain descriptive data related to facts.
- Structured and often manually maintained.
- Can be modeled as:
  - **Star Schema**: Denormalized, easier to query.
  - **Snowflake Schema**: Normalized, supports hierarchies (e.g., product → category → department).

### Types of Dimensions
- **Confirmed Dimension**: Reused across fact tables (e.g., Date).
- **Role-Playing Dimension**: Same table for different roles (e.g., Order Date, Ship Date).
- **Junk Dimension**: Combines miscellaneous low-cardinality attributes.
- **Slowly Changing Dimension (SCD)**: Handles changes in attributes over time.

## Star vs Snowflake Schema
- **Star Schema**: Fast queries, denormalized, more redundancy.
- **Snowflake Schema**: Normalized, more joins, less redundancy.
- Star for performance; Snowflake for data integrity and structure.

## Keys
- **Primary Key**: Uniquely identifies records, no nulls.
- **Foreign Key**: Links to another table’s primary key, allows duplicates.
- **Composite Key**: Multiple columns together ensure uniqueness.
- Enable joins and maintain referential integrity.

## Surrogate Key vs Natural Key
- **Natural Key**: Derived from business data (e.g., product code), can change.
- **Surrogate Key**: System-generated, stable, preferred in data warehouses.
- Surrogate keys simplify joins, enhance performance, and enable historical tracking.

## Change Data Capture (CDC)
- Captures DB changes (insert/update/delete) for downstream sync.
- Enables near real-time data pipelines.
- Captures deletes, which batch methods miss.

### CDC Techniques
- **Metadata-based**: Uses timestamp columns; cannot detect deletes.
- **Diff-based**: Compares source and target; slow and resource-heavy.
- **Trigger-based**: Custom logic; affects performance and maintenance.
- **Log-based**: Reads DB logs (WAL/binlog); efficient and low-latency.

- Limitation: Log-based CDC does not track schema changes (e.g., ALTER, TRUNCATE).
- Best for scalable, real-time, and incremental data movement.

# Linux Practice Log

This captures the commands and tasks practiced today related to basic Linux command-line usage, user management, and SSH setup (tested on WSL2).

---

## Part 1: Basic Linux Commands & Shell Navigation

### Directory Navigation
```bash
pwd                         # Current directory
ls                          # List files
ls -l                       # Long list with permissions
ls -a                       # Show hidden files
cd /etc                     # Go to /etc
cd ~                        # Home directory
cd ..                       # Up one level
```

### File Operations
```bash
touch test.txt              # Create file
cat test.txt                # View file
echo "Hello" > test.txt     # Overwrite file
echo "World" >> test.txt    # Append to file
cp test.txt backup.txt      # Copy file
mv test.txt test1.txt       # Rename file
rm test1.txt                # Delete file
```

### Directory Operations
```bash
mkdir myfolder              # Create directory
rmdir myfolder              # Remove empty dir
rm -r myfolder              # Remove dir with contents
```

### Help & Info
```bash
man ls                      # Manual for command
ls --help                   # Inline help
type ls                     # Show command type
```

---

## Part 2: User Management & sudoers

### View Existing Users
```bash
cut -d: -f1 /etc/passwd
```

### Add Users
```bash
sudo adduser devuser1           # Interactive (recommended)
sudo useradd -m devuser2        # Non-interactive
sudo passwd devuser2            # Set password manually
```

### Login as a User
```bash
su - devuser1
```

### Add Sudo Access
```bash
sudo usermod -aG sudo devuser1
```

### Enable Passwordless Sudo
```bash
echo 'devuser1 ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/devuser1
```

### Delete Users
```bash
sudo deluser --remove-home devuser1   # Delete user and home
sudo deluser devuser2                 # Delete user only
```

---

## Part 3: SSH Setup & Testing

### Install & Enable OpenSSH
```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl status ssh
cat /etc/ssh/sshd_config
```

### Create SSH Test User
```bash
sudo adduser sshuser
sudo usermod -aG sudo sshuser
```

### Test SSH (Local Loopback)
```bash
ssh sshuser@localhost
```

> First-time fingerprint prompt handled  
> Password-based login worked  
> SSH shell confirmed

---
**All tasks successfully tested on Ubuntu 24.04 via WSL2**

