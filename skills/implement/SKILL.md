---
name: implement
description: |
  Code generation with Codex delegation.
  Understands task, finds patterns, delegates to Codex, validates output.
  Use when: implementing a feature, writing code, building functionality.
argument-hint: <task>
effort: high
---

# /implement

Delegate implementation to Codex with good context.

## Role

Senior engineer who writes great delegation prompts.

## Objective

Implement `$ARGUMENTS` with passing tests and clean code.

## Latitude

- Delegate to Codex by default
- Keep for yourself only: trivial (<10 lines) with deep context already loaded
- When in doubt, delegate

## Workflow

1. **Understand** — Read issue/spec, find existing patterns to follow
2. **Prepare** — Clear Codex prompt with pattern references and quality gates
3. **Delegate** — Codex at high reasoning
4. **Validate** — `git diff --stat && pnpm typecheck && pnpm lint && pnpm test`
5. **Commit** — `feat: description`

## Pre-Delegation Checklist

- Existing tests? Warn Codex: "Don't break tests in [file]"
- Add or replace? Be explicit
- Pattern to follow? Include reference file
- Quality gates? Include verify command

## Output

Files modified, tests passing, commit created.
