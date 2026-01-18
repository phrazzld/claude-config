---
description: Two-pass code refinement - clarity then architecture
---

# REFACTOR

> "Simplicity is the ultimate sophistication." — da Vinci

Post-implementation code refinement. Run after `/build` completes.

## Codex Pre-Analysis

Before diving in, get Codex's take on the code:
- "Codex, review this code for simplification opportunities"
- "Codex, identify any code smells or unnecessary complexity"

Codex provides a cheap second opinion. You decide what to act on.

## Mission

Two-pass refinement:
1. **Clarity** — Simplify code without changing behavior
2. **Architecture** — Improve module depth and information hiding

## Phase 1: Simplification

Launch `code-simplifier:code-simplifier` agent.

Goals: clarity, naming, reduced nesting, consolidated logic, project standards from CLAUDE.md.

Commit: `refactor: simplify implementation`

## Phase 2: Deep Module Review

Launch `ousterhout` agent to review for Ousterhout's design principles.

Looking for:
- Shallow modules or pass-through methods
- Leaky abstractions exposing implementation details
- Change amplification risk (small change → many edits)
- Cognitive load issues (too much to hold in head)

If high-impact issues found:
1. Implement suggested refactorings
2. Commit: `refactor: improve module depth`

## Completion

Report what was simplified and any architectural improvements made.
