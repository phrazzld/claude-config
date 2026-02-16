---
name: brand-init
description: |
  Unified brand discovery that outputs brand.yaml. Merges brand-builder
  (voice/audience) + design-exploration (visual direction) into one flow.
  Run once per project to establish brand identity.
argument-hint: "[project-name]"
effort: high
---

# /brand-init

Create `brand.yaml` from scratch through interactive discovery.

## What This Does

Guided process that produces a complete `brand.yaml` — the single source of truth
for brand identity, visual tokens, voice, and content strategy. Replaces running
`/brand-builder` + `/design-tokens` separately.

## Process

### Phase 1: Discovery (Interactive)

Gather context automatically, then ask focused questions.

**Auto-gather:**
```bash
# Tech stack, features, README
cat package.json 2>/dev/null | jq '{name, description, keywords}'
cat README.md 2>/dev/null | head -100
git log --oneline -10
```

**Ask via AskUserQuestion:**

1. **Identity**: Product name, domain, tagline, category
2. **Audience**: Primary user, segments, pain points
3. **Voice**: Tone (casual/professional/technical/playful), personality traits, things to avoid
4. **Content**: Topics, mix (product vs valuable), posting frequency

### Phase 2: Visual Direction (Interactive)

5. **Brand hue**: Present 4 hue options based on category:
   - SaaS/tech → blue (250), purple (280)
   - Health/fitness → green (140), teal (170)
   - Finance → navy (220), emerald (160)
   - Creative → orange (30), magenta (330)
   - Custom hue (0-360)

6. **Typography**: Display + sans + mono font stacks
   - Modern: Inter/Geist
   - Classical: Playfair Display + serif
   - Technical: JetBrains Mono focused
   - Custom

7. **Color overrides**: Accept specific hex colors if the brand already has them.
   Convert to OKLCH using `hexToOklch()` from brand-kit.

### Phase 3: Generation

Build the `brand.yaml` structure:

```bash
# If brand-profile.yaml already exists, offer migration instead
if [ -f brand-profile.yaml ]; then
  node ~/Development/brand-kit/dist/src/cli.js migrate \
    --profile brand-profile.yaml \
    $([ -f design-tokens.json ] && echo "--tokens design-tokens.json") \
    --out brand.yaml
fi
```

For new brands, construct the YAML programmatically with all sections:
- `version: "1"`
- `identity` from Phase 1
- `audience` from Phase 1
- `voice` from Phase 1
- `palette` with brand_hue, primary/secondary/accent (OKLCH + hex), light/dark backgrounds
- `typography` from Phase 2
- `spacing`, `radii`, `elevation`, `motion` with sensible defaults
- `content` from Phase 1
- `inspirations` from Phase 1
- `meta` with generation timestamp

### Phase 4: Validate + Compile

```bash
node ~/Development/brand-kit/dist/src/cli.js validate brand.yaml
node ~/Development/brand-kit/dist/src/cli.js compile --out ./src/styles
```

### Phase 5: Preview

Generate a sample OG card to show the brand visually:

```bash
node ~/Development/brand-kit/dist/src/cli.js render og-default \
  --title "[Product Name]" \
  --subtitle "[Tagline]" \
  --out ./brand-preview.png
```

Show the preview to the user for approval.

## Re-running

If `brand.yaml` exists:
1. Load existing brand
2. Ask which sections to update
3. Preserve unchanged sections
4. Recompile tokens

## Migration Path

Existing projects with `brand-profile.yaml`:
- Auto-detect and offer migration
- Preserves all voice/content data
- Adds visual tokens (palette, typography, spacing)
- Old file kept as backup

## Output

- `brand.yaml` in project root
- Compiled tokens in `./src/styles/` (or specified directory)
- Preview image `./brand-preview.png`

## Related Skills

- `/brand-compile` — Recompile tokens after editing brand.yaml
- `/brand-assets` — Generate OG cards and social images
- `/brand-builder` — Legacy brand discovery (superseded)
- `/design-tokens` — Design token patterns reference
