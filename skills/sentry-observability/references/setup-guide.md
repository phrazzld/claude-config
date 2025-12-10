# Sentry Setup Guide

Complete walkthrough for setting up Sentry in Next.js/Vercel projects.

## Prerequisites

- Next.js project (App Router recommended)
- Vercel deployment (recommended) or self-hosted
- Sentry account (free tier works)

## Quick Setup (Recommended)

### 1. Install Vercel Integration

The Vercel Integration is the recommended approach for 2025:

```bash
# Visit: https://vercel.com/integrations/sentry
# Click "Add Integration" → Select your project
```

**Benefits:**
- ✅ Zero manual token management
- ✅ Automatic source map upload on every deploy
- ✅ Release tracking with correct git SHA
- ✅ No "release not found" errors
- ✅ Works with Vercel preview deployments

### 2. Verify Environment Variables

```bash
# Check that integration created the variables
vercel env ls | grep SENTRY

# Expected output:
# SENTRY_AUTH_TOKEN (production, preview)
# NEXT_PUBLIC_SENTRY_DSN (production, preview)
# SENTRY_ORG (all environments)
# SENTRY_PROJECT (all environments)
```

### 3. Local Development Setup

```bash
# Copy DSN to .env.local for development
echo "NEXT_PUBLIC_SENTRY_DSN=<your-dsn>" >> .env.local
echo "SENTRY_DSN=<your-dsn>" >> .env.local
```

### 4. Run Setup Script

```bash
~/.claude/skills/sentry-observability/scripts/init_sentry.sh
```

### 5. Verify Setup

```bash
# Test locally
curl http://localhost:3000/test-error

# Check Sentry dashboard
# Verify error appears in Issues tab
```

## Manual Setup (Alternative)

Only use this if:
- Self-hosting (not using Vercel)
- Organization security policy prevents integrations
- Need fine-grained token permissions

### 1. Create Sentry Project

1. Go to https://sentry.io
2. Create new project → Select "Next.js"
3. Copy the DSN

### 2. Install Packages

```bash
pnpm add @sentry/nextjs
# or: npm install @sentry/nextjs
```

### 3. Run Sentry Wizard

```bash
npx @sentry/wizard@latest -i nextjs
```

The wizard will:
- Create `sentry.client.config.ts`
- Create `sentry.server.config.ts`
- Update `next.config.ts`
- Create `.sentryclirc`

### 4. Set Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SENTRY_DSN=https://...@o0.ingest.sentry.io/0
SENTRY_DSN=https://...@o0.ingest.sentry.io/0
SENTRY_AUTH_TOKEN=sntrys_...
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
```

### 5. Create Auth Token

1. Visit https://sentry.io/settings/account/api/auth-tokens/
2. Create token with scopes:
   - `project:releases`
   - `project:read`
   - `org:read`

## Backend Setup

### Convex

```bash
# Set DSN for Convex functions
npx convex env set SENTRY_DSN "https://...@o0.ingest.sentry.io/0" --prod
```

### API Routes

Server-side API routes automatically use `SENTRY_DSN` from environment.

## Verification Checklist

After setup, verify:

- [ ] Error appears in Sentry dashboard (Issues tab)
- [ ] Environment name is clean ("production" not "vercel-production")
- [ ] Source maps show original TypeScript code
- [ ] Email alert received (if configured)
- [ ] Session Replay attached (if error sampling enabled)

Use the verification script:

```bash
~/.claude/skills/sentry-observability/scripts/verify_setup.sh
```

## Common Issues

### Minified Stack Traces

**Cause:** Source maps not uploading

**Fix:** Install Vercel Integration (handles this automatically)

### "Release not found" Errors

**Cause:** Manual token setup with mismatched release IDs

**Fix:** Switch to Vercel Integration

### Errors Not Appearing

**Cause:** DSN mismatch between environments

**Fix:** Verify DSN in both .env.local and Vercel deployment

### Preview Deployments Not Working

**Cause:** Missing environment variables for preview

**Fix:** Vercel Integration sets these automatically
