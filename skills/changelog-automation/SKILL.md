---
name: changelog-automation
description: "Apply changelog automation and semantic versioning patterns using Changesets or semantic-release: conventional commits, automated version bumping, release notes generation. Use when setting up release workflows, discussing versioning, or implementing changelog automation."
---

# Changelog Automation

**Manual changelog maintenance is error-prone. Automate version bumping, changelog updates, and release notes.**

## Philosophy

Two proven approaches:
1. **Changesets**: PR-based workflow with explicit change declarations (best for monorepos)
2. **Semantic-release**: Commit-based workflow using conventional commits (best for single packages)

Both enforce Semantic Versioning and integrate with CI/CD.

## Semantic Versioning (SemVer)

`MAJOR.MINOR.PATCH`:
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward-compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

## Comparison

| Feature | Changesets | Semantic-release |
|---------|-----------|------------------|
| **Best for** | Monorepos | Single packages |
| **Workflow** | PR-based (explicit files) | Commit-based |
| **Automation** | Semi-automated | Fully automated |
| **Control** | High | Low |
| **Team discipline** | Low | High (strict commits) |
| **Monorepo support** | Excellent | Requires plugins |

## Decision Guide

- **Monorepo (2+ packages)**: Changesets
- **Single package, disciplined team**: semantic-release
- **Single package, less strict team**: Changesets
- **Need gradual adoption**: Changesets

## Best Practices

### Do
- Choose one approach, not both
- Enforce conventional commits (commitlint)
- Automate with GitHub Actions
- Write clear changeset descriptions
- Review generated changelog before releasing
- Tag releases in git

### Don't
- Manually edit CHANGELOG.md
- Skip changesets on PRs
- Ignore breaking changes
- Publish without CI
- Forget to build before publish

## Quick Setup

**Changesets (Monorepo):**
```bash
pnpm add -D @changesets/cli
pnpm changeset init
# Add GitHub Action, document workflow
```

**Semantic-release (Single Package):**
```bash
pnpm add -D semantic-release @semantic-release/git @semantic-release/changelog
pnpm add -D @commitlint/cli @commitlint/config-conventional
# Configure .releaserc.js, commitlint, GitHub Action
```

## References

Detailed configurations:
- `references/changesets.md` — Installation, config, workflow, GitHub Actions
- `references/semantic-release.md` — Installation, config, conventional commits
- `references/conventional-commits.md` — Commitlint setup, Lefthook integration

**"Versioning should be automatic, not an afterthought."**
