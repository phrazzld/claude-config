# CI Failure Analysis & Resolution Plan - Round 3

## Current Status

| Check | Status | Issue |
|-------|--------|-------|
| **drift** | ❌ Expected | Production DB has unapplied migrations (legitimate drift) |
| **test** | ❌ 1/781 | Flaky concurrency test |

---

## Failure 1: Drift Check - Expected Behavior

The drift check is now **working correctly**. It points to production (`ep-broad-credit-adnne0ox-pooler`) and reports 4 unapplied migrations.

**This is legitimate drift** - the schema in code is ahead of production. This is expected for a feature branch.

**Options:**
1. **Skip drift check for PRs** - Only run on `master` branch pushes
2. **Allow drift on feature branches** - Add `|| exit 0` for non-master
3. **Accept current behavior** - Drift check exists to catch real issues

**Recommendation**: Modify workflow to only fail on master, warn on PRs.

---

## Failure 2: Test - Flaky Concurrency Test

### Classification
**Flaky Test** - Race condition in concurrent sync test.

### Evidence
```
Error Handling > should handle concurrent sync attempts gracefully
expected false to be true // Object.is equality

Unique constraint failed on the fields: (`id`)
```

### Root Cause
The test runs 3 concurrent `syncUser` calls:
```typescript
await Promise.allSettled([
  syncUser(newUserId, testEmail),
  syncUser(newUserId, testEmail),
  syncUser(newUserId, testEmail),
]);
// Expects all to fulfill
```

But `syncUser` in `lib/db.ts:81-106` has a race condition:
1. `findUnique` returns null for all 3 (no user exists yet)
2. All 3 reach line 176: `prisma.user.create({ id: clerkUserId })`
3. First wins, others get P2002 unique constraint error

### Fix Options

**Option A: Fix the test** - Acknowledge the race condition is expected behavior
```typescript
// At least one succeeds
expect(results.filter((r) => r.status === 'fulfilled').length).toBeGreaterThanOrEqual(1);
```

**Option B: Fix the implementation** - Make `syncUser` truly idempotent with upsert or retry
```typescript
// Instead of findUnique + create, use upsert
return await prisma.user.upsert({
  where: { id: clerkUserId },
  update: { email },
  create: { id: clerkUserId, email },
});
```

**Option C: Catch unique constraint error** - Retry on conflict
```typescript
try {
  // existing logic
} catch (e) {
  if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002') {
    // Race condition: another request created the user, fetch and return
    return await prisma.user.findUniqueOrThrow({ where: { id: clerkUserId } });
  }
  throw e;
}
```

**Recommendation**: Option B (upsert) - Cleaner, truly idempotent, no race conditions.

---

## Files to Modify

1. **`.github/workflows/db-drift-check.yml`** - Only fail on master branch
2. **`lib/db.ts`** - Use upsert for simple user sync case (lines 92-106)

---

## Implementation Details

### 1. db-drift-check.yml - Warn on PRs, fail on master

```yaml
- name: Load prod DB URL
  env:
    PROD_DB_URL: ${{ secrets.PROD_DB_URL }}
  run: |
    if [ -z "$PROD_DB_URL" ]; then
      echo "PROD_DB_URL secret missing"; exit 1;
    fi
    POSTGRES_URL="$PROD_DB_URL" \
    POSTGRES_URL_NON_POOLING="$PROD_DB_URL" \
    npx prisma migrate status --schema prisma/schema.prisma || {
      if [ "$GITHUB_REF" = "refs/heads/master" ]; then
        echo "::error::Migration drift detected on master!"
        exit 1
      else
        echo "::warning::Migration drift detected (expected on feature branches)"
        exit 0
      fi
    }
```

### 2. lib/db.ts - Use upsert for idempotent sync

Replace lines 92-106:
```typescript
// Use upsert for idempotent user creation/update
return await prisma.user.upsert({
  where: { id: clerkUserId },
  update: { email },
  create: { id: clerkUserId, email },
});
```

Then handle the orphaned user case separately after checking email mismatch.

---

## Verification

After fixes:
1. Push changes
2. Verify drift check passes on PR (warning only)
3. Verify all 781 tests pass
