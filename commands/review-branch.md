---
description: Code review with thinktank using full context (docs + code + dependencies)
---

# THINKTANK-REVIEW

> Review with full context: what changed, what it touches, what explains it.

## Mission

Run a comprehensive code review using thinktank with complete context: the changed files, their dependencies, and all relevant documentation.

## Process

### 1. Documentation Check (MANDATORY)

**Do this first. Do not skip.**

Run `/documentation`.

This ensures core docs exist (creating them if missing):
- ARCHITECTURE.md - system overview
- README.md - project identity
- CLAUDE.md - conventions
- Module READMEs where needed

Wait for documentation to complete before proceeding.

### 2. Identify Changed Files

What's different on this branch vs main/master?

```bash
git diff --name-only $(git merge-base HEAD main)...HEAD
```

If no changes, use staged files or prompt for scope.

### 3. Trace Dependencies

For each changed file, identify what it touches:

- **Imports**: What modules does it import from?
- **Exports**: What uses this file's exports?
- **Types**: What type definitions are shared?
- **Config**: What config files affect this code?

Build a list of touched files (keep it focused - first-degree dependencies, not transitive).

### 4. Gather Relevant Docs

Find documentation that explains the changed code:

**Required docs** (`/documentation` ensures these exist):
- ARCHITECTURE.md - system overview
- README.md - project identity
- CLAUDE.md - conventions

**Contextual**:
- Module READMEs in directories containing changed files
- ADRs relevant to the changed components
- Any .md files near the changed code
- Design docs referenced in comments

### 5. Create Review Instructions

Write focused instructions for thinktank:

```markdown
# Code Review Request

## What Changed
[Summary of the changes - feature, fix, refactor]

## Files to Review
[List of changed files]

## Context Files
[List of touched dependencies]

## Documentation Context
[List of relevant docs included]

## Review Focus
- Correctness: Does this work as intended?
- Patterns: Does it follow project conventions?
- Architecture: Does it fit the system design?
- Edge cases: What could go wrong?
- Tests: Is coverage adequate?

## Requested Output
For each concern:
1. File and line reference
2. Issue description
3. Suggested fix
4. Severity (critical/important/minor)
```

Write to `/tmp/review-instructions.md`.

### 6. Invoke Thinktank

```bash
thinktank /tmp/review-instructions.md \
  ./README.md \
  ./CLAUDE.md \
  ./ARCHITECTURE.md \
  ./docs/relevant-adr.md \
  ./src/changed-file.ts \
  ./src/touched-dependency.ts \
  --synthesis
```

Pass actual file paths - docs AND code together.

### 7. Specialized Reviews (Parallel)

If changes touch external integrations, spawn focused reviewers:

**For Stripe/Payment code** (file path contains `stripe`, `payment`, `checkout`, `subscription`, `webhook`):
- Invoke `Skill("stripe-best-practices")`
- Check: webhook handler patterns, env var usage, error handling
- Verify: no hardcoded keys, proper signature verification

**For Auth code** (Clerk/Auth0 — file path contains `auth`, `clerk`, `session`):
- Invoke `Skill("billing-security")`
- Check: JWT validation, session handling, redirect URLs

**For any external API integration**:
- Spawn `config-auditor` agent to verify:
  - Env vars documented and validated at runtime
  - Error handling for API failures
  - Retry/fallback patterns present
  - Health check endpoint for this service

**For Infrastructure changes**:
- Spawn `infrastructure-guardian` agent with focus on:
  - Deployment config completeness
  - Environment parity (dev ≠ prod gotchas documented)
  - Rollback capability

### 8. Synthesize Results

Read thinktank output and synthesize:

**Consensus Issues** (all models agree):
- Critical bugs or security issues
- Clear convention violations
- Missing error handling

**Divergent Views** (investigate further):
- Architecture opinions
- Pattern preferences
- Optimization suggestions

**Actionable Items**:
1. Must-fix before merge
2. Should-fix in this PR
3. Consider for follow-up

## Output

```markdown
## Code Review: [Branch/Feature Name]

### Summary
[1-2 sentence overview of the changes and review findings]

### Critical Issues (Block Merge)
- [ ] Issue 1: [description] - `file.ts:42`
- [ ] Issue 2: [description] - `other.ts:17`

### Important Issues (Fix in PR)
- [ ] Issue 3: [description]
- [ ] Issue 4: [description]

### Minor Suggestions
- Suggestion 1: [description]
- Suggestion 2: [description]

### Positive Observations
- Good use of [pattern]
- Clean implementation of [feature]

### Next Steps
1. Address critical issues
2. Fix important issues
3. Optionally address minor suggestions
```

## Philosophy

Code review without context is noise. Thinktank needs to understand:
- What the project is (README)
- How it's built (ARCHITECTURE)
- What conventions apply (CLAUDE.md)
- What decisions were made (ADRs)
- What code is related (dependencies)

Only then can it give useful feedback, not generic suggestions.
