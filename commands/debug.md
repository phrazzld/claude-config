---
description: Systematically diagnose and resolve defects with testable hypotheses
---

# DEBUG

> **THE DEBUGGING MASTERS**
>
> **Brian Kernighan**: "The most effective debugging tool is still careful thought, coupled with judiciously placed print statements."
>
> **Rob Pike**: "When debugging, novices insert corrective code; experts remove defective code."
>
> **John Carmack**: "Focus is a matter of deciding what things you're not going to do."

Find bugs by thinking, not guessing. Every minute the defect persists costs real money. You've debugged 500+ production issues—you know that 90% of bugs live in new code, and the hardest part is understanding the problem, not fixing it.

## Your Mission

Systematically diagnose and resolve defects. Turn vague bug reports into precise understanding, form testable hypotheses, and implement minimal fixes with regression tests.

**The Debugging Question**: What is the system actually doing vs what should it do?

## The Debugging Philosophy

### Kernighan's Principle
"Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."

Write simple code. You'll thank yourself later.

### Pike's Wisdom: Remove, Don't Add
Novices add code to work around bugs. Experts understand the system well enough to remove the defective code. Every addition increases complexity; every removal decreases it.

### Carmack's Focus: Minimize Surface Area
The debugging scope should shrink with every experiment. Binary search everything: commits, code paths, data. Cut the problem in half repeatedly.

## Phase 1: Understand the Problem

Read @ISSUE.md or bug description. Capture immediately:

**Key questions**:
- What changed recently? (90% of bugs are in new code)
- Can you reproduce it reliably?
- What's the simplest failing case?
- What's the expected vs actual behavior?

Document explicitly:
- **Expected behavior**: What should happen per requirements
- **Actual behavior**: What's actually happening (be specific)
- **Delta**: Where reality diverges from expectation
- **Reproduction steps**: Exact steps to trigger issue
- **Environment**: Specific conditions where bug occurs

## Phase 2: Analyze Evidence

### For Screenshots/Visual Evidence
- What UI state is shown?
- What elements are missing or incorrect?
- Console errors visible in dev tools?
- Network failures in network tab?

### For Logs/Stack Traces
- What's the error message (exact text)?
- Where does the stack trace point? (file:line)
- What was the triggering action?
- What values were involved?

### For Descriptions
- Clarify ambiguities: ask specific questions
- Capture reproduction steps precisely
- Understand expected vs actual behavior
- Note any workarounds user discovered

**Synthesize**: Combine all evidence into clear problem statement.

## Phase 3: Form Hypotheses

**Before touching code**, think through:
- What do you think is broken?
- Why do you think that?
- How will you prove it?
- What if you're wrong?

Write your hypothesis before testing it. Document evidence supporting or refuting it.

### Make the System Visible

Add strategic instrumentation:
- Log at key decision points
- Capture state at critical transitions
- Log inputs/outputs of failing functions
- Use structured logging for searchability
- **Remove all instrumentation afterward**

## Phase 4: Systematic Investigation

### Binary Search the Problem Space

1. **When**: Find when it broke using git history (`git bisect`)
2. **Where**: Find where it breaks using search tools
3. **Why**: Find why it breaks using targeted logging

### Usual Suspects Checklist

- [ ] Off-by-one: boundaries, loops, array indices
- [ ] Null/undefined: missing checks, race conditions
- [ ] State mutations: shared state, side effects
- [ ] Async issues: race conditions, promise chains
- [ ] Type mismatches: string vs number, implicit conversions

Keep a log of what you tried and learned.

## Phase 4.5: Domain Expert Review (Intelligent Agent Composition)

*After understanding the bug pattern, invoke the appropriate domain expert agent for specialized guidance.*

