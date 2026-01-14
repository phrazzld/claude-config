---
description: Flesh out GitHub issue with product spec
argument-hint: <issue-id>
allowed-tools: Bash(gh:*)
---

# PRODUCT

> "People don't want a quarter-inch drill. They want a quarter-inch hole." — Levitt

Define WHAT to build and WHY. Technical HOW comes in `/architect`.

## Mission

Transform Issue #$1 into a precise product specification. Post as comment, update labels.

## Process

1. **Read**: `gh issue view $1 --comments`
2. **Interview**: Surface hidden assumptions via polls
3. **Research**: Understand users, pain points, competitive landscape
4. **Consult Council**: Get multi-model perspectives on requirements
5. **Write spec**: Post as comment with structure below
6. **Update labels**: `gh issue edit $1 --remove-label "status/needs-spec" --add-label "status/needs-design"`

## Interview Phase

Before researching, interview the user to surface non-obvious assumptions.

Use AskUserQuestion with batched polls (2-4 options each, up to 4 questions per batch):

**Context** — Who and why:
- Who exactly uses this? (roles, frequency)
- What triggers this need? (scenarios)
- What's the urgency? (horizon)

**Scope** — What's in and out:
- What's MVP vs nice-to-have? (multiSelect)
- What's explicitly NOT in scope?

**Success** — How we'll know it worked:
- How will we measure success?
- What failure mode are we preventing?

**Edge cases** — Non-obvious scenarios:
- What happens when [discovered edge case]?

Continue interviewing until assumptions exhausted. Use answers to inform spec.

## Council Consultation

After research, consult thinktank for product perspective validation.

### Doc-Check (MANDATORY)

**Do this first. Do not skip.**

Run `/doc-check`.

Doc-check ensures key docs exist (creating them if missing). Council needs this context to validate requirements effectively.

Wait for doc-check to complete before proceeding.

### Gather Context

Identify relevant files AND documentation:
- README.md, CLAUDE.md (project conventions)
- Existing specs or product docs
- Related feature implementations
- ADRs for past product decisions

### Create Instructions

**Create instructions file with:**
- Issue context and user stories
- Key assumptions gathered from interview
- Request: "Review these requirements. Identify gaps, edge cases, and potential user confusion."

### Run Thinktank

```bash
thinktank /tmp/product-review.md \
  ./README.md ./CLAUDE.md \
  ./docs/product-context.md \
  ./relevant-code \
  --synthesis
```

Pass docs AND code for full context.

**Incorporate council feedback into spec:**
- Missing edge cases
- User story gaps
- Scope concerns
- Potential user confusion points

## Spec Structure

```markdown
## Product Spec

### Problem
[2-3 sentences: What, who, why]

### Users
**Primary**: [Role] — [context, pain, goal]

### User Stories
- As [persona], I want [action] so that [value]
  - [ ] [Testable acceptance criterion]

### Success Metrics
| Metric | Target | How Measured |

### Non-Goals
- [What we're NOT building and why]

### Open Questions for Architect
[Technical unknowns]
```

## Output

Comment posted to Issue #$1. Labels updated. Report: "Product spec complete. Next: `/architect $1`"
