---
description: Analyze codebase and create GitHub Issues for improvements
---

# GROOM

> Complexity is the enemy. Find it. Flag it. File issues.

Analyze this codebase through multiple lenses. Create GitHub Issues for actionable improvements.

## Mission

Produce a prioritized backlog of GitHub Issues representing the most valuable improvements. Each issue: specific, actionable, properly labeled.

## Process

### 1. Understand Current State

**Check existing backlog first:**
```bash
# Get open issues
gh issue list --state open --limit 50

# Get recent closed issues (context)
gh issue list --state closed --limit 20

# Check project boards if any
gh project list 2>/dev/null || echo "No projects"
```

**Understand what's already planned.** Don't duplicate. Build on existing work.

### 2. Multi-Perspective Investigation

Launch parallel subagents to investigate from different angles. Each agent should:
- Explore the codebase autonomously
- Research best practices via web search
- Identify specific, actionable improvements
- Return findings with file:line locations

**Agent perspectives to consider** (choose based on project needs):

| Perspective | Focus | Agent Type |
|-------------|-------|------------|
| Architecture | Module boundaries, coupling, complexity | architecture-guardian |
| Security | Vulnerabilities, auth, input validation | security-sentinel |
| Performance | Bottlenecks, queries, bundle size | performance-pathfinder |
| UX/Product | User friction, missing features, delight | user-experience-advocate |
| Testing | Coverage gaps, test quality, flaky tests | test-strategy-architect |
| Maintainability | Tech debt, naming, documentation | maintainability-maven |
| Dependencies | Outdated packages, vulnerabilities | dependency-health-monitor |
| Infrastructure | CI/CD, quality gates, deployment | infrastructure-guardian |

**Don't use all of them.** Pick 3-5 most relevant based on what you learn about the project.

### 3. Clarifying Questions (Organic)

After initial investigation, ask questions that actually matter based on what you found.

**Trust your judgment.** If you discovered:
- A security concern → ask about threat model, user data sensitivity
- Performance issues → ask about scale expectations, SLAs
- Architecture sprawl → ask about team structure, ownership
- Missing tests → ask about deployment confidence, failure tolerance
- Product gaps → ask about roadmap, user feedback

**Don't ask generic questions.** Ask about what you actually need to know to prioritize effectively.

### 4. Iterate on Investigation

Based on user answers, go deeper where needed:
- Spawn additional focused agents
- Do targeted web research on specific problems
- Examine specific files/modules in detail
- Cross-reference with existing issues

### 5. Synthesize and Create Issues

**Before filing:**
- Deduplicate against existing open issues
- Group related findings into coherent issues
- Assess impact vs effort for prioritization
- Consider dependencies between issues

**File to GitHub** with appropriate labels.

## Labels

Use existing repo labels when available. Create these if missing:

```bash
# Priority
gh label create "priority/critical" -c "d73a4a" -d "Drop everything"
gh label create "priority/high" -c "ff6b6b" -d "This sprint"
gh label create "priority/medium" -c "ffd93d" -d "Next sprint"
gh label create "priority/low" -c "6bcb77" -d "Backlog"

# Type
gh label create "type/bug" -c "d73a4a"
gh label create "type/feature" -c "0075ca"
gh label create "type/refactor" -c "7057ff"
gh label create "type/docs" -c "0e8a16"
gh label create "type/chore" -c "bfd4f2"

# Area (add as needed)
gh label create "area/security" -c "d73a4a"
gh label create "area/performance" -c "ff9f1c"
gh label create "area/ux" -c "a855f7"
gh label create "area/architecture" -c "6366f1"
gh label create "area/testing" -c "10b981"

# Size
gh label create "size/xs" -c "c5def5" -d "< 1 hour"
gh label create "size/s" -c "c5def5" -d "1-4 hours"
gh label create "size/m" -c "bfd4f2" -d "1-2 days"
gh label create "size/l" -c "d4c5f9" -d "3-5 days"
gh label create "size/xl" -c "f9d0c4" -d "1+ week (consider splitting)"
```

## Issue Format

```bash
gh issue create \
  --title "Concise problem statement" \
  --body "$(cat <<'EOF'
## Problem
[What's wrong — be specific]

## Impact
[Why it matters — who's affected, what's at risk]

## Proposed Solution
[Optional: suggested approach if obvious]

## Location
`path/file.ts:123` — [brief context]

## References
- [Link to related issues, docs, or discussions]

---
🤖 Created by `/groom`
EOF
)" \
  --label "priority/medium,type/refactor,area/architecture,size/m"
```

## Quality Bar

**Before filing each issue:**
- [ ] Not a duplicate of existing open issue
- [ ] Actionable: clear what success looks like
- [ ] Right-sized: XL issues should be epics with sub-issues
- [ ] Has location: specific files/lines, not vague areas
- [ ] Has impact: explains why it matters

**Before finishing groom session:**
- [ ] Issues form coherent backlog (no contradictions)
- [ ] Dependencies noted (X blocks Y)
- [ ] Quick wins identified (high impact + low effort)
- [ ] User validated priorities match their needs
