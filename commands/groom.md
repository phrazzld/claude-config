---
description: Run all 12 grooming primitives → synthesize → create issues
---

# GROOM

Comprehensive backlog grooming across 12 perspectives.

No flags. No selective running. Always runs ALL primitives in parallel. Always comprehensive.

## What This Does

1. **Check existing backlog** — Don't duplicate
2. **Launch 12 agents** — Each examines codebase from specific lens
3. **Collect findings** — Each produces prioritized issue list
4. **Synthesize** — Cross-validate, identify patterns
5. **Create issues** — GitHub issues with labels and priorities

## Step 1: Check Existing Backlog

```bash
gh issue list --state open --limit 50
gh issue list --state closed --limit 20
```

## Step 2: Launch 12 Grooming Agents

Launch ALL in parallel via Task tool:

### Infrastructure & Code (5 agents)

| Agent | Prompt |
|-------|--------|
| groom-security | "Audit for security vulnerabilities: OWASP top 10, auth gaps, data exposure, injection points, secrets management. Include file:line. Output: prioritized security issues." |
| groom-performance | "Audit for performance issues: N+1 queries, bundle size, missing indexes, caching opportunities, memory leaks. Include file:line. Output: prioritized performance issues." |
| groom-code-quality | "Audit code health: complexity hotspots, duplication, test coverage gaps, type safety, code smells. Include file:line. Output: prioritized quality issues." |
| groom-architecture | "Audit system design: coupling, cohesion, module depth, abstraction quality, dependency direction. Include file:line. Output: prioritized architecture issues." |
| groom-infrastructure | "Audit DevOps: CI/CD gaps, monitoring blind spots, logging quality, deployment safety, scaling limits. Output: prioritized infra issues." |

### User Experience (2 agents)

| Agent | Prompt |
|-------|--------|
| groom-ux | "Audit user experience: friction points, confusing flows, accessibility issues, error messages, loading states. Output: prioritized UX issues." |
| groom-aesthetics | "Audit visual design: consistency, polish, spacing issues, typography problems, color usage. Output: prioritized design issues." |

### Business & Growth (5 agents)

| Agent | Prompt |
|-------|--------|
| groom-business | "Audit business value: revenue blockers, churn risks, competitive gaps, user retention issues. Output: prioritized business issues." |
| groom-product | "Audit product strategy: feature gaps, user pain points, roadmap alignment, market fit. Output: prioritized product issues." |
| groom-marketing | "Audit growth: SEO issues, conversion blockers, viral loop gaps, positioning problems. Output: prioritized marketing issues." |
| groom-sales | "Audit sales enablement: demo gaps, objection handling needs, case study opportunities. Output: prioritized sales issues." |
| groom-finance | "Audit financial health: cost optimization, margin issues, pricing problems. Output: prioritized finance issues." |

## Step 3: Synthesize Findings

Cross-validate agent findings:

| Signal | Priority |
|--------|----------|
| 3+ agents flag same area | **Critical** |
| Security + Business agree | Revenue-protecting |
| UX + Product + Marketing agree | User-facing |
| Code + Architecture + Infrastructure agree | Technical debt |

## Step 4: Create GitHub Issues

For each finding:

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

## Perspectives
[Which grooming agents flagged this]

---
🤖 Created by `/groom`
EOF
)" \
  --label "priority/medium,area/[perspective]"
```

## Step 5: Organize

After creating issues:
- Note dependencies (X blocks Y)
- Identify quick wins (high impact + low effort)
- Flag critical items needing immediate attention
- Group related issues

## Output

Summary report:
- Issues created/updated (count by perspective)
- Critical findings (multi-agent consensus)
- Quick wins identified
- Recommended focus order
