---
name: schema-design
description: "Universal database schema design principles: normalization strategy, data types, primary keys, constraints, anti-patterns, and red flags. Apply when designing schemas, reviewing database architecture, or refactoring data models."
---

# Database Schema Design Principles

You're an IQ 170 database architect who's designed 100+ production databases supporting 1B+ rows. Your schemas have saved $2M by catching design flaws early. Let's bet $2000 your first schema attempt misses critical patterns—explore alternatives, spot red flags, make intentional trade-offs.

## Core Philosophy

**"Schema design debt compounds faster than code debt. Fix it now or pay 10x later."**

A well-designed schema is the foundation for performance, data integrity, scalability, and maintainability. Poor schema design creates cascading problems: slow queries, data corruption, impossibility to refactor, and maintenance nightmares.

## 1. Foundation Principles (Universal)

### Primary Keys: The Non-Negotiable

**Every table MUST have a primary key.**

Real horror story: 200+ tables without primary keys in production. Result: duplicates, broken relationships, catastrophic performance.

**Natural vs Surrogate Keys:**

```sql
❌ BAD: Composite natural key on mutable data
PRIMARY KEY (email, created_date)
-- Email changes break referential integrity
-- Cascading updates across tables
-- Composite foreign keys everywhere

✅ GOOD: Surrogate key + unique constraint
id BIGINT PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
created_date TIMESTAMP NOT NULL
-- Email can change without cascade
-- Simple foreign key references
-- Stable identity
```

**UUID vs Auto-increment Decision Framework:**

| Factor | Auto-increment (INT/BIGINT) | UUID | UUIDv7 (2025+) |
|--------|----------------------------|------|----------------|
| Storage | 4-8 bytes | 16 bytes | 16 bytes |
| Insert performance | Excellent (sequential) | Poor (random I/O) | Good (time-ordered) |
| Index size | Small | Large (4x) | Medium |
| Distributed systems | Requires coordination | Native support | Native support |
| Readability | issue-123 | b1e92c3b-a44a-... | Time-sortable |
| Security | Exposes count/rate | Opaque | Opaque |
| **Verdict** | Default for monoliths | Legacy distributed | **Modern default** |

**Recommendation**:
- Monolithic OLTP → Auto-increment BIGINT
- Distributed systems → UUIDv7
- Legacy distributed → UUIDv4 (migrate to v7)
- Avoid UUIDv1 (insert performance killer)

### Foreign Keys: Enforce Integrity at Database Level

**Use foreign key constraints unless you have a specific reason not to.**

```sql
❌ BAD: Manual referential integrity
CREATE TABLE orders (
  customer_id BIGINT  -- No constraint
);
-- Orphaned records inevitable
-- Data integrity in application code only
-- Silent corruption

✅ GOOD: Database-enforced integrity
CREATE TABLE orders (
  customer_id BIGINT NOT NULL,
  FOREIGN KEY (customer_id)
    REFERENCES customers(id)
    ON DELETE RESTRICT
);
-- Database prevents orphans
-- Referential integrity guaranteed
-- Errors caught immediately
```

**ON DELETE strategies:**
- `RESTRICT` - Prevent deletion (default, safest)
- `CASCADE` - Delete dependents (use sparingly, dangerous)
- `SET NULL` - Null out references (audit trail breaks)
- `NO ACTION` - Like RESTRICT but deferred

**When to skip FKs** (rare):
- High-volume event logging (accepting risk for throughput)
- Temporal data with historical snapshots (integrity at snapshot level)
- Sharded databases where related data spans shards

### Data Types: Precision Matters at Scale

**Choose the smallest sufficient data type. Every byte multiplies at scale.**

```sql
❌ BAD: Wasteful types
created_at DATETIME,     -- 8 bytes when DATE (4 bytes) sufficient
status VARCHAR(255),     -- 255 bytes for 'active'/'inactive'
price DOUBLE,            -- Floating point for money (rounding errors!)
user_count BIGINT,       -- 8 bytes for values that fit in INT (4 bytes)

✅ GOOD: Precise types
created_date DATE,                     -- 4 bytes (no time needed)
status ENUM('active', 'inactive'),     -- 1-2 bytes + constraint
price DECIMAL(10,2),                   -- Exact arithmetic
user_count INT UNSIGNED,               -- 4 bytes, 0-4B range
```

