---
name: groom
description: |
  Comprehensive backlog grooming. Orchestrates issue-creator skills and agents.
  Creates prioritized GitHub issues across all domains.
  No flags. Always comprehensive.
---

# /groom

Orchestrate comprehensive backlog grooming. Create prioritized issues across all domains.

## Philosophy

**Orchestrator pattern.** /groom invokes skills, doesn't reimplement logic.

**Unix philosophy.** Small, focused skills that compose. Investigate ≠ Fix.

**No flags.** Always runs full audit. Always creates issues.

## What This Does

1. **Gather vision** — Single open-ended question about product direction
2. **Run issue-creator skills** — Each domain gets audited, issues created
3. **Adaptive agent analysis** — Based on backlog size, run specialized agents
4. **Dedupe & consolidate** — Remove duplicates, update existing issues
5. **Summarize** — Report P0/P1/P2/P3 counts and recommended focus

## Priority System

```
🔴 P0: CRITICAL PRODUCTION BUGS
   └─ Errors actively breaking production
   └─ Critical security vulnerabilities

🟠 P1: FUNDAMENTALS (Foundation)
   ├─ Testing (coverage, quality gates)
   ├─ Documentation (README, architecture)
   ├─ Quality gates (hooks, CI/CD)
   ├─ Observability (logging, error tracking)
   └─ Working prototype (not stubs)

🟡 P2: LAUNCH READINESS
   ├─ Compelling landing page
   ├─ Boutique onboarding
   ├─ Stripe monetization
   └─ Viral growth infrastructure

🟢 P3+: EVERYTHING ELSE
   └─ Innovation, polish, strategic improvements

⚠️  SECURITY: Own severity scale
   Critical → P0, High → P1, Medium → P2, Low → P3
```

## Process

### Step 1: Gather Vision

Use AskUserQuestion with single open-ended prompt:

```
What's your vision for this product? Where should it go?
```

Store response as `{vision}` for agent context.

### Step 2: Check Existing Backlog

```bash
gh issue list --state open --limit 100 --json number,title,labels
```

### Step 3: Run Issue-Creator Skills

Invoke in sequence (each creates GitHub issues):

| Skill | Domain | Priority Range |
|-------|--------|----------------|
| `/log-production-issues` | Production health | P0-P3 |
| `/log-quality-issues` | Tests, CI/CD, hooks | P0-P3 |
| `/log-doc-issues` | Documentation | P0-P3 |
| `/log-observability-issues` | Monitoring, logging | P0-P3 |
| `/log-stripe-issues` | Payments | P0-P3 |
| `/log-virality-issues` | Sharing, referrals | P0-P3 |
| `/log-landing-issues` | Landing page | P0-P3 |
| `/log-onboarding-issues` | New user experience | P0-P3 |

**Why invoke skills, not reimplement?**
- Each skill has deep domain knowledge
- Consistent output format
- Can be run independently
- Easy to update without changing groom

### Step 4: Adaptive Agent Analysis

After issue creation, count by priority:

```bash
p0_count=$(gh issue list --label priority/p0 --state open --json number | jq length)
p1_count=$(gh issue list --label priority/p1 --state open --json number | jq length)
total=$((p0_count + p1_count))
```

**Heavy backlog (P0+P1 > 15):**
Run only core agents:
- `security-sentinel` — Security vulnerabilities
- `architecture-guardian` — Structural issues

**Medium backlog (P0+P1 = 5-15):**
Add creative agents:
- `aesthetician` — Visual excellence
- `pioneer` — Innovation opportunities
- `visionary` — Vision acceleration (receives `{vision}`)

**Light backlog (P0+P1 < 5):**
Full suite:
- `product-visionary` — Feature opportunities
- `user-experience-advocate` — UX improvements

Each agent receives `{vision}` context and creates additional issues.

### Step 5: Dedupe & Consolidate

Review created issues for duplicates:

```bash
# Find potential duplicates (similar titles)
gh issue list --state open --json number,title,labels | jq '.[] | .title' | sort | uniq -d
```

