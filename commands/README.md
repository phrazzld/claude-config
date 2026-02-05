# Claude Skills

Unix philosophy: small composable primitives + thin orchestration.

All workflows live in `~/.claude/skills/`. Each skill is a directory with `SKILL.md` + optional `references/` and `scripts/`.

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
/review-branch   # ~12 reviewers: personas + specialists + hindsight
/review-and-fix  # Full flow: review → fix → quality → pr
/address-review  # TDD fix workflow for review findings
/critique grug   # Adversarial review from persona
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOWS (Thin Orchestrators)                              │
│ /autopilot, /incident-response, /design-sprint,             │
│ /review-and-fix                                             │
├─────────────────────────────────────────────────────────────┤
│ DOMAIN SKILLS (Single-Purpose)                              │
│ /spec, /architect, /build, /groom, /investigate, /commit    │
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVES (Deep Modules)                                   │
│ /pr, /thinktank, /critique, /implement, /fix, /check-quality│
│ /review-branch, /address-review, /respond                   │
└─────────────────────────────────────────────────────────────┘
```

### Code Review System

```
┌─────────────────────────────────────────────────────────────┐
│ /review-and-fix (Thin Orchestrator)                         │
│   Chains: review-branch → address-review → check-quality → pr│
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVES                                                  │
├──────────────────┬──────────────────┬───────────────────────┤
│ /review-branch   │ /address-review  │ /respond              │
│ ~12 reviewers    │ TDD fix workflow │ Human PR feedback     │
│ parallel exec    │ GitHub issues    │ Radical transparency  │
└──────────────────┴──────────────────┴───────────────────────┘
```

**Reviewers (~12):**
- **Personas:** Grug, Carmack, Ousterhout, Beck, Fowler (via Moonbridge)
- **Specialists:** security-sentinel, performance-pathfinder, data-integrity-guardian, architecture-guardian (via Task)
- **Meta:** hindsight-reviewer, Synthesizer (orchestrator)

---

## Workflows

### /autopilot [issue-id]
Full delivery: `/spec → /architect → /build → /refactor → /update-docs → /pr`

### /incident-response <bug-report>
Fix + prevent: `/investigate → /fix → /postmortem → prevent → /codify-learning`

### /design-sprint [route-or-url]
Visual exploration: `/design-audit → /design-catalog → select → /design-theme → /build`

---

## Domain Skills

### Development Flow

| Skill | Purpose | Branching |
|-------|---------|-----------|
| `/spec <issue>` | Add product requirements | No changes |
| `/architect <issue>` | Add technical design | No changes |
| `/build <issue>` | Implement the feature | Creates branch |
| `/refactor` | Improve code architecture | Current branch |
| `/update-docs` | Audit + update documentation | Current branch |
| `/commit` | Tidy + semantic commits + push | Current branch |

### Quality & Review

| Skill | Purpose |
|-------|---------|
| `/review-branch` | ~12 reviewers: personas + specialists + hindsight |
| `/review-and-fix` | Full flow: review → fix → quality → pr |
| `/address-review` | TDD fix workflow for review findings |
| `/fix-ci` | Analyze CI failure → fix → verify |
| `/check-quality` | Bundled tests + lint + typecheck |

### Incident Response

| Skill | Purpose |
|-------|---------|
| `/investigate <bug>` | Debug production issues, create INCIDENT.md |
| `/postmortem` | Create blameless postmortem |

---

## Primitives

| Skill | What It Does |
|-------|--------------|
| `/pr` | Commit staged → push → create draft PR |
| `/thinktank <query>` | Multi-model review + synthesis |
| `/critique <persona>` | Adversarial expert review |
| `/implement <task>` | Code generation via Codex |
| `/fix <error>` | Diagnose and fix via Codex |
| `/codify-learning` | Extract patterns → skills/agents/tests |

---

## Infrastructure Skills

Full-cycle workflows: Audit → Plan → Execute → Verify.

| Skill | What It Does |
|-------|--------------|
| `/stripe` | Payment integration lifecycle |
| `/observability` | Error tracking, alerts, health checks |
| `/quality-gates` | Lefthook, Vitest, CI/CD |
| `/documentation` | README, architecture, .env.example |
| `/llm-infrastructure` | Model currency, evals, tracing |
| `/changelog` | semantic-release, commitlint, public page |
| `/virality` | OG images, social sharing, referrals |

---

## Branching Convention

1. **Start on master/main** — Clean working directory
2. **Branch for work** — `/build` and `/incident-response` create branches
3. **PR to merge** — `/pr` opens draft PR

Branch naming: `feature/issue-{id}`, `fix/issue-{id}`, `fix/incident-{timestamp}`, `hotfix/{description}`

---

## Principles

1. **Deep modules only** — Primitives hide significant complexity
2. **Natural language for shallow ops** — Don't create skills for simple git operations
3. **Codex delegation** — `/implement` and `/fix` delegate to Codex CLI
4. **GitHub as source of truth** — Issues hold specs and designs
5. **Branch from master** — Workflows assume clean master start
6. **Role + Objective + Latitude** — Skills state goals, not steps (see `/llm-communication`)
