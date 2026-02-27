---
name: evolve
description: |
  Compounding design intelligence. Genetic algorithm for design systems with
  persistent cross-project memory, brand auto-detection, and image generation.

  Invoke when:
  - User wants to explore design directions iteratively
  - "evolve", "design evolution", "genetic design", "iterate on designs"
  - Before /design-theme when direction is unclear and user wants options
  - Logo/icon generation with brand enforcement
  - Brand infrastructure audit ("what design tokens exist?")

  What makes it different from /design-and-refine or /frontend-design:
  - Persistent memory: taste compounds across sessions and repos
  - Hard preferences: vetoes ("never sans-serif") and mandates ("always OKLCH")
  - DNA bank: save interesting designs from any project for reuse
  - Brand auto-detection: scans repos for existing design infrastructure
  - Image generation: Recraft AI for vector logos, nano-banana for raster
effort: high
argument-hint: "[project-name] [--scope full|component] [--contexts saas,landing] [--variance=N] [--motion=N] [--density=N]"
---

# Design Evolution v2

Genetic algorithm over DNA codes + persistent design memory.
Simple loop: detect brand → generate population → user selects winners/losers →
mutate winners, kill losers, add immigrants → repeat until lock-in.
Learning persists across sessions and repositories.

## Engine

All state via `engine.py`. Per-project state in `.design-evolution/evolution.yaml`.
Global memory in `~/.claude/design-memory.db` (SQLite, auto-created).

```bash
ENGINE="$HOME/.claude/skills/evolve/engine.py"
python3 "$ENGINE" --repo "$REPO" <command> [args]
```

## First Invocation

### 1. Brand Auto-Detection

Run brand detection first:

```bash
python3 "$ENGINE" --repo "$REPO" detect
```

This scans for: brand.yaml, tailwind config, @theme CSS blocks, Google Fonts,
component libraries (shadcn, Radix, etc.), dark mode support. Reports completeness
score (0-100%) and remediation suggestions.

If gaps found, offer to run remediation:
- Missing brand.yaml → "Run /brand-init first?"
- Missing tokens → "Run /brand-compile first?"

### 2. Ask Constraint Level

```
AskUserQuestion:
"How much creative freedom?"
- "Strict" → Lock color+typography. Evolve layout/motion/density/background only.
- "Extend" → Respect existing tokens but allow new ones.
- "Reimagine" → Brand as inspiration only. Everything open.
- "Greenfield" → Ignore existing design system. Start fresh.
```

### 3. Ask Scope + Context

```
AskUserQuestion:
"What's the scope?"
- "Full design system" → scope=full
- "Specific component" → scope=component (ask which)

"What context?" (multiselect)
- SaaS / Landing / Dashboard / Portfolio / E-commerce
```

Context tags affect which taste data is loaded from memory. A "saas" project
inherits preferences from past "saas" work but not "landing" preferences.

### 3b. Parse Taste Dials

Parse `--variance`, `--motion`, `--density` args. Defaults from taste-skill: **8/6/4**.

```
DESIGN_VARIANCE = args.variance ?? 8   # Layout axis: 1-3=centered, 4-7=offset, 8-10=asymmetric
MOTION_INTENSITY = args.motion ?? 6    # Motion axis: 1-3=none/subtle, 4-7=orchestrated, 8-10=aggressive
VISUAL_DENSITY = args.density ?? 4     # Density axis: 1-3=spacious, 4-7=mixed, 8-10=compact
```

These values are injected into EVERY proposal generation prompt. They override the DNA axes
for Layout, Motion, and Density (additive precision — not a replacement for DNA codes).

### 4. Initialize

```bash
python3 "$ENGINE" --repo "$REPO" init \
  --project "$PROJECT" \
  --scope "$SCOPE" \
  --contexts "saas,dashboard" \
  --brand "$BRAND_FILE" \
  --lock "$LOCKED_AXES" \
  --population 8
```

This auto-detects brand state, registers the project in memory, and imports
any existing evolution data.

### 5. Generate Population

```bash
python3 "$ENGINE" --repo "$REPO" suggest --count 8
```

For first pass exploration, prefer hardened seed mode:

```bash
python3 "$ENGINE" --repo "$REPO" seed --count 8
```

`seed` guarantees:
- high-variance DNA spread (diversity floor 4+)
- materialized HTML previews for every proposal
- fallback logo assets per proposal

