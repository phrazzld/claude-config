---
description: Full autonomous delivery from issue to PR
argument-hint: "[issue-id]"
---

# AUTOPILOT

> From issue to PR in one command.

Assumes backlog is groomed. Run `/groom` first if needed.

## Argument

- `issue-id` — Optional. If provided, work on that issue. If omitted, find highest-priority open issue labeled `ready`.

## Role

You are the engineering lead running a sprint. You find work, ensure it's ready, delegate implementation, and ship.

Codex implements. You orchestrate.

## Workflow

### 1. Find Issue

If `$1` provided:
```bash
gh issue view $1 --comments
```

If no argument:
```bash
gh issue list --label "status/ready" --limit 10
```
Select ONE based on: `horizon/now` > `horizon/next` > blocking others > clear scope.

### 2. Spec

Read issue comments. If no `## Product Spec` section:
```
/spec $ISSUE
```

### 3. Design

Read issue comments. If no `## Technical Design` section:
```
/architect $ISSUE
```

### 4. Build

```
/build $ISSUE
```
Handles: branching, implementation (Codex), commits.

### 5. Refine

```
/refactor
/update-docs
```

### 6. Ship

```
/pr
```
Ensures PR references issue with `Closes #N`.

## Stopping Conditions

Stop and report if:
- No `status/ready` issues found (run `/groom` first)
- Issue is blocked by another issue
- Build fails repeatedly
- Scope unclear (needs user clarification)

## Output

Report: issue worked, spec status, design status, commits made, PR URL.
