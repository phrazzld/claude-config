---
name: groom
description: |
  Comprehensive backlog grooming. Orchestrates issue-creator skills and agents.
  Creates prioritized GitHub issues across all domains.
  Uses Gemini, Kimi, Codex, and Thinktank to flesh out issues with research,
  implementation recommendations, and multi-perspective validation.
  Enforces Misty Step org-wide standards: canonical labels, issue types,
  milestones, and project linking.
  No flags. Always comprehensive.
effort: high
---

# /groom

Orchestrate comprehensive backlog grooming. Create prioritized issues across all domains.

## Philosophy

**Orchestrator pattern.** /groom invokes skills, doesn't reimplement logic.

**Unix philosophy.** Small, focused skills that compose. Investigate ≠ Fix.

**AI-augmented analysis.** External AI tools provide specialized capabilities:
- **Gemini** — Web-grounded research, current best practices, huge context
- **Kimi** — Frontend/visual expertise, Agent Swarm for parallel analysis
- **Codex** — Implementation recommendations, concrete code suggestions
- **Thinktank** — Multi-model consensus, diverse expert perspectives

**No flags.** Always runs full audit. Always creates issues.

## Misty Step Org-Wide Standards (MANDATORY)

Every issue created or modified by /groom MUST comply with these standards.
These apply to ALL repositories in the misty-step organization.

### Canonical Label Taxonomy

Labels are enforced org-wide. Use ONLY these labels (plus repo-specific `domain/` labels).
Legacy labels (`priority/p0`, `P0`, `priority:p0`, `type/bug`, `type:bug`, etc.) are deprecated.

**Priority** (exactly one required):
- `p0` — Critical: production broken or security vulnerability
- `p1` — Essential: foundation and fundamentals
- `p2` — Important: launch readiness
- `p3` — Nice to have: polish and innovation

**Type** (exactly one required):
- `bug` — Something isn't working
- `feature` — New capability or behavior
- `task` — Implementation work item
- `refactor` — Code improvement without behavior change
- `research` — Investigation or spike
- `epic` — Large multi-issue initiative

**Horizon** (exactly one required):
- `now` — Current sprint focus
- `next` — Next sprint candidate
- `later` — Backlog, not yet scheduled
- `blocked` — Waiting on external dependency

**Effort** (recommended):
- `effort/s` — Less than a day
- `effort/m` — 1-3 days
- `effort/l` — 3-5 days
- `effort/xl` — More than a week

**Source** (exactly one required for groom-created issues):
- `source/groom` — Created by /groom skill
- `source/user` — Reported by user observation
- `source/agent` — Created by AI agent

**Domain** (at least one, repo-specific):
- `domain/{name}` — e.g., `domain/api`, `domain/infra`, `domain/security`
- These vary per repo and that's expected

### Issue Types (GitHub native)

Every issue MUST have an issue type set via GraphQL. Available types:
- **Bug** (node_id: `IT_kwDODnuAzs4Bxgbl`) — For bugs
- **Task** (node_id: `IT_kwDODnuAzs4Bxgbk`) — For tasks, refactors, research
- **Feature** (node_id: `IT_kwDODnuAzs4Bxgbm`) — For features

Set issue type after creation:
```bash
# Get issue node ID
ISSUE_ID=$(gh api graphql -f query='{ repository(owner: "misty-step", name: "REPO") { issue(number: NUM) { id } } }' --jq '.data.repository.issue.id')

# Set issue type
gh api graphql -f query="mutation { updateIssue(input: { id: \"$ISSUE_ID\", issueTypeId: \"TYPE_NODE_ID\" }) { issue { number issueType { name } } } }"
```

Map label type → issue type:
- `bug` label → Bug issue type
- `feature` label → Feature issue type
- `task`, `refactor`, `research`, `epic` labels → Task issue type

### Milestones (REQUIRED)

Every issue MUST be assigned to a milestone. If the repo has no milestones:
1. Create a "Backlog" milestone (no due date) for unscheduled work
2. Create milestone(s) for current work based on vision.md focus

```bash
# Check existing milestones
gh api "/repos/misty-step/REPO/milestones" --jq '.[].title'

# Create milestone if needed
gh api -X POST "/repos/misty-step/REPO/milestones" -f title="Backlog" -f description="Unscheduled work items"

# Assign issue to milestone
gh issue edit NUM --milestone "Milestone Name"
```