Population is biased by:
- **Local taste** from this project's prior selections (2x weight)
- **Global taste** from all past projects
- **Contextual taste** from projects with matching context tags (1.5x weight)
- **Hard preferences**: vetoed values excluded, mandated values boosted
- **DNA bank**: 1-2 slots seeded from banked interesting designs

### 5b. Explicit Anchor Mode (Mandatory)

If user explicitly names a prior proposal as target direction (example: `gen-5/5a`):
- Freeze that proposal as the baseline archetype for next generation.
- Build survivors/mutations from that anchor first, not from latest generation winners.
- Keep at least one near-faithful baseline variant to prevent drift.
- Treat "go back to X" as a hard constraint, not soft preference.

### 5c. Hard Preference Enforcement (MANDATORY — Run Before EVERY Generation)

Before generating ANY proposals, query ALL hard preferences from the design memory DB:

```bash
python3 "$ENGINE" memory rules
```

Extract every VETO and MANDATE. Build a **BANNED/REQUIRED** block that gets
injected verbatim into EVERY agent prompt (survivors, mutations, immigrants — all of them).

Format for agent prompts:
```
=== HARD VETOES (ABSOLUTE — violating ANY of these = instant rejection) ===
- NEVER use [font]: [reason]
- NEVER use [CSS pattern]: [reason]
- NEVER use [color/background]: [reason]
...

=== HARD MANDATES (REQUIRED — omitting ANY of these = instant rejection) ===
- ALWAYS use [pattern]: [reason]
...
```

**Why this exists:** Vetoes stored in the DB were not reaching agent prompts,
causing the same rejected patterns (border-top on rounded cards, banned fonts)
to reappear generation after generation. This step is non-negotiable.

CSS-level vetoes (card border treatments, dark-in-light theming) are stored
alongside DNA-axis vetoes. Both MUST be included in prompts.

### 5d. Survivor Fidelity (MANDATORY)

Survivors and mutations MUST be given the actual parent HTML file to READ and MODIFY.
Giving agents only a DNA code and description causes them to generate from scratch,
losing all the qualities that made the parent a winner.

For each survivor/mutation agent prompt:
1. Include the full path to the parent HTML file
2. Instruct the agent to READ the parent file FIRST
3. Instruct the agent to MODIFY the parent, not generate from scratch
4. Specify ONLY the targeted changes (e.g., "change background from gradient to patterned")
5. Verify output file size is within 20% of parent (drift guard)

Template:
```
Read the parent proposal at: [path to parent index.html]
This file is the STARTING POINT. You MUST modify this file, NOT generate from scratch.
The user selected this proposal as a winner because [reasons].
Your job: make ONLY these targeted changes: [specific axis changes].
Preserve everything else — layout, typography, component structure, color relationships.
```

### 6. Generate Proposals — MULTI-PROVIDER DELEGATION

Distribute proposals across **varied AI providers** for aesthetic diversity.
Each provider brings different creative biases — mixing them prevents convergence.

**Provider roster (use 2+ per generation):**

| Provider | Via | Strengths |
|----------|-----|-----------|
| Claude | Task tool (general-purpose agent) | Nuanced design thinking |
| Codex | `codex exec --full-auto` CLI | Systematic, architecture-first |
| Gemini | `gemini "..."` CLI | Creative divergence, experimental UI, brainstorming |

**Provider diversity (user preference):**
Aim for genuine diversity — don't lock any provider to a fixed percentage. Track which providers produce
liked proposals and bias toward them in subsequent generations. Codex is weakest for frontend design work.
Don't use the same provider for both survivors.

