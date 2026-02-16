---
name: brand-logo
description: |
  Generate and optimize brand logos. LLM SVG generation with SVGO optimization,
  favicon variants, and vision-model critique loop.
argument-hint: "[style: geometric|minimal|abstract] [--prompt \"...\"]"
effort: high
---

# /brand-logo

Generate brand logos through AI with automated optimization.

## What This Does

Creates SVG logos using LLM generation, optimizes with SVGO, generates favicon
variants, and uses a vision-model critique loop to select the best candidate.

## Process

### Phase 1: Context

Read `brand.yaml` for identity, palette, and voice:
```bash
node ~/Development/brand-kit/dist/src/cli.js validate brand.yaml
```

Extract: brand name, brand_hue, primary color, category, personality traits.

### Phase 2: Generate Candidates

Generate 4 SVG logo candidates using LLM with constrained prompts:

**Prompt template:**
```
Generate a minimal SVG logo for "[brand name]".
Constraints:
- Viewbox: 64x64
- Max 3 shapes (geometric primitives only)
- Colors: only use [primary hex] and [foreground hex]
- Style: [geometric|minimal|abstract|typographic]
- No text elements (wordmark is separate)
- No gradients, no filters, no embedded images
- Clean, scalable, distinctive at 16px
```

Generate 4 variants with different styles.

### Phase 3: Critique Loop

For each candidate:
1. Save as temporary SVG
2. Convert to PNG at 512px for vision model review
3. Score on: distinctiveness, scalability, brand alignment, simplicity
4. Select top 2 candidates

### Phase 4: User Approval

Present top 2 candidates via AskUserQuestion:
- Show rendered previews
- Ask for selection or request modifications

### Phase 5: Optimize + Variants

```bash
# Optimize SVG
npx svgo --config '{"plugins":["preset-default",{"name":"removeViewBox","active":false}]}' logo.svg -o logo-optimized.svg

# Generate favicon variants
for size in 16 32 48 180 192 512; do
  npx sharp-cli -i logo-optimized.svg -o "favicon-${size}.png" resize $size $size
done

# Generate ICO (16+32+48)
# Use sharp to combine into ICO format
```

### Phase 6: Update brand.yaml

Add logo paths to `identity.logo`:
```yaml
identity:
  logo:
    svg: ./assets/logo.svg
    mark: ./assets/logo-mark.svg
    favicon: ./assets/favicon.ico
```

## Output

```
assets/
  logo.svg              # Full optimized logo
  logo-mark.svg         # Icon/mark only
  favicon-16.png
  favicon-32.png
  favicon-48.png
  favicon-180.png       # Apple touch icon
  favicon-192.png       # Android
  favicon-512.png       # PWA splash
  favicon.ico           # Multi-resolution ICO
```

## Related Skills

- `/brand-init` — Create brand.yaml (prerequisite)
- `/brand-assets` — Generate OG cards using brand tokens
- `/nano-banana` — AI image generation (complementary for non-logo assets)
