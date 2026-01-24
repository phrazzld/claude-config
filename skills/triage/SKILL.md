---
name: triage
description: |
  Multi-source observability triage. Checks Sentry, Vercel logs, health endpoints.
  Drives: investigate -> fix -> PR -> postmortem workflow.
  Invoke for: production issues, error spikes, user reports, incident response.
argument-hint: "[action: status | investigate ISSUE-ID | fix | postmortem ISSUE-ID]"
---

# /triage

Check all observability sources. Investigate, fix, postmortem.

## Usage

```bash
/triage                        # Status overview (default)
/triage investigate VOL-456    # Deep dive on specific issue
/triage fix                    # Create PR for current fix
/triage postmortem VOL-456     # Generate postmortem after merge
```

## Stage 1: Status Overview

**Command:** `/triage` or `/triage status`

Parallel checks (<10s):
1. **Sentry** - Unresolved issues via `triage_score.sh`
2. **Vercel logs** - Recent errors in stream
3. **Health endpoints** - `/api/health` response

**Output format:**
```
TRIAGE STATUS - 2026-01-23 15:30
================================

SENTRY (volume-fitness)
  [CRITICAL] 3 unresolved issues
  Top: VOL-456 "PaymentIntent failed" (Score: 147, 23 users)

VERCEL LOGS
  [OK] No errors in last 10 minutes

HEALTH ENDPOINTS
  [OK] volume.fitness/api/health (200, 45ms)

RECOMMENDATION:
  Investigate VOL-456 immediately - 23 users affected
  Run: /triage investigate VOL-456
```

If all clean: "All systems nominal. No action required."

## Stage 2: Investigate

**Command:** `/triage investigate ISSUE-ID`

Actions:
1. Fetch full issue context from Sentry
2. Create branch: `fix/ISSUE-ID-description`
3. Load affected files from stack trace
4. Check git history for related changes
5. Form root cause hypothesis

**Output:** Investigation summary with hypothesis and next steps.

## Stage 3: Fix

**Command:** `/triage fix`

Prerequisites: On `fix/` branch with changes.

Actions:
1. Run tests to verify fix
2. Create PR with standard format
3. Link Sentry issue in PR description

**PR format:**
```markdown
## Summary
[Fix description]

## Sentry Issue
- ID: ISSUE-ID
- Users affected: N
- First seen: DATE

## Test Plan
- [ ] Test case 1
- [ ] Test case 2
```

## Stage 4: Postmortem

**Command:** `/triage postmortem ISSUE-ID`

Prerequisites: Fix deployed (PR merged).

Actions:
1. Verify no new errors in Sentry
2. Generate postmortem document from template
3. Resolve Sentry issue
4. Create `docs/postmortems/YYYY-MM-DD-ISSUE-ID.md`

## Scripts

```bash
# Multi-source orchestrator
~/.claude/skills/triage/scripts/check_all_sources.sh

# Individual checks
~/.claude/skills/triage/scripts/check_sentry.sh
~/.claude/skills/triage/scripts/check_vercel_logs.sh
~/.claude/skills/triage/scripts/check_health_endpoints.sh

# Postmortem generator
~/.claude/skills/triage/scripts/generate_postmortem.sh ISSUE-ID
```

## Workflow

```
/triage
   |
   v
[Issues found?]
   |
   +-- Yes --> /triage investigate ISSUE-ID
   |              |
   |              v
   |           [Fix locally]
   |              |
   |              v
   |           /triage fix (creates PR)
   |              |
   |              v
   |           [PR merged & deployed]
   |              |
   |              v
   |           /triage postmortem ISSUE-ID
   |
   +-- No --> "All systems nominal"
```

## Environment Variables

```bash
# Required for Sentry
SENTRY_AUTH_TOKEN   # or SENTRY_MASTER_TOKEN
SENTRY_ORG          # Organization slug

# Auto-detected per project
SENTRY_PROJECT      # From .sentryclirc or .env.local

# Optional for Vercel
VERCEL_TOKEN        # For `vercel logs` access
```

## Reuses

- `~/.claude/skills/sentry-observability/scripts/triage_score.sh`
- `~/.claude/skills/sentry-observability/scripts/issue_detail.sh`
- `~/.claude/skills/sentry-observability/scripts/resolve_issue.sh`

## Related

- `observability` - Full observability setup
- `sentry-observability` - Sentry-specific operations
- `verify-fix` - Verification checklist
