# Claude Skills

Unix philosophy: small composable primitives + thin orchestration.

## Core Delivery Pipeline

The primary workflow. Four skills that cover the full lifecycle from backlog to merged PR.

```
/groom  →  /autopilot  →  /pr-fix  →  /pr-polish  →  merge
 plan       build        unblock      elevate
```

### `/groom` — Plan the work

Comprehensive backlog grooming. Loads vision, captures user observations, audits existing issues, runs domain auditors in parallel, enriches with external AI (Gemini, Codex, Thinktank), deduplicates, and produces a prioritized backlog.

**Composes:** 11 `log-*-issues` skills, security-sentinel, architecture-guardian, aesthetician, pioneer, visionary agents.

**Output:** Prioritized GitHub issues (P0-P3) with labels, milestones, and org project links.

### `/autopilot` — Build the work

From issue to PR in one command. Picks highest-priority issue, specs it (`/spec`), designs it (`/architect`), builds it (`/build`), refines it (`/refactor`, `/update-docs`), and ships it (`/pr`).

**Composes:** `/spec` → `/architect` → `/build` → `/refactor` → `/update-docs` → `/pr`

**Output:** Draft PR with tests passing, linked to issue.

### `/pr-fix` — Unblock the PR

One command takes a blocked PR to green. Resolves merge conflicts (semantic, not mechanical), fixes CI failures, addresses review feedback with full transparency.

**Composes:** `git-mastery` conflict resolution → `/fix-ci` → `/respond` → `/address-review`

**Output:** No conflicts, CI green, reviews addressed/deferred/declined.

### `/pr-polish` — Elevate the PR

Holistic quality pass for a PR that already works. Starts with hindsight analysis ("would we build it the same way?"), then refactors, audits tests, updates docs, and runs quality gates.

**Composes:** `hindsight-reviewer` agent → `/refactor` → test audit → `/update-docs` → `/check-quality` → `/distill`

**Output:** Cleaner architecture, better tests, current docs, codified learnings.

### Pipeline Usage

Run individually or chain:

```
/groom                    # Populate backlog
/autopilot 42             # Build issue #42
/pr-fix                   # Unblock if stuck
/pr-polish                # Elevate before merge
```

`/pr-polish` has a precondition gate — if the PR has conflicts, red CI, or unaddressed reviews, it redirects to `/pr-fix`.

## Supporting Delivery Skills

Skills invoked by the pipeline or used standalone.

### Planning & Design

| Skill | Purpose | Invoked By |
|-------|---------|------------|
| `/spec` | Product requirements from issue | `/autopilot` |
| `/architect` | Technical design from spec | `/autopilot` |
| `/build` | Implementation with Codex | `/autopilot` |
| `/critique` | Adversarial review | standalone |

### Code Quality

| Skill | Purpose | Invoked By |
|-------|---------|------------|
| `/review-branch` | ~12 parallel AI reviewers | `/review-and-fix` |
| `/review-and-fix` | Review → fix → quality → PR | standalone |
| `/refactor` | Two-pass code improvement | `/autopilot`, `/pr-polish` |
| `/check-quality` | Quality gate verification | `/pr-polish` |

### PR Lifecycle

| Skill | Purpose | Invoked By |
|-------|---------|------------|
| `/pr` | Create draft PR from branch | `/autopilot` |
| `/respond` | Categorize review feedback | `/pr-fix` |
| `/address-review` | TDD fixes for review findings | `/pr-fix` |
| `/fix-ci` | Classify + fix CI failures | `/pr-fix` |
| `/commit` | Semantic commits + push | standalone |

### Documentation

| Skill | Purpose | Invoked By |
|-------|---------|------------|
| `/update-docs` | ADRs, diagrams, READMEs | `/autopilot`, `/pr-polish` |
| `/distill` | Codify learnings to skills/hooks | `/pr-polish` |

### Incident Response

| Skill | Purpose |
|-------|---------|
| `/investigate` | Debug production issues |
| `/triage` | Multi-source observability check |
| `/postmortem` | Blameless analysis |
| `/incident-response` | Full incident lifecycle |
| `/verify-fix` | Confirm fix with observables |

## Domain Orchestrators

Each composes domain-specific primitives.

