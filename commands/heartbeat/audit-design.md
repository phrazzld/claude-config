---
description: Audit Heartbeat components for Kyoto Moss design system compliance
---

# Audit Kyoto Moss Design System Compliance

Scan Heartbeat components for design system violations. Report issues with file:line and suggested fixes.

## Audit Categories

### 1. Token Usage

Search for hardcoded colors, spacing, and fonts that should use design tokens:

**Violations to find:**
- `bg-[#...]` or `text-[#...]` - arbitrary color values
- `bg-blue-500`, `bg-green-400`, etc. - Tailwind defaults without semantic mapping
- `bg-white`, `bg-black` - hardcoded instead of semantic
- `text-gray-*` - should use `text-[var(--color-text-*)]`
- Direct hex values in className or style props

**Correct patterns:**
- `bg-up`, `bg-degraded`, `bg-down` for status
- `text-[var(--color-text-primary)]` or CSS classes
- Design token CSS variables

### 2. Component Patterns

Check for correct usage of CVA components:

**Violations to find:**
- Inline status indicator implementations (should use `<StatusIndicator />`)
- Custom button styling (should use `<Button variant="..." />`)
- Manual card styling (should use `<Card variant="..." />`)
- Missing `cn()` utility for className composition

**Correct patterns:**
```tsx
import { StatusIndicator, Button, Card } from "@/components/ui";
import { cn } from "@/lib/cn";
```

### 3. Alert/Callout Patterns

**CRITICAL VIOLATION:** Left border accent with rounded corners

```tsx
// BANNED - Report as HIGH severity
className="border-l-4 border-blue-500 rounded-lg"
className="border-l-2 rounded-md bg-blue-50"
style={{ borderLeft: "3px solid", borderRadius: "8px" }}
```

**Correct alternatives:**
- Icon-led with full background tint
- Top/bottom border instead of left
- Full outline style
- No border, background only

### 4. Typography

**Violations to find:**
- `font-sans` without override (should be `font-body`)
- `font-serif` without override (should be `font-display`)
- Inter, Roboto, Arial, Space Grotesk references
- Missing `text-balance` on headlines
- Missing `text-pretty` on body paragraphs
- Missing `tabular-nums` on numeric data

### 5. Animation

**Violations to find:**
- Custom animation without reduced-motion handling
- Animations longer than 200ms for interaction feedback
- `transition-all` usage (too broad)
- Missing `will-change` cleanup

**Correct patterns:**
- Use `animate-km-breathe` for status indicators
- Use `duration-normal` (200ms) for transitions
- Leverage CSS `@media (prefers-reduced-motion)` handling

### 6. Status Semantics

**Violations to find:**
- Using generic colors for status (green/red/yellow instead of up/degraded/down)
- Status without proper aria-label
- Missing breathing animation on "up" status indicators

## Output Format

For each violation found:

```
[SEVERITY] file:line
  Issue: Description of the violation
  Found: The problematic code
  Fix: Suggested correction
```

Severity levels:
- **HIGH**: Left-border alerts, hardcoded status colors, banned fonts
- **MEDIUM**: Missing CVA components, arbitrary colors
- **LOW**: Typography improvements, animation optimizations

## Scan Commands

Run these searches to find violations:

```bash
# Find arbitrary colors
rg 'bg-\[#' --type tsx components/
rg 'text-\[#' --type tsx components/

# Find Tailwind defaults used for status
rg 'bg-(green|red|yellow|blue)-[0-9]' --type tsx components/

# Find left-border patterns
rg 'border-l-[0-9].*rounded' --type tsx components/
rg 'borderLeft.*borderRadius' --type tsx components/

# Find banned fonts
rg '(Inter|Roboto|Arial|Space.Grotesk)' --type tsx --type css

# Find inline status implementations
rg 'status.*===.*"up".*bg-' --type tsx components/
```

## Summary Report

After scanning, provide:

1. Total violations by severity
2. Most common violation types
3. Files with most issues
4. Prioritized fix list (high severity first)
