# Intent-Focused Command Design Pattern

**Extracted from git worktree, /simplify, and /observe optimizations (Jan 2025)**

This pattern dramatically improves command execution speed (30-50% faster) by focusing on WHAT needs to happen and WHY, rather than prescriptively dictating HOW with exact bash commands.

---

## Core Principle

**Commands should describe problems to solve and constraints to respect, not procedures to execute.**

Modern LLMs (like Claude) excel at problem-solving when given clear intent. They struggle when forced to follow rigid procedures that can't adapt to context.

### The Transformation

**Before (Prescriptive):**
```markdown
## Phase 1: Map Module Structure

```bash
# Top-level structure
find src -maxdepth 2 -type d | head -30

# Count files per directory
find src -type f -name "*.ts" | xargs dirname | sort | uniq -c | sort -rn
```

**Document**:
- **Module count**: [number]
- **Distribution**: [even or concentrated?]
```

**After (Intent-Focused):**
```markdown
## Understand the Complexity

**Map the landscape:**
- Identify module structure and distribution
- Find coupling hotspots (most-imported modules)
- Locate large files (>300 lines)

**Key questions:**
- Where is complexity concentrated?
- What's the overall architecture story?
```

---

## The Five Principles

### 1. Balanced Clarity

**Primary focus:** Describe WHAT needs to happen and WHY
**Secondary:** Keep essential bash examples for complex/non-obvious operations
**Tertiary:** Minimal troubleshooting for common issues

**Example:**
```markdown
## What It Does

**Fetch & Setup:**
- Use `gh pr view` to get PR details (number, title, branch)
- Fetch PR branch with `gh pr checkout`
- Create worktree from fetched commit
- Copy environment files (.env, .env.local, .env.test)
```

**Not:**
```markdown
**1. Fetch PR Information**
```bash
gh pr view $PR_NUMBER --json headRefName,number,title
PR_BRANCH=$(gh pr view $PR_NUMBER --json headRefName --jq .headRefName)
PR_TITLE=$(gh pr view $PR_NUMBER --json title --jq .title)
```
```

### 2. Speed Through Parallelization

**Explicitly call out operations that can/should run concurrently**
**Remove sequential phase numbering where possible**
**Emphasize performance-critical optimizations**

**Example:**
```markdown
## Key Optimization

**Run all validation checks concurrently** rather than sequentially.
These checks are independent and represent the slowest part (~40-90s).
Running in parallel can reduce total time by 30-40%.

**Validate (Parallel):**
- TypeScript compilation (`pnpm run typecheck`)
- Linting (`pnpm run lint`)
- Test suite (`pnpm run test`)
```

**Not:**
```markdown
**4. Run Initial Checks**
```bash
pnpm run typecheck  # TypeScript validation
pnpm run lint       # Linting
pnpm run test       # Run test suite
```
```

### 3. Flexible Intelligence

**Make checks conditional** ("if needed") **not mandatory** ("always")
**Trust Claude to choose optimal approaches**
**Allow Claude to skip unnecessary steps**

**Example:**
```markdown
### Optional: Contemporary Pattern Research

**When to use:**
If stack is unfamiliar or patterns seem outdated.

**When to skip:**
If stack is familiar and patterns are current, proceed directly.
```

**Not:**
```markdown
## Phase 2.2: Research Contemporary Patterns

Before analysis, research current patterns:
```bash
gemini "Research modern patterns for ${FRAMEWORK}..."
```
[Always executed, no conditional logic]
```

### 4. Maintainable Structure

**Keep one concrete example per command**
**Preserve essential workflow patterns**
**Balance brevity with comprehensibility**

**Example:**
```markdown
## Workflow Example

```bash
# From main project
/git-worktree-review 123

# Open NEW terminal window
cd ../myproject-worktree-pr-123
claude

# Review in isolated environment
/groom
git diff main

# When done
/git-worktree-cleanup
```
```

**Not:**
- 5-7 verbose use case examples
- Every edge case documented
- Extensive "how-to" for each scenario

### 5. Natural Language First, Code Second

**Describe outcomes in plain English**
**Include bash snippets only for non-obvious operations**
**Let Claude adapt commands to context**

**Example:**
```markdown
**Create Worktree:**
- Determine worktree path: `../$PROJECT-worktree-$BRANCH_NAME`
- Create worktree with new branch: `git worktree add -b $BRANCH_NAME $PATH`
- Or checkout existing branch: `git worktree add $PATH $BRANCH_NAME`
```

**Not:**
```markdown
**2. Create Worktree**
```bash
# Determine worktree path
WORKTREE_DIR="../$(basename $PWD)-worktree-$BRANCH_NAME"

# Create worktree
if git rev-parse --verify $BRANCH_NAME >/dev/null 2>&1; then
  git worktree add $WORKTREE_DIR $BRANCH_NAME
else
  git worktree add -b $BRANCH_NAME $WORKTREE_DIR
fi
```
```

---

## Command Structure Template

