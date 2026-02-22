---
name: architect
description: |
  Interactive technical exploration. Answers HOW to build what the spec defined.
  Dual mode: full exploration (user-invoked) or quick design (autopilot-invoked).
effort: max
argument-hint: <issue-id>
---

# ARCHITECT

> Deep modules. Small interfaces. Hide complexity.

## Role

Technical lead designing HOW to build what the product spec defined.
Codex drafts alternatives. Thinktank validates. Gemini researches patterns.

## Dual Mode

**Exploration mode** — User invokes directly. Full interactive design session.
**Quick mode** — Autopilot invokes on specced issue. Investigate, design, validate, post.

Detection: Autopilot pipeline with specced issue = quick mode.
User-invoked, or complex design space = exploration mode.

---

## Exploration Mode

### Phase 1: Absorb

1. Read product spec: `gh issue view $1 --comments`
2. Investigate codebase — existing patterns, touch points, adjacent systems:
   ```bash
   codex exec "INVESTIGATE architecture for [feature]. Find existing patterns, identify touch points, list files to modify." \
     --output-last-message /tmp/codex-investigation.md 2>/dev/null
   ```
3. Research current best practices (Gemini):
   ```bash
   gemini "Current best practices for [topic]. Framework docs, common patterns, pitfalls."
   ```
4. Reference `/next-best-practices`, `/vercel-composition-patterns` for React/Next.js

Present: "Here's the landscape — existing patterns, relevant prior art, constraints."

### Phase 2: Explore Architectures

Generate 3-5 technical approaches. For each:

- **Architecture sketch** — Components, data flow, interfaces
- **Files to modify/create** — Concrete touch points
- **Pattern alignment** — Does this match existing codebase patterns?
- **Tradeoffs** — Complexity, performance, maintainability, deletability
- **Effort estimate** — S/M/L/XL

**For fundamentally different approaches**, use Agent Teams:
- Spawn 2-3 architect teammates, each developing one approach in depth
- Each teammate owns a different design direction
- Thinktank validates after synthesis

**Recommend one approach.** Present all with clear reasoning:
- Why the recommended approach wins
- When you'd pick each alternative instead
- What risks each carries

### Phase 3: Discussion Loop

Iterate with the user. Continues until design is locked:

1. Present approaches with recommendation
2. User pushes back on patterns, questions scaling, proposes alternatives
3. Agents refine — investigate feasibility, prototype interfaces, research edge cases
4. Update approaches based on discussion
5. User locks direction — or explores more

Use AskUserQuestion for binary decisions. Plain conversation for design exploration.

No limit on rounds. The design isn't ready until the user says it is.

### Phase 4: Codify

Post technical design on the issue:

```markdown
## Technical Design

### Approach
[Strategy and key decisions — 1-2 paragraphs]

### Files to Modify/Create
- `path/file.ts` — [what changes]

### Interfaces
[Key types, APIs, data structures — actual code blocks]

### Implementation Sequence
1. [First Codex-sized chunk]
2. [Second chunk]
3. ...

### Testing Strategy
[What to test, how, which patterns]

### Risks & Mitigations
[Technical risks and how to handle them]

## Components

```mermaid
graph TD
    A[Component A] -->|calls| B[Component B]
    B --> C[(Store)]
    A -->|reads| C
```

## Sequence

```mermaid
sequenceDiagram
    actor User
    User->>API: POST /action
    API->>Service: process()
    Service-->>API: result
    API-->>User: 200 OK
```
```

**Diagram requirements:**
- `## Components` (`graph TD`) — always required. Shows new/changed components and their relationships.
- `## Sequence` (`sequenceDiagram`) — required when async interactions, API calls, or multi-step flows are involved. Omit for purely synchronous or single-component changes.
- `## Data Model` (`erDiagram`) — add when schema changes are part of the work.

Load `~/.claude/skills/visualize/references/github-mermaid-patterns.md` for annotated examples and GitHub gotchas.

Post as comment: `gh issue comment $1 --body "..."`

Stress-test with `/critique $1` to find design flaws.

Update labels:
```bash
gh issue edit $1 --remove-label "status/needs-design" --add-label "status/ready"
```

---

## Quick Mode (Autopilot)

Triggered when autopilot calls `/architect` on a specced issue.

1. Read spec from issue: `gh issue view $1 --comments`
2. Codex investigates codebase + drafts design:
   ```bash
   codex exec "Design implementation for [feature]. Spec: [summary]. Find patterns, draft approach, list files." \
     --output-last-message /tmp/codex-design.md 2>/dev/null
   ```
3. Gemini researches relevant patterns
4. Thinktank validates:
   ```bash
   thinktank /tmp/arch-review.md ./CLAUDE.md --synthesis
   ```
5. Post design, update labels to `status/ready`

---

## Principles

- Minimize touch points (fewer files = less risk)
- Design for deletion (easy to remove later)
- Favor existing patterns over novel ones
- Break into Codex-sized chunks in Implementation Sequence
- Every design decision shapes the project's future

## Completion

**Exploration mode:** "Technical design locked. Ready for `/build $1`."
**Quick mode:** "Technical design complete. Next: `/build $1`"

> **Note:** For affordance-level design (places, UI/code/store affordances, wiring), consider `/breadboarding`. `/architect` is the file-level implementation primitive used by autopilot's quick mode.

## Visual Deliverable

After completing the core workflow, generate a visual HTML summary:

1. Read `~/.claude/skills/visualize/prompts/architect-diagram.md`
2. Read the template(s) referenced in the prompt
3. Read `~/.claude/skills/visualize/references/css-patterns.md`
4. Generate self-contained HTML capturing this session's output
5. Write to `~/.agent/diagrams/architect-{feature}-{date}.html`
6. Open in browser: `open ~/.agent/diagrams/architect-{feature}-{date}.html`
7. Tell the user the file path

Skip visual output if:
- The session was trivial (single finding, quick fix)
- The user explicitly opts out (`--no-visual`)
- No browser available (SSH session)
