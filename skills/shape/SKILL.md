---
name: shape
description: |
  Full interactive planning for a single idea. Product + technical thinking
  in one conversational session. The "ad hoc issue grooming" command.
  Named after Basecamp's Shape Up.
effort: high
argument-hint: <issue-id-or-idea>
---

# SHAPE

> Take a raw idea and shape it into something buildable.

## Role

You are both product lead and technical lead. Shape an idea from raw concept
to implementation-ready issue(s) in one interactive session.

## When to Use

| Situation | Skill |
|-----------|-------|
| Full backlog session, many issues | `/groom` |
| Just need a product spec | `/spec` |
| Just need a technical design | `/architect` |
| Full planning for one idea: product + technical + discussion | **`/shape`** |

## Workflow

### Phase 1: Understand

Accept input: raw idea (string), issue ID, or observation.

1. If no issue exists: create skeleton immediately
2. If issue exists: `gh issue view $1 --comments`
3. Load `vision.md` if present
4. Read relevant codebase context — adjacent features, existing patterns, constraints

Present: "Here's what I understand. Let me explore the problem space."

### Phase 2: Product Exploration

Run `/spec` logic in exploration mode:

1. **Investigate** — Problem space, user impact, prior art (parallel agents)
2. **Brainstorm** — 3-5 product approaches with tradeoffs. Recommend one.
3. **Discuss** — User steers. Iterate until product direction is locked.
4. **Draft spec** — Problem, users, approach, user stories, success metrics

### Phase 3: Technical Exploration

Run `/architect` logic in exploration mode:

1. **Absorb** — Read locked product spec, investigate codebase, research patterns
2. **Explore** — 3-5 technical approaches with tradeoffs. Recommend one.
3. **Discuss** — User steers. Iterate until design is locked.
4. **Draft design** — Approach, files, interfaces, implementation sequence, tests

### The Interweaving

Key difference from running `/spec` then `/architect` sequentially:

During technical exploration, product decisions can be revisited.
"This architecture would be simpler if we scoped the feature differently"
-> return to product discussion -> refine -> continue.

The skill explicitly allows looping back. Technical constraints inform product
decisions and vice versa. No phase is final until everything is locked.

### Phase 4: Synthesis

Once both product and technical directions are locked:

1. **Verify alignment** — Do spec and design tell a coherent story?
2. **Break down** — If scope warrants, yield multiple atomic issues
3. **Enrich each issue** — Product spec + technical design on every issue
4. **Apply standards** — Labels, milestones, org-wide standards (see `groom/references/org-standards.md`)
5. **Signal readiness** — `status/ready` for `/build` or `/autopilot`

Post spec + design as comments on each issue.

### Agent Teams Mode

For ambitious ideas (multiple issues expected):

| Teammate | Role |
|----------|------|
| Product explorer | `/spec` exploration for the idea |
| Technical explorer | `/architect` exploration in parallel |
| Research agent | Best practices, competitive analysis (Gemini) |

Lead synthesizes and presents unified view. User steers both product and
technical directions simultaneously rather than sequentially.

Use when: large feature, greenfield module, multiple valid approaches.
Don't use when: small idea, clear direction, single issue output.

## Completion

"Shape complete. {N} issue(s) ready for `/build` or `/autopilot`."

List issues with links. Summarize: product direction, technical approach,
implementation sequence, estimated effort.
