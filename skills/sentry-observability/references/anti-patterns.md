# Anti-Patterns Scanner

Common mistakes to avoid when configuring Sentry.

## ❌ Manual Environment Naming

**Bad:**
```typescript
// Hardcoded environment strings
Sentry.init({
  environment: 'production', // Will be wrong in preview deployments
});
```

**Good:**
```typescript
// Dynamic environment from Vercel
Sentry.init({
  environment: resolveEnvironment(), // Adapts to VERCEL_ENV
});
```

**Why:** Hardcoded strings cause preview deployments to pollute production data.

---

## ❌ No PII Redaction

**Bad:**
```typescript
// Sending raw user data
Sentry.setUser({
  email: user.email, // Violates privacy regulations
  ip_address: request.ip,
});
```

**Good:**
```typescript
// Automatic redaction
Sentry.init({
  sendDefaultPii: false,
  beforeSend: (event) => sanitizeEvent(event),
});
```

**Why:** Storing PII violates GDPR/CCPA. Sentry events are retained for 90 days.

---

## ❌ Source Maps in Production Bundle

**Bad:**
```typescript
// Exposes source code to users
const nextConfig = {
  productionBrowserSourceMaps: true, // Security risk!
};
```

**Good:**
```typescript
// Source maps only in Sentry
const sentryOptions = {
  hideSourceMaps: true, // Not in bundle
};
```

**Why:** Exposing source maps reveals your code structure and potential vulnerabilities.

---

## ❌ Uncontrolled Sample Rates

**Bad:**
```typescript
// Default 100% tracing (expensive)
Sentry.init({
  tracesSampleRate: 1.0, // Will exceed free tier quickly
  replaysSessionSampleRate: 1.0, // Very expensive
});
```

**Good:**
```typescript
// Configurable via env vars
const tracesSampleRate = parseSampleRate(
  process.env.SENTRY_TRACES_SAMPLE_RATE,
  0.1 // 10% default
);

const replaysSessionSampleRate = parseSampleRate(
  process.env.SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
  0 // Disabled by default
);
```

**Why:** 100% sampling quickly exhausts quotas and adds overhead.

---

## ❌ Manual Auth Token Setup

**Bad:**
```bash
# Manual token creation and environment variable setup
# Problems:
# - Release ID mismatches between frontend and backend
# - Token rotation requires manual updates
# - No automatic source map upload
# - Preview deployments break
```

**Good:**
```bash
# Use Vercel Integration
# https://vercel.com/integrations/sentry
```

**Why:** Vercel Integration handles tokens, release IDs, and source maps automatically.

---

## ❌ Catching Errors Without Reporting

**Bad:**
```typescript
try {
  await riskyOperation();
} catch (error) {
  console.error(error); // Error is swallowed!
}
```

**Good:**
```typescript
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  // Handle the error appropriately
  throw error; // Or return error response
}
```

**Why:** Swallowed errors are invisible. Always report to Sentry or rethrow.

---

## ❌ Missing Test Error Route

**Bad:**
```
# No way to verify Sentry is working
# Deploy to production and hope for the best
```

**Good:**
```typescript
// app/test-error/route.ts
export async function GET() {
  throw new Error('Test error - Sentry integration check');
}
```

**Why:** Without a test route, you can't verify setup before production errors occur.

---

## ❌ Ignoring Server-Side Setup

**Bad:**
```typescript
// Only client config exists
// sentry.client.config.ts ✓
// sentry.server.config.ts ✗ (missing!)
```

**Good:**
```
// Both configs present
sentry.client.config.ts ✓
sentry.server.config.ts ✓
```

**Why:** Server-side errors (API routes, SSR) won't be captured without server config.

---

## ❌ Using Old Sentry SDK

**Bad:**
```json
{
  "dependencies": {
    "@sentry/browser": "^7.0.0" // Old SDK, missing features
  }
}
```

**Good:**
```json
{
  "dependencies": {
    "@sentry/nextjs": "^8.0.0" // Modern SDK with full Next.js support
  }
}
```

**Why:** Old SDKs miss App Router support, automatic instrumentation, and security fixes.

---

## Anti-Pattern Checklist

Use this to audit your Sentry configuration:

- [ ] Environment is dynamically resolved (not hardcoded)
- [ ] `sendDefaultPii: false` is set
- [ ] `beforeSend` sanitizes PII
- [ ] `hideSourceMaps: true` in production
- [ ] Sample rates are configurable via env vars
- [ ] Using Vercel Integration (not manual tokens)
- [ ] Test error route exists
- [ ] Both client and server configs present
- [ ] Using `@sentry/nextjs` (not `@sentry/browser`)
- [ ] Errors are reported, not swallowed
