Break down a large feature branch into multiple reviewable PRs.

# SHATTER

Think very very hard, investigate thoroughly, and perform a comprehensive architectural analysis and commit history dissection of the feature branch to identify logical breakpoints.

## Tenet Reminder: Modularity
**Modularity** - Build independent, focused components with clear boundaries. Each PR should represent a complete, testable unit of work that can be reviewed and merged independently. Avoid coupling between PRs where possible.

## Approach

Analyze the feature branch to identify refactorable units suitable for atomic pull request decomposition. Propose multiple strategies for breaking down the changes into discrete, reviewable PRs (e.g., by functional module, architectural layer, or dependency chain), explicitly detailing the advantages (e.g., reduced cognitive load for reviewers, improved CI/CD pipeline efficiency) and disadvantages (e.g., potential rebase complexity, temporary broken states) for each approach.

Articulate a strongly opinionated recommendation for the optimal PR sequencing and commit restructuring, emphasizing maintainability and integration stability.

Subsequently, provision a dedicated Git worktree for each confirmed logical segment, pre-populating each with a PRD/PLAN.md document that includes the precise scope, validation requirements, and a clear instruction to leverage strategic cherry-picking from the original monolithic branch for efficient commit reconstruction. Make sure each git worktree follows the naming convention `<repo-name>__<branch-name>`.
