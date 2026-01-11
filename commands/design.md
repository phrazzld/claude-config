---
description: Explore design directions, generate visual proposal catalogue, iterate with user, implement selected design
argument-hint: "[route-or-url]"
---

# DESIGN

> **"Design is not just what it looks like. Design is how it works."** — Steve Jobs

Generate a visual catalogue of design proposals, iterate through collaborative refinement, and implement the selected direction.

## Intent

Transform design exploration from verbal descriptions into **visual demonstrations**. Build working HTML previews so you can *see* each direction before committing.

## Workflow

### 1. Load Design Philosophy

```
Skill("design-exploration")
Skill("frontend-design")
Skill("aesthetic-system")
Skill("ui-skills")
```

### 2. Investigation Phase

**Capture current state:**

If `$1` provided (route or URL):
```bash
# Screenshot the target
mcp__claude-in-chrome__tabs_context_mcp
mcp__claude-in-chrome__navigate url="$1"
mcp__claude-in-chrome__computer action="screenshot"
```

If no argument:
```
AskUserQuestion:
"What should I analyze for design exploration?"
Options:
- "Current project homepage" → screenshot localhost
- "Specific route" → ask for route
- "External inspiration" → ask for URL
- "Describe verbally" → proceed without screenshot
```

**Analyze existing design:**
- Typography (fonts, scale, hierarchy)
- Colors (palette, semantic usage)
- Layout (composition, whitespace)
- Motion (animations, transitions)
- Components (patterns, consistency)

**Infer current DNA:**
```
Layout: [centered|asymmetric|grid-breaking|full-bleed|bento|editorial]
Color: [dark|light|monochrome|gradient|high-contrast|brand-tinted]
Typography: [display-heavy|text-forward|minimal|expressive|editorial]
Motion: [orchestrated|subtle|aggressive|none|scroll-triggered]
Density: [spacious|compact|mixed|full-bleed]
Background: [solid|gradient|textured|patterned|layered]
```

**Research via Gemini:**
```bash
gemini "Analyze this [product type] design for improvement opportunities.
Current DNA: [inferred code]

Research:
- What patterns feel dated or generic?
- What distinctive directions could elevate this in 2025?
- Anti-convergence: Avoid Inter, Space Grotesk, purple gradients
- Real examples of memorable design in this category"
```

### 3. Build Visual Catalogue

**Create catalogue structure:**
```bash
mkdir -p .design-catalogue/{styles,proposals,assets}
```

**Generate 5-8 proposals** with DNA variety:
- Each proposal = working HTML preview
- No two proposals share >2 DNA axes
- At least 1 bold, 1 subtle, 1 wild card direction

**Reference templates:**
- `design-exploration/references/viewer-template.html`
- `design-exploration/references/proposal-template.html`

**Build each proposal:**
1. Copy proposal-template.html
2. Replace CSS custom properties with proposal's design tokens
3. Add Google Fonts link for proposal's typography
4. Customize hero, colors, components to match DNA

**Build viewer:**
1. Copy viewer-template.html
2. Generate proposal cards
3. Add proposal metadata (names, DNA, souls)

### 4. Present Catalogue

**Start local server:**
```bash
cd .design-catalogue && python -m http.server 8888 &
```

**Open in browser:**
```bash
mcp__claude-in-chrome__navigate url="http://localhost:8888"
mcp__claude-in-chrome__computer action="screenshot"
```

**Present to user:**
```
Design Catalogue Ready

I've built [N] visual proposals exploring different directions.
Live catalogue: http://localhost:8888

Overview:
1. [Name] - [soul statement] - DNA: [code]
2. [Name] - [soul statement] - DNA: [code]
...

Browse the catalogue, click cards for full preview, use Compare mode
to see options side-by-side. Then tell me which 2-3 resonate.
```

### 5. Collaborative Refinement

**First selection:**
```
AskUserQuestion:
"Which directions interest you most? (select 2-3)"
Options: [Proposal names with brief descriptions]
multiSelect: true
```

**Refinement dialogue:**
- "What specifically appeals about [selection]?"
- "Anything to change or combine from different proposals?"
- "Should I generate hybrid proposals?"

**If hybrid requested:**
- Generate 2-3 new proposals blending selected elements
- Add to catalogue
- Re-serve and present

### 6. Final Selection

```
AskUserQuestion:
"Which direction should we implement?"
Options: [Finalist names]
+ "Generate more options"
+ "Refine existing options"
```

### 7. Implementation Path

```
AskUserQuestion:
"How should we implement [selected direction]?"
Options:
- "Full aesthetic overhaul (/aesthetic)" → invoke /aesthetic with direction
- "Iterative polish (/polish)" → invoke /polish with direction
- "Generate design tokens only" → output tokens, manual implementation
```

**Pass selected direction to implementation command:**
```
Selected Direction: [Name]
DNA: [code]
Typography: [fonts]
Colors: [palette]
Key Moves: [changes]
```

### 8. Cleanup

```bash
# Stop server
pkill -f "python -m http.server 8888"

# Keep or remove catalogue
AskUserQuestion:
"Keep the design catalogue for reference?"
Options:
- "Yes, keep .design-catalogue/"
- "No, remove it"
```

---

## DNA Variety Rules

**No two proposals may share >2 axes.**

Example valid catalogue:
```
01-midnight:  [editorial, dark, display, scroll, spacious, layered]
02-swiss:     [grid-breaking, light, minimal, none, compact, solid]
03-warm:      [centered, brand-tinted, text-forward, subtle, spacious, gradient]
04-brutalist: [asymmetric, monochrome, display, aggressive, mixed, textured]
05-luxe:      [asymmetric, gradient, expressive, orchestrated, spacious, layered]
```

---

## Anti-Convergence Checklist

Before finalizing catalogue, verify no proposal uses:
- Inter, Roboto, Space Grotesk, Satoshi as primary fonts
- Purple gradients on white backgrounds
- Tailwind default blue-500 (#3B82F6) unchanged
- Centered max-w-4xl container on every proposal
- No animations at all

Reference: `aesthetic-system/references/banned-patterns.md`

---

## Related Commands

- `/aesthetic` - Strategic design audit (invokes this skill at Phase 0)
- `/polish` - Iterative refinement (invokes this skill when direction unclear)
- `/build` - Implementation (receives selected direction)
