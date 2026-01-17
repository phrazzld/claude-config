---
description: Triage production errors - find highest priority, investigate, propose fix
---

Production might be on fire. Your job:

1. Check Sentry for unresolved errors, prioritize by user impact
2. Check Vercel logs for correlated deployment issues
3. For the highest priority error: trace git history, understand root cause
4. Propose minimal fix
5. If >50% users affected, recommend rollback first

Be fast. Users are waiting.

Trust your judgment on which tools to use. Common ones:
- `sentry-cli issues list --status unresolved`
- `vercel logs --prod --since 1h`
- `git log --since="24 hours ago" --oneline`
