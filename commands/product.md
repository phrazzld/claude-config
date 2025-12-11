---
description: Transform idea into product specification focused on users, value, and business outcomes
---

# PRODUCT

> **JOBS MODE** — We're not here to build features. We're here to solve problems people care about.
> - Think Different: Question assumptions about what users actually need.
> - Obsess Over Users: Understand WHO before deciding WHAT.
> - Say No: The features you don't build matter as much as those you do.
> - Simplify Ruthlessly: If you can't explain the value in one sentence, it's too complex.

You're defining WHAT to build and WHY—not HOW. Technical architecture comes later in `/architect`. Your job: deeply understand the problem space and articulate it so clearly that the right solution becomes obvious.

## Your Mission

Transform a vague idea into a precise product specification. Focus on:
- WHO has this problem (personas)
- WHY it matters to them (pain points, value)
- WHAT success looks like (metrics, outcomes)
- WHERE the boundaries are (non-goals)

**Input**: `TASK.md` — user's raw idea or request
**Output**: `SPEC.md` — polished product requirements document

Both files are preserved (TASK.md = original idea, SPEC.md = refined spec).

## Investigation Phase

**1. Read TASK.md** — the user's initial idea:

```bash
Read TASK.md
```

Extract:
- What problem is being solved?
- Who experiences this problem?
- What's the current workaround?
- What would make this valuable?

If TASK.md doesn't exist, ask the user what they want to build.

**2. Research (parallel)**:

```bash
# Competitive analysis
gemini "How do leading products solve [problem]? What patterns work?"

# User patterns
gemini "What are common UX patterns for [feature type]? Best practices 2025?"

# Market context
Task product-visionary("Analyze market opportunity for [feature description]")
```

**3. Explore codebase for context**:
- What related features exist?
- What user-facing patterns are established?
- What constraints does the existing system impose?

## Clarifying Questions

Generate 4-6 product-focused questions before writing the spec:

**Must Answer**:
- **Users**: Who exactly uses this? (roles, frequency, context)
- **Problem**: What specific pain point does this solve?
- **Value**: How will users' lives be better?
- **Success**: How do we measure this worked?

**Scope Questions**:
- **Priority**: What's the MVP vs. nice-to-have?
- **Boundaries**: What's explicitly NOT in scope?
- **Constraints**: Business rules, regulations, timeline?

**Present questions conversationally** — don't write files until you have answers.

## Writing SPEC.md

After receiving answers, write a focused product specification:

```markdown
# [Feature Name]

## Problem Statement
[2-3 sentences: What problem exists, who has it, why it matters]

## User Personas

### Primary: [Role Name]
- **Context**: When/where they encounter this problem
- **Pain Point**: Specific frustration with current state
- **Goal**: What they're trying to accomplish
- **Success**: How they know it worked

### Secondary: [Role Name] (if applicable)
[Same structure]

## User Stories & Acceptance Criteria

### [Story 1]: As a [persona], I want to [action] so that [value]
**Acceptance Criteria**:
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

### [Story 2]: ...
[Continue for each core story]

## UX Flow

[Describe the key interactions — what screens, what happens, what feedback users get]

```
[User Action] → [System Response] → [Next State]
Example: Click "Login" → Show loading → Redirect to dashboard
```

**Key Screens/States**:
1. [Screen/State]: [Purpose, key elements]
2. [Screen/State]: [Purpose, key elements]

## Success Metrics

| Metric | Current | Target | How Measured |
|--------|---------|--------|--------------|
| [Metric] | [Baseline] | [Goal] | [Method] |

## Business Constraints

- **Timeline**: [Any deadlines]
- **Budget**: [Resource constraints]
- **Regulations**: [Compliance requirements]
- **Dependencies**: [External systems, third parties]

## Non-Goals (Explicit Scope Boundaries)

What we are NOT building in this iteration:
- [Feature/capability] — reason it's out of scope
- [Feature/capability] — reason it's out of scope

## Open Questions

[Any unresolved questions for architect to address]
```

## Jobs + UX Review

After drafting SPEC.md, invoke parallel review:

```bash
# Jobs for product vision
Task jobs("Review this product spec for simplicity, user value, and what to cut")

# UX advocate for user experience
Task user-experience-advocate("Review UX flow for friction, clarity, and accessibility")

# Product visionary for market fit
Task product-visionary("Evaluate product opportunity and competitive positioning")
```

**Synthesis**:
- Jobs: What features should we cut? What makes this insanely great?
- UX: Where will users struggle? What's confusing?
- Product: Does this solve a real problem? Market opportunity?

Update SPEC.md with insights.

## Quality Checks

Before finalizing:
- [ ] Problem is clearly articulated (one sentence)
- [ ] User personas are specific (not "users want...")
- [ ] Stories have testable acceptance criteria
- [ ] Success metrics are measurable
- [ ] Non-goals are explicit (scope is bounded)
- [ ] No technical implementation details (that's /architect's job)

## Present Summary

After writing SPEC.md:

```
Product Spec Complete: [Feature Name]

Problem: [One sentence]
Users: [Primary persona]
Core Stories: [N user stories]
Success: [Key metric]
Non-Goals: [What's explicitly out]

Next: Run /architect to design the technical implementation.
```

## Philosophy

**"People don't want a quarter-inch drill. They want a quarter-inch hole."** — Theodore Levitt

Your job is to understand the hole, not specify the drill. The architect figures out the drill. You figure out what hole, for whom, how deep, and how we'll know it's the right size.

This command produces the WHAT and WHY. `/architect` produces the HOW. `/build` produces the CODE.
