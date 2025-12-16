---
description: Transform learnings into executable artifacts - code, tests, skills, commands, agents, or documentation
---

Codify learnings into permanent, executable knowledge.

# CODIFY

Transform patterns, learnings, and solutions into executable artifacts that compound over time. Learnings become code abstractions, tests, skills, commands, agent instructions, and living documentation.

## Philosophy

**"Code is the truth. Everything else is opinion."**

Learnings locked in text files `/memory/*.md` are write-only archives. True compounding engineering means:
- Patterns → Code abstractions (execute)
- Bug resolutions → Tests (prevent regression)
- Multi-step workflows → Skills (automate)
- Frequent operations → Commands (one keystroke)
- Review feedback → Agent updates (enforce)
- Architectural decisions → Living docs (contextualize)

## Usage

```bash
/codify [topic]         # Analyze recent work, suggest codifications
/codify --last-n=10     # Analyze last 10 tasks
/codify --force         # Skip analysis, go straight to menu
```

## Codification Hierarchy (Descending Permanence)

### 1. Code Abstractions (Most Permanent)
Patterns → reusable functions, classes, hooks

**Example:**
```
Learning: "Convex functions must be pure - Date.now() fails"

Codify as code:
lib/convex/validators.ts:
  export function isPureConvexFunction(fn) {
    // Validates function has no side effects
    // Checks for Date.now(), Math.random(), fetch(), etc.
  }
```

**When to codify as code:**
- Pattern used 3+ times
- Clear abstraction boundary
- Non-trivial logic (>10 lines)
- Domain-specific pattern
- Idiomatic pattern (replaces non-canonical implementations)

### 2. Tests (Executable Specs)
Bug resolutions → regression tests, pattern → example tests

**Example:**
```
Bug: "Date.now() in Convex function caused validation error"

Codify as test:
lib/convex/validators.test.ts:
  describe('isPureConvexFunction', () => {
    it('rejects functions with Date.now()', () => {
      const impure = () => Date.now()
      expect(isPureConvexFunction(impure)).toBe(false)
    })

    it('accepts pure functions', () => {
      const pure = (timestamp: number) => timestamp
      expect(isPureConvexFunction(pure)).toBe(true)
    })
  })
```

**When to codify as test:**
- Bug was non-obvious
- Regression risk is high
- Pattern needs examples
- Edge case discovered

### 3. Skills (Reusable Workflows)
Multi-step patterns → executable workflows

**Example:**
```
Pattern: "Setting up Convex function with validation, types, tests"

Codify as skill:
skills/convex-function-setup/
  README.md - What this skill does
  template.ts - Function template
  template.test.ts - Test template
  install.sh - Setup script
```

**When to codify as skill:**
- Multi-step workflow (>3 steps)
- Used across projects
- Onboarding bottleneck
- Complex setup process

### 4. Commands (Workflow Automation)
Frequent operations → slash commands

**Example:**
```
Pattern: "Debugging Convex functions always requires same 5 steps"

Codify as command:
commands/debug-convex.md:
  1. Check function logs (npx convex logs)
  2. Validate function schema
  3. Check database state
  4. Run function in isolation
  5. Review error stack trace
```

**When to codify as command:**
- Operation done weekly+
- >5 steps to remember
- Error-prone manual process
- Domain-specific workflow

### 5. Agent Instructions (Review Patterns)
Code review feedback → agent prompt updates

**Example:**
```
PR Feedback (3rd time): "Always check Convex functions for purity"

Codify as agent update:
agents/architecture-guardian.md:
  ## Convex Function Validation
  - [ ] No Date.now(), Math.random()
  - [ ] No fetch(), external API calls
  - [ ] All dynamic values passed as arguments
  - [ ] Pure functions only
```

**When to codify as agent:**
- Feedback given 3+ times
- Automatable check
- Clear rule/pattern
- Prevents common mistake

### 6. Documentation (Living Context)
Architecture decisions → living docs

**Example:**
```
Decision: "Use Convex for backend, avoid REST API"

Codify as documentation:
ARCHITECTURE.md:
  ## Backend: Convex
  - Real-time subscriptions
  - Type-safe functions
  - No REST API needed
  - Rationale: [link to ADR]

docs/adr/005-convex-backend.md:
  # ADR 005: Convex for Backend
  ## Status: Accepted
  ## Context: ...
  ## Decision: ...
  ## Consequences: ...
```

**When to codify as docs:**
- Architectural decision made
- Pattern established
- Setup process defined
- Onboarding knowledge

### 7. CLAUDE.md / agents.md (Philosophy)
Universal principles, team conventions

**When to codify as philosophy:**
- Applies to all projects
- Fundamental principle
- Team standard
- Decision framework

## Implementation Flow

**Step 1: Launch Learning Codifier**
```bash
Task learning-codifier("Extract patterns from recent work")
```

Agent analyzes:
- Recent work logs in TODO.md (last 5-10 tasks)
- Recent commits (`git log -10`)
- Recent bug resolutions
- PR feedback patterns (via gh pr list)

**Step 2: Pattern Detection**
```
Analyzing recent work...

Detected 3 patterns worth codifying:

1. Convex Function Purity (HIGH confidence)
   - Occurrences: 3 times in last 10 tasks
   - Context: Date.now(), Math.random() validation errors
   - Impact: Production bugs, wasted dev time
   - Recommendation: Code abstraction + Test + Agent update

2. Error Boundary Setup (MEDIUM confidence)
   - Occurrences: 2 times in last 10 tasks
   - Context: React error boundaries for async components
   - Impact: Better UX, easier debugging
   - Recommendation: Skill + Documentation

3. Tailwind Responsive Pattern (LOW confidence)
   - Occurrences: 1 time (new pattern)
   - Context: Breakpoint utilities
   - Impact: Consistency
   - Recommendation: Documentation only

Recommend codifying #1 (HIGH) and #2 (MEDIUM). Proceed? [y/N]
```

