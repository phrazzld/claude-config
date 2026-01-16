# Audit Logging

Immutable, complete, queryable records of all data changes.

## Schema

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    user_id UUID NOT NULL,
    operation VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    request_id UUID,
    ip_address INET,

    -- Prevent modification
    CONSTRAINT no_update CHECK (false)
);

-- Prevent updates and deletes
CREATE RULE audit_no_update AS ON UPDATE TO audit_log DO INSTEAD NOTHING;
CREATE RULE audit_no_delete AS ON DELETE TO audit_log DO INSTEAD NOTHING;

-- Query indices
CREATE INDEX idx_audit_user ON audit_log (user_id, timestamp);
CREATE INDEX idx_audit_table ON audit_log (table_name, record_id);
```

## Trigger Pattern

```sql
CREATE OR REPLACE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (
        user_id, operation, table_name, record_id,
        old_values, new_values, changed_fields
    ) VALUES (
        current_setting('app.user_id')::uuid,
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP != 'INSERT' THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP != 'DELETE' THEN to_jsonb(NEW) END,
        CASE WHEN TG_OP = 'UPDATE' THEN
            array_agg(key) FROM jsonb_each(to_jsonb(NEW))
            WHERE to_jsonb(NEW)->key != to_jsonb(OLD)->key
        END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger();
```

## Application Context

```python
# Set user context before operations
await db.execute("SET LOCAL app.user_id = $1", user_id)
await db.execute("SET LOCAL app.request_id = $1", request_id)
```

## Compliance Queries

```sql
-- User's data access history
SELECT * FROM audit_log
WHERE user_id = $1
ORDER BY timestamp DESC;

-- Changes to specific record
SELECT * FROM audit_log
WHERE table_name = 'users' AND record_id = $1
ORDER BY timestamp;
```
