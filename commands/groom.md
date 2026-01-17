---
description: Analyze codebase and create GitHub Issues for improvements
---

# GROOM

> Complexity is the enemy. Find it. Flag it. File issues.

Go wide. Go deep. Create a comprehensive backlog of the most compelling work.

## Mission

Explore this codebase from multiple perspectives. Generate issues for everything worth doing. Let quality be the filter, not arbitrary limits.

## Process

### 1. Understand Current State

Check existing backlog first. Don't duplicate.

```bash
gh issue list --state open --limit 50
gh issue list --state closed --limit 20
```

### 2. Multi-Perspective Investigation

Launch agents in parallel to explore from different angles. Pick perspectives relevant to this project:

- **architecture-guardian** — module boundaries, coupling, complexity
- **security-sentinel** — vulnerabilities, auth, data protection
- **performance-pathfinder** — bottlenecks, queries, scalability
- **user-experience-advocate** — friction, accessibility, delight
- **test-strategy-architect** — coverage gaps, flaky tests, quality
- **maintainability-maven** — tech debt, naming, clarity
- **dependency-health-monitor** — outdated packages, vulnerabilities
- **infrastructure-guardian** — CI/CD, quality gates, deployment
- **config-auditor** — external service config, env vars, webhooks, API keys
- **observability-advocate** — logging coverage, monitoring gaps, alerting rules

Each agent explores autonomously, researches best practices, identifies specific improvements with file:line locations.

### 3. Synthesize and Ideate

Combine agent findings with your own analysis. Think broadly:

- What's causing friction for users?
- What's causing friction for developers?
- What patterns are fighting the codebase?
- What's obviously missing?
- What would make this codebase a joy to work in?
- What would make this product a joy to use?
- What external services are we integrating with?
- What happens when those services fail silently?
- Can we see what's happening in production?
- Would we know within minutes if something broke?

Generate ideas across all dimensions: performance, reliability, maintainability, security, UX, features, developer experience, infrastructure.

### 4. Evaluate Each Idea

For each potential issue, reason through:

- **Impact**: How much does this improve things? Who benefits?
- **Feasibility**: How confident are we? What's the risk?
- **Urgency**: Is this blocking other work? Time-sensitive?

Trust your judgment. If something feels compelling, it probably is.

### 5. Create Issues

File everything worth doing. Each issue should be:

- **Specific**: Clear what success looks like
- **Located**: File paths, line numbers when known
- **Sized**: Rough scope (tiny/small/medium/large)
- **Contextualized**: Why it matters, what's at risk

```bash
gh issue create \
  --title "Concise problem statement" \
  --body "$(cat <<'EOF'
## Problem
[What's wrong — be specific]

## Impact
[Why it matters — who's affected]

## Proposed Solution
[Suggested approach if obvious]

## Location
`path/file.ts:123` — [context]

---
🤖 Created by `/groom`
EOF
)" \
  --label "priority/medium,type/refactor"
```

### 6. Organize the Backlog

After creating issues:
- Note dependencies (X blocks Y)
- Identify quick wins (high impact + low effort)
- Flag critical items that need immediate attention
- Group related issues

## Labels

Use existing repo labels. Create if missing:

```bash
# Priority: critical, high, medium, low
# Type: bug, feature, refactor, docs, chore
# Size: xs, s, m, l, xl
# Area: security, performance, ux, architecture, testing
```

## Quality

Before finishing:
- Issues form coherent backlog (no contradictions)
- No duplicates of existing open issues
- Each issue is actionable with clear success criteria
- Quick wins are identified
