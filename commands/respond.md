---
description: Analyze PR review comments, categorize by priority, create action plan
---

Systematically analyze all PR review feedback and comments, categorize them by priority and scope, and create actionable responses for immediate and future work.

## 1. Review Analysis
- **Goal:** Comprehensively evaluate all PR comments and feedback.
- **Actions:**
    - **Collect all feedback types** - GitHub PRs have three distinct comment sources:
        - **Review comments**: Inline code comments attached to specific file lines (where bots like Codex leave suggestions)
        - **Issue comments**: General PR conversation comments
        - **Review summaries**: Top-level review state and summary feedback
        - Use pagination when fetching to ensure no comments are missed on large PRs
    - **Parse bot-generated feedback** - Automated review bots (e.g., Codex, Danger, lint bots) often include:
        - Priority/severity indicators (P0, P1, P2 badges or similar)
        - Structured suggestions with specific line numbers and file paths
        - Links to documentation or standards
        - Extract and respect these priority signals when categorizing
    - **Handle large PRs strategically** - For PRs with >1000 lines changed or >10 comments:
        - First assess scope: count comments by type and priority
        - Group related feedback by file/component
        - Process high-priority/blocking items first to avoid context overflow
        - Consider loading only changed portions of large files rather than full diffs
    - Think critically about each comment's legitimacy, scope, and impact.
    - Assess technical merit, alignment with project goals, and implementation complexity.
    - Consider reviewer expertise and context behind each suggestion.

## 2. Categorize Feedback
- **Goal:** Classify comments into actionable categories based on urgency and scope.
- **Categories:**
    - **Critical/Merge-blocking:** Issues that must be addressed before merge
    - **In-scope improvements:** Enhancements that fit this branch's purpose
    - **Follow-up work:** Valid suggestions for future iterations
    - **Low priority/Not applicable:** Comments that don't warrant immediate action

## 3. Create Action Plans

### Categorization Summary
First, present categorized summary:
- **Critical/Merge-blocking**: {count} items
- **In-scope improvements**: {count} items
- **Follow-up work**: {count} items
- **Low priority/Not applicable**: {count} items

### Parallel Fix Implementation (Critical + In-scope)

For actionable feedback, use parallel pr-comment-resolver agents:

**If 1-3 comments**: Launch Task agents in parallel
```
Task pr-comment-resolver("Comment: Add error handling to payment processing method at PaymentService.ts:45")
Task pr-comment-resolver("Comment: Extract validation logic from UserController to helper at app/controllers/users_controller.rb:120")
Task pr-comment-resolver("Comment: Fix variable naming - rename `data` to `userData` in UserService.ts:78")
```

**If 4+ comments**: Process in batches of 3-5 to avoid overwhelming context
```
# Batch 1: Most critical issues
Task pr-comment-resolver("Comment 1 details")
Task pr-comment-resolver("Comment 2 details")
Task pr-comment-resolver("Comment 3 details")

# Wait for completion, review changes, commit

# Batch 2: Remaining issues
Task pr-comment-resolver("Comment 4 details")
Task pr-comment-resolver("Comment 5 details")
```

**Agent input format**: Pass comment text with file location context
- Include: File path, line number, reviewer's specific request
- Each agent makes changes and reports resolution independently
- Review agent reports before committing

**Manual fallback**: If comment is ambiguous or requires design decision:
- Add to TODO.md as regular task
- Document question/blocker in task details

### For Follow-up Work
- Create GitHub issues for valid suggestions using `gh issue create`
- Include rationale for deferring and link back to original PR comments
- Label appropriately (e.g., `enhancement`, `tech-debt`, `low-priority`)

### For Low Priority/Rejected Feedback
- Document reasoning for not addressing immediately
- Consider: erroneous suggestions, out-of-scope changes, low ROI improvements
- Provide clear justification to inform future discussions

## 4. Document Decisions
- **Goal:** Create transparent record of feedback handling decisions.
- **Actions:**
    - Summarize analysis approach and decision criteria
    - For each comment category, explain rationale and next steps
    - Ensure all feedback is acknowledged and appropriately addressed

## 5. Learning Codification (Feedback Pattern Detection)

After resolving PR feedback, detect recurring patterns that should be enforced automatically.

### Doc-Check First

Run /doc-check to understand existing documentation structure. Codification targets should align with project docs:
- CLAUDE.md for conventions (not new files)
- Existing docs/adr/ folder for decisions
- Existing agent files for enforcement
- Module READMEs for local patterns

