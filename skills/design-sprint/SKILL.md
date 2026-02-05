---
name: design-sprint
description: |
  Full design cycle: audit, catalog, pick, theme, build.
  Explores visual options before committing to implementation.
  Use when: redesigning UI, exploring visual directions, design system work.
  Composes: /design-audit, /design-catalog, /design-theme, /build.
argument-hint: "[route-or-url]"
effort: high
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
