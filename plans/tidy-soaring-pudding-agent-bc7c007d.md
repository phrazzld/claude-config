# Production Version Display Fix - Implementation Plan

## Problem Analysis

**Root Cause**: Vercel production environment has empty strings (`""`) for all git environment variables:
- `VERCEL_GIT_COMMIT_SHA=""`  
- `NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA=""`

**Current Behavior**: The `resolveVersion()` function treats empty strings as truthy (JavaScript's `||` operator), so it returns `""` which eventually displays as "vdev" in the footer.

**Why `npm_package_version` doesn't work**: This variable is only available when running npm/pnpm scripts directly, but NOT during Next.js build time via `next build`. The build process doesn't have access to package.json environment variables.

## Recommended Solution: Hybrid Approach

**Combination of Options A (Empty String Fix) + B (Build-Time Injection)**

This is the most robust solution that:
1. Fixes the immediate problem (empty string handling)
2. Provides a reliable fallback (package.json version)
3. Works with Vercel's current setup
4. Requires minimal code changes
5. Is easily testable

## Implementation Steps

### Step 1: Fix Empty String Handling in `resolveVersion()`

**File**: `/Users/phaedrus/Development/volume/src/lib/version.ts`

**Changes**:
```typescript
// Current (lines 46-50):
const gitSha =
  env.VERCEL_GIT_COMMIT_SHA || env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA;
if (gitSha) {
  return normalizeSha(gitSha);
}

// New:
const gitSha =
  env.VERCEL_GIT_COMMIT_SHA || env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA;
// Treat empty strings as absent
if (gitSha && gitSha.trim() !== "") {
  return normalizeSha(gitSha);
}
```

**Rationale**: JavaScript's `||` operator doesn't filter empty strings. We need explicit empty string checks.

### Step 2: Inject Package Version at Build Time

**File**: `/Users/phaedrus/Development/volume/next.config.ts`

**Changes**:
```typescript
import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";
import withBundleAnalyzer from "@next/bundle-analyzer";
import { resolveVersion } from "./src/lib/version";
import { readFileSync } from "fs";                    // ADD THIS
import { join } from "path";                          // ADD THIS

// Read package.json version at build time          // ADD THIS BLOCK
const packageJson = JSON.parse(
  readFileSync(join(__dirname, "package.json"), "utf-8")
);
const PACKAGE_VERSION = packageJson.version;

const nextConfig: NextConfig = {
  env: {
    // Expose a deterministic, pre-resolved app version to the client.
    NEXT_PUBLIC_APP_VERSION: resolveVersion(),
    
    // ADD THIS LINE - Fallback version from package.json
    NEXT_PUBLIC_PACKAGE_VERSION: PACKAGE_VERSION,
  },
  // ... rest of config
};
```

**Rationale**: Reading package.json at build time (in next.config.ts) makes the version available to the Next.js environment, which `resolveVersion()` can then use.

### Step 3: Update `resolveVersion()` to Use Injected Version

**File**: `/Users/phaedrus/Development/volume/src/lib/version.ts`

**Changes**:
```typescript
// Update type (line 10-18):
type EnvSource = Partial<
  Pick<
    NodeJS.ProcessEnv,
    | "SENTRY_RELEASE"
    | "VERCEL_GIT_COMMIT_SHA"
    | "NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA"
    | "npm_package_version"
    | "NEXT_PUBLIC_PACKAGE_VERSION"  // ADD THIS
  >
>;

// Update fallback logic (lines 52-54):
if (env.npm_package_version) {
  return env.npm_package_version;
}

// ADD THIS BLOCK - Use injected package version
if (env.NEXT_PUBLIC_PACKAGE_VERSION) {
  return env.NEXT_PUBLIC_PACKAGE_VERSION;
}

return "dev";
```

**Rationale**: This creates a clear fallback chain:
1. SENTRY_RELEASE (explicit override)
2. Git SHA (from Vercel, if available)
3. npm_package_version (npm scripts only)
4. NEXT_PUBLIC_PACKAGE_VERSION (build-time injection)
5. "dev" (local development)

### Step 4: Update Sentry `resolveRelease()` Function

**File**: `/Users/phaedrus/Development/volume/src/lib/sentry.ts`

**Changes**:
```typescript
// Current (lines 317-324):
function resolveRelease(): string | undefined {
  return (
    process.env.SENTRY_RELEASE ||
    process.env.VERCEL_GIT_COMMIT_SHA ||
    process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA ||
    process.env.npm_package_version
  );
}

// New:
function resolveRelease(): string | undefined {
  const release =
    process.env.SENTRY_RELEASE ||
    process.env.VERCEL_GIT_COMMIT_SHA ||
    process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA ||
    process.env.npm_package_version ||
    process.env.NEXT_PUBLIC_PACKAGE_VERSION;
  
  // Filter empty strings
  return release && release.trim() !== "" ? release : undefined;
}
```

**Rationale**: Ensures Sentry uses the same version resolution logic as the footer and health endpoint.

### Step 5: Update Health Endpoint

**File**: `/Users/phaedrus/Development/volume/src/app/api/health/route.ts`

**Changes**:
```typescript
// Current (lines 15-18):
const version =
  process.env.VERCEL_GIT_COMMIT_SHA ||
  process.env.npm_package_version ||
  "unknown";

// New:
import { resolveVersion } from "@/lib/version";  // ADD THIS IMPORT

const version = resolveVersion() || "unknown";
```

**Rationale**: Centralizes version resolution to a single function, eliminating duplication and ensuring consistency.

### Step 6: Update Tests

**File**: `/Users/phaedrus/Development/volume/src/lib/version.test.ts`

**Changes**: Add new test case after line 81:

```typescript
it("uses NEXT_PUBLIC_PACKAGE_VERSION when npm_package_version is unavailable", () => {
  const env = {
    SENTRY_RELEASE: undefined,
    VERCEL_GIT_COMMIT_SHA: undefined,
    NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA: undefined,
    npm_package_version: undefined,
    NEXT_PUBLIC_PACKAGE_VERSION: "0.1.0",
  };

  expect(resolveVersion(env)).toBe("0.1.0");
});

it("prefers npm_package_version over NEXT_PUBLIC_PACKAGE_VERSION", () => {
  const env = {
    SENTRY_RELEASE: undefined,
    VERCEL_GIT_COMMIT_SHA: undefined,
    NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA: undefined,
    npm_package_version: "0.2.0",
    NEXT_PUBLIC_PACKAGE_VERSION: "0.1.0",
  };

  expect(resolveVersion(env)).toBe("0.2.0");
});
```

**File**: `/Users/phaedrus/Development/volume/src/lib/sentry.test.ts`

**Changes**: Find the `resolveRelease` test section and add:

```typescript
it("filters empty strings from git SHAs", () => {
  vi.stubEnv("VERCEL_GIT_COMMIT_SHA", "");
  vi.stubEnv("NEXT_PUBLIC_PACKAGE_VERSION", "0.1.0");

  const options = createSentryOptions("server");
  expect(options.release).toBe("0.1.0");
});
```

### Step 7: Update Documentation

**File**: `/Users/phaedrus/Development/volume/CLAUDE.md`

**Changes**: Update the version resolution section:

```markdown
**Current Resolution Priority**:
1. SENTRY_RELEASE (explicit override)
2. VERCEL_GIT_COMMIT_SHA or NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA (git commit SHA, if available)
3. npm_package_version (npm scripts only - not available during Next.js build)
4. NEXT_PUBLIC_PACKAGE_VERSION (injected from package.json at build time)
5. "dev" (fallback for local development)

**Note**: Empty strings are treated as absent values and filtered out.
```

## Testing Strategy

### Unit Tests
```bash
pnpm test src/lib/version.test.ts
pnpm test src/lib/sentry.test.ts
```

**Expected**: All tests pass, including new empty string handling tests.

### Local Development Test
```bash
# Should show "dev"
pnpm dev
# Visit http://localhost:3000 and check footer
```

**Expected**: Footer shows "vdev" (current behavior preserved).

### Production Build Test
```bash
# Clean build
rm -rf .next
pnpm build

# Check what version was injected
grep -r "NEXT_PUBLIC_PACKAGE_VERSION" .next/server/app-build-manifest.json || 
grep -r "0.1.0" .next/static/chunks/app/layout-*.js
```

**Expected**: Version "0.1.0" appears in build artifacts.

### Vercel Deployment Verification

**After deploying to production**:

1. **Check Footer**: Visit https://volume.fitness and scroll to footer
   - **Expected**: Shows "v0.1.0" (not "vdev")

2. **Check Health Endpoint**: `curl https://volume.fitness/api/health | jq .version`
   - **Expected**: Returns `"0.1.0"` (not `"unknown"`)

3. **Check Sentry**: Visit Sentry dashboard and trigger a test error
   - **Expected**: Release tag shows "0.1.0"

4. **Verify Environment**: Check Vercel deployment logs
   - **Expected**: No errors during build, `NEXT_PUBLIC_PACKAGE_VERSION` injected

## Rollback Plan

If issues occur in production:

1. **Quick Fix**: Set `NEXT_PUBLIC_SENTRY_RELEASE=0.1.0` in Vercel dashboard
   - This overrides all version resolution
   - No code deployment needed

2. **Full Rollback**: Revert the PR and redeploy
   - Footer will show "vdev" again (original behavior)
   - Health endpoint will show "unknown"

## Why This Solution is Best

1. **Minimal Code Changes**: Only 3 files modified (version.ts, next.config.ts, sentry.ts)
2. **Works with Current Setup**: No Vercel environment variable changes needed
3. **Robust Fallback**: Multiple fallback layers ensure version always displays
4. **Testable**: All logic is in testable functions with explicit empty string handling
5. **Future-Proof**: If Vercel ever populates git SHAs, they'll automatically take precedence
6. **Centralized**: All version resolution happens in one place (`resolveVersion()`)

## Alternative Solutions (Not Recommended)

### Option C: Manual Vercel Environment Variable
- **Why Not**: Requires manual updates on every release (error-prone)
- **Why Not**: Doesn't solve the empty string problem
- **Why Not**: Adds maintenance overhead

### Option D: Git Command at Build Time
- **Why Not**: Vercel doesn't clone full git history (shallow clone)
- **Why Not**: May not have git available in all build environments
- **Why Not**: More complex than reading package.json

## Expected Outcome

After this fix:

- **Production Footer**: "v0.1.0" (instead of "vdev")
- **Development Footer**: "vdev" (unchanged)
- **Health Endpoint**: `{"version": "0.1.0"}` (instead of `"unknown"`)
- **Sentry Release**: "0.1.0" (proper grouping)
- **All Tests**: Pass with 100% coverage on version resolution

## Implementation Checklist

- [ ] Update `src/lib/version.ts` (empty string filtering + NEXT_PUBLIC_PACKAGE_VERSION)
- [ ] Update `next.config.ts` (inject package version)
- [ ] Update `src/lib/sentry.ts` (empty string filtering in resolveRelease)
- [ ] Update `src/app/api/health/route.ts` (use centralized resolveVersion)
- [ ] Add tests to `src/lib/version.test.ts`
- [ ] Add tests to `src/lib/sentry.test.ts`
- [ ] Update `CLAUDE.md` documentation
- [ ] Run full test suite (`pnpm test --run`)
- [ ] Run typecheck (`pnpm typecheck`)
- [ ] Test local build (`pnpm build`)
- [ ] Deploy to production
- [ ] Verify footer shows "v0.1.0"
- [ ] Verify health endpoint returns "0.1.0"
- [ ] Verify Sentry release tag
