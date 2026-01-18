---
description: Discover highest-priority issue, spec it, design it, implement it, open PR
allowed-tools: Bash(gh:*), Bash(git:*), Bash(codex:*)
---

# AUTOPILOT

> From backlog to PR in one command.

Full autonomous workflow: discover → spec → design → branch → implement → PR.

## Token Strategy (MANDATORY)

Your tokens are expensive. Codex tokens are cheap. **Actually invoke Codex** throughout this workflow:

```bash
# For each implementation chunk in /build:
codex exec --full-auto "Implement [chunk]. Follow pattern in [file]." \
  --output-last-message /tmp/codex-out.md 2>/dev/null

# For test writing:
codex exec --full-auto "Write tests for [module]." --output-last-message /tmp/tests.md

# For documentation drafts:
codex exec --full-auto "Draft README for [module]." --output-last-message /tmp/docs.md
```

You orchestrate and validate. Codex implements. This is not optional.

## Phase 1: Issue Discovery

Fetch open issues and analyze them to identify the single highest-priority issue.

Consider:
- **Labels**: `horizon/now` > `horizon/next` > `horizon/soon` > unlabeled
- **Status**: Issues with `status/ready` are preferred; `status/needs-spec` or `status/needs-design` need work first
- **Blocking**: Issues that block other work
- **Age + Activity**: Older issues with recent discussion
- **Scope**: Prefer actionable issues over vague epics

Select one issue. Report why it's highest priority.

## Phase 2: Spec Check

Read the issue comments. If no `## Product Spec` exists, run `/product` on it.

## Phase 3: Design Check

Read the issue comments again. If no `## Technical Design` exists, run `/architect` on it.

## Phase 4: Branch + Build

Run `/build` on the issue. It handles:
- Branch naming: `feature/issue-{N}` or `fix/issue-{N}`
- Commits reference issue: `feat: description (#N)`
- Final commit closes issue: `closes #N`

## Phase 5: Refactor

Run `/refactor` to:
- Simplify code (clarity, naming, nesting, project standards)
- Review for deep module design (Ousterhout principles)
- Fix high-impact architectural issues

## Phase 6: Documentation

Run `/document` to generate state diagrams for stateful components, update READMEs, and add architecture diagrams if needed.

## Phase 7: Pull Request

Run `/open-pr`. Ensure PR description references the issue with `Closes #N` for auto-linking.

## Completion

Report:
- Issue selected and rationale
- Spec: created or already existed
- Design: created or already existed
- Implementation summary
- PR URL
