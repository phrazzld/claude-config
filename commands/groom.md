---
description: Analyze codebase and create GitHub Issues for improvements
---

# GROOM

> Complexity is the enemy. Find it. Flag it. File issues.

Analyze this codebase through multiple lenses: architecture, security, performance, UX, product opportunity. Create GitHub Issues for actionable improvements.

## Mission

Produce a prioritized set of GitHub Issues representing the most valuable improvements to this codebase. Each issue should be specific, actionable, and properly labeled.

## Process

1. **Interview**: Understand user context and priorities first
2. **Explore**: Understand the codebase structure, patterns, and pain points
3. **Analyze**: Examine from multiple perspectives (spawn subagents as beneficial)
4. **Synthesize**: Deduplicate findings, assess impact vs effort
5. **Create Issues**: File to GitHub with appropriate labels

## Interview Phase

Before analyzing, understand user context to focus the audit.

Use AskUserQuestion with batched polls (2-4 options each, up to 4 questions per batch):

**Context** — Current state:
- What's been frustrating you lately? (free-form)
- Areas to focus on? (multiSelect: security/perf/ux/architecture/testing)
- Areas to skip? (multiSelect: specific modules)

**Priorities** — Constraints:
- Development phase? (prototype/growth/mature)
- Team size? (solo/small/large)
- Timeline pressure? (urgent/normal/relaxed)

Weight analysis by user priorities. Skip areas user marks as low-priority.

## Labels

Use this taxonomy (create labels if missing via `gh label create`):

- `horizon/now|next|soon|later` — urgency
- `type/bug|feature|refactor|docs|chore` — nature
- `category/security|performance|ux|architecture|testing` — domain
- `perspective/grug|carmack|ousterhout|jobs|fowler|beck|torvalds` — who flagged it
- `effort/s|m|l|xl` — size estimate

When multiple perspectives flag the same issue, add `consensus/high-priority`.

## Issue Format

```bash
gh issue create \
  --title "[Category] Concise problem statement" \
  --body "## Problem
[What's wrong]

## Impact
[Why it matters]

## Location
\`path/file.ts:123\`" \
  --label "horizon/now,category/security,type/bug,effort/s,perspective/grug"
```

## Quality Bar

- Every issue is actionable (clear what to do)
- Issues are properly sized (xl → consider sub-issues)
- No duplicates of existing open issues
- High-impact items in horizon/now
