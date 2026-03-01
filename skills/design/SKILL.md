---
name: design
description: |
  Top-level design orchestrator. Compose Tier 1 static skills + design-tokens into
  complete design systems. Two modes: Explore (greenfield, 6 distinct directions) or
  Extend (6 targeted refinements to existing system). Replaces evolve, aesthetic-system,
  design-theme, ui-skills.
effort: high
---

# DESIGN

Top-level design orchestrator. Composes:
- **`frontend-design`** (Anthropic) — aesthetic philosophy, distinctive direction
- **`taste-skill`** (Leonxlnx) — anti-slop rules, 100 AI tells, dials (8/6/4)
- **`web-design-guidelines`** (Vercel) — compliance check
- **`design-tokens`** — CSS @theme foundation, OKLCH, 8pt grid (always invoked first)

Never modify the Tier 1 static skills above — they are upstream-maintained.

---

## Mode Selection

Ask the user upfront:

> **Which mode?**
> - **Explore** — new design system, major rebrand, greenfield project → 6 distinct directions
> - **Extend** — variations within an existing system → 6 targeted refinements

---

## Phase 1: Detect Context

Check for an existing design system:
- `brand.yaml`
- `tailwind.config.ts` / `tailwind.config.js`
- `globals.css` or `app.css` (CSS `@theme` blocks, CSS custom properties)
- Component library directories (`components/ui`, `src/components`)
- `DESIGN_MEMORY.md` (per-project decision record — read this first if present)

Output summary: **Has system / Partial / None** + what exists.

---

## Phase 2: Live Research

Do NOT use a hardcoded list. Research the current ecosystem using the tools available:

```bash
gemini "Research the current state (2026) of OSS UI/UX libraries for React/Next.js.
Categorize by: component libraries (shadcn/ui, Mantine, Catalyst, daisyUI, Radix Themes,
Park UI, Ark UI), dashboard kits (Tremor, shadcn blocks), animation (Framer Motion,
Motion One, GSAP, AutoAnimate, Vaul), icon sets (Lucide, Phosphor, Heroicons),
design token systems (Radix Colors, Open Props). For each: GitHub stars, npm weekly
downloads, notable adopters, key differentiator, and whether it's still actively
maintained. Also surface any significant new entrants in 2025-2026."
```

If Gemini CLI is unavailable, use WebSearch with targeted queries per category.

Present findings as a ranked, annotated list — not a flat table. Highlight:
- What's gained serious adoption since last year
- What's declined / abandoned
- What combinations work well together (e.g., shadcn/ui + Radix Colors + Lucide)
- What's relevant specifically to **this project's domain** (e.g., dashboards, status pages, monitoring tools)

**User selects** which libraries/references to incorporate before proceeding.

---

## Phase 3: Visual Catalog — 6 Full-Page Directions

**Do not output text tables describing directions. Do not render small grid panels. Build a full-page visual catalog.**

Write a **self-contained HTML file** (`design-catalog.html` at the project root) with **tab navigation** — 6 tabs, one per direction. Each tab reveals a full-page scrollable experience that looks like a real, functioning version of the app styled in that direction.

### What "full page" means

Each direction is a complete app experience, not a component strip. The user needs to be able to scroll through the direction and understand exactly what the product would feel like to use. Every page must include:

1. **App shell** — top navigation bar with logo, nav links (Dashboard, Status Pages, Incidents, Settings), user avatar. This is the most-seen UI surface; it must feel right.

2. **Dashboard stats strip** — 4 metric cards showing monitors total, operational count, issues count, avg uptime. Use the project's real data shape.

3. **Monitor list** — 4 monitor cards in a 2-column grid showing all three status states (up, degraded, down). Each card shows: URL, status badge, response time, uptime %, 30-tick uptime bar (SVG or divs), last checked. This is the **primary component** of the app — render it with full fidelity.

4. **Active incident alert** — a banner or card showing one active incident: affected URL, duration, started time.

5. **Component kit section** (below a visual separator) — the full palette of UI primitives rendered in this direction's style:
   - All button variants: primary, secondary, ghost, outline, destructive, disabled, loading
   - All badge variants: operational, degraded, outage, unknown, neutral
   - Form input with label + helper text, and a select dropdown
   - A text input in error state
   - A toggle/switch
   - Typography scale: display heading, section heading, body, caption, monospace value
   - Color palette: all semantic tokens as labeled swatches

### Libraries must be present and visible

Each direction is anchored to a specific UI library. **The components must visually match that library** — not generic CSS that could be from anywhere.

Mandatory library inclusions via CDN:
- **Tailwind CSS** (`<script src="https://cdn.tailwindcss.com">`) — used for structural utilities in ALL directions
- **daisyUI** (`<link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css">`) — used for the daisyUI direction with `data-theme` on the section and actual semantic class names (`btn`, `badge`, `card`, `stat`, `alert`)