### Detect Patterns

**Ask yourself**: Is this feedback recurring? Have I seen this pattern before?

✅ **Codifiable feedback patterns** (worth automating):
- Same feedback given 3+ times across PRs
- Structural pattern enforceable as rule (DRY violations, naming conventions, missing tests, etc.)
- Security/performance/correctness issues that can be detected automatically
- Code quality standards repeatedly mentioned
- Framework-specific best practices violated repeatedly

❌ **Not worth codifying** (one-off or subjective):
- One-time suggestion specific to this PR
- Subjective style preferences without clear rule
- Context-dependent decisions
- Design discussions

**After resolving all feedback, automatically check for patterns**:

Search recent PR history (`gh pr list --state all --limit 20 --json number,reviews`) for similar feedback.

**Codify if**:
- 3+ occurrences of same pattern, OR
- CRITICAL security issue (even 1st occurrence)

Otherwise, complete the PR response cycle silently.

**If pattern detected (3+ occurrences)**:
```bash
Task learning-codifier("Analyze recent PR feedback history and detect recurring patterns worth codifying into automated enforcement")

# Agent will:
# 1. Search PR history for similar feedback (gh pr list + comments)
# 2. Count occurrences of feedback patterns
# 3. Categorize patterns (code quality, testing, security, architecture, naming, etc.)
# 4. Recommend codification targets (agent updates, ESLint rules, pre-commit hooks)
# 5. Launch agent-updater for high-confidence patterns
# 6. Commit with "codify: Automate {pattern} enforcement from PR feedback"
```

**Codification priority for PR feedback**:
1. **Agent Updates** (HIGHEST - catch in /groom before review)
2. **ESLint/Lint Rules** (catch at development time)
3. **Pre-commit Hooks** (block commit if violated)
4. **Tests** (if feedback is about missing test coverage)
5. **Documentation** (if feedback is about missing docs)

**If no pattern detected (<3 occurrences)**:
Complete PR response cycle silently. No prompt needed.

**Examples**:

<details>
<summary>Example 1: "Extract to Helper" (3rd Occurrence) → Agent Update</summary>

```
✅ PR feedback resolved: 5 comments addressed
  - Extract validation logic to helper (UserController.ts:120)
  - Fix naming convention (PaymentService.ts:45)
  - Add error handling (OrderService.ts:89)
  - Add JSDoc comments (ProductService.ts:234)
  - Extract repeated query to helper (ReportController.ts:167)

Checking PR history for recurring patterns...

Searching recent PRs for similar feedback patterns:
  gh pr list --state all --limit 50 --json number,reviews

Pattern detected: "Extract to helper" feedback
  - PR #123: "Extract validation to helper" (UserController)
  - PR #145: "Extract formatting logic to utility" (ReportService)
  - PR #167: "This should be a helper function" (PaymentProcessor)
  - PR #189: "Extract to helper" (UserController + OrderService)
  - **This PR (3rd occurrence this month)**

Pattern: DRY Violations - Repeated logic not extracted (HIGH confidence)
Occurrences: 5 times in last 50 PRs
Impact: HIGH (review time, code maintainability)

Recommended codifications:
  [ ] Code abstraction - Case-by-case, not general
  [ ] Tests - Not applicable
  [ ] Skill - Not applicable
  [ ] Command - Not applicable
  [✓] Agent update - Add to complexity-archaeologist checklist
  [✓] ESLint rule - Configure no-duplicate-code plugins
  [ ] Docs - Already documented in Ousterhout principles

Proceed with agent + eslint? [y/N]
> y

Launching agent-updater...

Which agent should enforce "Extract repeated logic" pattern?
1. complexity-archaeologist (DRY violations, shallow modules)
2. maintainability-maven (code organization, naming)
> 1

✅ Updated: agents/complexity-archaeologist.md
  Added check:
    "- [ ] Repeated logic (>10 lines, appears 2+ times) extracted to helper/utility
     - [ ] Helper functions have clear single responsibility
     - [ ] Helpers are well-named and documented"
✅ Committed: codify: Add DRY violation detection to complexity-archaeologist

Configuring ESLint...
✅ Updated: .eslintrc.json
  Added: sonarjs/no-duplicate-string, sonarjs/no-identical-functions
✅ Committed: codify: Configure ESLint to detect code duplication

Syncing configs...
✅ Synced to ~/.codex/agents/complexity-archaeologist.md
✅ Synced to ~/.gemini/system-instructions/complexity-archaeologist.txt

✅ Codification complete
Prevention: /groom will now catch DRY violations before PR, ESLint catches during dev
Next: This feedback pattern should not recur
```
</details>