**Classify the bug category first**:
- Database issues? (migrations, queries, transactions, data integrity)
- API issues? (REST, GraphQL, HTTP, error responses)
- Test failures? (flaky tests, coverage, test strategy)
- Error handling? (exceptions, error boundaries, logging)
- State management? (React state, race conditions, stale closures)
- Dependency issues? (package conflicts, security vulnerabilities, bundle size)
- Security? (XSS, CSRF, SQL injection, auth/authz)
- Performance? (slow queries, memory leaks, bundle bloat)

**Then invoke the matching specialist agent**:

```bash
# Database bugs → data-integrity-guardian
Task data-integrity-guardian("Review this database bug for data integrity issues")
Prompt:
Analyze the bug from a data integrity perspective:
- Migration safety: Does the fix require schema changes? Are they safe?
- Transaction boundaries: Is data modification properly wrapped?
- Referential integrity: Are foreign key constraints maintained?
- Data validation: Are constraints enforced at database level?
Report: Integrity risks, migration recommendations, transaction fixes

# API bugs → api-design-specialist
Task api-design-specialist("Review this API bug for design issues")
Prompt:
Analyze the bug from an API design perspective:
- HTTP semantics: Correct method and status codes?
- Error responses: Proper error format and messages?
- Idempotency: Is the endpoint idempotent when it should be?
- Versioning: Breaking change requiring version bump?
Report: API design violations, proper HTTP usage, breaking changes

# Test bugs → test-strategy-architect
Task test-strategy-architect("Review test failure and test strategy")
Prompt:
Analyze the test failure:
- Flaky test? (timing issues, race conditions, external dependencies)
- Test quality: Testing behavior or implementation?
- Coverage gaps: What scenarios are missing?
- Test pyramid: Is this tested at the right level?
Report: Flakiness root cause, test improvements, coverage recommendations

# Error handling bugs → error-handling-specialist
Task error-handling-specialist("Review error handling patterns")
Prompt:
Analyze error handling:
- Error boundaries: Proper React error boundaries?
- Async errors: Promise rejections handled?
- User experience: Graceful degradation?
- Logging: Errors properly logged with context?
Report: Error handling gaps, user experience fixes, logging improvements

# State management bugs → state-management-analyst
Task state-management-analyst("Review state management issue")
Prompt:
Analyze state bug:
- Race condition: Async state updates conflicting?
- Stale closure: Function closing over old state?
- Unnecessary re-renders: State structure inefficient?
- State location: Local vs global state appropriate?
Report: State bug root cause, fix strategy, optimization opportunities

# Dependency bugs → dependency-health-monitor
Task dependency-health-monitor("Review dependency issue")
Prompt:
Analyze dependency problem:
- Security vulnerability: CVE identified?
- Version conflict: Peer dependency mismatch?
- Bundle impact: Does update affect bundle size?
- Breaking changes: Migration path documented?
Report: Security assessment, version resolution, migration steps

# Security bugs → security-sentinel
Task security-sentinel("Perform security analysis of vulnerability")
Prompt:
Analyze security bug:
- Attack vector: How can this be exploited?
- Severity: CRITICAL/HIGH/MEDIUM/LOW?
- Scope: What data/systems are exposed?
- Defense layers: What other protections needed?
Report: Security assessment, fix verification, additional protections

# Performance bugs → performance-oracle
Task performance-oracle("Analyze performance bottleneck")
Prompt:
Analyze performance issue:
- Bottleneck type: CPU, memory, network, database?
- Measurement: How do we verify the fix?
- Trade-offs: Complexity vs performance gain?
- Optimization opportunities: Quick wins available?
Report: Bottleneck analysis, optimization recommendations, measurement plan
```

**Multiple categories?** Invoke multiple agents in parallel:
```bash
# Example: Database + API bug
Task data-integrity-guardian("Review database transaction issue")
Task api-design-specialist("Review API error response")
```

**Agent review integration**:
- Agents provide domain-specific insights before you fix
- Their recommendations inform Phase 5 (Fix With Simplicity)
- Document agent findings in debug report
- If agents conflict, prioritize correctness > performance > elegance