Rules:
- `now` horizon issues → current sprint/active milestone
- `next` horizon issues → next milestone or "Backlog"
- `later` horizon issues → "Backlog" or "Someday"
- `blocked` issues → keep in their target milestone

### Org-Level Projects

Three org-level GitHub Projects exist. Link issues to them as appropriate:
- **Active Sprint** — Issues with `now` horizon
- **Product Roadmap** — All `p0`, `p1`, `p2` issues across repos
- **Triage Inbox** — New issues pending classification

After creating issues, add high-priority ones to the relevant project:
```bash
# Add to project (get project number first)
gh project item-add PROJECT_NUMBER --owner misty-step --url "https://github.com/misty-step/REPO/issues/NUM"
```

### Label Migration (during backlog audit)

When auditing existing issues (Step 3), migrate legacy labels:
```bash
# Example: migrate priority/p0 → p0
gh issue edit NUM --remove-label "priority/p0" --add-label "p0"
gh issue edit NUM --remove-label "P0" --add-label "p0"
gh issue edit NUM --remove-label "priority:p0" --add-label "p0"

# Example: migrate type/bug → bug
gh issue edit NUM --remove-label "type/bug" --add-label "bug"
gh issue edit NUM --remove-label "type:bug" --add-label "bug"

# Add missing required labels (horizon, source)
gh issue edit NUM --add-label "later" # if no horizon set
```

## What This Does

1. **Load or gather vision** — Check vision.md or ask about product direction
2. **Capture what's on your mind** — Bugs, UX friction, nitpicks from using the app
3. **Audit existing backlog** — Validate, reprioritize, close stale issues
4. **Run issue-creator skills** — Each domain gets audited, issues created
5. **AI-assisted enrichment** — Gemini, Kimi, Codex, Thinktank flesh out issues
6. **Adaptive agent analysis** — Based on backlog size, run specialized agents
7. **Dedupe & consolidate** — Merge duplicates, finalize issue set
8. **Summarize** — Report P0/P1/P2/P3 counts and recommended focus

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
   ├─ Product standards (version, attribution, contact)
   └─ Working prototype (not stubs)

🟡 P2: LAUNCH READINESS
   ├─ Compelling landing page
   ├─ Boutique onboarding
   ├─ Stripe monetization
   ├─ Viral growth infrastructure
   └─ Marketing readiness (demo video, brand profile, analytics, distribution prep)

**Marketing Readiness checks:**
- Demo video exists (30-60s screen recording)
- brand-profile.yaml configured
- PostHog events defined (signup, activation, [core_action])
- Distribution drafts prepared (Twitter, Reddit, HN)

🟢 P3+: EVERYTHING ELSE
   └─ Innovation, polish, strategic improvements

⚠️  SECURITY: Own severity scale
   Critical → P0, High → P1, Medium → P2, Low → P3
```

## Process

### Step 1: Load or Gather Vision

Vision should persist across sessions. Check for `vision.md` in project root:

```bash
[ -f "vision.md" ] && echo "Vision found" || echo "No vision.md"
```

**If vision.md exists:**
1. Read and display current vision
2. Ask: "Is this still accurate? Any updates?"
3. If updates provided, rewrite vision.md

**If vision.md doesn't exist:**
1. Ask open-ended question:
   ```
   What's your vision for this product? Where should it go?
   ```
2. Write response to `vision.md`

**vision.md format:**
```markdown
# Vision