**At 100M rows:**
- VARCHAR(255) vs VARCHAR(50): **20GB** wasted
- DATETIME vs DATE: **400MB** wasted
- BIGINT vs INT: **400MB** wasted

**Data type guidelines:**
- Money → `DECIMAL` (never FLOAT/DOUBLE)
- Dates without time → `DATE` (not DATETIME/TIMESTAMP)
- Small sets → `ENUM` or lookup table (not VARCHAR)
- Boolean → `BOOLEAN` or `TINYINT(1)` (not VARCHAR/CHAR)
- Text blobs → `TEXT` types, consider external storage for >1MB

### Constraints: Data Integrity Guardrails

**Use constraints to prevent bad data at the source.**

```sql
❌ BAD: Hope application validates
CREATE TABLE users (
  email VARCHAR(255),
  age INT,
  status VARCHAR(50)
);
-- NULL emails possible
-- Negative ages possible
-- Typos in status ("activ")

✅ GOOD: Database enforces rules
CREATE TABLE users (
  email VARCHAR(255) NOT NULL UNIQUE,
  age INT CHECK (age >= 0 AND age <= 150),
  status ENUM('active', 'inactive', 'suspended') NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Invalid data rejected at DB level
-- Application bugs caught immediately
-- Data quality guaranteed
```

**Constraint types:**
- `NOT NULL` - Prevent missing required data
- `UNIQUE` - Prevent duplicates
- `CHECK` - Enforce business rules
- `DEFAULT` - Ensure values exist
- `FOREIGN KEY` - Maintain relationships

## 2. Normalization vs Denormalization Decision Framework

### The Golden Rule

**"Start normalized (3NF), selectively denormalize for proven performance needs."**

Premature denormalization is the root of much maintenance evil.

### Normalization Strategy

**1NF (First Normal Form):**
- ✅ Atomic values (no multi-valued fields)
- ✅ No repeating groups

```sql
❌ VIOLATES 1NF: Multi-valued field
CREATE TABLE shipments (
  tags VARCHAR(500)  -- "fragile;overnight;insured"
);
-- Can't query "all shipments with fragile tag"
-- Can't compute per-tag statistics
-- Parsing required for every query

✅ 1NF: Separate table
CREATE TABLE shipments (id BIGINT PRIMARY KEY);
CREATE TABLE shipment_tags (
  shipment_id BIGINT REFERENCES shipments(id),
  tag VARCHAR(50) NOT NULL,
  PRIMARY KEY (shipment_id, tag)
);
-- Tags queryable
-- Referential integrity
-- Clean aggregation
```

**2NF (Second Normal Form):**
- ✅ In 1NF
- ✅ No partial dependencies (all columns depend on entire primary key)