```markdown
---
description: [One-line description of what command does]
---

[One-sentence summary]

# COMMAND NAME

[2-3 sentence description of command purpose and value]

## Intent

[What this command accomplishes]
[List 3-5 key outcomes]

## Key Optimization (Optional)

**[Performance insight if applicable]**
[Why this optimization matters, what it improves]

## Your Approach

### 1. [First Major Step]

**[What to do]:**
- [Bullet point description of actions]
- [Focus on WHAT, not exact HOW]
- [Include constraints and goals]

**[Key questions or checks]:**
- [What to verify]
- [What to look for]

### 2. [Second Major Step]

**[When to use this step]:**
[Conditions that make this relevant]

**[When to skip]:**
[Conditions where this isn't needed]

### 3. [Synthesis/Output Step]

**[How to organize results]:**
- [Priority tiers, categories, or structure]
- [Action items or recommendations]

## [Core Principles/Philosophy Section]

**[Key concept]:**
- [Principle or guideline]
- [Example or pattern]

## [Common Issues/Patterns Section]

**[Issue]:**
[Brief resolution guidance]

**[Pattern]:**
[Recommended approach]

## Your Output

**[Expected deliverable]:**
- [What to report]
- [How to structure it]

**[Success criteria]:**
- [How to know you've succeeded]

## Related Commands

- `/command-name` - Description
```

---

## Metrics for Success

**File Length:**
- **Target:** 40-50% reduction from original
- **Git worktree commands:** Achieved 35-57% reduction
- **/simplify:** Achieved 62% reduction (701 → 267 lines)
- **/observe:** Achieved 62% reduction (712 → 272 lines)

**Execution Speed:**
- **Target:** 30-40% faster execution
- **Review command:** 30-35% faster (parallel validation checks)
- **Cleanup command:** 30-40% faster (parallel status detection)

**Maintainability:**
- Easier to update (less detailed procedure to maintain)
- Clearer intent (easier to understand purpose)
- More adaptable (Claude can optimize for context)

---

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Numbered Phases

**Bad:**
```markdown
## Phase 1: Understanding
## Phase 1.1: Map Structure
## Phase 1.2: Identify Patterns
## Phase 2: Summoning the Council
## Phase 2.5: Grug's First Pass
## Phase 2.2: Optional Research
```

**Good:**
```markdown
## Your Approach

### 1. Understand the Complexity
### 2. Invoke the Council (In Parallel)
### 3. Optional: Contemporary Pattern Research
### 4. Synthesize & Prioritize
```

### ❌ Anti-Pattern 2: Exact Bash Commands

**Bad:**
```markdown
```bash
find src -type f -name "*.ts" | xargs wc -l | sort -rn | head -20
grep -rn "Manager\|Helper\|Util" src/ --include="*.ts" -l
```
```

**Good:**
```markdown
- Locate large files (>300 lines) and complexity magnets
- Detect red flag names (Manager/Helper/Util)
```

### ❌ Anti-Pattern 3: Verbose Documentation Templates

**Bad:**
```markdown
**Document**:
```markdown
## Complexity Inventory

**Module Structure**: [count] top-level modules
**Large Files** (>300 lines): [list with line counts]
**Red Flag Names**: [Manager/Helper/Util occurrences]
```
```

**Good:**
```markdown
**Complexity Analysis:**
- Current state summary
- Complexity hotspots identified
- Council perspectives synthesized
```

### ❌ Anti-Pattern 4: Mandatory Sequential Steps

**Bad:**
```markdown
**3. Environment Setup**

Copy environment files:
```bash
[ -f .env ] && cp .env $WORKTREE_DIR/
[ -f .env.local ] && cp .env.local $WORKTREE_DIR/
```

Then install dependencies:
```bash
pnpm install
```

Then setup hooks:
```bash
lefthook install
```
```

**Good:**
```markdown
**Environment Setup:**
- Copy environment files if they exist
- Symlink node_modules (or install if needed)
- Install git hooks
```

### ❌ Anti-Pattern 5: Excessive Use Cases

**Bad:**
- 5-7 detailed use case scenarios
- Every edge case documented
- Verbose "how-to" for each scenario

**Good:**
- 1-2 clear workflow examples
- Essential patterns only
- Trust Claude to adapt

---

## When to Use This Pattern

**✅ Use for:**
- Complex commands with multiple steps
- Commands that invoke tools or run processes
- Workflows that benefit from Claude's intelligence
- Commands where context matters (different projects, stacks)

**❌ Don't use for:**
- Simple, single-action commands
- Commands where exact procedure is critical (security, compliance)
- Domain-specific commands requiring precise steps

---

## Migration Guide

**To migrate an existing prescriptive command:**

1. **Identify core intent**: What problem does this solve?
2. **Extract key constraints**: What must be respected?
3. **Remove procedural detail**: Delete exact bash commands unless essential
4. **Consolidate phases**: Group related steps, remove numbering
5. **Add parallelization hints**: Where can things run concurrently?
6. **Preserve one example**: Keep one clear workflow demonstration
7. **Test with real usage**: Verify Claude understands intent

**Expected outcome:** 40-60% reduction in file length, maintained or improved functionality.

---

## Future Improvements

**Potential enhancements to this pattern:**
- Structured output schemas (JSON/YAML) for command results
- Confidence scoring for recommendations (high/medium/low confidence)
- Built-in feedback loops (command asks clarifying questions)
- Integration with learning codification (capture patterns from execution)

---

**Last Updated:** 2025-01-27
**Pattern Version:** 1.0
**Author:** Extracted from command optimization sprint

**Related Documents:**
- `/Users/phaedrus/.claude/plans/swift-percolating-marble.md` (optimization plan)
- `/Users/phaedrus/.claude/CLAUDE.md` (global instructions)
