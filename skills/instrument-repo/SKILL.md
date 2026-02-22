---
name: instrument-repo
description: |
  Add observability to any repo: Sentry (errors), PostHog (analytics), Helicone (LLM costs).
  Auto-detects language/framework. Creates Sentry project via MCP. Installs SDKs, writes config,
  updates .env.example, opens PR. Supports: Next.js, Node/Express/Hono, Go, Python, Swift, Rust, React Native.
argument-hint: "[repo path] [--audit] [--helicone] [--posthog] [--sentry-only]"
effort: high
---

# /instrument-repo

Add production observability to a repository. Detects stack, installs SDKs, writes config, opens PR.

## Shared Config

```
SENTRY_ORG=misty-step
SENTRY_TEAM=misty-step
POSTHOG_PROJECT_ID=293836
POSTHOG_HOST=https://us.i.posthog.com
```

All repos share ONE PostHog project (segmented by events). Each repo gets its OWN Sentry project.

## Detection

Before instrumenting, detect what we're working with:

```bash
# Language detection
[ -f package.json ] && echo "typescript"
[ -f go.mod ] && echo "go"
[ -f pyproject.toml ] || [ -f setup.py ] && echo "python"
[ -f Package.swift ] && echo "swift"
[ -f Cargo.toml ] && echo "rust"

# Framework detection (TypeScript)
grep -q '"next"' package.json 2>/dev/null && echo "nextjs"
grep -q '"hono"' package.json 2>/dev/null && echo "hono"
grep -q '"express"' package.json 2>/dev/null && echo "express"
grep -q '"react-native"' package.json 2>/dev/null && echo "react-native"

# LLM usage detection (for Helicone)
grep -rq '@ai-sdk\|openai\|anthropic\|@google/genai' package.json src/ lib/ app/ 2>/dev/null && echo "has-llm"
grep -rq 'openai\|anthropic\|langchain' *.go cmd/ internal/ 2>/dev/null && echo "has-llm"
grep -rq 'openai\|anthropic\|langchain' *.py src/ 2>/dev/null && echo "has-llm"

# Existing instrumentation
grep -q '@sentry' package.json 2>/dev/null && echo "has-sentry"
grep -q 'posthog' package.json 2>/dev/null && echo "has-posthog"
grep -rq 'helicone' src/ lib/ app/ 2>/dev/null && echo "has-helicone"
```

## Per-repo Workflow

```
1. cd ~/Development/$REPO
2. Detect language, framework, LLM usage, existing instrumentation
3. git fetch origin && git checkout -b infra/observability origin/main (or master)
4. Create Sentry project if needed → mcp__sentry__create_project
5. Install packages (language-specific)
6. Write/update config files from templates
7. Update .env.example
8. Typecheck/build to verify
9. git add <specific files> && git commit
10. git push -u origin infra/observability
11. gh pr create with structured body
```

## What to Add (Decision Matrix)

| Condition | Sentry | PostHog | Helicone |
|-----------|--------|---------|----------|
| Any app/service | YES | — | — |
| User-facing web app | YES | YES | — |
| Has LLM SDK imports | YES | maybe | YES |
| CLI tool | YES | NO | maybe |
| GitHub Action / lib | NO | NO | NO |

## Sentry Sampling Rates

Cost-conscious defaults (5k errors/mo free tier):

```
tracesSampleRate: 0.1          # 10% of transactions
replaysSessionSampleRate: 0    # Don't record sessions by default
replaysOnErrorSampleRate: 1.0  # Always replay on error
```

## Templates

### Next.js → `templates/nextjs/`

Files to create:
- `sentry.client.config.ts` — Client-side Sentry init
- `sentry.server.config.ts` — Server-side Sentry init
- `sentry.edge.config.ts` — Edge runtime Sentry init (same as server)
- `instrumentation.ts` — Next.js instrumentation hook
- `lib/sentry.ts` — Shared Sentry config factory with PII scrubbing
- `components/posthog-provider.tsx` — PostHog React provider
- `components/posthog-pageview.tsx` — Route-aware pageview tracking
- `lib/posthog.ts` — PostHog client init + helpers

Install: `pnpm add @sentry/nextjs posthog-js posthog-node`

Next.js config: wrap with `withSentryConfig()` in `next.config.ts`

PostHog `/ingest` rewrite in `next.config.ts`:
```typescript
async rewrites() {
  return [
    { source: "/ingest/static/:path*", destination: "https://us-assets.i.posthog.com/static/:path*" },
    { source: "/ingest/:path*", destination: "https://us.i.posthog.com/:path*" },
    { source: "/ingest/decide", destination: "https://us.i.posthog.com/decide" },
  ];
},
```