**Performance tracking (update after each generation's feedback):**
- Gemini: 2/4 liked in gen 2 (2E winner, 2F decent; 2C broken, 2D disliked)
- Kimi: mixed (2A decent/2B AI slop in gen 2; 1A ok/1B wrong direction in gen 1)
- Claude: mixed (2G promising/2H disliked in gen 2)
- Codex: 0/2 liked in gen 1 (both killed)

**Example distribution for 8 proposals:** Gemini(3-4), Kimi(2), Claude(2-3). Adjust per generation.
Vary per generation. Don't use same provider for both survivors.

Each proposal MUST include:
- Color palette (hex + OKLCH, semantic names)
- Typography scale (families, sizes, weights, line heights)
- Spacing system (base unit, scale)
- Component examples (button, card, input, nav item)
- Animation specifications (if motion axis != "none")
- Externalized logo/mark slot (`gen-N/assets/logos/*`) instead of only inline placeholder
- **Light AND dark theme support** (default to system `prefers-color-scheme`)
- Full rendered HTML preview

**Quality gate:** Each proposal should target 90+/100 from the `/ui-skills` expert
panel (Ogilvy, Rams, Scher, Wiebe, Laja, Walter, Cialdini, Ive, Wroblewski, Millman).
Apply `/frontend-design` aesthetic guidelines: bold direction, no generic AI slop,
distinctive font choices, intentional composition.

**taste-frontend injection (MANDATORY):** Every proposal prompt MUST include:

```
Load ~/.claude/skills/aesthetic-system/references/taste-frontend.md and follow strictly.
Active dials: DESIGN_VARIANCE={DESIGN_VARIANCE}, MOTION_INTENSITY={MOTION_INTENSITY}, VISUAL_DENSITY={VISUAL_DENSITY}.
Apply pre-flight checklist (Section 10 of taste-frontend.md) before finalizing.
```

Resolved dial values override DNA axes for Layout, Motion, and Density.

**Layout rule:** Items in the same state (pending, alive, winner, killed) MUST
occupy equal space. No arbitrary bento sizing for same-status proposals.

```
// Claude batch (via Task tool — parallel in single message)
Task({ subagent_type: "general-purpose", prompt: claudePrompt(dna_a) })
Task({ subagent_type: "general-purpose", prompt: claudePrompt(dna_b) })
Task({ subagent_type: "general-purpose", prompt: claudePrompt(dna_c) })
Task({ subagent_type: "general-purpose", prompt: claudePrompt(dna_d) })

// Codex batch (via CLI — run sequentially or background)
codex exec --full-auto "${codexPrompt(dna_e)}" --output-last-message /tmp/evolve-e.md
codex exec --full-auto "${codexPrompt(dna_f)}" --output-last-message /tmp/evolve-f.md

// Gemini batch (via CLI)
gemini "${geminiPrompt(dna_g)}" > /tmp/evolve-g.md
gemini "${geminiPrompt(dna_h)}" > /tmp/evolve-h.md
```
```

### 6b. Asset Batch (Mandatory)

After DNA proposal generation, run `/asset-generation` and mount assets into each proposal.

Rules:
1. Use **Recraft + OpenAI + Nano Banana Pro** in exploratory rounds.
2. Generate assets **per proposal** (`7a`, `7b`, ...) using that proposal's palette and style.
3. Match exploration width to design uncertainty:
   - Early rounds: broad style/color/logo families
   - Late rounds: narrow around surviving direction
4. Never ship noisy illustration-style logos as the primary mark.
5. Logo marks must be favicon/app-icon safe (legible at 16/24px, flat, low detail).
6. If generated logos fail QA, synthesize deterministic geometric SVG fallback marks.
7. Ensure proposal variants are meaningfully distinct; near-clone rounds are invalid.
8. User-provided logo references are **principle references only**:
   - extract qualities (simplicity, geometry, proportion, negative space)
   - never replicate exact silhouettes/compositions
   - reject outputs resembling known or provided logos

Required structure:
- `.design-evolution/gen-N/assets/logos/7a/{recraft,openai,gemini}-*.{svg,png}`
- `.design-evolution/gen-N/assets/logos/7a/final.{svg,png}`
- `.design-evolution/gen-N/assets/textures/7a/*.png` (optional)

In each proposal HTML:
- reference external assets via relative paths
- do not hardcode a one-size-fits-all logo across all variants
- keep background motifs subtle; no text artifacts/gibberish textures
- enforce CTA button label optical centering and stable line-height

### 7. Register, Catalog, Serve

```bash
python3 "$ENGINE" --repo "$REPO" add "dna1" "dna2" ... --origins "random,random,..."
python3 "$ENGINE" --repo "$REPO" catalog
python3 "$ENGINE" --repo "$REPO" serve &
```

**Catalog quality is part of the feature.** The catalog should not be a bare file list.
It must help the user build design taste and vocabulary.

Each proposal card should include:
- DNA code + axis pills
- **Design vocabulary readout** per axis (term + concise meaning)
- **Critique prompts** ("what to inspect") for structure, typography, motion, spacing
- Proposal notes + origin provenance

If catalog clarity is weak, improve engine rendering before generating more proposals.

**NEVER hardcode port 8888.** Engine hashes project name → port 8800-9799.

**MANDATORY VERIFICATION:** After catalog generation, verify EVERY proposal link works:
```bash
for id in a b c d e f g h; do
  ls "$REPO/.design-evolution/gen-${GEN}/${GEN}${id}/index.html" || echo "MISSING: ${GEN}${id}"
done
grep -c "Open Preview" "$REPO/.design-evolution/catalog.html"
```

### 8. Selection

User provides feedback → translate to engine commands:

```bash
python3 "$ENGINE" --repo "$REPO" select --winners "1a,1e" --kill "1b,1c,1f"
python3 "$ENGINE" --repo "$REPO" note --proposal 1a --text "love the asymmetry"
python3 "$ENGINE" --repo "$REPO" note --text "want more editorial feel overall"
```

Selection writes to both local taste AND global memory. Winners accumulate
positive scores globally; killed proposals accumulate negative. This learning
carries over to the next project.

### 9. Evolution

```bash
python3 "$ENGINE" --repo "$REPO" advance
```

Then generate new proposals (same delegation as step 6) and repeat.

For the winner/loser loop, prefer hardened breed mode:

```bash
python3 "$ENGINE" --repo "$REPO" breed
```

`breed` guarantees:
- winners persist as survivors
- mutations are parented from winners
- at least two immigrants (new species) are injected
- parent lineage is recorded in evolution state
- next generation previews are materialized immediately

### 10. Lock-in

```bash
python3 "$ENGINE" --repo "$REPO" lock 3b
python3 "$ENGINE" --repo "$REPO" export
```

Locked DNA is auto-banked in global memory for future seeding.

**Handoff routing:**
- Full system → `/design-theme` with locked DNA
- Component → `/ui-skills` or direct implementation
- Brand update → `/brand-compile` if tokens changed

### 10b. Enhanced Handoff — Component Seeding (Full System Only)

When scope=full and user confirms lock-in, the handoff generates a complete design system:

**1. Design tokens** → `/design-theme` generates `globals.css` with `@theme` block.

**2. Component seeds** → Generate initial `components/ui/` using the locked token system.
Minimum set (delegate to Codex or Kimi with taste-frontend.md loaded):
- Button (variants: default, ghost, destructive, outline)
- Card, CardHeader, CardContent, CardFooter
- Input, Textarea, Select
- Badge, Avatar
- Separator
- Typography (H1-H4, P, Muted)

Components must:
- Import only `~/lib/cn` and consume tokens via Tailwind classes
- No inline `style={{}}` props
- No hardcoded hex/px values outside token names

**3. Guardrail rules** → Invoke `/guardrail` to generate `guardrails/no-adhoc-styling.js`
(blocks arbitrary Tailwind values + inline styles). Enforced via lefthook pre-commit.

**4. Design system doc** → Write `design-system.md` at repo root documenting:
- Active DNA code and axis values
- Active dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY)
- Token list with semantic names
- Component inventory
- What's enforced by linting

## Memory

Global design memory persists across sessions at `~/.claude/design-memory.db`.

### Taste

Accumulated preference scores for each axis value. Updated on every
selection. Global taste merges with contextual taste (scoped to tags
like "saas", "landing") and hard preferences.

```bash
python3 "$ENGINE" memory taste                    # Show merged taste
python3 "$ENGINE" memory taste --context saas     # Context-filtered
```

### Hard Preferences

Vetoes exclude values from population generation. Mandates force inclusion.

```bash
python3 "$ENGINE" memory veto typography minimal --reason "boring"
python3 "$ENGINE" memory mandate color dark --reason "brand identity"
python3 "$ENGINE" memory rules                    # List all
python3 "$ENGINE" memory rules --remove 1         # Remove by ID
```

### DNA Bank

Save interesting designs across projects for reuse. Winners are auto-banked
after 2+ selections. Locked proposals always banked.

```bash
python3 "$ENGINE" --repo "$REPO" bank 2c --note "great editorial feel" --tags "saas,dark"
python3 "$ENGINE" memory bank                     # Browse bank
python3 "$ENGINE" memory bank --search editorial  # Search
```

### History + Import

```bash
python3 "$ENGINE" memory history                  # All feedback
python3 "$ENGINE" memory history --project scry   # Per-project
python3 "$ENGINE" memory import PATH --project scry --context saas  # Import YAML
```

## Brand Detection

Auto-detects existing design infrastructure via `detect.py`:

| Artifact | How Detected |
|---|---|
| brand.yaml | File at root |
| Tailwind CSS | Config files or `@import "tailwindcss"` in CSS |
| Design tokens | `@theme` blocks or `tokens.css` |
| Fonts | Google Fonts imports, Next.js font modules |
| Component lib | package.json deps (shadcn, Radix, MUI, etc.) |
| Dark mode | CSS `prefers-color-scheme` or Tailwind `darkMode` |
| Framework | package.json deps (Next.js, Remix, Astro, etc.) |

```bash
python3 "$ENGINE" --repo "$REPO" detect           # Summary
python3 "$ENGINE" --repo "$REPO" detect --json    # Machine-readable
```

## Image Generation (Recraft AI)

Generate vector logos, icons, and illustrations via Recraft API.
Requires `RECRAFT_AI_API_KEY` (preferred) or `RECRAFT_API_TOKEN`.

```bash
python3 "$ENGINE" recraft logo "minimalist owl logo" --colors "#1a1a2e,#e94560" --n 4
python3 "$ENGINE" recraft icon "search magnifying glass" --colors "#1a1a2e" --n 4
python3 "$ENGINE" recraft illustrate "abstract data visualization" --n 4
python3 "$ENGINE" recraft vectorize IMAGE_URL
python3 "$ENGINE" recraft test    # API connectivity check
```

Brand colors from brand.yaml can be auto-injected into the `--colors` flag.
Vector output (SVG) for `logo` and `icon` styles. Raster (PNG) for illustrations.

For multi-provider workflows (Recraft + Nano Banana Pro + OpenAI), use `/asset-generation`.

## Subsequent Invocations

If `.design-evolution/evolution.yaml` exists:

```bash
python3 "$ENGINE" --repo "$REPO" status
```

Based on state:
- **Has alive proposals** → prompt for selection
- **Has winners, no next gen** → run advance + generate
- **Locked** → offer handoff to implementation skill

## Integration

| Consumes | Produces |
|----------|----------|
| `brand.yaml` (if brand-adherent) | `.design-evolution/evolution.yaml` |
| `~/.claude/design-memory.db` | `.design-evolution/export.json` |
| `aesthetic-system` DNA codes | HTML proposal previews |
| `ui-skills` constraints | SVG/PNG logos and icons (via Recraft) |
| `asset-generation` prompts + QA gates | Proposal-mounted logos/illustrations/textures |

**Hands off to:**
- `/design-theme` — implement locked DNA as tokens
- `/brand-compile` — update brand tokens from locked DNA
- `/brand-assets` — generate branded visual assets
- `/pencil-to-code` — if Pencil backend used
- `/theme-factory` — apply 10 pre-built visual themes (color palettes, font pairings) to artifact outputs (slides, reports, HTML)
- `/design-md` — generate `DESIGN.md` as source-of-truth for Stitch MCP design system generation

## Anti-Convergence

Enforced by `min_diversity` (default 3 = proposals differ on 3+ axes),
immigration (fresh random genes), and DNA bank seeding (proven winners
from other projects injected into population).

## Maintenance & Scalability

Evolve is designed to scale across hundreds of repos and generations.

### Automatic bounds

- **Taste scores** clamped to ±20 on every update (prevents runaway accumulation)
- **Evolution YAML** archived beyond 10 generations (older gens → `generations-archive.jsonl`)
- **Connection caching** — single SQLite connection per process (no open/close per call)

### `evolve gc [--keep-gens N]`

Manual garbage collection. Safe to run anytime, idempotent.

What it does:
1. **Clamp taste** — caps all scores to ±20
2. **Prune DNA bank** — keeps 200 most recent entries (locked designs protected)
3. **Prune feedback** — keeps 500 per project (oldest deleted)
4. **WAL checkpoint** — reclaims SQLite journal space
5. **HTML cleanup** — removes old `gen-N/` preview directories, keeping last N (default: 3)

### `evolve memory` maintenance subcommands

```
evolve memory stats           # DB overview
evolve memory taste           # Current taste profile
evolve memory bank            # Browse DNA bank
evolve memory veto AXIS VAL   # Hard veto (never use this value)
evolve memory mandate AXIS VAL # Hard mandate (always use this value)
evolve memory rules           # List/remove hard preferences
evolve memory history         # Feedback log
evolve memory import --path P # Import from evolution.yaml
```