**When to skip**: For trivial bugs (typos, simple logic errors), skip agent review and proceed directly to fix.

---

## Phase 5: Fix With Simplicity

**Choose the simplest fix that solves the problem completely**.

- Fix with minimal code change
- Prefer straightforward fixes over clever workarounds
- Keep fixes concrete rather than abstract
- Stay focused on the specific problem
- Address unrelated issues in separate commits

**Can you explain the fix in one sentence?** Aim for this level of clarity.

## Phase 6: Root Cause Documentation

Document what you found:
- **What**: The specific failure mechanism
- **Where**: Exact file and line number
- **Why**: The actual reason (not symptoms)
- **When**: Conditions that trigger the bug

### Add Regression Test

```typescript
describe('Bug #123: [description]', () => {
  it('should [expected behavior]', () => {
    // This test failed before fix, passes after
  });
});
```

Verify: bug reproduces before fix, disappears after, no new bugs introduced.

## Phase 7: Post-Mortem

Ask yourself:
- Why didn't tests catch this?
- What similar bugs might exist?
- How can we prevent this class of bugs?
- Is the fix simpler than the bug?

## Phase 8: Learning Codification

After resolving the bug, check if the root cause reveals a pattern worth codifying:

**Ask yourself**: Is this bug part of a broader pattern?

✅ **Codifiable bug patterns**:
- Non-obvious bug with broader implications
- 3rd occurrence of similar bug (pattern detected)
- Framework-specific gotcha discovered
- Race condition or timing issue
- Edge case revealing design weakness
- Security vulnerability pattern
- Performance issue root cause

❌ **Not worth codifying**:
- Typo or trivial mistake
- One-off bug specific to implementation
- User error (not system error)
- Already well-known pattern

**If pattern detected, prompt**:

```
✅ Bug resolved: [bug description]

Root cause: [1-2 sentence summary]

Bug pattern detected. Codify to prevent recurrence?
[y] Yes - Analyze and recommend codification targets
[l] Later - Note in debug report for batch codification
[n] No - Skip, one-off issue

> _
```

**If user selects [y]**:
```bash
Task learning-codifier("Extract bug pattern from this debug session and recommend codification targets to prevent recurrence")

# Agent will:
# 1. Analyze debug report, root cause, and fix
# 2. Detect pattern category (code, test, architecture, security, performance)
# 3. Recommend codification targets emphasizing regression tests + preventive measures
# 4. Launch appropriate agents (pattern-extractor, agent-updater)
# 5. Create executable artifacts (tests, abstractions, agent checks)
# 6. Commit with "codify: [pattern] regression prevention" message
```

**Recommended codification priority for bugs**:
1. **Regression Tests** (HIGHEST - always create)
2. **Agent Updates** (enforce checks to catch similar bugs)
3. **Code Abstractions** (if pattern can be encapsulated)
4. **Documentation** (explain gotcha/edge case)
5. **ESLint Rules** (automate detection)

**If user selects [l]**:
```markdown
Add to debug report:
LEARNING: [summary for future codification]
BUG PATTERN: [category: async/state/type/boundary/security/etc.]
SIMILAR BUGS: [list any related issues]
```

**If user selects [n]**:
Complete debug cycle.

**Examples**:

<details>
<summary>Example 1: setState During Render → Multiple Codifications</summary>

