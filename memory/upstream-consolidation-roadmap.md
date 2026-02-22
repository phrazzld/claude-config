# Upstream Toolkit Consolidation Roadmap

## Current Upstream Routing

| I want to... | Skill | Notes |
|--------------|-------|-------|
| Groom entire backlog | `/groom` | Orchestrates check-* skills, parallel agents, org standards |
| Plan one idea formally | `/shaping` | Rs/Ss/fit checks → locked shape. Then `/breadboarding` |
| Map system affordances | `/breadboarding` | Places, UI/Code/Store affordances, wiring, vertical slices |
| Validate a breadboard | `/breadboard-reflection` | Design smell detection |
| Product spec only | `/spec` | WHAT/WHY. Primitive used by autopilot quick mode |
| Technical design only | `/architect` | HOW. Primitive used by autopilot quick mode |
| Stress-test a design | `/critique` | Adversarial expert review (7 personas) |
| Multi-model consensus | `/thinktank` | Hard decisions, security validation |
| Diagnose production bug | `/triage` | Full incident response (investigate + fix + postmortem) |
| Diagnose local failure | `/debug` | Test failures, build errors, local dev issues |
| Autonomous delivery | `/autopilot` | Issue → spec → architect → build → ship |

## Tier 1: Merge Opportunities (high overlap, clear winner)

| Current | Action | Rationale |
|---------|--------|-----------|
| `/shape` | **RETIRED** → `/shaping` | Singer's methodology is strictly better. Archived to `_archived/shape/` |
| `/investigate` | **FOLD INTO** `/triage` | `/triage` already includes investigate; standalone `/investigate` is confusing |
| `check-*/log-*/fix-*` triples | **MERGE** `log-*` into `check-*` | 3-skill pattern → 2-skill. Audits should create issues directly (`--log` flag) |

## Tier 2: Clarify Boundaries (fuzzy, not broken)

| Pair | Clarification |
|------|---------------|
| `/spec` vs `/shaping` | `/spec` = autopilot primitive (quick product spec). `/shaping` = interactive formal planning |
| `/architect` vs `/breadboarding` | `/architect` = file-level implementation plan. `/breadboarding` = affordance-level system map |
| `/debug` vs `/triage` | `/debug` = local dev. `/triage` = production incidents |
| `/critique` vs `/thinktank` | `/critique` = single persona adversarial. `/thinktank` = multi-model consensus |

## Tier 3: Domain Consolidation (future, lower priority)

| Domain | Current | Proposal |
|--------|---------|----------|
| Stripe | 12 skills | Consolidate to 4: `/stripe` (lifecycle), `/stripe-audit` (health), `/stripe-design` (planning), `/stripe-local-dev` (debugging) |
| Crypto | 10 skills | Consolidate to 3: `/bitcoin`, `/lightning`, `/check-payments` |
| Brand | 7 skills | Keep pipeline as-is (well-structured) |
| Docs | 6 skills | Merge `/documentation` + `/update-docs` + `/documentation-standards` → single `/docs` |

## Tier 4: Noise Reduction (meta)

- Archive unused skills to `_archived/` after 90 days without invocation
- Add `last-used:` frontmatter field to skills (updated by hook)
- Routing tables in every upstream skill pointing to alternatives
