---
name: audit
description: |
  Unified domain auditor. Replaces individual check-* and log-* skills.
  Action is the command, domain is the parameter.
  `/audit [domain|--all]` with modes: --report (default), --issues, --fix.
  Invoke for: domain audit, issue creation from findings, automated fixes.
argument-hint: "[domain|--all] [--report|--issues|--fix]"
effort: high
---

# /audit

Unified domain auditor. One skill, all domains.

## Philosophy

**Domain as parameter, not command.** Instead of 15 `check-*` skills and 12 `log-*`
skills that share identical structure, `/audit` takes the domain as an argument and
reads domain-specific config from `audit/domains/{domain}.yml`.

**Three output modes:**
- `--report` (default) — Structured findings report, no side effects
- `--issues` — Same audit, then create GitHub issues from findings
- `--fix` — Same audit, then attempt automated fixes

## Usage

```
/audit quality              # Report on quality gates
/audit stripe --issues      # Audit Stripe, create issues
/audit bitcoin --fix        # Audit Bitcoin, fix what's possible
/audit --all                # Run all domain configs in parallel
/audit --all --issues       # Audit everything, create issues for all findings
```

## Process

### 1. Load Domain Config

```
Read ~/.claude/skills/audit/domains/{domain}.yml
```

If `--all`, load all `.yml` files from `domains/` directory.

If domain argument doesn't match a config file, auto-detect applicable domains
from the project (check for package.json dependencies, config files, directory
structure) and run those.

### 2. Execute Audit

For each domain config:

1. **Environment checks** — Verify required tools/env vars exist
2. **Automated checks** — Run each check defined in the config
3. **Deep audit** — Spawn specialized agent if defined in config
4. **Classify findings** — Map to P0-P3 using config's priority rules

### 3. Output

#### `--report` mode (default)

```markdown
## {Domain} Audit

### P0: Critical
- [finding]: [detail]

### P1: Essential
- [finding]: [detail]

### P2: Important
- [finding]: [detail]

### P3: Nice to Have
- [finding]: [detail]

## Summary
- P0: N | P1: N | P2: N | P3: N
- Recommendation: [top action]
```

#### `--issues` mode

After generating report, for each finding:

1. Check existing issues for duplicates: `gh issue list --state open --label "domain/{domain}" --limit 50`
2. Create issues using org-standards format (load `groom/references/org-standards.md`)
3. All sections required: Problem, Context, Acceptance Criteria (Given/When/Then), Affected Files, Verification, Boundaries, Approach
4. Apply canonical labels, set issue type, assign milestone
5. Run `/issue lint` on created issues to verify score >= 70
6. Report created issue count by priority

#### `--fix` mode

After generating report, for each finding with a defined fix:

1. Attempt the fix defined in the domain config
2. Re-run the check to verify
3. Commit fix if successful
4. Report what was fixed vs what needs manual intervention

### 4. Parallel Execution (`--all`)

When `--all`, spawn one agent per domain config. Run all in parallel.
Merge results into a single report organized by domain.

## Domain Config Schema

Each file in `audit/domains/{domain}.yml` defines:

```yaml
name: quality
description: Quality gates audit
labels:
  - domain/quality
agent: test-strategy-architect  # optional deep audit agent

# Optional applicability gate
detect:
  commands:
    - "shell command returning 0 if domain applies"
  # If detect block exists: run BEFORE checks
  # Any detect command succeeds (exit 0) → domain is applicable
  # All detect commands fail → skip domain, note "N/A"
  # No detect block → domain always runs (backwards-compatible)

checks:
  - id: test-runner
    name: Test runner configured
    commands:
      - "[ -f vitest.config.ts ] || [ -f vitest.config.js ]"
    priority: p0
    fix: "pnpm add -D vitest @vitest/coverage-v8"
    issue_title: "No test runner configured"
    issue_body: |
      ## Problem
      No testing framework configured. Code changes cannot be validated.

  - id: ci-workflow
    name: CI workflow exists
    commands:
      - "[ -f .github/workflows/ci.yml ] || [ -f .github/workflows/test.yml ]"
    priority: p0

  - id: git-hooks
    name: Git hooks configured
    commands:
      - "[ -f lefthook.yml ] || [ -f .husky/_/husky.sh ]"
    priority: p1
    fix: "pnpm add -D lefthook && pnpm lefthook install"

priority_rules:
  p0: "Production broken, no safety net"
  p1: "Missing fundamentals"
  p2: "Launch readiness gaps"
  p3: "Polish and optimization"
```

## Migration from check-*/log-*

Existing `check-*` skills migrate to domain configs:

| Old Skill | Domain Config |
|-----------|--------------|
| `/check-quality` | `domains/quality.yml` |
| `/check-production` | `domains/production.yml` |
| `/check-docs` | `domains/docs.yml` |
| `/check-observability` | `domains/observability.yml` |
| `/check-product-standards` | `domains/product-standards.yml` |
| `/check-stripe` | `domains/stripe.yml` |
| `/check-bitcoin` | `domains/bitcoin.yml` |
| `/check-lightning` | `domains/lightning.yml` |
| `/check-virality` | `domains/virality.yml` |
| `/check-landing` | `domains/landing.yml` |
| `/check-onboarding` | `domains/onboarding.yml` |
| `/check-posthog` | `domains/posthog.yml` |
| `/check-bun` | `domains/bun.yml` |
| `/check-btcpay` | `domains/btcpay.yml` |
| `/check-payments` | `domains/payments.yml` |

The `log-*` skills are subsumed by `--issues` mode.
The `fix-*` skills remain separate (fixing is genuinely domain-specific).

During migration, existing `check-*` skills remain as fallback. Once all configs
are validated, archive the old skills.

## Related

- `/groom` — Phase 2 invokes `/audit --all`
- `/issue lint` — Validate issues created by `--issues` mode
- `/tidy` — Calls `/audit --all --issues` as part of backlog hygiene
- `groom/references/org-standards.md` — Issue format for `--issues` mode