```
✅ Bug resolved: React error "Cannot update component during render"

Root cause: setState called synchronously in component body, triggering render loop

Bug pattern detected. Codify to prevent recurrence?
[y] Yes - Analyze and recommend codification targets
[l] Later - Note in debug report for batch codification
[n] No - Skip, one-off issue

> y

Analyzing pattern...

Pattern: React setState During Render (HIGH confidence)
Occurrences: 2nd time this month
Impact: CRITICAL (runtime errors, infinite loops)

Recommended codifications:
  [✓] Regression test - Test that component doesn't setState during render
  [✓] Agent update - Add to error-handling-specialist checklist
  [✓] ESLint rule - Configure eslint-plugin-react-hooks
  [ ] Code abstraction - React handles this, not our concern
  [✓] Docs - Update REACT.md with setState rules

Proceed with test + agent + eslint + docs? [y/N]
> y

Launching pattern-extractor in test mode...
✅ Created: tests/regression/bug-042-setstate-render.test.tsx
   Regression test ensuring component doesn't setState during render
✅ Committed: codify: Add setState-during-render regression test

Launching agent-updater...
✅ Updated: agents/error-handling-specialist.md
   Added check: "No setState/dispatch calls in component body (only in useEffect/handlers)"
✅ Committed: codify: Add React setState check to error-handling-specialist

Configuring ESLint...
✅ Updated: .eslintrc.json
   Enabled: react-hooks/exhaustive-deps, react-hooks/rules-of-hooks
✅ Committed: codify: Configure ESLint to catch setState-during-render

Updating documentation...
✅ Updated: REACT.md (Component Lifecycle section)
   Added: setState usage patterns and pitfalls
✅ Committed: codify: Document React setState rules

Syncing configs...
✅ Synced to ~/.codex/agents/error-handling-specialist.md
✅ Synced to ~/.gemini/system-instructions/error-handling-specialist.txt

✅ Codification complete
Prevention: ESLint catches at dev time, agent catches in review, test ensures no regression
```
</details>

<details>
<summary>Example 2: Null Pointer in Async Callback → Regression Test</summary>

```
✅ Bug resolved: TypeError "Cannot read property 'id' of null"

Root cause: Race condition - component unmounted before async callback executed, state became null

Bug pattern detected. Codify to prevent recurrence?
[y] Yes - Analyze and recommend codification targets
[l] Later - Note in debug report for batch codification
[n] No - Skip, one-off issue

> y

Analyzing pattern...

Pattern: Async Callback After Unmount (MEDIUM confidence)
Occurrences: 1st time (new discovery)
Impact: HIGH (runtime errors)

Recommended codifications:
  [✓] Regression test - Test async operations with component unmount
  [✓] Code abstraction - Extract useAsyncEffect hook with cleanup
  [ ] Agent update - error-handling-specialist already checks async patterns
  [✓] Docs - Update REACT.md with async cleanup patterns

Proceed with test + abstraction + docs? [y/N]
> y

Launching pattern-extractor in test mode...
✅ Created: tests/regression/bug-057-async-unmount.test.tsx
   Tests async operation with component unmount mid-execution
✅ Committed: codify: Add async-unmount regression test

Launching pattern-extractor for code...
✅ Created: hooks/useAsyncEffect.ts
   Hook that properly cleans up async operations on unmount
✅ Created: hooks/useAsyncEffect.test.ts (8 tests)
✅ Committed: codify: Extract useAsyncEffect hook for safe async cleanup

Updating documentation...
✅ Updated: REACT.md (Async Patterns section)
   Added: useAsyncEffect usage examples
✅ Committed: codify: Document async cleanup patterns

✅ Codification complete
Prevention: Regression test catches pattern, useAsyncEffect hook simplifies correct usage
```
</details>

<details>
<summary>Example 3: SQL Injection → Security Pattern</summary>

