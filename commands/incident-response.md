---
description: Investigate → fix → postmortem → prevent
argument-hint: <bug-report>
---

# INCIDENT-RESPONSE

> Fix the fire. Then prevent the next one.

Full incident lifecycle from bug report to prevention.

## Argument

- `bug-report` — Error message, logs, user report, or description of the problem

## Workflow

### 1. Investigate

```
/investigate $ARGUMENTS
```

Creates `INCIDENT-{timestamp}.md` with:
- Timeline
- Evidence
- Hypotheses
- Root cause

### 2. Fix

```
/fix "Root cause from investigation"
```

Diagnose → delegate to Codex → verify → commit.

### 3. Verify

Demand observable proof:
- Log entry showing fix worked
- Metric that changed
- Database state confirming resolution

Mark **UNVERIFIED** until observables confirm. Never trust "should work."

### 4. Postmortem

```
/postmortem
```

Creates blameless postmortem:
- Summary
- Timeline
- Root cause
- 5 Whys
- What went well/wrong
- Follow-up actions

### 5. Prevent

If postmortem reveals systemic issue:

```bash
gh issue create --title "Prevent: [class of incident]" \
  --body "## From Postmortem\n[Link to postmortem]\n\n## Prevention\n[What to build]"
```

Then optionally:
```
/autopilot $PREVENTION_ISSUE
```

### 6. Codify Learning

```
/codify-learning
```

Transform incident into:
- Regression test
- Agent update
- Monitoring rule
- Documentation

## Output

Report: incident resolved, postmortem filed, prevention issue created (if applicable).