| Skill | Domain | Primitives |
|-------|--------|------------|
| `/stripe` | Payments | audit, health, configure, verify, reconcile, scaffold |
| `/changelog` | Releases | audit, setup, page, automation |
| `/observability` | Monitoring | sentry, verify-fix, triage |
| `/documentation` | Docs | standards, update-docs |
| `/virality` | Growth | sharing, referrals, OG images |
| `/cro` | Conversion | form, page, signup, onboarding, paywall |
| `/social-content` | Marketing | post, announce, copywriting |
| `/llm-infrastructure` | LLM ops | evaluation, gateway-routing |
| `/quality-gates` | CI/CD | testing-philosophy, code-quality |
| `/brand-pipeline` | Brand | brand-init → brand-compile → brand-assets |

## Check / Log / Fix Pattern

Three-tier pattern for each domain. Check audits, Log creates issues, Fix resolves them.

| Domain | Check | Log | Fix |
|--------|-------|-----|-----|
| Production | `/check-production` | `/log-production-issues` | `/triage` |
| Quality | `/check-quality` | `/log-quality-issues` | `/fix-quality` |
| Docs | `/check-docs` | `/log-doc-issues` | `/fix-docs` |
| Observability | `/check-observability` | `/log-observability-issues` | `/fix-observability` |
| Stripe | `/check-stripe` | `/log-stripe-issues` | `/fix-stripe` |
| Bitcoin | `/check-bitcoin` | `/log-bitcoin-issues` | `/fix-bitcoin` |
| Lightning | `/check-lightning` | `/log-lightning-issues` | `/fix-lightning` |
| Virality | `/check-virality` | `/log-virality-issues` | `/fix-virality` |
| Landing | `/check-landing` | `/log-landing-issues` | `/fix-landing` |
| Onboarding | `/check-onboarding` | `/log-onboarding-issues` | `/fix-onboarding` |

`/groom` runs all `log-*` skills. Individual `check-*` and `fix-*` for targeted work.

## References

Auto-loaded for context. Not in `/` menu. Set `user-invocable: false`.

| Skill | Purpose |
|-------|---------|
| `git-mastery` | Git workflow, commit conventions, conflict resolution |
| `testing-philosophy` | Test behavior not implementation |
| `naming-conventions` | Intention-revealing names |
| `documentation-standards` | Comment why not what |
| `external-integration-patterns` | External service integration |
| `ui-skills` | Interface constraints |
| `business-model-preferences` | Pricing philosophy |
| `toolchain-preferences` | Stack defaults (pnpm, Next.js, etc.) |
| `design-tokens` | Tailwind @theme patterns |

## Language-Specific

Reference-style but remain invocable for explicit use.

| Skill | Language |
|-------|----------|
| `typescript-excellence` | TypeScript best practices |
| `python-standards` | Modern Python with uv, ruff |
| `go-idioms` | Idiomatic Go patterns |
| `rust-patterns` | Ownership, errors, traits |
| `ruby-conventions` | Rails services, testing |
| `csharp-modern` | .NET 8+ patterns |

## Skill Types

| Type | Frontmatter | Who Invokes | Examples |
|------|-------------|-------------|----------|
| **Reference** | `user-invocable: false` | Claude auto-loads | git-mastery, testing-philosophy |
| **Primitive** | (default) | Model + user | stripe-audit, spec, fix-ci |
| **Orchestrator** | (default) | Model + user | /stripe, /autopilot, /groom |
| **Top-level Workflow** | `disable-model-invocation: true` | User only | /audit |

## Adding Skills

1. **Create directory:** `skills/{name}/SKILL.md`
2. **Add frontmatter:** name, description, effort level
3. **Follow pattern:** Look at existing skills in same category
4. **Declare effort:** `max` / `high` / `medium` / `low`

## Principles

1. **Deep modules** — Hide significant complexity behind simple interfaces
2. **Compose, don't duplicate** — Orchestrators call primitives
3. **Model-invocable by default** — Only restrict when necessary
4. **References auto-load** — No need to invoke explicitly

---

## Next Steps

Areas to flesh out in future iterations:

- **Grooming & planning depth** — `/groom` and `/spec` are the top of the hourglass. Expand product thinking: user research patterns, competitive analysis, prioritization frameworks.
- **Product skills** — Vision management, roadmap generation, sprint planning beyond what `/groom` currently covers.
- **Spec → Architect handoff** — Tighten the contract between product spec and technical design.