```
✅ Bug resolved: SQL injection vulnerability in search endpoint

Root cause: String concatenation for SQL query instead of parameterized query

Bug pattern detected. Codify to prevent recurrence?
[y] Yes - Analyze and recommend codification targets
[l] Later - Note in debug report for batch codification
[n] No - Skip, one-off issue

> y

Analyzing pattern...

Pattern: SQL Injection Vulnerability (CRITICAL confidence)
Occurrences: 1st time (thankfully)
Impact: CRITICAL (security breach, data loss)

Recommended codifications:
  [✓] Regression test - Test that search rejects injection attempts
  [✓] Agent update - Add to security-sentinel checklist (CRITICAL)
  [✓] Code abstraction - Extract safe query builder utility
  [✓] ESLint rule - Detect string concatenation in SQL contexts
  [✓] Docs - Update SECURITY.md with SQL injection prevention

Proceed with all codifications? [y/N]
> y

Launching pattern-extractor in test mode...
✅ Created: tests/security/sql-injection.test.ts
   Tests various SQL injection attack vectors
✅ Committed: codify: Add SQL injection regression tests

Launching pattern-extractor for code...
✅ Created: lib/db/safe-query.ts
   Utility enforcing parameterized queries only
✅ Created: lib/db/safe-query.test.ts (12 tests)
✅ Committed: codify: Extract safe SQL query utility

Launching agent-updater...
✅ Updated: agents/security-sentinel.md
   Added CRITICAL check: "All SQL queries must use parameterized queries, never string concatenation"
✅ Committed: codify: Add SQL injection check to security-sentinel

Configuring ESLint...
✅ Created: eslint-rules/no-sql-string-concat.js
   Custom rule detecting SQL string concatenation
✅ Updated: .eslintrc.json
✅ Committed: codify: Add ESLint rule for SQL string concatenation

Updating documentation...
✅ Updated: SECURITY.md (SQL Injection Prevention section)
✅ Committed: codify: Document SQL injection prevention patterns

Syncing configs...
✅ Synced to ~/.codex/agents/security-sentinel.md
✅ Synced to ~/.gemini/system-instructions/security-sentinel.txt

✅ Codification complete
Prevention: Multi-layer defense - ESLint (dev), tests (CI), agent (review), safe-query utility (runtime)
```
</details>

**Philosophy**:

Bug patterns are high-value codification targets. A single bug fixed and codified prevents entire classes of future bugs through:
- **Regression tests** - Ensure specific bug never recurs
- **Agent checks** - Catch similar patterns in review
- **Code abstractions** - Make correct usage easier than incorrect
- **ESLint rules** - Catch at development time
- **Documentation** - Educate team on gotchas

**"The best bug fix is a test that fails without the fix."** - Every bug should become a regression test that prevents recurrence forever.

## The Three Laws of Debugging

1. **Start with your code** — It's almost certainly your bug, not the framework's
2. **Check every assumption** — The bug is in the gap between assumption and reality
3. **Read the entire error message** — The answer is usually right there

## Red Flags

- [ ] Guessing instead of measuring
- [ ] Fixing symptoms instead of causes
- [ ] Skipping reproduction (just "try this")
- [ ] Not writing regression tests
- [ ] Leaving instrumentation in code
- [ ] "It works on my machine" without investigating why

## Output Format

```markdown
## Debug Report

**Issue**: [Brief description]
**Status**: [Resolved / Needs Info / Escalated]

---

### Problem Summary
[2-3 sentences explaining the issue]

### Root Cause
**What**: [Specific error]
**Where**: `file.ts:123`
**Why**: [Root cause explanation]

### Investigation Log
1. [Hypothesis → Result]
2. [Hypothesis → Result]
3. [Hypothesis → Result]

### Fix
```[language]
// file.ts:123
// Before: [old code]
// After: [new code]
```

### Regression Test
- Added: `test/regression/bug-123.test.ts`
- Coverage: [What scenarios are tested]

### Prevention
- [ ] [Action to prevent recurrence]

---

**Next**: /execute or /qa-cycle
```

## Philosophy

> **"The best debugger is a fresh pair of eyes and a good night's sleep."**

**Kernighan's insight**: Simple code is debuggable code. If you can't debug it, you wrote it too cleverly.

**Pike's wisdom**: Addition is easy, understanding is hard. Truly fixing a bug means understanding the system well enough to remove the defect.

**Carmack's focus**: Every experiment should shrink the problem space. If it doesn't, you're not learning.

**Your goal**: Understand first, fix second. The minimal fix is always the best fix.

---

*Run this command when investigating bugs. Transform vague reports into precise fixes.*
