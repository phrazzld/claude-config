# Normalization vs Denormalization

## The Golden Rule

**"Start normalized (3NF), selectively denormalize for proven performance needs."**

Premature denormalization is the root of much maintenance evil.

## Normalization Strategy

### 1NF (First Normal Form)

- Atomic values (no multi-valued fields)
- No repeating groups

```sql
-- VIOLATES 1NF: Multi-valued field
CREATE TABLE shipments (
  tags VARCHAR(500)  -- "fragile;overnight;insured"
);
-- Can't query "all shipments with fragile tag"
-- Can't compute per-tag statistics
-- Parsing required for every query

-- 1NF: Separate table
CREATE TABLE shipments (id BIGINT PRIMARY KEY);
CREATE TABLE shipment_tags (
  shipment_id BIGINT REFERENCES shipments(id),
  tag VARCHAR(50) NOT NULL,
  PRIMARY KEY (shipment_id, tag)
);
```

### 2NF (Second Normal Form)

- In 1NF
- No partial dependencies (all columns depend on entire primary key)

### 3NF (Third Normal Form)

- In 2NF
- No transitive dependencies (non-key columns don't depend on other non-key columns)

```sql
-- VIOLATES 3NF: Transitive dependency
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT,
  customer_city VARCHAR(100),  -- Depends on customer_id, not order_id
  customer_state VARCHAR(2)    -- Transitive dependency
);
-- Update anomaly: Customer moves, must update all orders
-- Data redundancy: City/state duplicated per order

-- 3NF: Separate entities
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

## When to Denormalize

**Denormalization is an optimization. Optimize when you have evidence of a problem.**

### Valid reasons to denormalize:

1. **Proven query performance issue:**
   ```sql
   -- Before: 5-table join takes 800ms
   -- After: Denormalized user.full_name (first + last) -> 10ms
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

### Bad reasons to denormalize:
- "Joins are slow" (without evidence)
- "It's easier to code" (technical debt)
- "We might need it later" (YAGNI violation)

## OLTP vs OLAP Pattern

| System Type | Pattern | Rationale |
|------------|---------|-----------|
| **OLTP** (transactional) | Normalize to 3NF | Data integrity, update efficiency, consistency |
| **OLAP** (analytical) | Denormalize selectively | Query performance, fewer joins, read-optimized |
| **Hybrid** | Normalize OLTP, ETL to denormalized warehouse | Best of both worlds |
