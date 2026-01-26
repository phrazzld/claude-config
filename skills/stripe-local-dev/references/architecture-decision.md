# Architecture Decision: Webhook Endpoint Location

## Context

Stripe webhooks need a secret to verify signatures. The Stripe CLI generates a new ephemeral secret each time it starts. This creates a sync problem in local development.

## Decision

**Prefer Convex HTTP webhooks over Next.js API routes for Stripe.**

## Rationale

### Convex HTTP Webhooks

**Pros:**
- Secret syncs instantly via `npx convex env set`
- No process restart needed
- Convex handles real-time updates naturally
- Single source of truth (Convex is already the data layer)

**Cons:**
- Webhook logic moves from Next.js to Convex
- Different deployment URL pattern (`.site` vs app URL)

### Next.js API Route Webhooks

**Pros:**
- Familiar pattern for Next.js developers
- Webhook handler co-located with other API routes
- Direct access to Next.js features (redirects, etc.)

**Cons:**
- Secret stored in `.env.local` requires file modification
- Next.js must restart to pick up new env vars
- Race condition: listener starts before Next.js restarts
- Harder to orchestrate in `concurrently`

## Comparison: Other Projects

| Project | Approach | Why It Works |
|---------|----------|--------------|
| volume | Convex HTTP | Script syncs to `convex env set` - instant |
| heartbeat | Convex HTTP | Same pattern as volume |
| chrondle | Manual | No auto-start, dev copies secret manually |
| bibliomnomnom | Next.js API | Was missing auto-sync entirely |

## Migration Path

To migrate from Next.js to Convex webhooks:

1. Create `convex/http.ts` with webhook handler
2. Move verification logic from API route
3. Update Stripe Dashboard webhook URL
4. Switch to `dev-stripe-convex.sh` script

## When to Use Each

**Use Convex HTTP when:**
- Convex is your primary data layer
- You want zero-restart local dev
- Webhook modifies Convex data directly

**Use Next.js API when:**
- Webhook triggers Next.js-specific actions (revalidation, etc.)
- You prefer co-located API routes
- You're okay with restart orchestration
