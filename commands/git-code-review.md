Comprehensive quality review: cleanup first, then brutal honesty.

# CODE-REVIEW

Two-phase approach: clean up the code, then tear it apart with critical analysis.

## Review Scope

Determine what you're reviewing:
- PR review: `gh pr view` or examine PR URL
- Branch review: `git diff main...HEAD` (or appropriate base)
- Post-task: `git diff HEAD~1` or recent changes
- Note changed files, affected modules, additions/deletions

## Phase 1: Cleanup (Matt Shumer's Rule)

"After completing your goal, clean up the code, remove bloat, and document clearly."

**Remove the obvious problems**:
- Debug statements (console.log, print, fmt.Println, debugger)
- Commented-out code and dead imports
- Inconsistent naming and magic numbers
- Temporary hacks and workarounds
- Missing documentation for complex sections

Make it code you'd be proud to show in a job interview.

## Phase 2: Brutal Honesty (Daniel Jeffries)

"Pretend it's NOT production ready. What did you miss, half-ass, or do wrong? Analyze like Linus on a code review bender."

**Ask yourself**:
- Where's the magical thinking and hallucination?
- What edge cases will explode in production?
- Where did I copy-paste without understanding?
- What assumptions will bite us at 3am?
- What tests would actually prove this works?

**Linus-Level Questions**:
- **Security**: What exposes user data or creates vulnerabilities?
- **Performance**: Where's the O(n²) loop becoming a DoS vulnerability?
- **Error handling**: "It probably won't fail" isn't error handling
- **Testing**: Do tests prove anything or just pass?
- **Architecture**: Is coupling so tight it needs therapy?

## Phase 3: Ousterhout Red Flags

Scan for six complexity red flags:

**1. Information Leakage**: Implementation details visible through interfaces. If changing internals breaks callers, you have leakage. (Example: returning raw DB rows exposes schema to callers)

**2. Temporal Decomposition**: Code organized by execution order (step1, step2), not functionality. Creates change amplification where simple changes require edits across multiple locations.

**3. Over-exposure / Generic Names**: Manager, Util, Helper, Context without domain meaning. Suggests unfocused responsibility, becomes dumping ground.

**4. Pass-through Methods**: Methods only calling another with same signature. Each layer should transform, not just forward.

**5. Configuration Overload**: Dozens of parameters forcing users to understand implementation. Good modules have defaults, hide internal knobs.

**6. Shallow Modules**: Interface complexity ≈ implementation complexity. Module Value = Functionality - Interface Complexity. Low value = shallow abstraction.

For each flag found: explain violation, suggest how to deepen module/hide implementation/simplify interface.

## Phase 4: Principle Compliance

Evaluate against core principles (weighted scoring):

**Simplicity (30%)**:
- Is this the simplest solution or clever when boring would work?
- **Violations**: Premature abstraction, unnecessary complexity, over-engineering
- **Test**: Can you explain it in one sentence? Would a junior understand?

**Explicitness (25%)**:
- Dependencies visible? Side effects obvious? Or hidden state and magic?
- **Violations**: Hidden dependencies, magic behavior, undocumented assumptions
- **Check**: Dependencies in signatures, return types clear, behavior understandable

**Modularity (25%)**:
- Independent components with clear boundaries? Or god classes and tight coupling?
- **Violations**: Mixed concerns, circular dependencies, can't test in isolation
- **Verify**: Single responsibility, loose coupling, high cohesion, clear boundaries

**Maintainability (20%)**:
- Would future you understand this? Or cryptic names and missing docs?
- **Violations**: Poor naming (a, temp, data, thing), no docs for complex logic
- **Future test**: Clear intent, obvious extension points, well-documented

## Phase 5: Technology-Specific Checks

Based on file types changed:

**Type Safety**: TypeScript 'any' without justification? Go errors ignored? Weak typing bypassing compile-time safety?

**Architecture Patterns**:
- **Domain Purity**: Business logic must be infrastructure-free. Flag direct database/HTTP/filesystem calls in domain code.
- **Component Isolation**: Single responsibility, no circular dependencies, testable independently
- **Interface Contracts**: Backward compatibility maintained, breaking changes versioned
- **Dependency Direction**: High-level modules don't depend on low-level details

**Common Violations**:
- Type safety issues (unjustified dynamic types, swallowed exceptions)
- Architecture violations (business logic mixed with infrastructure)
- Dependency problems (circular references, improper layering)
- Testing impediments (tight coupling preventing isolation)
- Performance issues (missing indexes, N+1 queries)

## Categorize & Generate TODOs

### BLOCKERS (Production Risks)
Security vulnerabilities, data loss scenarios, performance issues, breaking changes without migration, unhandled errors crashing everything

### IMPROVEMENTS (Fix Before Merge)
Code that works but makes no sense, missing critical tests, unhandled errors, technical debt accumulating

### POLISH (Nice to Have)
Style issues, better naming, refactoring opportunities

**For each violation, generate specific TODO**:
```markdown
- [ ] [CRITICAL] Handle ignored error in api/handler.go:89
  Principle: Explicitness (silent failures hide problems)
  Problem: Database errors swallowed, data loss risk
  Fix: Add error handling, return to caller or log with context
  Time: 15min
```

## Scoring & Decision

Overall code quality score:
- **90-100**: Exceptional, ready to merge
- **70-89**: Minor improvements needed
- **50-69**: Significant issues before merge
- **Below 50**: Major revision required

Score breakdown:
- Code Quality (25%): Coverage, documentation, error handling
- Principle Compliance (35%): Simplicity, explicitness, modularity, maintainability
- Technology Best Practices (20%): Type safety, architecture, patterns
- Architecture Alignment (20%): Clean architecture, proper layering

**Merge Decision**: BLOCKED or APPROVED with frank explanation of issues and required fixes.

Remember: No sugar-coating. Brutal honesty helps more than false confidence.