For each duplicate:
- Close older issue with link to newer
- Or update existing issue with new findings

### Step 6: Summarize

Output final report:

```
GROOM SUMMARY
=============

Issues by Priority:
- P0 (Critical): 2
- P1 (Essential): 8
- P2 (Important): 12
- P3 (Nice to Have): 5

Issues by Domain:
- Production: 2
- Quality: 3
- Docs: 2
- Observability: 3
- Stripe: 2
- Virality: 4
- Landing: 3
- Onboarding: 3
- Security: 2 (from agents)
- Other: 3 (from agents)

Recommended Focus Order:
1. [P0] Fix production payment failures
2. [P0] Patch security vulnerability
3. [P1] Add test coverage
4. [P1] Configure Sentry
...

View all: gh issue list --state open
View P0: gh issue list --label priority/p0
```

## Agent Prompts

### Security (Always Run)

```
Audit for security vulnerabilities: OWASP top 10, auth gaps,
data exposure, injection points, secrets management.
Include file:line. Output: prioritized security issues as GitHub issues.
```

### Architect (Always Run)

```
Audit system design: coupling, cohesion, module depth,
abstraction quality, dependency direction.
Include file:line. Output: prioritized architecture issues as GitHub issues.
```

### Aesthetician (Medium+ Backlog)

```
Audit visual design: distinctiveness, craft, trends, typography,
color sophistication, motion quality.
Focus: "Does this make people gasp?"
Output: prioritized design issues as GitHub issues.
```

### Pioneer (Medium+ Backlog)

```
Explore innovation opportunities: AI/LLM integration, Gordian knot
solutions, emerging tech, pattern modernization.
Output: prioritized R&D opportunities as GitHub issues.
```

### Visionary (Medium+ Backlog)

```
The user shared this vision:
{vision}

Accelerate this vision. Find gaps, blockers, accelerators.
100% aligned with stated goals.
Output: prioritized vision-alignment actions as GitHub issues.
```

## Issue Format

All issues created by /groom (via skills or agents):

```markdown
## Title
[P{0-3}] Clear, actionable description

## Labels
- priority/p0|p1|p2|p3
- domain/production|quality|docs|observability|stripe|virality|landing|onboarding|security|architecture|design|innovation
- type/bug|enhancement|chore

## Body
### Problem
What's wrong or missing

### Impact
Why this matters (user impact, risk, blocked work)

### Suggested Fix
Concrete next steps or skill to run

### Source
Which skill or agent identified this

---
Created by `/groom`
```

## What You Get

After running /groom:
- Complete issue backlog in GitHub
- Issues prioritized P0-P3
- Issues labeled by domain
- Issues with actionable next steps
- Duplicates removed
- Summary of recommended focus

User can:
- See all work in GitHub Issues
- Filter by priority: `label:priority/p0`
- Filter by domain: `label:domain/stripe`
- Assign and track progress
- Run `/fix-*` skills to address issues

## Related Skills

### Primitives (Investigate)
- `/check-production`, `/check-docs`, `/check-quality`, `/check-observability`
- `/check-stripe`, `/check-virality`, `/check-landing`, `/check-onboarding`

### Issue Creators (Document)
- `/log-production-issues`, `/log-doc-issues`, `/log-quality-issues`
- `/log-observability-issues`, `/log-stripe-issues`, `/log-virality-issues`
- `/log-landing-issues`, `/log-onboarding-issues`

### Fixers (Act)
- `/triage`, `/fix-docs`, `/fix-quality`, `/fix-observability`
- `/fix-stripe`, `/fix-virality`, `/fix-landing`, `/fix-onboarding`

## Running Individual Domains

Don't want full groom? Run specific skills:

```bash
/check-production     # Audit only, no issues
/log-production-issues # Create issues, no fixes
/triage              # Fix highest priority

/check-stripe        # Audit only
/log-stripe-issues   # Create issues
/fix-stripe          # Fix highest priority
```
