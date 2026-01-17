---
description: Create strategic TODO.md with atomic implementation tasks from plan
---

Ultrathink. Channel Ousterhout strategic programming principles. Favor taking the time to make deep modules and strategic improvements to system design, architecture, abstractions, quality gates, tests, documentation, etc; as opposed to quick, tactical fixes that incur technical debt.

Channel John Carmack, and synthesize this plan into a TODO.md file composed of discrete, well defined, narrowly scoped, highly detailed, context rich, atomic and actionable task items that start with `- [ ]`

If a TODO.md file already exists, incorporate your tasks elegantly into it. If a TODO.md file doesn't yet exist, create one.

## TODO.md Scope Boundaries

**INCLUDE in TODO.md (Implementation Tasks Only):**
- Writing/modifying code for the feature
- Creating tests for the implementation
- Updating types/interfaces/schemas
- Refactoring code directly related to the feature
- Adding/updating code documentation (JSDoc, inline comments)

**EXCLUDE from TODO.md (Not Implementation Tasks):**
- ❌ PR creation, code review, or git workflow tasks
- ❌ Deployment, monitoring, or post-merge activities
- ❌ Future enhancements or "nice-to-have" features
- ❌ Pre-merge checklists or quality gate running
- ❌ Process meta-tasks about the development workflow
- ❌ "Address review feedback" or "Respond to comments"
- ❌ "Monitor production" or "Check analytics"

**Future Enhancements → BACKLOG.md:**
If you identify optional features, improvements, or "nice-to-have" items during planning, write them to BACKLOG.md instead of TODO.md.

Structure BACKLOG.md as:
```markdown
# BACKLOG: [Feature Name]

## Future Enhancements
- [Optional feature]: [description, value, estimated effort]

## Nice-to-Have Improvements
- [Improvement]: [description, impact]

## Technical Debt Opportunities
- [Refactoring]: [benefit if addressed]
```

**Acceptance Criteria Format:**
- Write as **notes within task descriptions**, NOT as separate `- [ ]` checklist items
- Format: "Success criteria: [description]" or inline notes explaining what success looks like
- They describe what the implementation should achieve, not separate tasks to complete