<details>
<summary>Example 2: "Add Tests" (3rd Occurrence) → Agent + Hook</summary>

```
✅ PR feedback resolved: 3 comments addressed
  - Add unit tests for PaymentProcessor
  - Add integration tests for OrderFlow
  - Increase coverage to 80%+

Checking PR history for recurring patterns...

Pattern detected: "Add tests" / "Coverage too low" feedback
  - PR #134: "Add tests for authentication flow"
  - PR #156: "Missing unit tests for refactored code"
  - **This PR (3rd occurrence)**

Pattern: Missing Tests (HIGH confidence)
Occurrences: 3 times in last 50 PRs
Impact: HIGH (production bugs, confidence)

Recommended codifications:
  [ ] Code abstraction - Not applicable
  [✓] Tests - Already added in this PR
  [ ] Skill - Not applicable
  [ ] Command - Already have /execute test-first prompt
  [✓] Agent update - Strengthen test-strategy-architect
  [✓] Pre-commit hook - Block commit if patch coverage <80%
  [ ] Docs - Already documented in testing-philosophy

Proceed with agent + hook? [y/N]
> y

Launching agent-updater...
✅ Updated: agents/test-strategy-architect.md
  Strengthened check:
    "- [ ] NEW CODE: Must have 80%+ patch coverage (or explicit justification)
     - [ ] Core logic: Must have unit tests
     - [ ] User flows: Must have integration tests
     - [ ] API endpoints: Must have E2E tests"
✅ Committed: codify: Strengthen test coverage requirements in test-strategy-architect

Configuring git hooks...
✅ Updated: .lefthook.yml
  Added pre-push hook:
    ```yaml
    pre-push:
      commands:
        coverage-check:
          run: pnpm test --coverage --changed
          fail_text: "Patch coverage below 80%. Add tests or use --no-verify with justification."
    ```
✅ Committed: codify: Add patch coverage pre-push hook (80% threshold)

Syncing configs...
✅ Synced to ~/.codex/agents/test-strategy-architect.md

✅ Codification complete
Prevention: Pre-push hook blocks low coverage, /groom enforces in review
Next: Test coverage requirements now enforced automatically
```
</details>

<details>
<summary>Example 3: Security Issue (1st Occurrence) → Immediate Agent Update</summary>

```
✅ PR feedback resolved: 1 critical comment addressed
  - Security: Use parameterized queries, not string concatenation (SearchController.ts:89)

Checking PR history for recurring patterns...

Pattern detected: SQL injection vulnerability pattern
  - **This PR (1st occurrence - CRITICAL)**

Pattern: SQL Injection Vulnerability (CRITICAL confidence despite single occurrence)
Occurrences: 1 time (but CRITICAL severity warrants immediate codification)
Impact: CRITICAL (security breach, data loss)

Recommended codifications:
  [✓] Code abstraction - Safe query builder utility
  [✓] Tests - Security regression tests
  [ ] Skill - Not applicable
  [ ] Command - Not applicable
  [✓] Agent update - Add to security-sentinel (CRITICAL priority)
  [✓] ESLint rule - Detect SQL string concatenation
  [✓] Docs - Update SECURITY.md

Proceed with full codification? [y/N]
> y

Note: Even though this is first occurrence, CRITICAL security issues
warrant immediate codification to prevent future vulnerabilities.

[Same codification flow as debug SQL injection example...]

✅ Codification complete
Prevention: Multi-layer defense prevents SQL injection from ever reaching PR again
```
</details>

**Philosophy**:

PR feedback patterns are the highest-value signal for what to automate. When reviewers repeatedly mention the same issue, it means:
1. The pattern is common enough to recur
2. It's not obvious enough to prevent proactively
3. It wastes reviewer time every time it appears

**"If you say it 3 times, automate it."** - Transform recurring PR feedback into automated enforcement that catches issues before human review.

**The codification loop**:
1. **PR feedback** reveals pattern
2. **Agent update** catches pattern in /groom
3. **ESLint/hooks** catch pattern before commit
4. **Tests** prevent regression
5. **Future PRs** don't have this feedback anymore

This is compounding engineering: each unit of review work improves the system's ability to catch issues automatically, reducing future review burden and increasing code quality baseline.
