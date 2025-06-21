# BOARD

## GOAL
Initialize GitHub repository with standardized labels and templates, and migrate existing backlog items to issues.

## 1. Repository Setup
- Set up standardized issue labels following engineering best practices:
  - Priority: `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
  - Type: `type:feature`, `type:bug`, `type:refactor`, `type:docs`, `type:test`, `type:chore`
  - Complexity: `size:xs`, `size:s`, `size:m`, `size:l`, `size:xl`
  - Domain: Domain-specific labels based on project architecture

- Create issue templates for consistent issue creation:
  - Feature request template
  - Bug report template
  - Refactoring task template

## 2. Backlog Migration
- Review BACKLOG.md to understand current tasks
- For each item in the backlog, create a GitHub issue with appropriate title, description, and labels
- Include any acceptance criteria, dependencies, or technical details from the backlog item
- After successful migration, rename BACKLOG.md to BACKLOG.md.migrated

## 3. Execute Repository Configuration
```bash
# Create all labels with appropriate colors and descriptions
gh label create priority:critical --color FF0000 --description "Critical issues requiring immediate attention"
gh label create priority:high --color FF9900 --description "High priority issues for current iteration"
gh label create priority:medium --color FFCC00 --description "Medium priority issues for planning"
gh label create priority:low --color FFFF00 --description "Low priority nice-to-have improvements"

gh label create type:feature --color 0075CA --description "New functionality"
gh label create type:bug --color D73A4A --description "Bug fixes"
gh label create type:refactor --color 6F42C1 --description "Code improvements without behavior change"
gh label create type:docs --color 0075CA --description "Documentation improvements"
gh label create type:test --color 0075CA --description "Test coverage improvements"
gh label create type:chore --color 0075CA --description "Maintenance tasks, dependencies, etc."

gh label create size:xs --color C2E0C6 --description "Very small changes (typo fixes, trivial changes)"
gh label create size:s --color C2E0C6 --description "Small changes (single file, simple logic)"
gh label create size:m --color C2E0C6 --description "Medium changes (multiple files, moderate complexity)"
gh label create size:l --color C2E0C6 --description "Large changes (significant refactoring, complex features)"
gh label create size:xl --color C2E0C6 --description "Very large changes (major architectural changes)"

# Create domain-specific labels based on project architecture
gh label create domain:frontend --color 5319E7 --description "Frontend changes"
gh label create domain:backend --color 5319E7 --description "Backend changes"
gh label create domain:api --color 5319E7 --description "API-related changes"
gh label create domain:database --color 5319E7 --description "Database changes"
gh label create domain:infra --color 5319E7 --description "Infrastructure changes"

# Set up issue templates
mkdir -p .github/ISSUE_TEMPLATE

# Feature request template
cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest a new feature or enhancement
title: ''
labels: type:feature
assignees: ''
---

## Feature Description
[Brief description of the feature]

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

## Technical Considerations
[Any technical details, architecture decisions, or implementation notes]

## Dependencies
[List any dependencies or blockers]
EOF

# Bug report template
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Report a bug to help us improve
title: ''
labels: type:bug
assignees: ''
---

## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Current Behavior
[What actually happens]

## Environment
- Version: [Software version]
- Platform: [OS, Browser, etc.]

## Additional Context
[Screenshots, logs, etc.]
EOF

# Refactoring template
cat > .github/ISSUE_TEMPLATE/refactoring.md << 'EOF'
---
name: Refactoring
about: Propose code refactoring
title: ''
labels: type:refactor
assignees: ''
---

## Refactoring Goal
[What this refactoring aims to accomplish]

## Motivation
[Why this refactoring is necessary]

## Scope
[Which parts of the codebase will be affected]

## Risk Assessment
[Potential risks and mitigation strategies]

## Verification Strategy
[How to verify the refactoring doesn't break existing functionality]
EOF

# Commit the templates
git add .github/
git commit -m "feat: add GitHub issue templates"
git push
```