---
name: autopilot
description: |
  Full autonomous delivery from issue to PR.
  Finds highest-priority issue, specs it, designs it, builds it, ships it.
  Use when: shipping an issue end-to-end, autonomous delivery, sprint execution.
  Composes: /spec, /architect, /build, /refactor, /update-docs, /pr.
argument-hint: "[issue-id]"
effort: high
---

# /autopilot

From issue to PR in one command.

## Role

Engineering lead running a sprint. Find work, ensure it's ready, delegate implementation, ship.

## Objective

Deliver Issue `$ARGUMENTS` (or highest-priority open issue) as a draft PR with tests passing.

## Latitude

- Codex writes first draft of everything (investigation, implementation, tests, docs)
- You orchestrate, review, clean up, commit, ship
- Flesh out incomplete issues yourself (spec, design)
- Never skip an issue because it's "not ready" — YOU make it ready

## Priority Selection

**Always work on the highest priority issue. No exceptions.**

1. `priority/p1` > `priority/p2` > `priority/p3` > unlabeled
2. Within tier: lower number first, `horizon/now` > `horizon/next`
3. Scope, cleanliness, comfort don't matter — priority is absolute

## Workflow

1. **Find issue** — `gh issue view $1` or `gh issue list --state open --limit 20`
2. **Spec** — Invoke `/spec` if no `## Product Spec` section
3. **Design** — Invoke `/architect` if no `## Technical Design` section
4. **Build** — Invoke `/build` (branching, Codex implementation, commits)
5. **Refine** — `/refactor`, `/update-docs`, then `ousterhout` agent for module depth review
6. **Ship** — `/pr` with `Closes #N`

## Parallel Refinement (Agent Teams)

After `/build` completes, parallelize the refinement phase:

| Teammate | Task |
|----------|------|
| **Simplifier** | Run code-simplifier agent, commit |
| **Depth reviewer** | Run ousterhout agent, commit |
| **Doc updater** | Run /update-docs, commit |

Lead sequences commits after all teammates finish. Then `/pr`.

Use when: substantial feature with multiple refinement needs.
Don't use when: small fix where sequential is fast enough.

## Stopping Conditions

Stop only if: issue explicitly blocked, build fails after multiple attempts, requires external action.

NOT stopping conditions: lacks description, seems big, unclear approach.

## Output

Report: issue worked, spec status, design status, commits made, PR URL.
