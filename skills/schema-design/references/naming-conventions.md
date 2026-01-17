# Schema Naming Conventions

**Consistency matters more than the specific convention. Pick one, enforce it.**

## Table Names

### Recommended:
- Singular nouns: `user`, `order`, `product` (not `users`, `orders`, `products`)
- Lowercase with underscores: `order_item`, `user_preference`
- Avoid prefixes: `product` not `tbl_product`

### Avoid:
- Plural (`users` vs `user` - inconsistent when singular naturally)
- Reserved words (`order` requires quoting in some DBs - use `orders` or `customer_order`)
- CamelCase (`OrderItem` - portability issues)
- Hungarian notation (`tbl_user`, `user_t`)

## Column Names

### Recommended:
- Descriptive: `created_at`, `email`, `total_price`
- Consistent foreign keys: `user_id` (references `user.id`)
- Boolean prefixes: `is_active`, `has_shipped`, `can_edit`
- Timestamps: `created_at`, `updated_at`, `deleted_at` (not `create_date`, `moddate`)

### Avoid:
- Ambiguous: `data`, `value`, `info`, `text`
- Type suffixes: `email_string`, `count_int`
- Reserved words: `order`, `user`, `table`, `column`

## Index Names

### Pattern:
```sql
-- idx_{table}_{columns}_{type}
idx_users_email_unique
idx_orders_customer_id_created_at
idx_products_category_id
```

## Foreign Key Names

### Pattern:
```sql
-- fk_{table}_{referenced_table}
fk_orders_customers
fk_order_items_orders
fk_order_items_products
```

## Constraint Names

### Pattern:
```sql
-- chk_{table}_{column}_{rule}
chk_users_age_positive
chk_orders_status_valid
chk_products_price_nonnegative
```
