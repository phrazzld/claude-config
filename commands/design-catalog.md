---
description: Generate visual design proposal catalog with 5-8 options
argument-hint: "[route-or-url]"
---

# DESIGN-CATALOG

Generate a catalog of 5-8 design proposals before implementing anything.

## Why Catalogs

Design is visual and iterative. Showing options before implementing:
- Prevents commitment to first idea
- Surfaces unexpected directions
- Lets user make informed choices

## Process

### 1. Load Design Skills

```
Skill("frontend-design")      # Philosophy
Skill("aesthetic-system")     # Strategic direction
Skill("ui-skills")            # Implementation constraints
```

### 2. Analyze Current State

If `$1` provided (route or URL):
- Screenshot the target via Chrome MCP
- Analyze existing design DNA (typography, colors, layout, motion)

If no argument:
- Ask what to design

### 3. Research via Gemini

```bash
gemini "Analyze this [product type] for distinctive design directions.
Research 2025 trends. Anti-convergence: avoid Inter, Space Grotesk,
purple gradients, Tailwind default blue-500."
```

### 4. Generate 5-8 Proposals

For EACH proposal:
1. Build working HTML/React preview
2. Validate against ui-skills constraints
3. Run `/rams` — Must score ≥70/100
4. Only passing proposals enter catalog

**DNA variety rule**: No two proposals share >2 axes.

### 5. Present Catalog

```bash
mkdir -p .design-catalog && cd .design-catalog
python -m http.server 8888 &
```

Open in browser, screenshot, present:

```
Design Catalog Ready

[N] proposals passed validation. Live: http://localhost:8888

1. [Name] - [soul] - DNA: [code] - RAMS: [score]/100
2. [Name] - [soul] - DNA: [code] - RAMS: [score]/100
...

Browse, compare, tell me which 2-3 resonate.
```

### 6. Iterate

User selects favorites → generate hybrids → re-validate.

## Anti-Convergence Checklist

Verify NO proposal uses:
- Inter, Roboto, Space Grotesk, Satoshi as primary fonts
- Purple gradients on white backgrounds
- Tailwind default blue-500 (#3B82F6)
- Centered max-w-4xl container everywhere
- No animations at all

## Output

Catalog ready for user selection. Next: User picks direction → `/design-theme`.
