# Schema Design & Migrations

## Convex Auto-Migrates (No Manual Migrations)

Schema changes are immediate in dev, require push in prod. No SQL migration files needed.

## The "Expand and Contract" Pattern

**Use for any breaking schema change** (renaming, type changes, removing fields).

**Four Phases**: Expand → Migrate → Contract → Cleanup

### Example: Renaming `name` to `fullName`

**Phase 1: Expand** — Add new field as optional, dual write
```typescript
// schema.ts - Step 1
defineTable({
  name: v.string(),
  fullName: v.optional(v.string()), // NEW - optional
});

// mutation.ts - Step 1
export const createUser = internalMutation({
  args: { name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("users", {
      name: args.name,
      fullName: args.name, // Write to both
    });
  },
});
```

**Phase 2: Migrate** — Backfill existing records
```typescript
// convex/migrations.ts
export const backfillFullNames = internalAction({
  handler: async (ctx) => {
    const users = await ctx.runQuery(internal.users.listAll);
    for (const user of users) {
      if (!user.fullName) {
        await ctx.runMutation(internal.users.patch, {
          userId: user._id,
          fullName: user.name,
        });
      }
    }
  },
});

// For large datasets, use Convex Migration Component
```

**Phase 3: Contract** — Switch reads to new field, stop writing to old field
```typescript
// Read from fullName only
export const getUser = query({
  handler: async (ctx, { userId }) => {
    const user = await ctx.db.get(userId);
    return { name: user.fullName }; // Read from new field
  },
});

// Stop dual-writing (remove name from inserts)
```

**Phase 4: Cleanup** — Remove old field from schema
```typescript
// schema.ts - Final
defineTable({
  fullName: v.string(), // Only new field remains
});

// May need migration to unset old field if Convex blocks removal
```

## Migration Best Practices

✅ **Safe patterns**:
- Add optional fields first
- Backfill via internal actions
- Test in dev/preview before prod
- Use `v.optional()` for backward compatibility
- Use Convex Migration Component for large datasets (>10k docs)

❌ **Dangerous patterns**:
- Removing fields before code updated
- Changing field types without migration
- Breaking changes without deprecation period
- Testing migrations directly in production
- No rollback strategy

## Staged Rollout for Large Tables

When backfilling large tables (>100k documents), use staged approach:

1. Deploy schema with optional field
2. Run backfill migration in background (may take hours)
3. Monitor completion in dashboard
4. Deploy code changes to read from new field
5. Remove old field after grace period

## Environment Management

### Deployment Flow: Dev → Preview → Prod

```
Local dev (convex dev)
  → Push to branch (preview deployment)
    → Merge to main (production deployment)
```

### Environment-Specific Patterns

**Local development**:
```bash
convex dev  # Hot reload, separate backend
```

**Preview deployments** (automatic per branch):
```bash
git push origin feature-branch
# Preview deployment auto-created
# Test migrations, features in isolation
```

**Production**:
```bash
git merge to main
# Auto-deploys to production
```

### Environment Variables

Use dashboard for configuration (not `.env` files in `convex/`).

✅ **Best practice**:
```typescript
export const sendEmail = action({
  handler: async (ctx, { to, subject, body }) => {
    const apiKey = process.env.SENDGRID_API_KEY; // ✅ From dashboard
    await sendEmail({ apiKey, to, subject, body });
  },
});
```

❌ **Anti-pattern**:
```typescript
const apiKey = "sk-..."; // ❌ Hardcoded!
```

## Migration Checklist

- [ ] Changes are additive (new fields optional with `v.optional()`)
- [ ] "Expand and Contract" pattern planned
- [ ] Backfill strategy defined (internal action)
- [ ] Tested in dev environment first
- [ ] Tested in preview environment
- [ ] Rollback plan defined
- [ ] Breaking changes have deprecation period
- [ ] Use Convex Migration Component for large datasets
