---
name: design-sprint
deprecated: true
superseded_by: evolve
description: |
  DEPRECATED — use /evolve instead.
  /evolve subsumes the full design cycle with persistent memory, genetic algorithm,
  taste injection (taste-frontend.md), dial args (--variance/--motion/--density),
  and component seeding at handoff. /design-sprint adds no value over /evolve.
argument-hint: "[route-or-url]"
effort: high
---

> **DEPRECATED.** Use `/evolve` instead.
>
> `/evolve` replaces this skill entirely: it runs the same audit → catalog → select →
> theme → build cycle, plus persistent cross-project memory, genetic algorithm evolution,
> taste-frontend.md injection, dial args (`--variance`, `--motion`, `--density`), and
> full design system handoff with component seeding.
>
> Original skill content preserved below for reference.

---

# /design-sprint

Explore before you implement.

## Role

Design lead guiding visual exploration through structured options.

## Objective

Full UI/UX design cycle for `$ARGUMENTS` (route, URL, or component). End with implemented, validated design.

## Latitude

- Research current trends via Gemini
- Generate multiple proposals before committing
- Multiple iteration rounds are expected
- User picks direction; you execute

## Workflow

1. **Audit** — `/design-audit` (token inventory, consistency, debt, accessibility)
2. **Catalog** — `/design-catalog $1` (5-8 visual proposals, validated against ui-skills + RAMS)
3. **Select** — User browses catalog, picks direction (hybrids OK)
4. **Theme** — `/design-theme` (tokens in CSS `@theme`, component updates, accessibility)
5. **Build** — `/build` (implement on feature branch)
6. **Cleanup** — Remove catalog artifacts with user approval

## Output

Design system implemented. Report: audit findings, proposals generated, selection, tokens defined, components updated.