**3NF (Third Normal Form):**
- ✅ In 2NF
- ✅ No transitive dependencies (non-key columns don't depend on other non-key columns)

```sql
❌ VIOLATES 3NF: Transitive dependency
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT,
  customer_city VARCHAR(100),  -- Depends on customer_id, not order_id
  customer_state VARCHAR(2)    -- Transitive dependency
);
-- Update anomaly: Customer moves, must update all orders
-- Data redundancy: City/state duplicated per order

✅ 3NF: Separate entities
CREATE TABLE customers (
  id BIGINT PRIMARY KEY,
  city VARCHAR(100),
  state VARCHAR(2)
);
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT REFERENCES customers(id)
);
-- Single source of truth
-- Update once
-- No redundancy
```

### When to Denormalize

**Denormalization is an optimization. Optimize when you have evidence of a problem.**

✅ **Valid reasons to denormalize:**

1. **Proven query performance issue:**
   ```sql
   -- Before: 5-table join takes 800ms
   -- After: Denormalized user.full_name (first + last) → 10ms
   ```

2. **Read-heavy OLAP/reporting:**
   ```sql
   -- Analytics warehouse with 1000 reads : 1 write
   -- Denormalize for query speed, accept update complexity
   ```

3. **Computed aggregates:**
   ```sql
   -- Frequently accessed: user.order_count
   -- Expensive to compute: SELECT COUNT(*) FROM orders per query
   -- Denormalize: Maintain count column, update on insert/delete
   ```

❌ **Bad reasons to denormalize:**
- "Joins are slow" (without evidence)
- "It's easier to code" (technical debt)
- "We might need it later" (YAGNI violation)

### OLTP vs OLAP Pattern

| System Type | Pattern | Rationale |
|------------|---------|-----------|
| **OLTP** (transactional) | Normalize to 3NF | Data integrity, update efficiency, consistency |
| **OLAP** (analytical) | Denormalize selectively | Query performance, fewer joins, read-optimized |
| **Hybrid** | Normalize OLTP, ETL to denormalized warehouse | Best of both worlds |

## 3. Critical Anti-Patterns & Red Flags

### 🚩 Red Flag #1: EAV (Entity-Attribute-Value) Model

**The EAV pattern trades database advantages for flexibility. You pay dearly.**

```sql
❌ ANTI-PATTERN: EAV "flexible" schema
CREATE TABLE entities (
  id BIGINT PRIMARY KEY,
  entity_type VARCHAR(50)
);
CREATE TABLE attributes (
  entity_id BIGINT,
  attribute_name VARCHAR(100),
  attribute_value TEXT
);
-- Looks "flexible"

-- Reality:
-- ❌ Can't enforce data types (everything is TEXT)
-- ❌ Can't enforce NOT NULL on specific attributes
-- ❌ Can't use CHECK constraints
-- ❌ Queries become nightmares (self-joins for each attribute)
-- ❌ No referential integrity on values
-- ❌ Index strategy nearly impossible

✅ BETTER: Properly modeled schema
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  category_id BIGINT REFERENCES categories(id)
);
-- Strong typing
-- Constraints work
-- Queries readable
-- Indexes effective
```

**When EAV might be acceptable** (very rare):
- Truly unpredictable sparse metadata (user preferences with 1000s of optional keys)
- Combine with JSON column in modern databases (typed EAV alternative)

### 🚩 Red Flag #2: God Tables (Wide Tables)

**Tables with 100+ columns signal design problems.**

Real example: Shipments table with 150+ columns.

```sql
❌ ANTI-PATTERN: God table
CREATE TABLE shipments (
  id BIGINT,
  -- Customer info (should be in customers table)
  customer_name VARCHAR(255),
  customer_email VARCHAR(255),
  customer_phone VARCHAR(50),
  -- Origin address (should be addresses table)
  origin_street VARCHAR(255),
  origin_city VARCHAR(100),
  origin_state VARCHAR(2),
  -- Destination address (duplicate structure!)
  dest_street VARCHAR(255),
  dest_city VARCHAR(100),
  dest_state VARCHAR(2),
  -- ...100+ more columns
);
-- Update anomalies everywhere
-- Massive redundancy
-- Index bloat
-- Query complexity
```

✅ BETTER: Normalized entities
```sql
CREATE TABLE customers (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(50)
);

CREATE TABLE addresses (
  id BIGINT PRIMARY KEY,
  street VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(2) NOT NULL
);

CREATE TABLE shipments (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT REFERENCES customers(id),
  origin_address_id BIGINT REFERENCES addresses(id),
  destination_address_id BIGINT REFERENCES addresses(id),
  status ENUM('pending', 'in_transit', 'delivered'),
  created_at TIMESTAMP NOT NULL
);
-- Single responsibility per table
-- No redundancy
-- Easy to extend
-- Efficient indexes
```

### 🚩 Red Flag #3: Multi-Valued Fields (CSV in Columns)

```sql
❌ ANTI-PATTERN: Delimited values in column
tags VARCHAR(500)  -- "urgent;fragile;international"

-- Problems:
SELECT * FROM shipments WHERE tags LIKE '%fragile%';
-- ❌ Can't index effectively
-- ❌ Matches "non-fragile" (substring match)
-- ❌ Can't compute tag statistics
-- ❌ Can't enforce valid tags

✅ SOLUTION: Junction table
CREATE TABLE tags (
  id BIGINT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE shipment_tags (
  shipment_id BIGINT REFERENCES shipments(id),
  tag_id BIGINT REFERENCES tags(id),
  PRIMARY KEY (shipment_id, tag_id)
);
-- Proper indexing
-- Exact matching
-- Referential integrity
-- Statistics trivial
```

### 🚩 Red Flag #4: Missing Primary Keys

**200+ tables without primary keys found in production database.**

Consequences:
- Duplicate rows (no way to identify unique records)
- Can't use many ORM features
- Foreign key relationships impossible
- Update/delete requires full table scan
- Replication breaks
- Clustering impossible (InnoDB uses PK for clustering)

**Fix immediately. No exceptions.**

### 🚩 Red Flag #5: Over-Normalization

**Too many tiny tables creates join hell.**

```sql
❌ EXCESSIVE: Separate table for currency code
CREATE TABLE currencies (
  id BIGINT PRIMARY KEY,
  code CHAR(3)  -- 'USD', 'EUR', 'GBP'
);
CREATE TABLE prices (
  product_id BIGINT,
  amount DECIMAL(10,2),
  currency_id BIGINT REFERENCES currencies(id)  -- Overkill
);

✅ REASONABLE: ENUM or CHAR(3) with CHECK
CREATE TABLE prices (
  product_id BIGINT PRIMARY KEY,
  amount DECIMAL(10,2) NOT NULL,
  currency_code CHAR(3) NOT NULL CHECK (currency_code IN ('USD', 'EUR', 'GBP'))
);
-- Fewer joins
-- Simpler queries
-- Sufficient constraint
```

**Guideline**: Normalize to avoid redundancy and update anomalies. Don't normalize static reference data with < 100 values if it adds joins without benefit.

### 🚩 Red Flag #6: DATETIME Everywhere

```sql
❌ WASTEFUL: DATETIME for date-only data
birth_date DATETIME,      -- "1990-01-01 00:00:00" (8 bytes)
order_date DATETIME,      -- Time component meaningless

✅ CORRECT: DATE when no time needed
birth_date DATE,          -- "1990-01-01" (4 bytes)
order_date DATE,

-- At 100M rows: 400MB saved
```

**Use TIMESTAMP for event times (created_at, updated_at, logged_at).**

### 🚩 Red Flag #7: SELECT * in Views

```sql
❌ DANGEROUS: Views with SELECT *
CREATE VIEW active_users AS
SELECT * FROM users WHERE status = 'active';

-- Schema evolves: Add password_hash column to users
-- View now exposes passwords!
-- Downstream systems break when columns change

✅ SAFE: Explicit column list
CREATE VIEW active_users AS
SELECT id, email, name, created_at
FROM users
WHERE status = 'active';
-- Schema evolution controlled
-- No unintended exposure
-- Explicit contract
```

## 4. Advanced Patterns & Trade-offs

### Soft Delete vs Hard Delete

**Soft delete = mark as deleted. Hard delete = remove from database.**

| Factor | Soft Delete | Hard Delete | Audit Table |
|--------|------------|-------------|-------------|
| Audit trail | ✅ Preserved | ❌ Lost | ✅ Preserved |
| Performance | ❌ Table bloat, index bloat | ✅ Clean | ✅ Clean |
| Unique constraints | ❌ Breaks (deleted_at workaround) | ✅ Works | ✅ Works |
| Query complexity | ❌ Must filter deleted everywhere | ✅ Simple | ✅ Simple |
| GDPR "right to erasure" | ❌ Problematic | ✅ Compliant | ⚠️ Must purge audit |
| Accidental deletion protection | ✅ Recoverable | ❌ Gone forever | ✅ Recoverable |

**Recommendation:**

```sql
✅ BEST: Audit table pattern
-- Main table: hard deletes
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,  -- UNIQUE works!
  name VARCHAR(255) NOT NULL
);

-- Audit table: captures all changes
CREATE TABLE users_audit (
  audit_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  email VARCHAR(255),
  name VARCHAR(255),
  operation ENUM('INSERT', 'UPDATE', 'DELETE'),
  changed_at TIMESTAMP NOT NULL,
  changed_by BIGINT
);

-- Main table stays clean and fast
-- Full audit trail preserved
-- UNIQUE constraints work
-- GDPR: purge from both tables
-- Queries don't need "WHERE deleted_at IS NULL"
```

**When soft delete acceptable:**
- Critical data (financial records)
- Legal retention requirements
- Undo functionality required
- Low deletion rate (< 5%)

**Soft delete implementation (if required):**
```sql
-- Use TIMESTAMP not BOOLEAN
deleted_at TIMESTAMP NULL,  -- NULL = active, timestamp = when deleted

-- Unique constraint workaround (PostgreSQL)
CREATE UNIQUE INDEX users_email_unique
ON users(email)
WHERE deleted_at IS NULL;  -- Partial index
```

### Temporal Data (Effective Dating)

**Tracking data validity over time.**

**Valid time** = when fact is true in real world
**Transaction time** = when fact recorded in database
**Bitemporal** = both valid time and transaction time

```sql
✅ PATTERN: Temporal table with effective dates
CREATE TABLE employee_salaries (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  employee_id BIGINT NOT NULL REFERENCES employees(id),
  salary DECIMAL(10,2) NOT NULL,
  effective_from DATE NOT NULL,
  effective_to DATE NULL,  -- NULL = current
  created_at TIMESTAMP NOT NULL,  -- Transaction time
  UNIQUE (employee_id, effective_from)
);

-- Query: What's John's salary on 2025-03-15?
SELECT salary
FROM employee_salaries
WHERE employee_id = 123
  AND effective_from <= '2025-03-15'
  AND (effective_to IS NULL OR effective_to > '2025-03-15');

-- Insert new salary (close previous, open new)
UPDATE employee_salaries
SET effective_to = '2025-06-01'
WHERE employee_id = 123 AND effective_to IS NULL;

INSERT INTO employee_salaries
(employee_id, salary, effective_from, effective_to)
VALUES (123, 85000.00, '2025-06-01', NULL);
```

**Impact**: Primary keys and unique constraints change. `employee_id` alone isn't unique—must include temporal dimension.

**Modern SQL support**: SQL:2011 added temporal table syntax (PostgreSQL, SQL Server, Oracle).

### JSON Columns: When to Use (and Avoid)

**JSON in relational databases = escape hatch, not default.**

❌ **AVOID JSON for:**
- Regularly queried fields
- Sortable/filterable data
- Aggregatable data
- Relational data with defined structure

✅ **JSON ACCEPTABLE for:**
- API request/response logs (display only, no queries)
- Sparse metadata (user preferences with 100s of optional keys)
- Semi-structured data from external APIs
- Rapid prototyping (migrate to columns later)

```sql
❌ BAD: Using JSON for structured data
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  details JSON  -- {"name": "Widget", "price": 29.99, "category": "Tools"}
);
-- Can't index effectively
-- Can't enforce constraints
-- Queries complex and slow
-- Violates 1NF

✅ GOOD: Columns for structured, JSON for sparse
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  category VARCHAR(100) NOT NULL,
  metadata JSON  -- {"custom_attr_1": "value", "custom_attr_2": "value"}
);
-- Core data queryable
-- Constraints enforceable
-- Metadata flexible
```

**Modern databases** (PostgreSQL, MySQL 8+) support JSON indexing and querying, but it's still slower than native columns.

## 5. Naming Conventions

**Consistency matters more than the specific convention. Pick one, enforce it.**

### Table Names

✅ **Recommended:**
- Singular nouns: `user`, `order`, `product` (not `users`, `orders`, `products`)
- Lowercase with underscores: `order_item`, `user_preference`
- Avoid prefixes: `product` not `tbl_product`

❌ **Avoid:**
- Plural (`users` vs `user` - inconsistent when singular naturally)
- Reserved words (`order` requires quoting in some DBs - use `orders` or `customer_order`)
- CamelCase (`OrderItem` - portability issues)
- Hungarian notation (`tbl_user`, `user_t`)

### Column Names

✅ **Recommended:**
- Descriptive: `created_at`, `email`, `total_price`
- Consistent foreign keys: `user_id` (references `user.id`)
- Boolean prefixes: `is_active`, `has_shipped`, `can_edit`
- Timestamps: `created_at`, `updated_at`, `deleted_at` (not `create_date`, `moddate`)

❌ **Avoid:**
- Ambiguous: `data`, `value`, `info`, `text`
- Type suffixes: `email_string`, `count_int`
- Reserved words: `order`, `user`, `table`, `column`

### Index Names

✅ **Pattern:**
```sql
-- idx_{table}_{columns}_{type}
idx_users_email_unique
idx_orders_customer_id_created_at
idx_products_category_id
```

## 6. Performance Patterns

### Indexing Strategy

**"Index for queries, not for every column."**

✅ **Index when:**
- Foreign keys (JOIN conditions)
- WHERE clause filters (high selectivity)
- ORDER BY columns
- Columns in GROUP BY

❌ **Don't index:**
- Low cardinality (gender with 2 values - wasteful)
- Rarely queried columns
- Columns that change frequently (update cost > query benefit)
- Large TEXT/BLOB columns

**Composite indexes:** Column order matters.

```sql
CREATE INDEX idx_orders_customer_date ON orders(customer_id, created_at);

-- Uses index:
SELECT * FROM orders WHERE customer_id = 123 AND created_at > '2025-01-01';
SELECT * FROM orders WHERE customer_id = 123;  -- Leftmost prefix

-- Doesn't use index:
SELECT * FROM orders WHERE created_at > '2025-01-01';  -- Not leftmost
```

**Guideline:** Order composite index columns by:
1. Equality conditions (`WHERE col = value`)
2. Range conditions (`WHERE col > value`)
3. Sort columns (`ORDER BY col`)

### Partitioning

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
-- - Queries scan only relevant partitions
-- - Drop old partitions (fast delete)
-- - Parallel maintenance operations
```

**When to partition:**
- Tables > 100GB
- Time-series data (events, logs)
- Archive old data (drop partitions)
- Query patterns match partition key

## 7. Quality Checklist

**Schema review checklist - run before deployment:**

### Structural Integrity
- [ ] Every table has a primary key
- [ ] Foreign key constraints defined and enforced
- [ ] Appropriate data types (smallest sufficient)
- [ ] NOT NULL on required columns
- [ ] UNIQUE constraints on natural keys
- [ ] CHECK constraints on business rules
- [ ] DEFAULT values where appropriate

### Normalization
- [ ] No multi-valued fields (violates 1NF)
- [ ] No partial dependencies (violates 2NF)
- [ ] No transitive dependencies (violates 3NF)
- [ ] Denormalization documented with rationale

### Anti-Pattern Scan
- [ ] No EAV (entity-attribute-value) patterns
- [ ] No god tables (> 50 columns triggers review)
- [ ] No missing primary keys
- [ ] No TEXT fields for structured data
- [ ] No DATETIME for date-only data

### Performance
- [ ] Indexes match query patterns
- [ ] Foreign keys indexed
- [ ] Composite index column order optimized
- [ ] No over-indexing (< 5 indexes per table guideline)
- [ ] Partitioning strategy for large tables (> 100GB)

### Naming & Documentation
- [ ] Consistent naming convention
- [ ] No reserved words without quoting
- [ ] No ambiguous names (`data`, `info`, `value`)
- [ ] Schema documentation exists
- [ ] Migration scripts in version control

### Temporal & Deletion Strategy
- [ ] Delete strategy chosen (soft/hard/audit)
- [ ] Temporal needs identified (effective dating)
- [ ] GDPR compliance considered

### Security & Compliance
- [ ] Sensitive data identified
- [ ] Encryption strategy defined
- [ ] Audit requirements met
- [ ] Data retention policy implemented

## 8. Decision Trees

### "Should I add this column?"

```
Is this data about the entity?
├─ YES → Add to table
└─ NO → Does it describe a related entity?
   ├─ YES → Create/use related table
   └─ NO → Reconsider if needed
```

### "Should I denormalize this?"

```
Do I have evidence of a query performance problem?
├─ NO → DON'T denormalize (premature optimization)
└─ YES → Have I tried indexes, query optimization, caching?
   ├─ NO → Try those first
   └─ YES → Is this read-heavy (> 100:1 read:write)?
      ├─ NO → Normalize, optimize queries
      └─ YES → Denormalize specific fields, maintain with triggers
```

### "UUID or auto-increment?"

```
Distributed system (multiple write nodes)?
├─ YES → UUID (prefer UUIDv7 for performance)
└─ NO → Exposed to users (issue-123 vs issue-uuid)?
   ├─ YES → Auto-increment (better UX)
   └─ NO → Auto-increment (better performance)
```

### "Soft or hard delete?"

```
GDPR "right to erasure" applies?
├─ YES → Hard delete or audit table (can purge audit)
└─ NO → Need audit trail?
   ├─ YES → Audit table pattern (best of both)
   └─ NO → High deletion rate (> 20%)?
      ├─ YES → Hard delete (avoid bloat)
      └─ NO → Soft delete acceptable
```

## Remember

**"A schema optimized for what you're building today becomes tomorrow's technical debt if you don't consider how it will evolve."**

Design schemas that:
1. **Enforce integrity** - Constraints, foreign keys, data types
2. **Optimize for common patterns** - Indexes, denormalization where proven
3. **Enable evolution** - Proper normalization, migration strategy
4. **Prevent known anti-patterns** - No EAV, god tables, multi-valued fields

**The best schema is one you can understand in 6 months and modify with confidence.**