### Node.js (Express/Hono) → `templates/node/`

Files to create:
- `lib/sentry.ts` — Sentry init for Node

Install: `pnpm add @sentry/node`

Express: `Sentry.setupExpressErrorHandler(app)` after all routes
Hono: Import and init at app entry, use `onError` hook

### Go → `templates/go/`

Files to create:
- `internal/observability/sentry.go` — Sentry init + flush helper

Install: `go get github.com/getsentry/sentry-go`

### Python → `templates/python/`

Files to create:
- `observability.py` — Sentry init

Install: `pip install sentry-sdk` or add to `pyproject.toml`

### Swift → `templates/swift/`

Files to create:
- `SentrySetup.swift` — Sentry init via SPM

SPM dependency: `https://github.com/getsentry/sentry-cocoa`
PostHog SPM: `https://github.com/PostHog/posthog-ios`

### Rust → `templates/rust/`

Files to create:
- `src/sentry_init.rs` — Sentry guard init

Install: Add `sentry = "0.35"` to `Cargo.toml`

### React Native → `templates/react-native/`

Install: `pnpm add @sentry/react-native posthog-react-native`

### Helicone → `templates/helicone/`

Files to create:
- `lib/ai-provider.ts` — Helicone-proxied AI SDK provider

Pattern: Change `baseURL` on AI SDK provider to Helicone gateway, add auth + property headers.

## Commit Message

```
feat: add observability (Sentry [+ PostHog] [+ Helicone])

- Sentry: error tracking with PII-safe defaults
[- PostHog: product analytics with privacy masking]
[- Helicone: LLM cost tracking via gateway proxy]
- Updated .env.example with required variables
```

## PR Body

```markdown
## Summary
Add production observability to {repo}.

## Changes
- Sentry error tracking (DSN: `{dsn}`)
  - PII scrubbing (emails, IPs, sensitive headers)
  - Environment-aware (production/preview/development)
  - Traces sample rate: 10%
[- PostHog product analytics
  - Pageview tracking via `/ingest` proxy rewrite
  - Privacy: `respect_dnt: true`, manual pageview capture]
[- Helicone LLM cost tracking
  - Proxied through gateway for cost/latency monitoring
  - Tagged with product name and environment]
- Updated `.env.example` with all required variables

## Required Env Vars
| Variable | Where | Value |
|----------|-------|-------|
| `NEXT_PUBLIC_SENTRY_DSN` | Vercel | `{dsn}` |
| `SENTRY_AUTH_TOKEN` | Vercel + GH Actions | org-level token |
[| `NEXT_PUBLIC_POSTHOG_KEY` | Vercel | project API key |]
[| `HELICONE_API_KEY` | Vercel (server) | Helicone API key |]

## Test Plan
- [ ] `pnpm build` passes
- [ ] Deploy to preview → check Sentry for test error
- [ ] Set env vars on Vercel production
[- [ ] Verify PostHog Live Events after deploy]
[- [ ] Verify Helicone dashboard shows tagged requests]
```

## Env Var Reference

| Variable | Scope | Notes |
|----------|-------|-------|
| `NEXT_PUBLIC_SENTRY_DSN` | Per-project | Unique per Sentry project |
| `SENTRY_DSN` | Per-project (server-only) | Same DSN, no NEXT_PUBLIC prefix |
| `SENTRY_AUTH_TOKEN` | Shared | For source map uploads |
| `SENTRY_ORG` | `misty-step` | Hardcode in config |
| `SENTRY_PROJECT` | Per-project | Matches Sentry project slug |
| `NEXT_PUBLIC_POSTHOG_KEY` | Shared | PostHog project API key |
| `NEXT_PUBLIC_POSTHOG_HOST` | `/ingest` | Via rewrite proxy |
| `HELICONE_API_KEY` | Shared (server-only) | Never expose client-side |

## Audit Mode

When `--audit` flag or repo already has instrumentation:

1. Check Sentry config against best practices (PII scrubbing, sampling rates, env detection)
2. Check PostHog config (respect_dnt, manual pageview, proxy rewrite)
3. Check Helicone config (product tag, environment tag, user-id)
4. Report findings, fix issues, open PR with fixes

## Anti-Patterns

- `tracesSampleRate: 1` — exhausts free tier instantly
- Missing PII scrubbing — privacy violation
- `sendDefaultPii: true` — leaks emails/IPs
- PostHog without `/ingest` rewrite — blocked by ad blockers
- Helicone API key in client-side code — key exposure
- Hardcoded DSN in code instead of env var — can't change per environment
- Missing `respect_dnt: true` on PostHog — privacy violation