## One-Liner
[Single sentence: what this product is and who it's for]

## North Star
[The dream state - what does success look like in 2 years?]

## Key Differentiators
[What makes this different from alternatives?]

## Target User
[Who specifically is this for? Be concrete.]

## Current Focus
[What's the immediate priority this quarter?]

---
*Last updated: YYYY-MM-DD*
*Updated during: /groom session*
```

Store content as `{vision}` for agent context throughout session.

**Why persist vision?**
- Vision shouldn't change dramatically between sessions
- Agents get consistent context
- Creates documentation artifact
- Enables other skills to reference it

### Step 2: Capture What's On Your Mind

Before structured analysis, ask:

```
Anything on your mind? Bugs you've noticed, UX friction, missing features,
nitpicks while using the app? These become issues alongside the automated findings.

(Skip if nothing comes to mind)
```

**What this captures:**
- Bugs encountered during manual testing
- UX friction points noticed while using the app
- Missing features that became obvious
- "Why doesn't this..." observations
- Quality-of-life improvements
- Things that annoyed you today

**For each item provided:**
1. Clarify if needed (one follow-up max)
2. Assign tentative priority based on description
3. Create as GitHub issue with `source: user-observation` tag
4. Include in final summary

**Why this step matters:**
- User has context automation doesn't (how it *feels* to use the app)
- Catches issues that slip through automated checks
- Captures the "I keep meaning to file this" backlog
- Makes groom feel collaborative, not just audit

**Format for user-submitted issues:**

```markdown
## Title
[P{0-3}] {user's description, cleaned up}

## Labels (canonical)
- p{n}                  (priority)
- bug|feature|task      (type — infer from description)
- now|next|later        (horizon — based on urgency)
- source/user           (source)
- domain/{best-fit}     (domain)

## Issue Type
Set via GraphQL after creation (Bug/Task/Feature)

## Milestone
Assign to current active milestone or "Backlog"

## Body
### Problem
{user's observation}

### Context
Reported during /groom session

---
Created by `/groom` (user observation)
```

### Step 3: Audit Existing Backlog

**Critical:** Existing issues are not sacred. They may be stale, irrelevant, misprioritized, or duplicative. Every issue must be validated.

```bash
gh issue list --state open --limit 100 --json number,title,labels,body,createdAt,updatedAt
```

**For each existing issue, evaluate:**

1. **Still relevant?** Does this issue still matter given current vision and codebase state?
   - If NO → Close with explanation
   - If UNCERTAIN → Flag for user confirmation

2. **Priority correct?** Given current vision.md focus, is the priority right?
   - Re-prioritize if focus has shifted
   - P0 from 6 months ago may be P3 now

3. **Description accurate?** Does the issue still describe the actual problem?
   - Update if codebase has changed
   - Flesh out if too vague to act on

4. **Duplicate?** Is this covered by another issue or will be covered by new findings?
   - Consolidate into single issue
   - Close duplicate with link to canonical

5. **Actionable?** Can someone pick this up and know what to do?
   - Add concrete next steps if missing
   - Break down if too large

**Actions to take:**

```bash
# Close irrelevant issue
gh issue close 123 --comment "Closing: no longer relevant. [reason]"

# Update priority
gh issue edit 123 --remove-label "priority/p1" --add-label "priority/p3"

# Update description
gh issue edit 123 --body "Updated description..."

# Close as duplicate
gh issue close 123 --comment "Duplicate of #456"
```

**Output from this step:**
- List of issues kept (with any priority/description changes)
- List of issues closed (with reasons)
- List of issues to consolidate with new findings

This prevents backlog bloat and ensures the backlog reflects current reality.

### Team-Accelerated Grooming (Default)

Steps 4-6 run as an agent team for parallel execution:

**Lead (you):** Coordinates team, handles Steps 1-3 and 7-8 directly.
Switch to delegate mode (Shift+Tab) before spawning.

**Spawn teammates by domain cluster:**

| Teammate | Skills/Tasks | Focus |
|----------|-------------|-------|
| **Infra** | log-production, log-quality, log-observability | P0-P1 foundation |
| **Docs & Standards** | log-doc, log-product-standards | Documentation gaps |
| **Payments** | log-stripe, log-bitcoin, log-lightning | Revenue infrastructure |
| **Growth** | log-virality, log-landing, log-onboarding | User acquisition/activation |
| **AI Enrichment** | Gemini research, Codex implementation recs | Issue enrichment |
| **Agents** | security-sentinel, architecture-guardian, etc. | Adaptive analysis |

Teammates share findings via messages. When Infra finds a P0, Growth teammate
can check if it affects onboarding. When Payments finds a Stripe issue,
AI Enrichment can research best practices immediately.

After all teammates finish, lead runs dedup (Step 7) and summary (Step 8).

**Fallback:** If team creation fails (experimental feature), fall back to
sequential skill invocation (current behavior).

### Step 4: Run Issue-Creator Skills

Invoke in sequence (each creates GitHub issues):

| Skill | Domain | Priority Range |
|-------|--------|----------------|
| `/log-production-issues` | Production health | P0-P3 |
| `/log-quality-issues` | Tests, CI/CD, hooks | P0-P3 |
| `/log-doc-issues` | Documentation | P0-P3 |
| `/log-observability-issues` | Monitoring, logging | P0-P3 |
| `/log-product-standards-issues` | Version, attribution, contact | P1 |
| `/log-stripe-issues` | Stripe payments | P0-P3 |
| `/log-bitcoin-issues` | Bitcoin on-chain | P0-P3 |
| `/log-lightning-issues` | Lightning Network | P0-P3 |
| `/log-virality-issues` | Sharing, referrals | P0-P3 |
| `/log-landing-issues` | Landing page | P0-P3 |
| `/log-onboarding-issues` | New user experience | P0-P3 |

**Why invoke skills, not reimplement?**
- Each skill has deep domain knowledge
- Consistent output format
- Can be run independently
- Easy to update without changing groom

### Step 5: AI-Assisted Issue Enrichment

After basic issue creation, use external AI tools to flesh out issues with deeper analysis.

**Why external tools?**
- **Gemini**: Web-grounded research for current best practices, framework docs
- **Kimi**: Frontend/visual expertise, can coordinate sub-agents for UI issues
- **Codex**: Implementation recommendations, concrete code suggestions
- **Thinktank**: Multi-model consensus for architecture/design decisions

**Run enrichment by domain:**

```bash
# 1. Gemini: Research current best practices for flagged issues
gemini "Review these issues and research current best practices:
$(gh issue list --label task --label domain/quality --state open --json title,number --jq '.[] | "#\(.number): \(.title)"')

For each issue, provide:
- Current industry best practices (2024-2025)
- Recommended tools/libraries
- Common pitfalls to avoid

Be specific and cite sources."

# 2. Kimi: Analyze frontend/visual issues with Agent Swarm
kimi "Analyze the UI/UX issues in this codebase:
$(gh issue list --label domain/landing,domain/onboarding --state open --json title,number --jq '.[] | "#\(.number): \(.title)"')

For each issue:
- Assess current implementation quality
- Suggest specific visual improvements
- Recommend component patterns" --thinking

# 3. Codex: Generate implementation recommendations
codex "For these technical issues, provide concrete implementation steps:
$(gh issue list --label p0 --label p1 --state open --json title,number,body --jq '.[:5] | .[] | "### #\(.number): \(.title)\n\(.body)\n"')

For each:
- Specific files to modify
- Code patterns to follow
- Test cases needed" --full-auto

# 4. Thinktank: Multi-perspective validation for architecture issues
thinktank "Evaluate these architecture decisions:
$(gh issue list --label domain/architecture --state open --json title,body --jq '.[] | "## \(.title)\n\(.body)\n"')

Provide:
- Consensus recommendation
- Dissenting opinions worth considering
- Risk assessment" ./src --synthesis
```

**Update issues with findings:**

```bash
# Append Gemini research to issue body
gh issue edit {number} --body "$(gh issue view {number} --json body --jq .body)

---
## Research (Gemini)
{gemini_findings}"

# Add implementation notes from Codex
gh issue comment {number} --body "## Implementation Recommendations (Codex)
{codex_recommendations}"

# Add architecture review from Thinktank
gh issue comment {number} --body "## Architecture Review (Thinktank)
{thinktank_synthesis}"
```

**When to run which tool:**

| Issue Domain | Primary Tool | Why |
|--------------|--------------|-----|
| Quality, Docs, Observability | Gemini | Needs current best practices research |
| Landing, Onboarding, Design | Kimi | Visual/frontend expertise |
| Security, Architecture | Thinktank | Needs multi-perspective validation |
| All P0/P1 technical issues | Codex | Implementation recommendations |

### Step 6: Adaptive Agent Analysis

After issue enrichment, count by priority:

```bash
p0_count=$(gh issue list --label p0 --state open --json number | jq length)
p1_count=$(gh issue list --label p1 --state open --json number | jq length)
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

### Step 7: Dedupe & Consolidate

**Three sources of duplicates:**
1. User observations (Step 2) may overlap with automated findings
2. New issues from Steps 4-5 that overlap with each other
3. New issues that overlap with existing issues kept from Step 3

**Find duplicates:**

```bash
# Find potential duplicates (similar titles)
gh issue list --state open --json number,title,labels | jq '.[] | .title' | sort | uniq -d

# Review issues flagged for consolidation in Step 3
# These were marked as "consolidate with new findings"
```

**For each duplicate set:**
- Keep the most comprehensive issue
- Close others with link to canonical: `gh issue close 123 --comment "Consolidated into #456"`
- Merge unique details from closed issues into the kept issue

**For issues to consolidate from Step 3:**
- If new findings cover the same ground → close old, reference new
- If new findings add to old → update old issue with new details
- If old issue is more comprehensive → close new, reference old

**Final pass (org-wide standards compliance):**
- Verify all open issues have exactly one priority label (p0/p1/p2/p3)
- Verify all open issues have exactly one type label (bug/feature/task/refactor/research/epic)
- Verify all open issues have exactly one horizon label (now/next/later/blocked)
- Verify all open issues have at least one domain label (domain/*)
- Verify all open issues have a source label (source/groom, source/user, source/agent)
- Verify all open issues have a milestone assigned
- Verify all open issues have issue type set (Bug/Task/Feature)
- Migrate any legacy labels found during audit (priority/p0 → p0, P0 → p0, etc.)

### Step 8: Summarize

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
View P0: gh issue list --label p0
View now: gh issue list --label now
View bugs: gh issue list --label bug
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
Read vision.md for the user's product vision.

Accelerate this vision. Find gaps, blockers, accelerators.
100% aligned with stated goals.
Output: prioritized vision-alignment actions as GitHub issues.
```

## Issue Format

All issues created by /groom (via skills or agents) MUST comply with org-wide standards:

```markdown
## Title
[P{0-3}] Clear, actionable description

## Labels (canonical — no legacy formats)
- p0|p1|p2|p3                    (priority — exactly one)
- bug|feature|task|refactor|research|epic  (type — exactly one)
- now|next|later|blocked          (horizon — exactly one)
- effort/s|m|l|xl                 (effort — recommended)
- source/groom|source/user|source/agent  (source — exactly one)
- domain/{name}                   (domain — at least one, repo-specific)

## Issue Type (GitHub native — set via GraphQL after creation)
- bug label → Bug issue type
- feature label → Feature issue type
- task/refactor/research/epic → Task issue type

## Milestone (REQUIRED — every issue must have one)
- now → current active milestone
- next/later → "Backlog" or appropriate future milestone

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

### Issue Creation Checklist

After creating each issue, verify:
- [ ] Has exactly one priority label (p0/p1/p2/p3)
- [ ] Has exactly one type label (bug/feature/task/refactor/research/epic)
- [ ] Has exactly one horizon label (now/next/later/blocked)
- [ ] Has at least one domain label (domain/*)
- [ ] Has a source label (source/groom, source/user, or source/agent)
- [ ] Has issue type set via GraphQL (Bug/Task/Feature)
- [ ] Is assigned to a milestone
- [ ] P0/P1 with `now` horizon added to Active Sprint project

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
- Filter by priority: `label:p0`
- Filter by type: `label:bug`
- Filter by horizon: `label:now`
- Filter by domain: `label:domain/stripe`
- View cross-repo in org projects: Active Sprint, Product Roadmap, Triage Inbox
- Assign and track progress
- Run `/fix-*` skills to address issues

## Related Skills

### Primitives (Investigate)
- `/check-production`, `/check-docs`, `/check-quality`, `/check-observability`
- `/check-product-standards` (version, attribution, contact)
- `/check-stripe`, `/check-bitcoin`, `/check-lightning`, `/check-btcpay`, `/check-payments`
- `/check-virality`, `/check-landing`, `/check-onboarding`

### Issue Creators (Document)
- `/log-production-issues`, `/log-doc-issues`, `/log-quality-issues`
- `/log-observability-issues`, `/log-product-standards-issues`
- `/log-stripe-issues`, `/log-bitcoin-issues`, `/log-lightning-issues`
- `/log-virality-issues`, `/log-landing-issues`, `/log-onboarding-issues`

### Fixers (Act)
- `/triage`, `/fix-docs`, `/fix-quality`, `/fix-observability`
- `/fix-stripe`, `/fix-bitcoin`, `/fix-lightning`
- `/fix-virality`, `/fix-landing`, `/fix-onboarding`

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
