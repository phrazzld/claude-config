# Claude Commands

Unix philosophy: small composable primitives + thin orchestration.

## Quick Reference

**Daily workflow:**
```
/groom           # Find work worth doing
/autopilot 123   # Ship issue end-to-end
/commit          # Clean commits + push
```

**Incident response:**
```
/investigate "error message"
/incident-response "production down"
```

**Code review:**
```
/review-branch   # Multi-model review of current branch
/critique grug   # Adversarial review from persona
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOWS (Thin Orchestrators)                              │
│ /autopilot, /incident-response, /design-sprint              │
├─────────────────────────────────────────────────────────────┤
│ DOMAIN COMMANDS (Single-Purpose)                            │
│ /spec, /architect, /build, /groom, /investigate, /commit    │
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVES (Deep Modules)                                   │
│ /pr, /thinktank, /critique, /implement, /fix, /check-quality│
└─────────────────────────────────────────────────────────────┘
```

---

## Workflows

Workflows orchestrate multiple commands. They assume you start on `master`/`main` and will checkout a feature branch when doing work.

### /autopilot [issue-id]
**Full delivery from issue to PR.**

```
/spec → /architect → /build → /refactor → /update-docs → /pr
```

| Step | What happens |
|------|--------------|
| 1. Find issue | Uses `$1` or finds highest-priority open issue |
| 2. Spec | Ensures `## Product Spec` exists |
| 3. Design | Ensures `## Technical Design` exists |
| 4. Build | Creates branch, delegates to Codex, commits |
| 5. Refine | Refactors and updates docs |
| 6. Ship | Opens draft PR |

### /incident-response <bug-report>
**Fix the fire, then prevent the next one.**

```
/investigate → /fix → /postmortem → prevent → /codify-learning
```

| Step | What happens |
|------|--------------|
| 1. Investigate | Create INCIDENT.md, find root cause |
| 2. Branch | Creates `fix/incident-{timestamp}` |
| 3. Fix | Delegate fix to Codex |
| 4. Verify | Demand observable proof (logs, metrics) |
| 5. Postmortem | Blameless analysis |
| 6. Prevent | Create prevention issue if systemic |

### /design-sprint [route-or-url]
**Explore before you implement.**

```
/design-audit → /design-catalog → select → /design-theme → /build
```

| Step | What happens |
|------|--------------|
| 1. Audit | Assess current design system |
| 2. Catalog | Generate 5-8 visual proposals |
| 3. Select | User picks direction |
| 4. Theme | Build design tokens |
| 5. Build | Implement selected design |

---

## Domain Commands

### Development Flow

| Command | Purpose | Branching |
|---------|---------|-----------|
| `/spec <issue>` | Add product requirements to issue | No changes |
| `/architect <issue>` | Add technical design to issue | No changes |
| `/build <issue>` | Implement the feature | Creates branch |
| `/refactor` | Improve code architecture | On current branch |
| `/update-docs` | Update documentation | On current branch |
| `/commit` | Tidy + semantic commits + push | On current branch |

### Quality & Review

| Command | Purpose |
|---------|---------|
| `/groom` | Run 12 grooming perspectives → create issues |
| `/review-branch` | Multi-model code review with thinktank |
| `/fix-ci` | Analyze CI failure → fix → verify |
| `/check-quality` | Bundled tests + lint + typecheck |

### Incident Response

| Command | Purpose |
|---------|---------|
| `/investigate <bug>` | Debug production issues, create INCIDENT.md |
| `/postmortem` | Create blameless postmortem |

### Design System

| Command | Purpose |
|---------|---------|
| `/design-catalog` | Generate 5-8 visual proposals |
| `/design-audit` | Assess current design system |
| `/design-theme` | Create/update theme with tokens |

---

## Primitives

Deep modules that hide significant complexity.

| Command | What It Does |
|---------|--------------|
| `/pr` | Commit staged changes → push → create draft PR |
| `/thinktank <query>` | Multi-model review + synthesis |
| `/critique <persona>` | Adversarial expert review (grug, carmack, etc.) |
| `/implement <task>` | Code generation via Codex delegation |
| `/fix <error>` | Diagnose and fix via Codex delegation |
| `/codify-learning` | Extract patterns → skills/agents/tests |

---

## Utilities

| Command | Purpose |
|---------|---------|
| `/respond` | Handle PR feedback systematically |
| `/distill` | Keep CLAUDE.md tight (~100 lines) |
| `/sync-configs` | Sync Claude config to Codex/Gemini |

---

## Infrastructure Skills

Full-cycle workflows for project infrastructure. Each follows Audit → Plan → Execute → Verify.

| Skill | What It Does |
|-------|--------------|
| `/audit` | Comprehensive project health check → GitHub issues |
| `/stripe` | Payment integration lifecycle |
| `/observability` | Error tracking, alerts, health checks |
| `/quality-gates` | Lefthook, Vitest, CI/CD |
| `/documentation` | README, architecture, .env.example |
| `/llm-infrastructure` | Model currency, evals, tracing |
| `/changelog` | semantic-release, commitlint, public page |
| `/virality` | OG images, social sharing, referrals |

Run `/audit` first to discover gaps, then run the specific skill to fix them.

---

## Branching Convention

All workflows assume:
1. **Start on master/main** — Clean working directory
2. **Branch for work** — `/build` and `/incident-response` create feature/fix branches
3. **PR to merge** — `/pr` opens draft PR back to main

Branch naming:
- Features: `feature/issue-{id}` or `feature/{description}`
- Fixes: `fix/issue-{id}` or `fix/incident-{timestamp}`
- Hotfixes: `hotfix/{description}`

---

## Source of Truth

**GitHub Issues** — All specs, designs, context live in issue title/description/comments.

No local TODO.md, DESIGN.md, TASK.md files needed.

---

## Principles

1. **Deep modules only** — Primitives hide significant complexity
2. **Natural language for shallow ops** — Don't create commands for simple git operations
3. **Codex delegation** — `/implement` and `/fix` delegate to Codex CLI
4. **GitHub as source of truth** — Issues hold specs and designs
5. **Branch from master** — Workflows assume clean master start

---

## Skills vs Commands

**As of January 2026, Claude Code has merged skills and commands.** Both create `/slash-commands`:
- `.claude/commands/review.md` → `/review`
- `.claude/skills/review/skill.md` → `/review`

**Skills are recommended** because they support:
- Directory for supporting files (templates, scripts, references)
- Frontmatter to control auto-invocation
- Claude can load them automatically when relevant

Existing commands keep working. New workflows should be created as skills.

**Consolidation plan:** Eventually migrate all commands to skills for consistency.
