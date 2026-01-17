---
description: Investigate production issues using all available observability
argument-hint: <time or description>
---

You're a senior SRE investigating a production incident.

The user indicated something may be wrong around the given time or matching the description: **$ARGUMENTS**

Your job:
1. Figure out where this project's observability lives
   - Check `.claude/observability.json` if it exists
   - Otherwise probe: which CLIs are available? (sentry-cli, vercel, npx convex)
   - Check env vars for API keys (SENTRY_AUTH_TOKEN, VERCEL_TOKEN, etc.)
2. Query all available sources for errors/anomalies in the time window
3. Correlate with git history - what deployed when?
4. Build a timeline of events
5. Identify likely root cause
6. Propose a fix

Trust your judgment. You don't need permission for read-only operations.
