---
description: Execute the next task from TODO.md with direct tactical focus
---

Execute the next task directly.

# EXECUTE

> **STEVE JOBS CRAFT REMINDER**
> - Think Different: if rote implementation drifts from intent, pause and re-evaluate.
> - Obsess Over Details: names, tests, error messages should feel inevitable.
> - Plan Like Da Vinci: visualize end state before touching code.
> - Craft, Don't Code: every function should "sing"—clear purpose, zero leaks.
> - Iterate Relentlessly: spike, measure, refine before committing.
> - Simplify Ruthlessly: delete anything not required for the win condition.

You're executing in a workflow that's successfully shipped 23 features this quarter with zero production incidents. The senior engineer reviewing your commits tomorrow values atomic changes, clear reasoning, and zero shortcuts. Every task you complete removes a blocker for 3 downstream developers. Channel Carmack: direct implementation, immediate refactoring, always shippable.

Grab next task → Implement → Commit → Mark complete

## Your Mission

Execute the next available task in TODO.md. The decision to work on this task has already been made during planning. Your job: carry it out skillfully.

## Process

**1. Find next task**: Read TODO.md, locate first `[~]` (in-progress) or `[ ]` (pending)

Batch tiny tasks (typo fix, rename, import): Execute consecutively, one commit.
Single substantial task: Execute it.

**2. Does task need research first?**

Ask: **"Am I familiar with the domain/patterns/tools required?"**

❓ Need research if:
- Implementing with unfamiliar framework/library
- Uncertain about current best practices
- Dealing with errors that need web research
- Evaluating multiple technical approaches

❓ YES, need research → Run `/research [topic]` to leverage Gemini's web grounding, then proceed
✅ NO, ready to implement → Proceed to step 3

**3. Is task specific enough?**

Ask only: **"Do I know exactly what to do?"**

✅ Specific enough if task has:
- File locations OR clear scope
- Approach OR pattern to follow
- Success criteria

✅ YES → Proceed to step 4
🔍 NO → Run /flesh to make it specific, then proceed to step 4

**4. Test-First Check**:

For non-trivial tasks (>20 lines, core logic, new features):

Ask: **"Do tests exist for this?"**
- Check for `*.test.ts`, `*.spec.ts` files for this module
- If YES → Proceed to step 5 (Implementation)
- If NO → Prompt:

  ```
  This task likely needs tests. Write tests first?
  [y] Yes, write tests now (TDD)
  [n] No, prototype first then add tests
  [s] Skip - not needed for this task
  ```

**If TDD (y)**:
1. Generate test list from task description
2. Write failing tests for first scenario
3. Implement to make tests pass
4. Refactor while keeping tests green
5. Commit tests separately: `test: add tests for [feature]`
6. Commit implementation: `feat: implement [feature]`

**If prototype-first (n)**:
1. Implement feature quickly
2. After proving approach, add tests
3. Commit together: `feat: add [feature] with tests`

**If skip (s)**:
- Trivial changes only (typo fixes, renaming, simple refactors)
- Document why skipped in commit or work log

**4. Mark in-progress**: Update `[ ]` → `[~]`

**5. Implement**

Read DESIGN.md for architectural guidance—the "how" is decided. Follow the module design, implement the pseudocode, match the interfaces. Your job: clean implementation of the planned architecture.

**Architecture blueprint** (from DESIGN.md):
- Module interfaces (match these exactly)
- Pseudocode algorithms (translate to real code)
- Data structures (use these types)
- Error handling strategy (follow this approach)
- Integration points (connect as specified)

**Apply principles while coding**:
- **Simplicity**: Prefer boring over clever. Aim for one-sentence explanations.
- **Maintainability**: Choose names that reveal purpose. Document "why" over "what".
- **Explicitness**: Make dependencies visible in signatures. Make side effects obvious from names.
- **Follow the blueprint**: Implement the architecture, don't redesign it.

**Check implementation quality**:
- Matches DESIGN.md? (Interface, behavior, error handling)
- Deep module? (Simple interface hiding powerful implementation)
- Information hiding intact? (Changing internals preserves caller code)
- Minimal complexity? (Few dependencies, clear behavior)
- Red flags absent? (Generic names, pass-through methods, temporal decomposition)

**6. Coverage Check** (if tests were added/modified):

Run locally:
```bash
pnpm test -- --coverage --changed
```

Check patch coverage for files you changed:
- If <80% → Add tests for critical uncovered paths
- If 80%+ → Proceed to commit

Note: Full coverage report will appear in PR automatically via GitHub Actions.

**7. Post-Implementation Quality Review**

Before committing, apply relevant skills and quality checks based on what you implemented:

**A. Load Relevant Skills (Conditional)**

Based on file types modified, explicitly load applicable skills:

