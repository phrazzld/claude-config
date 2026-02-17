---
name: evolve
description: |
  Genetic algorithm for design systems. Generates populations of design
  proposals, collects feedback, evolves winners through mutation/crossover,
  kills losers, repeats until lock-in.

  Invoke when:
  - User wants to explore design directions iteratively
  - "evolve", "design evolution", "genetic design", "iterate on designs"
  - Before /design-theme when direction is unclear and user wants options

  Matrix: scope (full system | specific component) × brand (adherent | free)
effort: high
argument-hint: "[project-name] [--scope full|component] [--brand brand.yaml]"
---

# Design Evolution

Genetic algorithm over the DNA code system. Simple loop:
generate population → user selects winners/losers → mutate winners,
kill losers, add immigrants → repeat until lock-in.

## Engine

All state management via `engine.py` in this skill's directory:

```bash
ENGINE="$HOME/.claude/skills/evolve/engine.py"
python3 "$ENGINE" --repo "$REPO" <command> [args]
```

The engine is the source of truth. Claude orchestrates, the engine tracks state.

## Workflow

### First Invocation (No State)

**1. Determine matrix position:**

```
AskUserQuestion:
"What's the scope?"
- "Full design system" → scope=full
- "Specific component" → scope=component (ask which)

"Brand adherence?"
- "Evolve freely" → brand=free, no locked axes
- "Stay on brand" → brand=adherent, lock color+typography axes
```

**2. Analyze codebase:**

- Detect framework (Next.js, Remix, vanilla, etc.)
- Find existing design tokens, brand.yaml, tailwind config
- Screenshot current state if URL available
- Infer current DNA

**3. Initialize:**

```bash
python3 "$ENGINE" --repo "$REPO" init \
  --project "$PROJECT" \
  --scope "$SCOPE" \
  --brand "$BRAND_FILE" \  # omit if free
  --lock "$LOCKED_AXES" \  # e.g. "color,typography" if brand-adherent
  --population 8
```

**4. Generate initial population:**

```bash
python3 "$ENGINE" --repo "$REPO" suggest --count 8
```

This outputs 8 DNA codes biased by taste (empty on first run = pure random).

**5. Generate proposals — DELEGATE to parallel agents:**

For EACH DNA code from suggest, spawn a parallel agent (Kimi preferred, Moonbridge/Codex fallback):

Each proposal MUST include:
- Color palette (hex + OKLCH values, semantic names)
- Typography scale (font families, sizes, weights, line heights)
- Spacing system (base unit, scale)
- Component examples (button, card, input, nav item)
- Animation specifications (if motion axis != "none")
- Full rendered HTML preview

```javascript
// Preferred: Kimi parallel swarm
mcp__kimi__spawn_agents_parallel({
  agents: dna_codes.map((code, i) => ({
    prompt: `Design system proposal. DNA: ${code}
Project: ${project_context}
Framework: ${framework}
Scope: ${scope}

Generate a COMPLETE design system preview as a single HTML file.
Include: color palette swatches, typography specimens, spacing scale,
button/card/input/nav components, animation demos (if DNA motion != "none").

Use real fonts from Google Fonts. Use OKLCH for colors.
Make it visually stunning — this competes against 7 other proposals.

BANNED: Inter, Roboto, Space Grotesk, Satoshi, purple gradients,
Tailwind default blue-500, centered-max-w-4xl-everything.

Output to: .design-evolution/gen-${genNum}/${genNum}${letter}/index.html`,
    thinking: true
  }))
})
```

If Kimi unavailable, use Moonbridge/Codex or generate directly.

**6. Register proposals:**

After all agents complete, register with engine:

```bash
python3 "$ENGINE" --repo "$REPO" add \
  "editorial.high-contrast.display-heavy.orchestrated.spacious.textured" \
  "bento.dark.expressive.subtle.compact.layered" \
  ... \
  --origins "random,random,random,..."
```

**7. Generate catalog, VERIFY links work, and serve:**

```bash
python3 "$ENGINE" --repo "$REPO" catalog
# Use project-specific port (deterministic hash, no cross-session collisions)
python3 "$ENGINE" --repo "$REPO" serve &
# Or get port only: python3 "$ENGINE" --repo "$REPO" port
```

**NEVER hardcode port 8888.** The engine hashes project name → port 8800-9799.
Different projects get different ports. No cross-session collisions.

**MANDATORY VERIFICATION — DO NOT SKIP:**
After generating the catalog, verify EVERY proposal is accessible:
1. Check that catalog.html contains an `<a href=...>` link for each proposal ID
2. Check that each linked HTML file exists on disk
3. If ANY proposal is missing a link or its HTML file is missing, FIX IT before presenting to the user

