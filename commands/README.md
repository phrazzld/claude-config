# Claude Commands

Unix philosophy redesign: small composable primitives + thin orchestration.

**Before:** 67 monolithic commands
**After:** 29 focused commands (7 primitives + 15 domain + 3 workflows + 4 utilities)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 3: WORKFLOWS (Thin Orchestrators)                 │
│ /autopilot, /incident-response, /design-sprint          │
├─────────────────────────────────────────────────────────┤
│ LAYER 2: DOMAIN COMMANDS (Single-Purpose)               │
│ /spec, /architect, /build, /groom, /investigate         │
├─────────────────────────────────────────────────────────┤
│ LAYER 1: PRIMITIVES (Deep Modules)                      │
│ /pr, /thinktank, /critique, /implement, /fix            │
└─────────────────────────────────────────────────────────┘
```

## Primitives (Deep Modules)

| Command | What It Does |
|---------|--------------|
| `/pr` | Full PR workflow: commits → understand issue → title/description → draft PR |
| `/thinktank <query>` | Multi-model review + synthesis |
| `/critique <persona>` | Adversarial expert review (grug, carmack, ousterhout, etc.) |
| `/implement <task>` | Code generation with Codex delegation |
| `/fix <error>` | Diagnose and fix with Codex delegation |
| `/check-quality` | Bundled tests + lint + typecheck |
| `/codify-learning` | Extract patterns → skills/agents/tests |

## Domain Commands

### Development Flow

| Command | Purpose |
|---------|---------|
| `/spec <issue>` | Flesh out product requirements in issue |
| `/architect <issue>` | Add technical design to issue |
| `/build <issue>` | Build the feature (Codex delegation) |
| `/refactor` | Improve code architecture |
| `/update-docs` | Update documentation |

### Design System

| Command | Purpose |
|---------|---------|
| `/design-catalog` | Generate 5-8 visual design proposals |
| `/design-audit` | Assess current design system |
| `/design-theme` | Create/update theme with tokens |

### Quality & Review

| Command | Purpose |
|---------|---------|
| `/groom` | Run all 12 grooming perspectives → create issues |
| `/review-branch` | Multi-model code review |
| `/fix-ci` | Analyze CI failure → fix → verify |

### Incident Response

| Command | Purpose |
|---------|---------|
| `/investigate <bug>` | Debug and fix production issues |
| `/postmortem` | Create blameless postmortem |

### Utilities

| Command | Purpose |
|---------|---------|
| `/respond` | Handle PR feedback |
| `/distill` | Keep CLAUDE.md tight (~100 lines) |

## Workflows (Thin Orchestrators)

| Workflow | Chain |
|----------|-------|
| `/autopilot [issue]` | spec → architect → build → refactor → docs → pr |
| `/incident-response` | investigate → fix → postmortem → prevent |
| `/design-sprint` | audit → catalog → pick → theme → build |

## Git Worktrees (Parallel Development)

| Command | Purpose |
|---------|---------|
| `/git-worktree-create` | Create isolated worktree |
| `/git-worktree-review` | Review PR in isolation |
| `/git-worktree-cleanup` | Remove stale worktrees |

## Source of Truth

**GitHub Issues** — All specs, designs, context live in issue title/description/comments. No local TODO.md, DESIGN.md, TASK.md files.

## Principles

1. **Deep modules only** — Primitives hide significant complexity
2. **Natural language for shallow ops** — Don't create commands for `git commit`
3. **Codex delegation** — `/implement` and `/fix` delegate to Codex CLI
4. **No flags** — Commands don't take flags; use arguments
5. **Full-stack grooming** — 12 perspectives from security to sales

## Obsolete Commands

Moved to `_obsolete/` directory. These were:
- Absorbed into new commands
- Too shallow (just wrappers)
- Redundant with natural language
