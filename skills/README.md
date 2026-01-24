# Skills Taxonomy

Unix philosophy: small composable primitives + thin orchestration.

## Skill Types

| Type | Frontmatter | Who Invokes | Examples |
|------|-------------|-------------|----------|
| **Reference** | `user-invocable: false` | Claude auto-loads | git-mastery, testing-philosophy |
| **Primitive** | (default) | Model + user | stripe-audit, post, spec |
| **Orchestrator** | (default) | Model + user | /stripe, /cro, /changelog |
| **Top-level Workflow** | `disable-model-invocation: true` | User only | /audit |

## Top-Level Workflows

User-initiated project health checks. These are rare—most workflows should be model-invocable.

| Skill | Purpose |
|-------|---------|
| `/audit` | Comprehensive health check → GitHub issues |

Note: `/autopilot`, `/incident-response`, `/design-sprint` remain as commands (thin orchestrators).

## Orchestrators

Compose primitives into domain workflows. Model can invoke these.

| Skill | Domain | Primitives Used |
|-------|--------|-----------------|
| `/stripe` | Payments | stripe-audit, stripe-health, stripe-configure, stripe-verify |
| `/changelog` | Releases | changelog-audit, changelog-setup, changelog-page |
| `/observability` | Monitoring | sentry-observability, verify-fix, triage |
| `/documentation` | Docs | documentation-standards, update-docs |
| `/quality-gates` | CI/CD | code-quality-standards, testing-philosophy |
| `/llm-infrastructure` | LLM ops | llm-evaluation, llm-gateway-routing |
| `/virality` | Growth | social sharing, referrals, OG images |
| `/cro` | Conversion | form, page, signup, onboarding, paywall, popup patterns |
| `/social-content` | Marketing | post, announce, copywriting |

## Primitives

Focused, single-purpose skills. Model can invoke these.

### Stripe
- `stripe-audit` - Configuration review
- `stripe-health` - Webhook diagnostics
- `stripe-configure` - Dashboard setup
- `stripe-design` - Integration planning
- `stripe-scaffold` - Code generation
- `stripe-verify` - End-to-end testing
- `stripe-reconcile` - Fix drift issues
- `stripe-subscription-ux` - UI patterns

### Content & Marketing
- `post` - Twitter/X content generation
- `announce` - Launch posts for multiple platforms
- `copywriting` - Marketing copy
- `brand-builder` - Brand discovery → brand-profile.yaml
- `pricing-strategy` - Monetization decisions
- `marketing-psychology` - Behavioral principles

### Development
- `spec` - Product requirements (→ commands)
- `architect` - Technical design (→ commands)
- `refactor` - Code improvement (→ commands)
- `critique` - Adversarial review (→ commands)
- `groom` - Issue discovery (→ commands)
- `skill-builder` - Create new skills

### Quality & Review
- `code-review-checklist` - Review guidance
- `testing-philosophy` - Test patterns (reference)
- `verify-fix` - Incident verification

### Incident Response
- `investigate` - Debug production (→ commands)
- `postmortem` - Blameless analysis (→ commands)
- `triage` - Multi-source observability
- `fix-ci` - CI failure → fix → verify (→ commands)

### Infrastructure
- `sentry-observability` - Error tracking setup
- `env-var-hygiene` - Environment management
- `database-patterns` - Database operations
- `schema-design` - Universal schema principles

## References

Auto-loaded for context. Not in `/` menu. Set `user-invocable: false`.

| Skill | Purpose |
|-------|---------|
| `git-mastery` | Git workflow, commit conventions |
| `testing-philosophy` | Test behavior not implementation |
| `naming-conventions` | Intention-revealing names |
| `documentation-standards` | Comment why not what |
| `external-integration-patterns` | External service integration |
| `ui-skills` | Interface constraints |
| `business-model-preferences` | Pricing philosophy |
| `toolchain-preferences` | Stack defaults (pnpm, Next.js, etc.) |
| `design-tokens` | Tailwind @theme patterns |

## Language-Specific

These are reference-style but remain invocable for explicit use.

| Skill | Language |
|-------|----------|
| `typescript-excellence` | TypeScript best practices |
| `python-standards` | Modern Python with uv, ruff |
| `go-idioms` | Idiomatic Go patterns |
| `rust-patterns` | Ownership, errors, traits |
| `ruby-conventions` | Rails services, testing |
| `csharp-modern` | .NET 8+ patterns |

## Adding Skills

1. **Create directory:** `skills/{name}/SKILL.md`
2. **Add frontmatter:**
   - Default: model + user can invoke
   - `user-invocable: false`: reference only
   - `disable-model-invocation: true`: user-initiated only (rare)
3. **Follow pattern:** Look at existing skills in same category

## Principles

1. **Deep modules** — Hide significant complexity
2. **Compose, don't duplicate** — Orchestrators call primitives
3. **Model-invocable by default** — Only restrict when necessary
4. **References auto-load** — No need to invoke explicitly