```bash
# Verify all proposal HTML files exist
for id in a b c d e f g h; do
  ls "$REPO/.design-evolution/gen-${GEN}/${GEN}${id}/index.html" || echo "MISSING: ${GEN}${id}"
done
# Verify catalog has links
grep -c "Open Preview" "$REPO/.design-evolution/catalog.html"
# Must equal population count. If not, regenerate catalog.
```

The user MUST be able to click through from the catalog to every individual proposal.
A catalog without working links to previews is useless. This has broken twice — never again.

**8. Present:**

```
Design Evolution — Generation 1

8 proposals generated. Browse: http://localhost:8888

Quick overview:
  1a: editorial.high-contrast.display-heavy.orchestrated.spacious.textured
  1b: bento.dark.expressive.subtle.compact.layered
  ...

Open each preview to see the full design system.
Tell me your winners and losers. You can also give notes on specific proposals.
```

### Selection Phase

User provides feedback. Translate to engine commands:

```bash
# Mark winners and losers
python3 "$ENGINE" --repo "$REPO" select --winners "1a,1e" --kill "1b,1c,1f"

# Specific proposal notes
python3 "$ENGINE" --repo "$REPO" note --proposal 1a --text "love the asymmetry, motion too aggressive"
python3 "$ENGINE" --repo "$REPO" note --proposal 1e --text "typography perfect, needs warmer colors"

# General direction notes
python3 "$ENGINE" --repo "$REPO" note --text "want more editorial feel overall"
```

### Evolution Phase

**1. Compute next generation:**

```bash
python3 "$ENGINE" --repo "$REPO" advance
```

Reads `next_gen_plan.json` — contains DNA codes with origins (survivor, mutation, crossover, immigration).

**2. Generate new proposals** — same delegation pattern as step 5.

Key differences from gen 1:
- **Survivors**: Re-render the winner DNA (or keep existing artifacts if unchanged)
- **Mutations**: Winner DNA with 1-2 axes perturbed. INCORPORATE NOTES. If user said "motion too aggressive" on 1a, bias the motion mutation away from "aggressive"
- **Crossover**: Combined axes from two winners
- **Immigration**: Completely new random DNA (prevents local optima)

**3. Register, catalog, present** — same as steps 6-8.

**4. Repeat** until user says "lock it in" or "that's the one."

### Lock-in

```bash
python3 "$ENGINE" --repo "$REPO" lock 3b
python3 "$ENGINE" --repo "$REPO" export
```

Export contains: locked DNA, full lineage, taste profile, generation count.

**Handoff routing:**
- Full system → `/design-theme` with the locked DNA
- Component → `/ui-skills` or direct implementation
- Brand update → `/brand-compile` if tokens changed

## Note Integration

User notes are critical for directed evolution. When processing notes:

1. **Specific proposal notes** → inform mutations of that proposal's descendants
2. **General notes** → bias ALL mutations in the stated direction
3. **Axis-specific feedback** → if user says "warmer colors" and winner has `color: high-contrast`, mutate toward `brand-tinted` or `gradient`

The engine handles taste accumulation automatically (winners +1, killed -1 per axis value).
Claude's job is translating natural language notes into informed mutation prompts.

## State Format

All state in `.design-evolution/evolution.yaml`. Structure:

```yaml
project: "my-app"
repo_path: "/path/to/repo"
config:
  scope: full
  brand_adherent: false
  locked_axes: []
  population_size: 8
  mutation_rate: 2
  immigration_rate: 2
  min_diversity: 3
generations:
  - number: 1
    proposals:
      - id: "1a"
        dna: {layout: editorial, color: high-contrast, ...}
        status: winner
        origin: random
        notes: ["love the asymmetry"]
        artifacts: {html: "gen-1/1a/index.html"}
    general_notes: ["want more editorial feel"]
    timestamp: "2026-02-15T..."
taste:
  layout: {editorial: 2, centered: -1}
  color: {high-contrast: 1, gradient: -2}
locked: null
```

Phase 2 web app reads/writes this same format.

## Subsequent Invocations (State Exists)

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
| `aesthetic-system` DNA codes | `.design-evolution/export.json` |
| `ui-skills` constraints | HTML proposal previews |

**Hands off to:**
- `/design-theme` — implement locked DNA as tokens
- `/brand-compile` — update brand tokens from locked DNA
- `/pencil-to-code` — if Pencil backend used

## Anti-Convergence

Enforced by engine's `min_diversity` parameter (default 3 = proposals must differ on 3+ axes).
Additionally, immigration guarantees fresh genes every generation.

Reference: `aesthetic-system/references/banned-patterns.md` — all proposals must pass.
