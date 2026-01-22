# Documentation Checklist

## Every Project (Minimum Viable)

- [ ] **README.md** with:
  - [ ] One-sentence description
  - [ ] Quick start (< 30 seconds to running)
  - [ ] Prerequisites
  - [ ] Installation steps
  - [ ] Basic usage

- [ ] **.env.example** (if env vars used)
  - [ ] All required variables listed
  - [ ] Placeholder values or descriptions
  - [ ] Comments for non-obvious vars

- [ ] **.gitignore** includes:
  - [ ] Build artifacts
  - [ ] Dependencies (node_modules)
  - [ ] Environment files (.env, .env.local)
  - [ ] Editor/IDE configs

## Applications (Production Deployment)

Everything above, plus:

- [ ] **Architecture documentation**
  - [ ] CODEBASE_MAP.md or ARCHITECTURE.md
  - [ ] High-level system diagram
  - [ ] Data flow explanation
  - [ ] Key components and their roles

- [ ] **ADR directory** (docs/adr/)
  - [ ] Template for new decisions
  - [ ] Key architectural decisions documented
  - [ ] Format: Context → Decision → Consequences

- [ ] **Configuration docs**
  - [ ] All env vars documented in README or separate doc
  - [ ] Required vs optional clearly marked
  - [ ] Example values where safe

## Libraries (Public Consumption)

Everything in "Every Project", plus:

- [ ] **API documentation**
  - [ ] All public functions/classes documented
  - [ ] Parameters and return types
  - [ ] Examples for each API
  - [ ] Error conditions documented

- [ ] **CONTRIBUTING.md**
  - [ ] Development setup
  - [ ] Testing requirements
  - [ ] Code style guidelines
  - [ ] PR process

- [ ] **CHANGELOG.md**
  - [ ] Version history
  - [ ] Breaking changes highlighted
  - [ ] Migration guides for major versions

- [ ] **LICENSE** file

## Monorepos

Everything in "Applications", plus:

- [ ] **Root README** with:
  - [ ] Project overview
  - [ ] Package list with descriptions
  - [ ] Workspace setup instructions
  - [ ] Cross-package development workflow

- [ ] **Subdirectory READMEs**
  - [ ] Each package has its own README
  - [ ] Explains package purpose
  - [ ] Lists key exports/APIs
  - [ ] Links to root docs

## Open Source Projects

Everything in "Libraries", plus:

- [ ] **CODE_OF_CONDUCT.md**

- [ ] **SECURITY.md**
  - [ ] How to report vulnerabilities
  - [ ] Security policy

- [ ] **Issue templates**
  - [ ] Bug report template
  - [ ] Feature request template

- [ ] **PR template**

- [ ] **Badges in README**
  - [ ] Build status
  - [ ] Coverage
  - [ ] Version
  - [ ] License

## Quality Indicators

### Good Documentation

✅ Quick start gets user running in < 1 minute
✅ Examples are copy-pasteable and work
✅ Links all work (verified by lychee)
✅ Updated in same PR as code changes
✅ Architecture matches current implementation
✅ No TODO/FIXME in user-facing docs

### Bad Documentation

❌ README is just project name
❌ "Documentation coming soon"
❌ Examples with syntax errors
❌ Broken links
❌ References deprecated APIs
❌ Last updated 2+ years ago
❌ Requires reading source to understand usage
