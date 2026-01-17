# Advanced Schema Patterns

## Soft Delete vs Hard Delete

**Soft delete = mark as deleted. Hard delete = remove from database.**

| Factor | Soft Delete | Hard Delete | Audit Table |
|--------|------------|-------------|-------------|
| Audit trail | Preserved | Lost | Preserved |
| Performance | Table bloat, index bloat | Clean | Clean |
| Unique constraints | Breaks (deleted_at workaround) | Works | Works |
| Query complexity | Must filter deleted everywhere | Simple | Simple |
| GDPR "right to erasure" | Problematic | Compliant | Must purge audit |
| Accidental deletion protection | Recoverable | Gone forever | Recoverable |

### Recommended: Audit Table Pattern

```sql
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

-- Benefits:
-- Main table stays clean and fast
-- Full audit trail preserved
-- UNIQUE constraints work
-- GDPR: purge from both tables
-- Queries don't need "WHERE deleted_at IS NULL"
```

### When soft delete acceptable:
- Critical data (financial records)
- Legal retention requirements
- Undo functionality required
- Low deletion rate (< 5%)

### Soft delete implementation (if required):

```sql
-- Use TIMESTAMP not BOOLEAN
deleted_at TIMESTAMP NULL,  -- NULL = active, timestamp = when deleted

-- Unique constraint workaround (PostgreSQL)
CREATE UNIQUE INDEX users_email_unique
ON users(email)
WHERE deleted_at IS NULL;  -- Partial index
```

## Temporal Data (Effective Dating)

**Tracking data validity over time.**

- **Valid time** = when fact is true in real world
- **Transaction time** = when fact recorded in database
- **Bitemporal** = both valid time and transaction time

```sql
-- PATTERN: Temporal table with effective dates
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

**Impact:** Primary keys and unique constraints change. `employee_id` alone isn't unique—must include temporal dimension.

**Modern SQL support:** SQL:2011 added temporal table syntax (PostgreSQL, SQL Server, Oracle).

## JSON Columns: When to Use (and Avoid)

**JSON in relational databases = escape hatch, not default.**

### AVOID JSON for:
- Regularly queried fields
- Sortable/filterable data
- Aggregatable data
- Relational data with defined structure

### JSON ACCEPTABLE for:
- API request/response logs (display only, no queries)
- Sparse metadata (user preferences with 100s of optional keys)
- Semi-structured data from external APIs
- Rapid prototyping (migrate to columns later)

```sql
-- BAD: Using JSON for structured data
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  details JSON  -- {"name": "Widget", "price": 29.99, "category": "Tools"}
);
-- Can't index effectively
-- Can't enforce constraints
-- Queries complex and slow
-- Violates 1NF

-- GOOD: Columns for structured, JSON for sparse
CREATE TABLE products (
  id BIGINT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  category VARCHAR(100) NOT NULL,
  metadata JSON  -- {"custom_attr_1": "value", "custom_attr_2": "value"}
);
```

**Modern databases** (PostgreSQL, MySQL 8+) support JSON indexing and querying, but it's still slower than native columns.
