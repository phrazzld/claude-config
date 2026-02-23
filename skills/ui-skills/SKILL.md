---
name: ui-skills
user-invocable: false
description: Opinionated constraints for building better interfaces with agents.
effort: high
---

# UI Skills

When invoked, apply these opinionated constraints for building better interfaces.

## MANDATORY: Kimi Delegation for UI Implementation

**All UI implementation work MUST be delegated to Kimi K2.5 via MCP.**

Kimi excels at frontend development. Claude reviews, Kimi builds:

```javascript
// Delegate UI implementation to Kimi
mcp__kimi__spawn_agent({
  prompt: `Implement [component/feature].
Apply ui-skills constraints:
- Tailwind CSS defaults, cn() utility
- Accessible primitives (Base UI/Radix/React Aria)
- No h-screen (use h-dvh), respect safe-area-inset
- Animator only transform/opacity, max 200ms feedback
- text-balance for headings, tabular-nums for data
Existing patterns: [reference files]
Output: ${targetPath}`,
  thinking: true
})
```

**Workflow:**
1. Define constraints → Claude (this skill)
2. Implement UI → Kimi (Agent Swarm)
3. Review quality → Claude (expert panel review)

**Anti-pattern:** Implementing UI yourself instead of delegating to Kimi.

## How to use

- `/ui-skills`
  Apply these constraints to any UI work in this conversation.

- `/ui-skills <file>`
  Review the file against all constraints below and output:
  - violations (quote the exact line/snippet)
  - why it matters (1 short sentence)
  - a concrete fix (code-level suggestion)

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `React Aria`, `Radix`)
- MUST use the project’s existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen` for full-height sections — ALWAYS use `min-h-[100dvh]` (prevents iOS Safari layout jump)
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements
- MUST verify 3rd-party package exists in `package.json` before importing — output install command if missing
- MUST provide Loading, Empty, and Error states for every data-driven surface

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces
- MUST isolate perpetual/infinite animations in their own `React.memo` Client Component — never in parent layout
- NEVER use React `useState` for continuous animations — use Framer Motion `useMotionValue`/`useTransform`
- NEVER mix GSAP/ThreeJS with Framer Motion in the same component tree
- MUST wrap grain/noise filters on `fixed inset-0 pointer-events-none` elements only — never on scrolling containers
- MUST include cleanup functions in all `useEffect` animations

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`) — use only for systemic layers (nav, modal, overlay)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`
- MUST use CSS Grid for multi-column structures — NEVER flexbox percentage math (`w-[calc(33%-1rem)]`)

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

## Expert Panel Review (MANDATORY)

**Before returning ANY design output to the user, it MUST pass expert panel review.**

See full details: `references/expert-panel-review.md`

### Quick Reference

1. Simulate 10 world-class advertorial experts:
   - **Ogilvy** (advertising), **Rams** (industrial design), **Scher** (typography)
   - **Wiebe** (conversion copy), **Laja** (CRO), **Walter** (UX)
   - **Cialdini** (persuasion), **Ive** (product design), **Wroblewski** (mobile)
   - **Millman** (brand strategy)

2. Each expert scores 0-100 with specific improvement feedback

3. **Threshold: 90+ average required**

4. If below 90: implement feedback, iterate, re-review

5. Only return design to user when 90+ achieved

### Example Output

```markdown
Expert Panel Review: Hero Section

| Expert | Score | Critical Improvement |
|--------|-------|---------------------|
| Ogilvy | 88 | Lead with benefit, not feature |
| Rams | 94 | Clean, focused |
| Scher | 86 | H2 needs more weight contrast |
| Wiebe | 81 | "Get Started" → "Start Free Trial" |
| Laja | 77 | No social proof above fold |
| Walter | 90 | Good emotional resonance |
| Cialdini | 83 | Add urgency element |
| Ive | 92 | Refined execution |
| Wroblewski | 88 | Touch targets good |
| Millman | 85 | Voice slightly inconsistent |

**Average: 86.4** ❌ Below threshold

Implementing: Laja (social proof), Wiebe (CTA), Cialdini (urgency)...
```

### Anti-Patterns

- ❌ Skipping review for "quick fixes"
- ❌ Accepting 85+ as "close enough"
- ❌ Generic feedback ("make it better")
- ❌ Returning design without 90+ score

## Pre-Flight Checklist (MANDATORY — After Expert Panel, Before Return)

Apply this checklist as the final gate before returning any design output:

```
- [ ] Mobile collapse guaranteed (single-column) for DESIGN_VARIANCE > 4?
- [ ] Full-height sections use min-h-[100dvh] not h-screen?
- [ ] All useEffect animations have cleanup functions?
- [ ] Empty, loading, and error states provided for data surfaces?
- [ ] CPU-heavy perpetual animations isolated in React.memo Client Components?
- [ ] Only transform/opacity animated (never top/left/width/height)?
- [ ] No Inter font, no 3-column equal card grid, no inline style={{}}?
- [ ] 3rd-party imports verified against package.json?
```

## Dial Reference (taste-skill Integration)

Active dials control generation behavior. Defaults from taste-skill (8/6/4):

| Dial | Axis | 1-3 | 4-7 | 8-10 |
|------|------|-----|-----|------|
| `DESIGN_VARIANCE` | Layout | Centered/symmetric | Offset | Asymmetric/masonry |
| `MOTION_INTENSITY` | Motion | None/hover only | Fluid CSS transitions | Spring physics, GSAP |
| `VISUAL_DENSITY` | Density | Spacious/gallery | Daily app | Cockpit/data-dense |

When `/evolve` passes `--variance=N --motion=N --density=N`, these override defaults.
Inject resolved dial values into every proposal generation prompt.
