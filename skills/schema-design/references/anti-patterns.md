# Schema Anti-Patterns & Red Flags

## Red Flag #1: EAV (Entity-Attribute-Value) Model

**The EAV pattern trades database advantages for flexibility. You pay dearly.**

```sql
-- ANTI-PATTERN: EAV "flexible" schema
CREATE TABLE entities (
  id BIGINT PRIMARY KEY,
  entity_type VARCHAR(50)
);
CREATE TABLE attributes (
  entity_id BIGINT,
  attribute_name VARCHAR(100),
  attribute_value TEXT
);

-- Reality:
-- Can't enforce data types (everything is TEXT)
-- Can't enforce NOT NULL on specific attributes
-- Can't use CHECK constraints
-- Queries become nightmares (self-joins for each attribute)
-- No referential integrity on values
-- Index strategy nearly impossible

-- BETTER: Properly modeled schema
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  category_id BIGINT REFERENCES categories(id)
);
```

**When EAV might be acceptable** (very rare):
- Truly unpredictable sparse metadata (user preferences with 1000s of optional keys)
- Combine with JSON column in modern databases (typed EAV alternative)

## Red Flag #2: God Tables (Wide Tables)

**Tables with 100+ columns signal design problems.**

```sql
-- ANTI-PATTERN: God table
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

-- BETTER: Normalized entities
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
```

## Red Flag #3: Multi-Valued Fields (CSV in Columns)

```sql
-- ANTI-PATTERN: Delimited values in column
tags VARCHAR(500)  -- "urgent;fragile;international"

-- Problems:
SELECT * FROM shipments WHERE tags LIKE '%fragile%';
-- Can't index effectively
-- Matches "non-fragile" (substring match)
-- Can't compute tag statistics
-- Can't enforce valid tags

-- SOLUTION: Junction table
CREATE TABLE tags (
  id BIGINT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE shipment_tags (
  shipment_id BIGINT REFERENCES shipments(id),
  tag_id BIGINT REFERENCES tags(id),
  PRIMARY KEY (shipment_id, tag_id)
);
```

## Red Flag #4: Missing Primary Keys

**200+ tables without primary keys found in production database.**

Consequences:
- Duplicate rows (no way to identify unique records)
- Can't use many ORM features
- Foreign key relationships impossible
- Update/delete requires full table scan
- Replication breaks
- Clustering impossible (InnoDB uses PK for clustering)

**Fix immediately. No exceptions.**

## Red Flag #5: Over-Normalization

**Too many tiny tables creates join hell.**

```sql
-- EXCESSIVE: Separate table for currency code
CREATE TABLE currencies (
  id BIGINT PRIMARY KEY,
  code CHAR(3)  -- 'USD', 'EUR', 'GBP'
);
CREATE TABLE prices (
  product_id BIGINT,
  amount DECIMAL(10,2),
  currency_id BIGINT REFERENCES currencies(id)  -- Overkill
);

-- REASONABLE: ENUM or CHAR(3) with CHECK
CREATE TABLE prices (
  product_id BIGINT PRIMARY KEY,
  amount DECIMAL(10,2) NOT NULL,
  currency_code CHAR(3) NOT NULL CHECK (currency_code IN ('USD', 'EUR', 'GBP'))
);
```

**Guideline:** Normalize to avoid redundancy and update anomalies. Don't normalize static reference data with < 100 values if it adds joins without benefit.

## Red Flag #6: DATETIME Everywhere

```sql
-- WASTEFUL: DATETIME for date-only data
birth_date DATETIME,      -- "1990-01-01 00:00:00" (8 bytes)
order_date DATETIME,      -- Time component meaningless

-- CORRECT: DATE when no time needed
birth_date DATE,          -- "1990-01-01" (4 bytes)
order_date DATE,

-- At 100M rows: 400MB saved
```

**Use TIMESTAMP for event times (created_at, updated_at, logged_at).**

## Red Flag #7: SELECT * in Views

```sql
-- DANGEROUS: Views with SELECT *
CREATE VIEW active_users AS
SELECT * FROM users WHERE status = 'active';

-- Schema evolves: Add password_hash column to users
-- View now exposes passwords!
-- Downstream systems break when columns change

-- SAFE: Explicit column list
CREATE VIEW active_users AS
SELECT id, email, name, created_at
FROM users
WHERE status = 'active';
```
