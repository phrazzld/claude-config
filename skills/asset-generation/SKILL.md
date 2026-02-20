---
name: asset-generation
description: Programmatic visual asset pipeline for proposal-context logos and images. Uses Recraft, OpenAI Image, and Nano Banana Pro together with phase-aware breadth vs convergence.
effort: high
---

# Asset Generation

Use this skill for logos, icon marks, hero/section imagery, and texture motifs.

## Trigger

Run when user asks for:
- logo exploration or logo revisions
- better visual assets in design proposals
- proposal-specific imagery
- provider comparison (Recraft, OpenAI, Gemini/Nano Banana)

## Core Rules

1. Use **all three providers** during exploratory rounds unless user opts out:
   - Recraft
   - OpenAI Image (`gpt-image-1`)
   - Nano Banana Pro (Gemini image model)
2. Generate assets **in proposal context**, not as detached global batch.
3. Exploration width must match design uncertainty:
   - Early rounds: high style/color diversity
   - Late rounds: narrow around survivors
4. Logos must pass favicon/app-icon constraints:
   - flat, simple, low-part count
   - legible at 16px/24px
   - works one-color and full-color
5. If provider outputs are noisy/illustrative, use a **deterministic geometric SVG fallback**.
6. Treat user-provided logo references as **quality primitives only**, never literal templates.
7. Never produce marks that can be confused with existing company logos.

## Reference Archetypes (Quality North Star)

Target mark families like:
- modular rounded blocks
- orbiting dot constellation
- constrained grid/mosaic tiles
- minimalist key/keyhole symbol
- 3x3 dot matrix
- hex-aperture emblem

Avoid mascot illustrations, scene composition, and decorative line clutter.

## Reference Use Policy (Hard)

When user provides inspiration logos:
1. Extract only abstract qualities:
   - simplicity level
   - geometry type
   - corner behavior
   - stroke/fill balance
   - negative-space strategy
2. Do **not** reuse exact silhouette, arrangement, or recognizable motif from references.
3. Do **not** preserve source colorways unless the user explicitly asks.
4. Generate at least 4 structural families per batch before narrowing.
5. Reject anything that looks like "same logo with minor tweaks."

This is a hard requirement. "Inspired by" means transferable principles, not copied form.

## Complexity Budget (Hard Limits)

Reject marks that exceed:
- 8 primary primitives
- 2 stroke widths
- 2 brand colors + 1 neutral
- more than 1 internal detail per major shape

Accept only marks that remain recognizable at 24px without anti-aliasing blur.

## Phase-Aware Breadth

### Phase A: Wide Exploration (no clear winner yet)

Per proposal, generate at least:
- 1 Recraft concept
- 1 OpenAI concept
- 1 Nano Banana concept

Diversity matrix (required across batch):
- Geometry: rounded / angular / mixed
- Weight: monoline / medium / bold
- Symbol strategy: abstract / mic-derived / node-derived
- Palette families: warm, cool, neutral, high-contrast, muted

### Phase B: Convergence (2-3 survivors)

Per proposal, generate:
- 2 focused variants (best provider + fallback provider)
- tightly constrained palette and stroke system

## Provider Routing

| Task | Primary | Secondary |
|---|---|---|
| Minimal vector-like symbol mark | Recraft (`icon` or simple `logo`) | OpenAI |
| Text-sensitive wordmark lockups | Nano Banana Pro | OpenAI |
| Stylized hero/section art | Nano Banana Pro | OpenAI/Recraft raster |
| Subtle background motifs | Recraft raster / Nano Banana | OpenAI |

## Logo Prompt Contract

Always include:
- `no text`
- `no mockup`
- `no shadows`
- `no gradients` (unless explicitly testing gradient direction)
- `centered symbol`
- `flat icon`

Template:
`[brand intent], [shape language], minimalist flat icon logo, no text, no mockup, no shadows, no gradients, centered symbol, transparent or plain background`

## Proposal-Context Workflow

For each proposal `7a..7h`:
1. Read proposal DNA + palette + typography mood.
2. Generate 3 logos (Recraft/OpenAI/Nano Banana) using that proposal context.
3. Pick best mark for that proposal only.
4. Embed into that proposal HTML and tune surrounding spacing/contrast.
5. Keep alternates for review.

Do not force one logo family across all proposals during exploratory rounds.

## QA Gates (Reject if fails)

- noisy illustration masquerading as logo
- too many micro-details for favicon scale
- style clashes with proposal typography/system
- same colorway/style duplicated across whole batch
- visible gibberish text baked into background assets
- mascot/character or scene illustration instead of symbol mark
- more than one focal object in a logo frame
- obvious resemblance to known logos or user-provided samples
- structural near-duplicate across proposal logos

## Deterministic Fallback

When model outputs fail QA, generate a clean SVG mark from geometric primitives.
This is not optional for quality: use it to guarantee a production-safe floor.

## Output Layout

Use proposal-scoped paths:
- `.design-evolution/gen-N/assets/logos/7a/recraft-1.svg`
- `.design-evolution/gen-N/assets/logos/7a/openai-1.png`
- `.design-evolution/gen-N/assets/logos/7a/gemini-1.png`
- `.design-evolution/gen-N/assets/textures/7a/*.png`

Chosen production candidate:
- `.design-evolution/gen-N/assets/logos/7a/final.(svg|png)`

## Minimal Command Patterns

### Recraft (symbol mark)
```bash
python3 "$ENGINE" --repo "$REPO" recraft icon \
  "minimal flat icon mark for Vox Cloud, abstract mic+node, no text, no gradients" \
  --colors "#1E5CFF,#111827" --n 3 --out "$OUT"
```

### OpenAI (`gpt-image-1`)
```bash
curl -sS https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-image-1","prompt":"minimal flat icon logo mark, no text, no gradients, no shadows","size":"1024x1024","background":"transparent"}'
```

### Nano Banana Pro (Gemini)
```bash
curl -sS "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"minimal flat icon logo mark, no text, no gradients"}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}'
```
