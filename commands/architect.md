---
description: Add technical design to GitHub issue
argument-hint: <issue-id>
allowed-tools: Bash(gh:*)
---

# ARCHITECT

> Deep modules. Small interfaces. Hide complexity.

Design HOW to build what the product spec defined.

## Mission

Add technical design to Issue #$1. Post as comment, update labels to `status/ready`.

## Process

1. **Read**: `gh issue view $1 --comments` (get product spec)
2. **Investigate**: Explore codebase patterns, identify touch points
3. **Interview**: Surface technical assumptions via polls
4. **Research**: Check current best practices if needed (2025 patterns)
5. **Draft Alternatives**: Have Codex draft 2-3 design approaches while you evaluate tradeoffs
6. **Consult Council**: Validate architecture with expert council
7. **Design**: Create implementation blueprint
8. **Post**: `gh issue comment $1 --body "## Technical Design\n..."`
9. **Adversarial Review**: Stress-test the design with `/adversarial $1`
10. **Update**: `gh issue edit $1 --remove-label "status/needs-design" --add-label "status/ready"`

## Codex for Design Exploration

Use Codex as a brainstorming partner during design:
- "Codex, draft 3 different approaches for implementing this feature"
- "Codex, what are the tradeoffs between approach A and approach B?"
- "Codex, review this design for scalability concerns"

You evaluate and decide. Codex generates options cheaply.

## Interview Phase

After investigating the codebase, surface technical assumptions before designing.

Use AskUserQuestion with batched polls (2-4 options each, up to 4 questions per batch):

**Constraints** — Non-functional requirements:
- Performance requirements? (latency tiers)
- Scale expectations? (users, requests)
- Breaking changes acceptable? (yes/migration/no)

**Architecture** — Implementation approach:
- Preferred pattern? (options from codebase investigation)
- State management approach?
- Testing strategy? (unit-heavy/integration/e2e)

**Tradeoffs** — Optimization priorities:
- Optimize for? (ship-speed/performance/flexibility)

Use answers to inform design decisions.

## Council Consultation

Before finalizing design, validate with thinktank expert council.

### Doc-Check (MANDATORY)

**Do this first. Do not skip.**

Run `/doc-check`.

Doc-check ensures key docs exist (creating them if missing). Council needs full architectural context.

Wait for doc-check to complete before proceeding.

### Gather Context

Identify relevant files AND documentation:
- ARCHITECTURE.md (system overview)
- README.md, CLAUDE.md (conventions)
- ADRs for past architectural decisions
- Module READMEs in affected areas
- Files that will be modified/created

### Create Instructions

**Create instructions file with:**
- Proposed architecture approach
- Key technical decisions from interview
- Request: "Review this architecture. Identify risks, better patterns, and potential issues."

### Run Thinktank

```bash
thinktank /tmp/architecture-review.md \
  ./ARCHITECTURE.md \
  ./README.md ./CLAUDE.md \
  ./docs/adr/*.md \
  ./relevant-code \
  --synthesis
```

Pass docs AND code for full context.

**Incorporate council feedback into design:**
- Alternative patterns worth considering
- Scalability concerns
- Maintenance implications
- Security considerations
- Performance risks

## Design Structure

```markdown
## Technical Design

### Approach
[1-2 paragraphs: Strategy and key decisions]

### Files to Modify/Create
- `path/file.ts` — [what changes]

### Interfaces
[Key types, APIs, data structures]

### Implementation Sequence
1. [First thing to build]
2. [Second thing]
...

### Testing Strategy
[What to test, how]

### Risks & Mitigations
[Technical risks and how to handle]
```

## Principles

- Favor existing patterns over novel ones
- Minimize touch points (fewer files = less risk)
- Design for deletion (easy to remove later)

## Adversarial Review

The design is posted. Now let hostile experts find the flaws.

Run `/adversarial $1` to stress-test the technical design. Architecture decisions are expensive to reverse—surface concerns now while they're cheap to address.

Focus areas for design review:
- Module boundaries that will leak
- Interfaces that expose too much
- Scalability assumptions that won't hold
- Edge cases the design doesn't address

If adversarial review surfaces issues, revise the design comment and re-run until the design is solid.

## Output

Comment posted. Labels updated. Report: "Technical design complete. Next: `/build $1`"
