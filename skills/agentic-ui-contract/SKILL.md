---
name: agentic-ui-contract
description: |
  Design and implement agentic product flows using the contract:
  model decides what to do, tools decide how it is done, UI schema decides
  how it is rendered. Use for chat-first apps, tool-calling agents,
  generative UI systems, and planner/tool architecture decisions.
  Keywords: agentic UX, tool calling, planner, generative UI, function tools.
effort: high
---

# Agentic UI Contract

Use this when building or refactoring toward agentic product behavior.

## Core Contract

1. Model decides WHAT to do.
2. Tools decide HOW it is done.
3. UI schema decides HOW it is rendered.

This gives open-ended behavior without fragile freeform execution.

## Architecture Shape

- Planner layer (LLM): intent interpretation + tool selection + sequencing.
- Tool layer (deterministic): typed side effects and data reads.
- UI contract layer (typed blocks): constrained rendering catalog.
- Control layer: auth, guardrails, tracing, evals, fallback.

## Rules

- Never let model write directly to persistence.
- Never trust model-generated metrics; compute metrics deterministically.
- Keep tool interfaces deep (few, meaningful tools), avoid tiny tool explosions.
- Keep UI blocks strict and versionable.
- Treat planner failure as recoverable; fallback to deterministic behavior.

## Implementation Workflow

1. Define typed block schema first.
2. Define deep tool surface second.
3. Implement server planner tool loop third.
4. Keep client thin: send messages, render blocks, apply client actions.
5. Add traces and eval fixtures before widening scope.

## Readiness Checklist

- [ ] Tool args validated with schema.
- [ ] Tool outputs deterministic and structured.
- [ ] Planner cannot bypass tools for data claims.
- [ ] UI renders only whitelisted block types.
- [ ] Planner + tool traces available per turn.
- [ ] Deterministic fallback path exists.

## Anti-Patterns

- Regex parser as primary intelligence layer.
- Model directly composing arbitrary UI markup/components.
- Over-fragmented tools that mirror internal implementation.
- Allowing model narration to replace data tool calls.
- No eval harness for prompt/tool regressions.

