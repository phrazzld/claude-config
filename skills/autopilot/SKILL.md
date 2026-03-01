---
name: autopilot
description: |
  Full autonomous delivery from issue to PR.
  Finds highest-priority issue, specs it, designs it, builds it, ships it.
  Use when: shipping an issue end-to-end, autonomous delivery, sprint execution.
  Composes: /spec, /architect, /build, /refactor, /update-docs, /dogfood, /pr.
argument-hint: "[issue-id]"
effort: high
---

# /autopilot

From issue to PR in one command.

## Role

Engineering lead running a sprint. Find work, ensure it's ready, delegate implementation, ship.

## Objective

Deliver Issue `$ARGUMENTS` (or highest-priority open issue) as a draft PR with tests passing
and a clean dogfood QA pass.

## Latitude

- Codex writes first draft of everything (investigation, implementation, tests, docs)
- You orchestrate, review, clean up, commit, ship
- Flesh out incomplete issues yourself (spec, design)
- Never skip an issue because it's "not ready" — YOU make it ready

## Priority Selection

**Always work on the highest priority issue. No exceptions.**

1. `p0` > `p1` > `p2` > `p3` > unlabeled
2. Within tier: `horizon/now` > `horizon/next` > unlabeled
3. Within same horizon: lower issue number first
4. Scope, cleanliness, comfort don't matter — priority is absolute

## Workflow

1. **Find issue** — `gh issue view $1` or `gh issue list --state open --limit 20`
2. **Load context** — Read `project.md` for product vision, domain glossary, quality bar
3. **Readiness gate** — Run `/issue lint $1`:
   - Score >= 70: proceed
   - Score 50-69: run `/issue enrich $1` first, then re-lint
   - Score < 50: flag to user, attempt enrichment, re-lint
   - **Never skip an issue because it scored low — YOU make it ready**
4. **Spec** — Invoke `/spec` if no `## Product Spec` section
5. **Design** — Invoke `/architect` if no `## Technical Design` section
6. **Build** — Invoke `/build` (branching, Codex implementation, commits)
7. **Visual QA** — If diff touches frontend files (`app/`, `components/`, `*.css`), run `/visual-qa --fix`. Fix P0/P1 before proceeding.
8. **Refine** — `/refactor`, `/update-docs`, then `ousterhout` agent for module depth review
9. **Dogfood QA** — Run automated QA against local dev server (see Dogfood QA section below).
   Iterate until no P0/P1 issues remain. **Do not open a PR until QA passes.**
10. **Ship** — `/pr` with `Closes #N` (must satisfy all PR Body Requirements from `/pr` skill)
11. **Retro** — Append implementation signals to `.groom/retro.md`:
    ```
    /retro append --issue $1 --predicted {effort_label} --actual {actual_effort} \
      --scope "{scope_changes}" --blocker "{blockers}" --pattern "{insight}"
    ```

## Dogfood QA

Run before every PR. No exceptions.

### Setup

```bash
# Start dev server if not already running
# Find existing server first
PORT=$(lsof -i :3000 -sTCP:LISTEN -t 2>/dev/null | head -1)
if [ -z "$PORT" ]; then
  bun dev:next &
  DEV_PID=$!
  sleep 10  # wait for compilation
fi

# Confirm it's up
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
```

If port 3000 is taken by another project, use `bun dev:next -- --port 3001` and adjust the
target URL accordingly.

### Run

```
/dogfood http://localhost:3000
```

Scope to the diff: if the issue only touches status pages, `/dogfood http://localhost:3000 Focus on the status page and badge changes`. For full-feature work, no scope restriction.

### Issue Severity Gate

After `/dogfood` completes, read the report:
- **P0 or P1 issues** → fix them, commit, re-run `/dogfood` on the affected area
- **P2 issues** → fix if quick (<15 min), otherwise document in PR as known and create a follow-up issue
- **P3 issues / no issues** → proceed to `/pr`

Never open a PR with unfixed P0 or P1 issues from the dogfood report.

### Iteration Cap

If the same P0/P1 issue resurfaces after two fix attempts, stop, document the blocker, and
flag to the user before proceeding. Don't loop indefinitely.

### Teardown

```bash
# Kill the dev server if we started it
[ -n "$DEV_PID" ] && kill $DEV_PID 2>/dev/null || true
```

If the user's own dev server was already running (no `$DEV_PID`), leave it alone.

## Parallel Refinement (Agent Teams)

After `/build` completes, parallelize the refinement phase:

| Teammate | Task |
|----------|------|
| **Simplifier** | Run code-simplifier agent, commit |
| **Depth reviewer** | Run ousterhout agent, commit |
| **Doc updater** | Run /update-docs, commit |

Lead sequences commits after all teammates finish. Then dogfood QA, then `/pr`.

Use when: substantial feature with multiple refinement needs.
Don't use when: small fix where sequential is fast enough.

## Stopping Conditions

Stop only if: issue explicitly blocked, build fails after multiple attempts, requires external action.

NOT stopping conditions: lacks description, seems big, unclear approach.

## Output

Report: issue worked, spec status, design status, commits made, dogfood QA summary (issues found/fixed), PR URL.
