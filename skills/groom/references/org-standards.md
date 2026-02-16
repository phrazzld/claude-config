# Misty Step Org-Wide Standards

Every issue created or modified MUST comply with these standards.
Applies to ALL repositories in the misty-step organization.

## Canonical Label Taxonomy

Use ONLY these labels (plus repo-specific `domain/` labels).
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

## Issue Types (GitHub native)

Every issue MUST have an issue type set via GraphQL. Available types:
- **Bug** (node_id: `IT_kwDODnuAzs4Bxgbl`) — For bugs
- **Task** (node_id: `IT_kwDODnuAzs4Bxgbk`) — For tasks, refactors, research
- **Feature** (node_id: `IT_kwDODnuAzs4Bxgbm`) — For features

Set issue type after creation:
```bash
ISSUE_ID=$(gh api graphql -f query='{ repository(owner: "misty-step", name: "REPO") { issue(number: NUM) { id } } }' --jq '.data.repository.issue.id')
gh api graphql -f query="mutation { updateIssue(input: { id: \"$ISSUE_ID\", issueTypeId: \"TYPE_NODE_ID\" }) { issue { number issueType { name } } } }"
```

Map label type to issue type:
- `bug` label -> Bug issue type
- `feature` label -> Feature issue type
- `task`, `refactor`, `research`, `epic` labels -> Task issue type

## Milestones (REQUIRED)

Every issue MUST be assigned to a milestone. If the repo has no milestones:
1. Create a "Backlog" milestone (no due date)
2. Create milestone(s) for current work based on vision.md focus

```bash
gh api "/repos/misty-step/REPO/milestones" --jq '.[].title'
gh api -X POST "/repos/misty-step/REPO/milestones" -f title="Backlog" -f description="Unscheduled work items"
gh issue edit NUM --milestone "Milestone Name"
```

Rules:
- `now` horizon -> current sprint/active milestone
- `next` horizon -> next milestone or "Backlog"
- `later` horizon -> "Backlog" or "Someday"
- `blocked` issues -> keep in their target milestone

## Org-Level Projects

Three org-level GitHub Projects. Link issues as appropriate:
- **Active Sprint** — Issues with `now` horizon
- **Product Roadmap** — All `p0`, `p1`, `p2` issues across repos
- **Triage Inbox** — New issues pending classification

```bash
gh project item-add PROJECT_NUMBER --owner misty-step --url "https://github.com/misty-step/REPO/issues/NUM"
```

## Label Migration

When auditing existing issues, migrate legacy labels:
```bash
gh issue edit NUM --remove-label "priority/p0" --add-label "p0"
gh issue edit NUM --remove-label "P0" --add-label "p0"
gh issue edit NUM --remove-label "type/bug" --add-label "bug"
gh issue edit NUM --add-label "later"  # if no horizon set
```

## Priority System

```
P0: CRITICAL — Production broken, security vulnerabilities
P1: FUNDAMENTALS — Testing, docs, quality gates, observability, working prototype
P2: LAUNCH READINESS — Landing page, onboarding, monetization, growth, marketing
P3: EVERYTHING ELSE — Innovation, polish, strategic improvements

Security mapping: Critical->P0, High->P1, Medium->P2, Low->P3
```

## Issue Format

```markdown
## Title
[P{0-3}] Clear, actionable description

## Labels (canonical)
- p0|p1|p2|p3                    (priority)
- bug|feature|task|refactor|research|epic  (type)
- now|next|later|blocked          (horizon)
- effort/s|m|l|xl                 (effort)
- source/groom|source/user|source/agent  (source)
- domain/{name}                   (domain)

## Body
### Problem
What's wrong or missing

### Impact
Why this matters

### Suggested Fix
Concrete next steps

### Source
Which skill or agent identified this

---
Created by `/groom`
```

## Issue Creation Checklist

After creating each issue, verify:
- [ ] Exactly one priority label (p0/p1/p2/p3)
- [ ] Exactly one type label (bug/feature/task/refactor/research/epic)
- [ ] Exactly one horizon label (now/next/later/blocked)
- [ ] At least one domain label (domain/*)
- [ ] Source label (source/groom, source/user, or source/agent)
- [ ] Issue type set via GraphQL (Bug/Task/Feature)
- [ ] Assigned to a milestone
- [ ] P0/P1 with `now` horizon added to Active Sprint project
