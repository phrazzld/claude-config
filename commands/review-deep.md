---
description: Comprehensive multi-agent code review using specialized agents and isolated worktree inspection
---

# REVIEW-DEEP

Exhaustive code review using parallel specialized agents. Analyzes code in isolated worktree without disturbing your working directory.

## When to Use

- Pre-PR quality gate: Catch issues before code review
- Complex changes: Multi-file refactors, architectural changes
- Learning: Understand what quality looks like from multiple perspectives
- Post-merge analysis: Review merged PRs to improve future work

## Prerequisites

- Git repository with clean working directory (or changes you're willing to stash)
- For PR reviews: gh CLI installed and authenticated
- For branch reviews: Branch name

## Usage

```bash
/review-deep [PR_NUMBER]           # Review specific PR
/review-deep [BRANCH_NAME]         # Review branch
/review-deep                       # Review latest PR on current repo
```

## Process

### Phase 1: Worktree Setup

**Create isolated review environment:**

1. Determine target (PR number, branch, or latest PR)
2. Create worktree directory: `$git_root/.worktrees/review-{identifier}`
3. Checkout target branch in worktree
4. Navigate to worktree for all subsequent analysis

**Why worktrees?**
- No merge conflicts with your working directory
- Review any branch without disturbing current work
- Clean up when done - just delete worktree
- Multiple simultaneous reviews possible

**Setup commands:**
```bash
git_root=$(git rev-parse --show-toplevel)
mkdir -p "$git_root/.worktrees"

# For PR:
gh pr checkout $PR_NUMBER --target-dir "$git_root/.worktrees/review-pr-$PR_NUMBER"

# For branch:
git worktree add "$git_root/.worktrees/review-$BRANCH_NAME" $BRANCH_NAME

cd "$git_root/.worktrees/review-{identifier}"
```

### Phase 2: Project Detection

Detect technology stack to determine relevant reviewers:

**Rails Project:**
- Check for `Gemfile` with `rails` gem
- Check for `config/application.rb`
- Reviewers: (skip kieran-rails-reviewer per user preference)

**TypeScript Project:**
- Check for `tsconfig.json`
- Check for TypeScript in package.json
- Reviewers: (skip kieran-typescript-reviewer per user preference)

**Python Project:**
- Check for `requirements.txt` or `pyproject.toml`
- Check for `.py` files
- Reviewers: (skip kieran-python-reviewer per user preference)

### Phase 3: Parallel Multi-Agent Analysis

**Launch all relevant agents in parallel** (single Task call):

**Universal Agents** (run for all projects):
1. Task architecture-strategist("Review code changes for architectural compliance")
2. Task security-sentinel("Audit code for security vulnerabilities")
3. Task performance-oracle("Identify performance bottlenecks and optimization opportunities")
4. Task pattern-recognition-specialist("Check for anti-patterns and consistency issues")
5. Task code-simplicity-reviewer("Evaluate complexity and suggest simplifications")
6. Task git-history-analyzer("Analyze commit history and change patterns")

**Conditional Agents** (based on changes):
7. Task data-integrity-guardian("Review migrations and data changes") - IF database changes detected
8. Task best-practices-researcher("Research latest best practices for [technologies used]") - IF using unfamiliar tech

**Wait for all agents to complete** before proceeding to synthesis.

### Phase 4: Findings Synthesis

**Consolidate multi-agent feedback:**

1. Collect findings from all agents
2. Categorize by severity:
   - 🔴 **P1 Critical**: Must fix before merge (security, data loss, breaking changes)
   - 🟡 **P2 Important**: Should fix before merge (performance, architecture, maintainability)
   - 🔵 **P3 Nice-to-have**: Consider for future (minor optimizations, style)
3. Remove duplicates (multiple agents flagging same issue)
4. Sort by impact and effort

### Phase 5: User Triage

**Present findings one at a time for decision:**

```
---
Finding #1: [Brief Title]

Severity: 🔴 P1
Category: [Security/Performance/Architecture/etc.]
Agent: [Which agent(s) found this]

Description:
[What's the issue]

Location: [file_path:line_number]

Impact:
[Why this matters, what could happen]

Proposed Solution:
[How to fix it]

Effort: [Small/Medium/Large]
---

What do you want to do?
1. fix-now - Add to TODO.md for immediate work
2. backlog - Add to BACKLOG.md for future
3. skip - Not relevant, move on
4. custom - Show me more details
```

**For "fix-now":**
- Add detailed task to TODO.md with context, location, approach
- Include finding #, agent name, full description
- Reference review session for traceability

**For "backlog":**
- Add to BACKLOG.md with review reference
- Include effort estimate and priority context

**For "skip":**
- Note in review summary why skipped
- Continue to next finding

### Phase 6: Cleanup

**Remove worktree and summarize:**

```bash
cd "$git_root"
git worktree remove ".worktrees/review-{identifier}"
```

**Summary Report:**
```markdown
## Review Complete

**Target**: PR #{number} / Branch {name}
**Agents**: {count} agents analyzed code
**Total Findings**: {X}
**Added to TODO**: {Y}
**Added to BACKLOG**: {Z}
**Skipped**: {W}

### Critical Issues (P1):
- [List critical items added to TODO.md]

### Important Issues (P2):
- [List important items]

### Future Improvements (P3):
- [List backlogged items]

### Next Steps:
1. Address TODO.md items (run /execute)
2. Re-run tests and validation
3. Push changes if fixing pre-PR
4. Or merge if this was post-merge learning
```

## Configuration

**Agent Selection:**
- Skip language-specific reviewers (kieran-*) per user preference
- Always run universal agents (architecture, security, performance, patterns, simplicity, git-history)
- Conditionally run specialized agents (data-integrity for migrations, best-practices for new tech)

**Worktree Location:**
- Stored in `$git_root/.worktrees/review-*`
- Automatically cleaned up after review
- Multiple reviews can run concurrently (different worktrees)

## Tips

**When to run:**
- Before creating PR: Catch issues early
- After feature complete: Quality gate before requesting review
- After PR merged: Learn from code review feedback
- Periodically: Audit old code for improvements

**What this doesn't replace:**
- Manual testing (QA)
- Human code review judgment
- Domain expertise

**What this excels at:**
- Systematic issue detection
- Multi-perspective analysis
- Learning from specialized agents
- Consistent quality standards

## Notes

This command creates NO permanent state in your working directory. The worktree is temporary, all analysis happens there, and cleanup is automatic.

Use this liberally - it's designed to be run frequently without disruption.
