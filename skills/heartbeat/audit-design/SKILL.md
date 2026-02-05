---
name: audit-design
description: |
  Audit Heartbeat components for Kyoto Moss design system compliance.
  Scans for token violations, banned patterns, typography issues, animation problems.
  Use when: checking Heartbeat UI compliance, design system audit, Kyoto Moss violations.
effort: high
---

# Audit Kyoto Moss Design System

Scan Heartbeat components for design system violations.

## Role

Design system auditor enforcing Kyoto Moss conventions.

## Objective

Find and report all design token violations, banned patterns, and accessibility gaps in Heartbeat components.

## Audit Categories

### 1. Token Usage
- `bg-[#...]`, `text-[#...]` arbitrary values
- Tailwind defaults without semantic mapping (`bg-blue-500`)
- Hardcoded `bg-white`, `bg-black`, `text-gray-*`
- Correct: `bg-up`, `bg-degraded`, `bg-down`, CSS variables

### 2. Component Patterns
- Inline implementations instead of `<StatusIndicator />`, `<Button />`, `<Card />`
- Missing `cn()` utility for className composition

### 3. Alert/Callout (CRITICAL)
- **BANNED**: `border-l-* rounded-*` (left border accent + rounded corners)
- Correct: icon-led with background tint, top/bottom border, full outline, or bg-only

### 4. Typography
- `font-sans` without override (should be `font-body`)
- Missing `text-balance` on headlines, `text-pretty` on body, `tabular-nums` on numbers

### 5. Animation
- Custom animation without reduced-motion handling
- `transition-all` (too broad)
- Animations >200ms for interaction feedback

### 6. Status Semantics
- Generic colors for status instead of `up`/`degraded`/`down`
- Missing aria-label on status indicators

## Output

```
[SEVERITY] file:line
  Issue: Description
  Found: Problematic code
  Fix: Suggested correction
```

HIGH: Left-border alerts, hardcoded status colors, banned fonts
MEDIUM: Missing CVA components, arbitrary colors
LOW: Typography improvements, animation optimizations

Summary: total violations by severity, most common types, prioritized fix list.