**Step 3: Codification Menu**

For each approved pattern:

```
Pattern: Convex Function Purity

How should we codify this learning?
1. ✅ Code abstraction (extract reusable function)
2. ✅ Test (add regression/example test)
3. ⬜ Skill (create reusable workflow)
4. ⬜ Command (automate frequent operation)
5. ✅ Agent update (add review pattern)
6. ✅ Documentation (update living docs)
7. ⬜ Skip (one-off, not worth codifying)

Select: [1,2,5,6]
```

**Step 4: Execute Codifications**

For each selected target:

**Code (Pattern Extractor):**
```bash
Task pattern-extractor("Extract Convex purity validation")

Agent:
1. Analyzes existing implementation
2. Identifies reusable logic
3. Creates abstraction in lib/
4. Generates TypeScript types
5. Shows code for review
6. Commits: "codify: Extract Convex purity validator"
```

**Test (Pattern Extractor - Test Mode):**
```bash
Task pattern-extractor("Create Convex purity tests", mode="test")

Agent:
1. Identifies edge cases from bug
2. Writes regression test
3. Writes example tests showing usage
4. Ensures 100% coverage of new code
5. Commits: "codify: Add Convex purity tests"
```

**Agent (Agent Updater):**
```bash
Task agent-updater("Add Convex purity check to architecture-guardian")

Agent:
1. Identifies relevant agent (architecture-guardian)
2. Drafts prompt update
3. Shows diff for approval
4. Updates agent prompt
5. Commits: "codify: Add Convex purity check to architecture-guardian"
```

**Documentation:**
```bash
# Update living docs in same commit
Edit CONVEX.md:
  ## Pure Functions
  Convex functions must be pure...
  See: lib/convex/validators.ts

Commit: "codify: Document Convex purity requirements"
```

**Step 5: Sync Configs**

After codifying agents/skills/commands:
```bash
/sync-configs --target=all

# Syncs to ~/.codex and ~/.gemini
# Ensures all systems have latest knowledge
```

**Step 6: Verification**

```
✅ Codification Complete

Codified as:
  ✅ Code: lib/convex/validators.ts (45 lines)
  ✅ Tests: lib/convex/validators.test.ts (12 tests, 100% coverage)
  ✅ Agent: agents/architecture-guardian.md (Convex purity section added)
  ✅ Docs: CONVEX.md (Pure functions section updated)

Commits: 4 (codify: ...)
Synced: ~/.codex, ~/.gemini

Next: This pattern is now enforced automatically in /groom and /execute
```

## Integration with Workflow

**/execute → Codify Prompt:**
```
✅ Task complete: Implement user authentication

Learning detected: JWT validation pattern with refresh tokens

Codify now? [y/n/later]
> y

Analyzing pattern...
Recommend: Code abstraction + Tests
Proceed? [y/N]
```

**/debug → Codify Prompt:**
```
✅ Bug fixed: Race condition in state updates

Bug pattern: setState called during render

Prevent recurrence via:
1. Regression test
2. ESLint rule update
3. Agent checklist (error-handling-specialist)

Codify which? [1,2,3/skip]
> 1,3

Creating regression test...
Updating error-handling-specialist agent...
✅ Codified
```

**/git-respond → Codify Prompt:**
```
✅ PR feedback resolved: Extract validation to helper

PR feedback pattern: "Extract X to helper" (3rd occurrence this month)

This pattern occurs frequently. Add to agent checklist?
[y/n]
> y

Which agent should enforce this?
1. complexity-archaeologist (DRY violations)
2. maintainability-maven (code organization)
> 1

Updating complexity-archaeologist...
✅ Agent updated - will catch in future reviews
```

## Advanced Usage

**Force Codification (Skip Analysis):**
```bash
/codify --force

# Goes straight to codification menu
# Useful when you know exactly what to codify
```

**Analyze Specific Time Range:**
```bash
/codify --since="2025-11-01"
/codify --last-n=20

# Analyzes more history
# Useful for periodic codification sessions
```

**Target Specific Pattern:**
```bash
/codify "Convex function purity"

# Focuses analysis on specific topic
# Faster, more targeted
```

**Dry Run:**
```bash
/codify --dry-run

# Shows what would be codified
# No actual changes made
```

## Success Metrics

**Compounding Effect:**
- Pattern occurs 3+ times → codified once → enforced automatically forever
- Bug fixed → regression test → never recurs
- Manual workflow → skill → onboarding time -50%
- Review feedback → agent update → consistent enforcement

**Quality Indicators:**
- /groom finds fewer issues over time (patterns enforced)
- /execute references codified patterns (knowledge reused)
- New team members productive faster (skills + docs)
- PR review time decreases (agents catch issues)

## Related Commands

- `/execute` - Prompts for codification after task completion
- `/debug` - Prompts for codification after bug fix
- `/git-respond` - Prompts for codification after PR feedback
- `/sync-configs` - Syncs codified knowledge to codex/gemini
- `/groom` - Uses codified agent knowledge for reviews

## Related Agents

- `learning-codifier` - Analyzes work for patterns
- `pattern-extractor` - Extracts code abstractions
- `skill-builder` - Converts workflows to skills
- `agent-updater` - Updates agent prompts
