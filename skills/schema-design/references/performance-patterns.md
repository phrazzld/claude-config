# Schema Performance Patterns

## Indexing Strategy

**"Index for queries, not for every column."**

### Index when:
- Foreign keys (JOIN conditions)
- WHERE clause filters (high selectivity)
- ORDER BY columns
- Columns in GROUP BY

### Don't index:
- Low cardinality (gender with 2 values - wasteful)
- Rarely queried columns
- Columns that change frequently (update cost > query benefit)
- Large TEXT/BLOB columns

### Composite indexes: Column order matters

```sql
CREATE INDEX idx_orders_customer_date ON orders(customer_id, created_at);

-- Uses index:
SELECT * FROM orders WHERE customer_id = 123 AND created_at > '2025-01-01';
SELECT * FROM orders WHERE customer_id = 123;  -- Leftmost prefix

-- Doesn't use index:
SELECT * FROM orders WHERE created_at > '2025-01-01';  -- Not leftmost
```

### Composite index column order:
1. Equality conditions (`WHERE col = value`)
2. Range conditions (`WHERE col > value`)
3. Sort columns (`ORDER BY col`)

## Partitioning

**Split large tables horizontally for performance and maintenance.**

```sql
-- Range partitioning by date
CREATE TABLE events (
  id BIGINT,
  event_type VARCHAR(50),
  created_at TIMESTAMP NOT NULL
)
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Benefits:
-- Queries scan only relevant partitions
-- Drop old partitions (fast delete)
-- Parallel maintenance operations
```

### When to partition:
- Tables > 100GB
- Time-series data (events, logs)
- Archive old data (drop partitions)
- Query patterns match partition key

## Data Type Optimization

**Choose the smallest sufficient data type. Every byte multiplies at scale.**

```sql
-- WASTEFUL:
created_at DATETIME,     -- 8 bytes when DATE (4 bytes) sufficient
status VARCHAR(255),     -- 255 bytes for 'active'/'inactive'
price DOUBLE,            -- Floating point for money (rounding errors!)
user_count BIGINT,       -- 8 bytes for values that fit in INT (4 bytes)

-- OPTIMIZED:
created_date DATE,                     -- 4 bytes (no time needed)
status ENUM('active', 'inactive'),     -- 1-2 bytes + constraint
price DECIMAL(10,2),                   -- Exact arithmetic
user_count INT UNSIGNED,               -- 4 bytes, 0-4B range
```

**At 100M rows:**
- VARCHAR(255) vs VARCHAR(50): **20GB** wasted
- DATETIME vs DATE: **400MB** wasted
- BIGINT vs INT: **400MB** wasted

## Data Type Guidelines

| Use Case | Type | Rationale |
|----------|------|-----------|
| Money | `DECIMAL` | Never FLOAT/DOUBLE (rounding errors) |
| Dates without time | `DATE` | Not DATETIME/TIMESTAMP |
| Small sets | `ENUM` or lookup table | Not VARCHAR |
| Boolean | `BOOLEAN` or `TINYINT(1)` | Not VARCHAR/CHAR |
| Text blobs | `TEXT` types | Consider external storage for >1MB |
