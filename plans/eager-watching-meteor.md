# Root Cause Analysis: UptimeRobot 405 Method Not Allowed

## Summary

UptimeRobot is reporting a 405 "Method Not Allowed" error for HEAD requests to `https://gitpulse.app/api/health`. Investigation reveals the **endpoint is now working correctly**, but there are configuration issues to address.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:05:48 | Production deployment `f3e5e08` |
| 14:12:16 | UptimeRobot incident starts (405 for HEAD) |
| 18:46:26 | Production deployment `d0cc095` |
| 20:18:52 | Production deployment `aa00578` |
| 21:54:40 | Production deployment `bdb1bdf` (added POST handler) |
| 22:22:31 | My tests confirm endpoint working (200 OK) |

## Root Cause

**The 405 error was NOT caused by missing HEAD handler** - the code at `f3e5e08` already had proper HEAD support:

```typescript
// app/api/health/route.ts at f3e5e08
export async function HEAD(request: Request) {
  return handle(request, "HEAD");
}
```

### Contributing Factors

1. **Domain Redirect Issue**
   - UptimeRobot monitors `https://gitpulse.app/api/health` (apex domain)
   - Vercel returns 307 redirect to `https://www.gitpulse.app/api/health`
   - Some HTTP clients mishandle HEAD + 307 combinations

2. **Possible Transient Deployment Issue**
   - The incident started 7 minutes after deployment `f3e5e08`
   - Could have been edge function cold start or rollout issue
   - Subsequent deployments resolved it

3. **Current State**
   - Endpoint NOW works: `curl -I https://www.gitpulse.app/api/health` returns 200
   - Apex domain still redirects: `curl -I https://gitpulse.app/api/health` returns 307

## Evidence

```bash
# Current test results (22:22 UTC)
$ curl -sI -X HEAD https://gitpulse.app/api/health
HTTP/2 307
location: https://www.gitpulse.app/api/health

$ curl -sI -X HEAD https://www.gitpulse.app/api/health
HTTP/2 200
cache-control: no-cache, no-store, must-revalidate

$ curl -s https://www.gitpulse.app/api/health
{"status":"ok","mode":"liveness","timestamp":1764022951874}
```

## Recommended Fix

### Option A: Update UptimeRobot Monitor (Quickest)

Change UptimeRobot to monitor `https://www.gitpulse.app/api/health` instead of the apex domain to avoid the 307 redirect entirely.

**Pros**: Immediate fix, no code changes
**Cons**: Doesn't address apex domain routing

### Option B: Add Redirect Bypass for /api/* Routes

Configure Vercel to NOT redirect `/api/*` paths from apex to www. This ensures API endpoints work identically on both domains.

Add to `vercel.json`:
```json
{
  "redirects": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*",
      "permanent": false
    }
  ]
}
```

Or handle in Next.js middleware.

**Pros**: API endpoints work on both domains
**Cons**: Requires deployment

### Option C: Canonical Domain Setup (Best Practice)

Remove the apex→www redirect at Vercel level for all paths, or vice versa. Ensure consistent domain handling.

## Files Involved

- `app/api/health/route.ts` - Health endpoint (no changes needed)
- `lib/health/index.ts` - Health utilities (no changes needed)
- `vercel.json` - Vercel configuration (potential changes)
- `middleware.ts` - Next.js middleware (potential changes)

## Immediate Actions

1. **Verify UptimeRobot recheck** - The endpoint works now; UptimeRobot may just need to poll again
2. **Update UptimeRobot URL** to use `www.gitpulse.app` if redirect is the issue
3. **Consider redirect bypass** for `/api/*` routes if you want apex domain support

## Sources

- [Vercel 405 Errors Documentation](https://vercel.com/docs/errors/INVALID_REQUEST_METHOD)
- [How to Fix 405 Errors on Next.js Hosted on Vercel](https://www.wisp.blog/blog/how-to-fix-405-errors-on-nextjs-hosted-on-vercel)
- [UptimeRobot HTTP Method Selection](https://uptimerobot.com/blog/introducing-http-method-selection-headgetpostputpatchdelete/)
- [UptimeRobot Redirect Following Option](https://uptimerobot.com/blog/july-2023-dont-follow-redirects-secondary-e-mail-address/)
