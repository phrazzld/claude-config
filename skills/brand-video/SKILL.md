---
name: brand-video
description: |
  Generate branded video content with Remotion. Combines brand tokens,
  voiceover, and screen captures into polished product videos.
argument-hint: "[type: demo|feature|launch] [--script \"...\"]"
effort: high
---

# /brand-video

Create branded video content using Remotion compositions.

## What This Does

Chains brand tokens, voiceover generation, and Remotion rendering into
branded video content. Consumes `tokens.ts` for consistent visual identity.

## Prerequisites

- `brand.yaml` in project root (run `/brand-init`)
- Compiled tokens (run `/brand-compile`)
- Remotion installed in project or available globally

## Process

### Phase 1: Script + Voiceover

1. Generate or accept video script
2. Run `/voiceover` to generate audio with ElevenLabs
3. Extract word-level timestamps from ElevenLabs response

### Phase 2: Scene Composition

Import brand tokens into Remotion compositions:

```typescript
import { brand } from "./brand-output/tokens.js";

// Available branded scenes:
// - TitleScene: Brand name + tagline with accent gradient
// - FeatureScene: Feature title + description + screenshot
// - EndCard: CTA with brand colors
// - CaptionOverlay: Synced captions using voiceover timestamps
```

### Phase 3: Assembly

Compose scenes with voiceover sync:
1. TitleScene (2-3s)
2. FeatureScene[] (per feature, synced to voiceover)
3. Screen capture segments (if demo)
4. EndCard (3s)

### Phase 4: Render

```bash
npx remotion render src/video/BrandVideo.tsx brand-video.mp4 \
  --props '{"brandTokens": "./brand-output/tokens.ts", "voiceover": "./voiceover.mp3"}'
```

## Video Types

| Type | Scenes | Duration |
|------|--------|----------|
| `demo` | Title → Screen capture → Features → End | 60-90s |
| `feature` | Title → Feature deep-dive → End | 30-45s |
| `launch` | Title → Problem → Solution → Features → CTA | 45-60s |

## Scene Templates

Templates live in the project's Remotion source and import `tokens.ts`:
- Branded title cards with primary color gradient
- Feature callouts with accent highlights
- Caption overlays with brand typography
- End cards with CTA and brand logo

## Related Skills

- `/brand-compile` — Compile tokens (prerequisite)
- `/voiceover` — Generate voiceover audio
- `/demo-video` — Legacy demo video (enhanced by brand-video)