```bash
# Frontend files (.tsx, .jsx, .vue, .svelte, .css, .scss)
→ Load: frontend-design, aesthetic-philosophy skills
→ Check: Typography, colors, animations, layout patterns, generic AI aesthetics

# Test files (*.test.*, *.spec.*, __tests__/*)
→ Load: testing-philosophy skill
→ Check: Test behavior not implementation, AAA structure, minimal mocks

# Documentation (*.md, docs/*, README.*)
→ Load: documentation-standards skill
→ Check: Why over what, minimal comments, maintained README

# Database/Schema (migrations/*, schema.*, models/*)
→ Load: schema-design skill
→ Check: Normalization, constraints, data types, indexes

# Infrastructure files (lefthook.yml, .github/workflows/*, utils/logger.ts, **/sentry.*)
→ Load: quality-gates, structured-logging, changelog-automation skills (as applicable)
→ Check: Quality gate completeness, logging patterns, version automation, error tracking setup

# Design system files (globals.css with @theme, tailwind.config.*)
→ Load: design-tokens, frontend-design skills
→ Check: Semantic token naming, OKLCH colors, typography scales, brand consistency

# Toolchain files (mobile/*, extension/*, cli/*)
→ Load: mobile-toolchain, extension-toolchain, cli-toolchain skills (as applicable)
→ Check: Framework best practices, manifest configuration, testing setup

# General code quality (all files)
→ Load: naming-conventions skill
→ Check: Intention-revealing names, domain language, verb+noun functions
```

**B. Simplicity Review**

Always run code-simplicity-reviewer to catch overcomplexity:

```
Task code-simplicity-reviewer("Review changes for simplification opportunities")
```

Review findings:
- **Trivial simplifications** (rename, extract small helper): Apply immediately
- **Substantial refactoring** (rethink approach): Add to task work log, address if time permits or note for future
- **No issues**: Proceed to commit

**C. Skill-Specific Quality Checks**

If skills were loaded, perform domain-specific validation:

**Frontend code**:
- Typography: Distinctive fonts? Or Inter/Roboto defaults?
- Colors: Cohesive palette? Or scattered hex codes?
- Animations: Purposeful motion? Or generic transitions?
- Layout: Visual interest? Or predictable grids?

**Tests**:
- Behavior tests? Or implementation details?
- Minimal mocks? Or heavy stubbing?
- Clear AAA structure? Or obscure test logic?

**Documentation**:
- Why documented? Or just what?
- Minimal comments? Or excessive noise?
- Up-to-date? Or stale references?

**Schema**:
- Proper normalization? Or data duplication?
- Constraints enforced? Or application-level only?
- Appropriate indexes? Or missing performance optimizations?

**Infrastructure (Quality Gates)**:
- Pre-commit hooks configured? (lint, format, typecheck)
- Pre-push tests running? Or skippable?
- CI/CD pipeline complete? Or missing steps?
- Branch protection enabled? Or direct main pushes allowed?

**Infrastructure (Logging)**:
- Structured JSON logging? Or console.log?
- Correlation IDs for request tracing? Or isolated logs?
- Sensitive data redacted? (passwords, tokens, PII)
- Log levels appropriate? (info/warn/error, not all debug)

**Infrastructure (Design Tokens)**:
- Semantic naming? (--color-primary) Or descriptive? (--color-blue-500)
- OKLCH colors for perceptual uniformity? Or hex codes?
- Design tokens in @theme? Or JavaScript config?
- Typography scales defined? Or magic numbers?

**Infrastructure (Changelog)**:
- Changesets created for changes? Or manual changelog?
- Conventional commit format? Or arbitrary messages?
- Version bump strategy clear? (MAJOR.MINOR.PATCH)
- Release automation configured? Or manual process?

This enforces "leave code better than you found it" while context is fresh and skills provide expert guidance.

**8. Commit atomically**

Every completed task → atomic commit with clear message.
Types: feat|fix|docs|refactor|test|chore

**9. Mark complete**: Update `[~]` → `[x]`

**10. Continue or stop**: Proceed to next task when appropriate, or report completion.

## Execute Regardless Of

**Execute when task is specific, regardless of:**
- Task complexity (simple or complex)
- Time estimates (15 minutes or 3 hours)
- Session duration (first task or tenth task)
- Implementation challenge (straightforward or intricate)
- Task scope (focused or comprehensive)

**These concerns were addressed upstream**:
- Complexity → Handled in /plan (appropriate breakdown)
- Risk → Handled in /flesh (clear approach)
- Size → Handled in /plan (proper scoping)

**Valid reasons to pause**:
- ✅ Task blocked by missing dependency requiring user input
- ✅ Environment broken (build fails, tests unavailable, fundamental tool failure)
- ✅ Task remains unclear even after /flesh
- ✅ User explicitly requests pause

## The Contract

By the time you run /execute, the decision to do this work **has been made**. That decision happened during:
- `/plan` - Breaking work into appropriate tasks
- `/flesh` - Understanding scope and approach
- User running `/execute` - Choosing to proceed

**Your responsibility**: Carry out that decision skillfully.

**Your focus**: How to implement (quality, simplicity, maintainability), rather than whether to implement.

## Handling Complex Tasks

**Ineffective approach**: Refuse to execute due to perceived complexity.

**Effective approach**:
1. Task genuinely unclear → Run /flesh to clarify
2. Task clear but substantial → Execute it (this is the job)
3. Discover task merits splitting → Add work log noting this for future planning

**Key insight**: Complex tasks are normal in software engineering. Your role: handle them capably.

## Work Logs

For substantial tasks, document discoveries as you go:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found auth pattern in services/auth.ts
  - Using JWT approach from api/middleware
  - Preserved existing session handling
  ```
```

Work logs capture discoveries, decisions, learnings for continuity.

## The Carmack Rule

**"A task without a commit is a task that's still pending."**

Every completed task results in an atomic commit. This is the definition of "done".

---

**Remember**: Execute is tactical. Strategic thinking happens upstream in plan/flesh. Your job: implement with quality, commit changes, mark complete. Repeat for next task.
