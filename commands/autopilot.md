---
description: Discover highest-priority issue, spec it, design it, implement it, open PR
allowed-tools: Bash(gh:*), Bash(git:*)
---

# AUTOPILOT

> From backlog to PR in one command.

Full autonomous workflow: discover → spec → design → branch → implement → PR.

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

## Phase 5: Simplification

Launch the `code-simplifier:code-simplifier` agent to refine recently modified code. It:
- Preserves functionality while improving clarity
- Applies project standards from CLAUDE.md
- Reduces unnecessary complexity and nesting
- Improves naming and consolidates related logic

Commit any simplifications with: `refactor: simplify implementation (#N)`

## Phase 6: Documentation

Run `/document` to generate state diagrams for stateful components, update READMEs, and add architecture diagrams if needed.

## Phase 7: Pull Request

Run `/git-pr`. Ensure PR description references the issue with `Closes #N` for auto-linking.

## Completion

Report:
- Issue selected and rationale
- Spec: created or already existed
- Design: created or already existed
- Implementation summary
- PR URL
