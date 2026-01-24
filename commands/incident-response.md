---
description: Investigate → fix → postmortem → prevent
argument-hint: <bug-report>
---

# INCIDENT-RESPONSE

> Fix the fire. Then prevent the next one.

Full incident lifecycle from bug report to prevention.

## Argument

- `bug-report` — Error message, logs, user report, or description of the problem

## Branching

Assumes you start on `master`/`main`. Before fixing, create a branch:

```bash
BRANCH="fix/incident-$(date +%Y%m%d-%H%M)"
git checkout -b $BRANCH
```

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

### 2. Branch

If on `master`/`main`, create fix branch:
```bash
git checkout -b fix/incident-$(date +%Y%m%d-%H%M)
```

### 3. Fix

```
/fix "Root cause from investigation"
```

Diagnose → delegate to Codex → verify → commit.

### 4. Verify

Demand observable proof:
- Log entry showing fix worked
- Metric that changed
- Database state confirming resolution

Mark **UNVERIFIED** until observables confirm. Never trust "should work."

### 5. Postmortem

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

### 6. Prevent

If postmortem reveals systemic issue:

```bash
gh issue create --title "Prevent: [class of incident]" \
  --body "## From Postmortem\n[Link to postmortem]\n\n## Prevention\n[What to build]"
```

Then optionally:
```
/autopilot $PREVENTION_ISSUE
```

### 7. Codify Learning

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
