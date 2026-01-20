---
description: Design lab with visual proposals validated by holy trinity
argument-hint: "[route-or-url]"
---

# DESIGN

> "Design is not just what it looks like. Design is how it works." — Steve Jobs

Design exploration with continuous quality validation. Every proposal passes the holy trinity before you see it.

## The Holy Trinity (Active Throughout)

1. **ui-skills** — Implementation constraints (8 domains: stack, components, interaction, animation, typography, layout, performance, design)
2. **rams** — Accessibility + visual design audit (WCAG 2.1, score /100)
3. **web-interface-guidelines** — Vercel web standards (15+ categories)

These are NOT gates at the end—they guide every proposal from creation.

## Workflow

### 1. Load Design Stack

```
Skill("frontend-design")        # Philosophy layer
Skill("aesthetic-system")       # Strategic direction
Skill("ui-skills")              # Implementation constraints (stays active)
```

### 2. Investigation

If `$1` provided (route or URL):
- Screenshot the target via Chrome MCP
- Analyze existing design DNA

If no argument:
```
AskUserQuestion:
"What should I analyze for design exploration?"
Options:
- "Current project homepage"
- "Specific route"
- "External inspiration URL"
- "Describe verbally"
```

**Analyze:**
- Typography, colors, layout, motion, components
- Infer current DNA code

**Research via Gemini:**
```bash
gemini "Analyze this [product type] for improvement opportunities.
Current DNA: [code]
Research distinctive directions for 2025.
Anti-convergence: Avoid Inter, Space Grotesk, purple gradients."
```

### 3. Generate Proposals (5-8)

For EACH proposal:

1. **Build** working HTML/React preview
2. **Validate ui-skills** — Fix any constraint violations
3. **Run /rams** — Must score ≥70/100 before inclusion
4. **Only passing proposals enter catalogue**

DNA variety rule: No two proposals share >2 axes.

### 4. Present Catalogue

```bash
mkdir -p .design-catalogue && cd .design-catalogue
python -m http.server 8888 &
```

Open in browser, take screenshot, present to user:

```
Design Catalogue Ready

[N] proposals passed validation. Live: http://localhost:8888

1. [Name] - [soul] - DNA: [code] - RAMS: [score]/100
2. [Name] - [soul] - DNA: [code] - RAMS: [score]/100
...

Browse, compare, tell me which 2-3 resonate.
```

### 5. Iterate

User selects favorites → generate hybrids → re-validate against trinity.

Each hybrid must pass:
- ui-skills constraints
- rams score ≥70/100

### 6. Final Selection

```
AskUserQuestion:
"Which direction should we implement?"
Options: [Finalist names]
```

### 7. Quality Gate

Run full `/web-interface-guidelines` audit on selected design.

Pass criteria: No critical or serious issues.

If issues found → fix → re-audit until clean.

### 8. Handoff

Output locked design DNA:

```markdown
## Selected Design: [Name]

**DNA**: [code]
**Typography**: [fonts]
**Colors**: [palette]
**Key Constraints**: [from ui-skills]
**RAMS Score**: [score]/100
**WIG Status**: Clean

Ready for /build.
```

## Anti-Convergence Checklist

Before finalizing, verify NO proposal uses:
- Inter, Roboto, Space Grotesk, Satoshi as primary fonts
- Purple gradients on white backgrounds
- Tailwind default blue-500 (#3B82F6) unchanged
- Centered max-w-4xl container on every proposal
- No animations at all

Reference: `aesthetic-system/references/banned-patterns.md`

## Cleanup

```bash
pkill -f "python -m http.server 8888"
```

```
AskUserQuestion:
"Keep the design catalogue?"
Options:
- "Yes, keep .design-catalogue/"
- "No, remove it"
```

## Related Commands

- `/aesthetic` - Strategic design audit (6 phases, council lenses)
- `/polish` - Iterative screenshot-critique refinement loop
- `/build` - Implementation (receives locked design DNA)