Other directions replicate their library's exact visual language through CSS — not generic custom styles. If the direction is "shadcn/ui", the buttons must look exactly like shadcn buttons (ring on focus, rounded-md, neutral dark, `bg-primary text-primary-foreground`). If it's "Mantine", cards must have Mantine's inset shadow + navy dark.

Label each component clearly with a comment naming the library: `<!-- shadcn/ui: Button variant=default -->`.

### Technical requirements

- **Single HTML file** with no local asset imports
- **Fonts** loaded via Google Fonts `<link>` (different font per direction)
- **Tailwind CDN** for structural layout utilities (`flex`, `grid`, `gap-*`, `px-*`, `max-w-*`)
- **Direction CSS** uses `[data-dir="d1"]` attribute selectors for scoping — no global resets that bleed between directions
- **Tab switcher** at the very top (fixed, 44px tall) — clicking a tab hides all sections and shows the selected one, scrolling to top
- **Each section** has `min-height: 100vh` and scrolls normally
- **Uptime bars** generated in JS (loop of div ticks or SVG rects) — not hardcoded HTML
- **Reduced motion** respected: all looping animations wrapped in `@media (prefers-reduced-motion: no-preference)`

### 6 maximally distinct directions

Differentiate across: type voice (serif / humanist / monospace), color temperature (warm / cool / neutral), surface treatment (flat / elevated / glass / textured), radius (sharp / medium / round), density (airy / balanced / dense), and personality (instrument / editorial / friendly / corporate / minimal / bold).

Each direction must name:
- Its anchor library/framework (e.g., "shadcn/ui", "daisyUI garden theme", "Tremor blocks")
- Why it's right for an uptime monitoring SaaS (1 sentence in a visible callout at the top of the page)
- Its taste dials (shown at the bottom of the page): DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY

### After writing the catalog

```bash
open design-catalog.html
```

Tell the user what they're looking at, what libraries are in use, and ask them to pick a direction or a hybrid.

**Explore mode:** 6 maximally distinct directions.
**Extend mode:** 6 targeted refinements of the existing system — same structure, varied on dials, token tweaks, and radius changes.

---

## Phase 4: Select + Build

User picks a direction (or hybrid of two). Then:

1. **Invoke `/design-tokens`** — token foundation first: CSS @theme, OKLCH palette, 8pt grid, semantic naming
2. **Apply constraint layers inline:**
   - `frontend-design` aesthetic principles (distinctive over generic, specific over vague)
   - `taste-skill` anti-slop rules (dials, 100 AI tells to avoid)
   - `web-design-guidelines` compliance (Vercel standards)
3. **Scaffold component library** if none exists (see Phase 5)

---

## Phase 5: Component Library Structure (if new)

Propose structure based on project type:

| Approach | Structure | When |
|----------|-----------|------|
| **Tokens + Components + Patterns** | `design-tokens/` · `ui/` · `features/` | SaaS apps — recommended default |
| **Shadcn-style** | `components/ui/` · `components/features/` | When using shadcn as base |
| **Atomic Design** | `atoms/` → `molecules/` → `organisms/` → `templates/` | Complex multi-product systems |

Scaffold includes:
- Directory structure
- Barrel exports (`index.ts` per category)
- ESLint rule stubs (no hardcoded colors/spacing outside tokens)
- TypeScript component interface conventions

---

## Design Memory

At the end of each session, write/update `DESIGN_MEMORY.md` in the project root:

```markdown
## Design Memory

- Component library: shadcn/ui + Tremor
- Font: Geist + Geist Mono
- Primary: oklch(55% 0.18 240)
- Vetoes: no purple gradients, no centered hero with DESIGN_VARIANCE > 4
- References used: Supabase Studio (navigation), Resend (typography)
- Last updated: YYYY-MM-DD
```

Read this at the start of every `/design` session. It is the source of truth for per-project decisions.

---

## Phase 6: Visual QA

After building tokens and components, verify in-browser:

1. Run `/visual-qa --fix` against affected routes
2. Check: do the rendered results match the chosen direction's intent?
3. Fix P0/P1 issues (spacing, contrast, overflow, slop indicators)
4. Re-screenshot to confirm
5. Iterate until the result passes visual inspection

Never ship design changes without seeing them rendered. Code that "should look right" often doesn't.

---

## Output

Session ends with:
1. `design-catalog.html` written and opened — user selects direction
2. Implemented token foundation (`globals.css` or equivalent) for chosen direction
3. Component library scaffold (if new)
4. Visual QA passed — screenshots confirm rendered output matches intent
5. `DESIGN_MEMORY.md` written with decisions and vetoes

Next: `/design-audit` to assess consistency, `/design-tokens` to iterate on the token layer.
