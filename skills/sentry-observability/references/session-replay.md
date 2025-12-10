# Session Replay Configuration

Session Replay records user interactions before errors for visual debugging.

## What It Does

- Records DOM mutations, clicks, scrolls
- Captures network requests (headers redacted)
- Creates video-like playback in Sentry dashboard
- Helps understand user journey before error

## Configuration

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Routine session recording (cost-aware default: 0%)
  replaysSessionSampleRate: parseSampleRate(
    process.env.NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
    0 // Disabled by default
  ),

  // Always record when errors occur (default: 100%)
  replaysOnErrorSampleRate: parseSampleRate(
    process.env.NEXT_PUBLIC_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE,
    1.0
  ),

  integrations: [
    Sentry.replayIntegration({
      // Privacy settings
      maskAllText: true,     // Mask all text by default
      blockAllMedia: true,   // Block images/videos
    }),
  ],
});
```

## Environment Variables

```bash
# .env.local or Vercel environment

# Routine recording (0.0 to 1.0)
# 0 = disabled, 0.05 = 5% of sessions
NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0

# Error recording (0.0 to 1.0)
# 1.0 = capture all sessions where errors occur
NEXT_PUBLIC_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0
```

## Decision Tree

```
Do you need visual debugging of user interactions?
├─ NO → Set SESSION_SAMPLE_RATE=0, ERROR_SAMPLE_RATE=1.0 (error-only)
│
└─ YES → Are you within free tier (5k errors/month)?
    ├─ YES → Start with SESSION_SAMPLE_RATE=0.05 (5%)
    │         ERROR_SAMPLE_RATE=1.0
    │
    └─ NO → Are you debugging a specific UX issue?
        ├─ YES → Temporarily increase to 0.5 (50%) during debug
        └─ NO → Lower to 0.01 (1%) or disable (0)
```

## Cost Considerations

- Free tier: 5,000 errors/month (~166/day)
- Session Replay events count toward quota
- Each replay can consume multiple "events"

**Recommendations:**
1. Start with error-only recording (0% routine, 100% error)
2. Increase routine sampling only when debugging UX issues
3. Monitor quota usage in Sentry Settings > Usage

## Privacy Settings

```typescript
Sentry.replayIntegration({
  // Mask all text content
  maskAllText: true,

  // Block all images and videos
  blockAllMedia: true,

  // Mask specific elements by selector
  mask: ['.sensitive-data', '[data-sentry-mask]'],

  // Block specific elements from recording
  block: ['.password-field', '[data-sentry-block]'],

  // Ignore specific elements from click tracking
  ignore: ['.tracking-opt-out'],
});
```

## Viewing Replays

1. Go to Sentry Dashboard
2. Open an Issue
3. Click "Replay" tab (if available)
4. Watch user session playback
5. See exact actions before error

## Debugging with Replays

Use replays to understand:
- What user actions led to the error
- Browser/device context
- Network requests before error
- UI state at time of error
- User journey through the app

## Temporarily Increasing Sample Rate

When debugging a specific issue:

```bash
# Temporarily increase for debugging
NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.5

# After debugging, restore cost-aware defaults
NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0
```
