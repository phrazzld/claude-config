---
name: heartbeat-design
description: |
  Kyoto Moss design system for Heartbeat uptime monitoring.
  Invoke when building, modifying, or reviewing Heartbeat UI components.
  Ensures visual consistency and prevents design violations.
---

# Heartbeat Design System: Kyoto Moss

## Philosophy

Japanese minimalism meets wabi-sabi. Technology in harmony with nature.

- **Uptime** = Spring growth (moss green vitality)
- **Degraded** = Autumn warning (clay/amber transition)
- **Downtime** = Winter stillness (brick red, managed with composure)

The interface should feel like a calm garden—incidents are natural cycles to acknowledge and address, not emergencies that induce panic.

## Token Architecture

Heartbeat uses a flat token structure where keys map directly to CSS variables.

### Required Imports

```tsx
import { cn } from "@/lib/cn";
import { kyotoMossTheme, getStatusClasses } from "@/lib/design";
import { Button, Card, StatusIndicator } from "@/components/ui";
```

### Background Tokens

| Token                   | Light               | Dark                | Usage                    |
| ----------------------- | ------------------- | ------------------- | ------------------------ |
| `--color-bg-primary`    | #f5f2eb             | #1a1f1c             | Page background          |
| `--color-bg-secondary`  | #ebe8e1             | #242a26             | Section backgrounds      |
| `--color-bg-tertiary`   | #e0ddd6             | #2e3630             | Hover states             |
| `--color-bg-elevated`   | rgba(255,255,255,0.6) | rgba(255,255,255,0.04) | Cards, panels     |

### Text Tokens

| Token                   | Light   | Dark    | Usage                    |
| ----------------------- | ------- | ------- | ------------------------ |
| `--color-text-primary`  | #2d4a3e | #e8e5de | Primary text             |
| `--color-text-secondary`| #5a6b62 | #b5b0a5 | Secondary text           |
| `--color-text-tertiary` | #8b7355 | #8b8578 | Tertiary/clay accent     |
| `--color-text-muted`    | #a09080 | #6b665c | Disabled, hints          |

### Status Tokens (CRITICAL)

These are the semantic heart of Heartbeat. ALWAYS use these for status-related UI.

| Status   | Solid Token               | Muted Token                     | Usage                    |
| -------- | ------------------------- | ------------------------------- | ------------------------ |
| Up       | `--color-status-up`       | `--color-status-up-muted`       | Healthy, operational     |
| Degraded | `--color-status-degraded` | `--color-status-degraded-muted` | Slow, warning            |
| Down     | `--color-status-down`     | `--color-status-down-muted`     | Outage, incident         |

### Typography

| Token           | Value                                         | Usage              |
| --------------- | --------------------------------------------- | ------------------ |
| `--font-display`| "Noto Serif JP", serif                        | Headlines, display |
| `--font-body`   | "Manrope", system-ui                          | Body text          |
| `--font-mono`   | "IBM Plex Mono", monospace                    | Data, code         |

## Component Patterns

### StatusIndicator

ALWAYS use the CVA-based StatusIndicator for status display:

```tsx
import { StatusIndicator } from "@/components/ui";

<StatusIndicator status="up" size="md" />
<StatusIndicator status="degraded" size="lg" glow />
<StatusIndicator status="down" size="xl" />
```

Status indicators use the `animate-km-breathe` animation for "up" state.

### Cards

Use the Card component with appropriate variants:

```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui";

<Card variant="default" padding="md">
  <CardHeader>
    <CardTitle>Monitor Name</CardTitle>
  </CardHeader>
  <CardContent>...</CardContent>
</Card>
```

### Buttons

```tsx
import { Button } from "@/components/ui";

<Button variant="primary">Add Monitor</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="danger">Delete</Button>
<Button variant="ghost" size="icon-sm">...</Button>
```

## Animation Guidelines

### Breathing Animation

Status indicators use `animate-km-breathe` (4s cycle, subtle scale):

- Up: Full breathing animation
- Degraded: Subtle breathing (`animate-km-breathe-subtle`)
- Down: No animation (stillness)

### Transitions

- Use `duration-normal` (200ms) for interaction feedback
- Use `duration-fast` (100ms) for micro-interactions
- Use `ease-out` for entrances
- NEVER exceed 200ms for hover/click feedback

### Reduced Motion

ALWAYS respect `prefers-reduced-motion`. The CSS handles this automatically, but avoid adding inline JavaScript animations that bypass it.

## BANNED PATTERNS

These patterns are EXPLICITLY FORBIDDEN in Heartbeat:

### Never Use

1. **Left-border accent with rounded corners** for alerts/callouts
2. **Purple/blue gradients** on any background
3. **Inter, Roboto, Arial, Space Grotesk** fonts
4. **Tailwind default colors** without semantic mapping (e.g., `bg-blue-500`)
5. **Arbitrary color values** (e.g., `bg-[#123456]`)
6. **Generic hero badges** ("New", "AI-Powered", "Beta")
7. **Glow effects as primary affordances**

### Instead Use

- Icon-led alerts with background tint
- Kyoto Moss semantic tokens
- Design system fonts (`font-display`, `font-body`, `font-mono`)
- Status colors for semantic meaning
- CSS variable references (`var(--color-status-up)`)

## File Structure

```
lib/design/
  tokens.ts          # Token type definitions
  schema.ts          # defineTheme factory + validation
  presets/
    kyoto-moss.ts    # Theme preset values
  apply.ts           # Runtime theme application
  index.ts           # Re-exports

components/ui/
  Button.tsx         # CVA-based button
  Card.tsx           # CVA-based card
  StatusIndicator.tsx # CVA-based status indicator
  index.ts           # Re-exports

app/globals.css      # Design tokens + Kyoto Moss styling
```

## Validation Checklist

Before committing UI changes, verify:

```
[ ] Uses design system tokens (not hardcoded colors)
[ ] Uses CVA variants for components
[ ] Status colors map to semantic tokens
[ ] No left-border-accent alerts
[ ] No banned fonts
[ ] No arbitrary Tailwind values for colors
[ ] Animations respect reduced motion
[ ] Text uses text-balance/text-pretty appropriately
[ ] Data uses tabular-nums
```

## Quick Reference

```tsx
// Status color classes
.bg-up          // Moss green
.bg-degraded    // Clay amber
.bg-down        // Brick red
.bg-up-muted    // Subtle moss background
.text-up        // Moss green text

// Animations
.animate-km-breathe         // Status indicator breathing
.animate-km-breathe-subtle  // Subtle breathing
.animate-km-fade-in-up      // Entrance animation

// Typography
.font-display   // Noto Serif JP
.font-body      // Manrope
.font-mono      // IBM Plex Mono
.text-display   // Display headline styling
.text-mono      // Monospace with tabular-nums

// Surfaces
.glass-panel    // Translucent with blur
.card-hover     // Interactive card hover effect
```
