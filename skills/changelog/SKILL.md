---
name: changelog
description: |
  Complete changelog and release notes infrastructure. Assesses current state and routes
  to appropriate workflow: setup (greenfield), fix (issues), or review (health check).
argument-hint: "[setup | fix | review]"
---

# /changelog

Automated changelogs, semantic versioning, and user-friendly release notes.

## What This Does

Assesses your project's release infrastructure and runs the appropriate workflow:

| State | Workflow | What Happens |
|-------|----------|--------------|
| No infrastructure | `changelog-setup` | Install semantic-release, CI, LLM synthesis, public page |
| Has issues | `changelog-fix` | Audit → reconcile → verify |
| Healthy | `changelog-review` | Audit → verify |

## Usage

```
/changelog              # Auto-detect and run appropriate workflow
/changelog setup        # Force greenfield workflow
/changelog fix          # Force fix workflow
/changelog review       # Health check
```

Arguments are passed as `$ARGUMENTS`. Interpret naturally - "setup", "from scratch", "new" all mean greenfield. "fix", "repair", "broken" all mean fix workflow.

## Process

### 1. Assess

First, understand what exists:
- Is semantic-release installed?
- Is conventional commits enforced (commitlint)?
- Does GitHub Actions workflow exist?
- Is LLM synthesis configured?
- Does public changelog page exist?

### 2. Route

Based on assessment:

**GREENFIELD** (no infrastructure)
→ Run `changelog-setup` workflow
→ Install semantic-release with full config
→ Set up GitHub Actions for releases
→ Configure Gemini 3 Flash synthesis
→ Scaffold public changelog page
→ Deep verification

**PARTIAL or HAS ISSUES** (broken/incomplete)
→ Run `changelog-audit` first
→ Then `changelog-reconcile` to fix
→ Then `changelog-verify`

**COMPLETE and HEALTHY**
→ Run `changelog-audit` for drift
→ Run `changelog-verify` to confirm

### 3. Execute

Run the selected workflow. Each workflow composes primitives:
- `changelog-assess` — understand state
- `changelog-setup` — greenfield installation
- `changelog-audit` — find issues
- `changelog-reconcile` — fix issues
- `changelog-verify` — prove it works
- `changelog-page` — public page scaffold

### 4. Quality Gate

Every workflow ends with `changelog-verify`. Nothing is complete until verification passes.

## Components Installed

### semantic-release
- Automatic version bumping from conventional commits
- CHANGELOG.md generation
- GitHub Release creation
- Git tags

### Conventional Commits (commitlint + Lefthook)
- Enforces commit message format
- Required for semantic-release to work
- Hooks into pre-commit via Lefthook

### GitHub Actions
- Triggers on push to main
- Runs semantic-release
- Triggers LLM synthesis post-release

### Gemini 3 Flash Synthesis
- Transforms technical changelog to user-friendly notes
- Runs after each release
- Stores in GitHub Release body
- Configurable personality per app

### Public Changelog Page
- Route: `/changelog` (no auth required)
- Fetches from GitHub Releases API
- Groups releases by minor version
- RSS feed support

## The Release Flow

```
Commit with conventional format (enforced by Lefthook)
       ↓
Push/merge to main
       ↓
GitHub Actions runs semantic-release
       ↓
Version bumped, CHANGELOG.md updated, GitHub Release created
       ↓
Post-release action triggers LLM synthesis
       ↓
Gemini 3 Flash transforms changelog → user notes
       ↓
Enhanced notes stored in GitHub Release
       ↓
Public /changelog page displays latest
```

## Key Principles

**Every merge is a release.** Web apps deploy on merge. Embrace frequent releases.

**Every change gets notes.** Even `chore:` commits become "Behind-the-scenes improvements." Users see active maintenance.

**Group for readability.** Public page groups patches under their minor version. Scannable, not overwhelming.

**Auto-publish.** No human gate on LLM synthesis. Trust the pipeline.

## Default Stack

Assumes Next.js + TypeScript + GitHub. Adapts gracefully to other stacks.

## What You Get

When complete:
- semantic-release configured and working
- Conventional commits enforced
- GitHub Actions workflow for releases
- Gemini 3 Flash synthesis for user-friendly notes
- Public `/changelog` page
- RSS feed at `/changelog.xml`
- Verified end-to-end

User can:
- Merge a PR with conventional commit
- See automatic version bump
- See GitHub Release created
- See user-friendly notes synthesized
- View public changelog page
