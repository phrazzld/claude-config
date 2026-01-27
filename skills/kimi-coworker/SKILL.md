# /kimi-coworker

Invoke Kimi K2.5 CLI as a coworker for implementation, brainstorming, and parallel task execution.

## When to Delegate to Kimi

**MANDATORY for:**
- **Design exploration** — Generating visual proposal catalogs
- **UI implementation** — React/Tailwind components, CSS
- **Design themes** — Token systems, globals.css
- **Frontend work** — Any visual coding tasks

**Prefer Kimi when:**
- Budget matters (Kimi is ~80% cheaper than Codex)
- Frontend/visual coding (Kimi K2.5's strength)
- Parallel subtasks (Agent Swarm handles 100+ agents)
- Multimodal input needed (screenshots, diagrams)
- Complex reasoning (use `--thinking` mode)

**Keep for Codex when:**
- Git-heavy workflows (Codex has better git integration)
- You already have deep Codex context loaded
- Backend/API work without visual components
- Mission-critical code needing GPT-5 capabilities

## Design Workflow Integration

Kimi is the designated agent for all design-related skills:

| Skill | Kimi's Role |
|-------|-------------|
| `/design-exploration` | Generate 6-12 visual proposals in parallel |
| `/design-catalog` | Build 5-8 design options |
| `/design-theme` | Implement token system in CSS |
| `/aesthetic-system` | Execute visual implementation |
| `/ui-skills` | Build UI components |

**Pattern:** Research (Gemini) → Build (Kimi) → Review (Claude)

## Invocation Patterns

### Single Agent
```
mcp__kimi__spawn_agent({
  "prompt": "Create a React hook for form validation. Follow pattern in src/hooks/useAuth.ts.",
  "thinking": false
})
```

### With Extended Reasoning
```
mcp__kimi__spawn_agent({
  "prompt": "Debug why the checkout flow fails intermittently. Trace through payment.ts and cart.ts.",
  "thinking": true
})
```

### Parallel Agents (Agent Swarm)
```
mcp__kimi__spawn_agents_parallel({
  "agents": [
    {"prompt": "Write unit tests for UserProfile component"},
    {"prompt": "Write unit tests for UserSettings component"},
    {"prompt": "Write integration tests for user flow", "thinking": true}
  ]
})
```

## Pre-Delegation Checklist

1. **Existing tests?** → Warn: "Don't break tests in [test file]"
2. **Add or replace?** → Be explicit: "ADD to this file" vs "REPLACE this file"
3. **Quality gates?** → Include: "Run pnpm typecheck && pnpm lint after"
4. **Patterns to follow?** → Include: "Follow pattern in [reference file]"

## Post-Delegation Validation

```bash
git diff --stat        # See what changed
pnpm typecheck         # Type check
pnpm lint             # Lint
pnpm test             # Run tests
```

## Kimi K2.5 Modes

| Mode | When to Use |
|------|-------------|
| Default | Standard tasks |
| `--thinking` | Complex debugging, architecture decisions |
| Agent Swarm | Parallel independent subtasks |

## Cost Comparison

| Provider | Input | Output |
|----------|-------|--------|
| Kimi K2.5 | $0.15/M | $2.50/M |
| Codex (GPT-5) | ~$2.50/M | ~$10/M |
| Claude Opus | $15/M | $75/M |

Kimi is **~80% cheaper** than Codex for equivalent tasks.

## Examples

### Design Catalog Generation (Parallel)
```
mcp__kimi__spawn_agents_parallel({
  "agents": [
    {"prompt": "Generate proposal: Midnight Editorial. DNA: editorial, dark, display-heavy, orchestrated, spacious, gradient. Build .design-catalog/proposals/01-midnight-editorial/ with preview.html, styles.css", "thinking": true},
    {"prompt": "Generate proposal: Swiss Brutalist. DNA: grid-breaking, monochrome, minimal, none, compact, solid. Build .design-catalog/proposals/02-swiss-brutalist/", "thinking": true},
    {"prompt": "Generate proposal: Warm Workshop. DNA: asymmetric, brand-tinted, text-forward, subtle, mixed, textured. Build .design-catalog/proposals/03-warm-workshop/", "thinking": true}
  ]
})
```

### UI Component Implementation
```
mcp__kimi__spawn_agent({
  "prompt": "Create a Modal component in src/components/Modal.tsx. Use Tailwind CSS. Follow the pattern in Button.tsx. Include: open/close state, backdrop click to close, escape key handler, focus trap. Apply ui-skills constraints. Run pnpm typecheck after."
})
```

### Theme Token Implementation
```
mcp__kimi__spawn_agent({
  "prompt": "Implement design theme in app/globals.css using Tailwind 4 @theme directive. Colors (OKLCH): primary oklch(0.7 0.15 250), background oklch(0.98 0 0). Typography: heading font JetBrains Mono, body Inter. Modular scale. Then update components to use tokens.",
  "thinking": true
})
```

### Bug Investigation
```
mcp__kimi__spawn_agent({
  "prompt": "Investigate why API calls in src/api/client.ts sometimes return stale data. Check caching logic, request deduplication, and race conditions. Report findings without making changes.",
  "thinking": true
})
```

### Parallel Test Writing
```
mcp__kimi__spawn_agents_parallel({
  "agents": [
    {"prompt": "Write tests for src/utils/format.ts covering all exported functions"},
    {"prompt": "Write tests for src/utils/validate.ts covering edge cases"},
    {"prompt": "Write tests for src/utils/transform.ts with snapshot tests"}
  ]
})
```
