# Observability Setup Pitfalls

Common mistakes when setting up Sentry, PostHog, or other observability tools.

## Never Use "latest" in package.json

Pin dependencies with caret versions (`^x.y.z`). "latest" causes:
- Non-reproducible builds
- Unexpected breaking changes
- CI failures when upstream releases

## Sentry tracesSampleRate Must Be Env-Controlled

Hardcoding `tracesSampleRate: 1` means 100% of transactions sampled. In production:
- Quota exhaustion in hours/days
- Significant cost increase

**Pattern:**
```typescript
const TRACES_SAMPLE_RATE = Math.min(
  1,
  Math.max(0, parseFloat(process.env.SENTRY_TRACES_SAMPLE_RATE ?? "0.1"))
);

Sentry.init({
  tracesSampleRate: TRACES_SAMPLE_RATE,
});
```

## Error Objects Serialize as `{}`

`JSON.stringify(new Error("msg"))` returns `{}` because `message`, `name`, `stack` are non-enumerable.

**Pattern:**
```typescript
function serializeError(err: Error) {
  return {
    name: err.name,
    message: err.message,
    stack: err.stack,
  };
}
```

## Health Checks Must Not Lie

Hardcoding `services: { db: "ok" }` without checking is worse than no health check—provides false confidence.

**Options:**
- Remove fake service status (honest liveness probe)
- Actually check connectivity (real readiness probe)

**Pattern:**
```typescript
export async function GET() {
  const dbOk = await checkDatabaseConnection();
  return Response.json({
    status: dbOk ? "healthy" : "unhealthy",
    services: { db: dbOk ? "ok" : "error" },
  });
}
```
