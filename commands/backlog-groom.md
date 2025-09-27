Organize and prioritize BACKLOG.md with quality-focused analysis.

# GROOM

What would a seasoned engineering manager do? Transform chaos into clarity.

## The Priority Principle

*"Perfect is the enemy of good, but broken is the enemy of everything."* - Every Senior Engineer

Prioritize by pain: What's breaking? What's blocking? What's bothering?

## 1. Clean the Backlog

**The Marie Kondo Pass**:
- Read @BACKLOG.md
- Archive completed items
- Delete obsolete wishes
- Group by theme (quality, features, debt, docs)
- Tag with effort (S/M/L) and impact (1-10)

**The Torvalds Test**: "Would I accept a PR for this today?" If no, it stays in backlog.

## 2. Quality-First Analysis

**Channel the Platform Engineer mindset**:

Run quality analysis using the helper agent:
```
Task: "Analyze codebase for quality issues and technical debt. Focus on:
- Security vulnerabilities and risks
- Code complexity and maintainability problems
- Missing tests and documentation gaps
- Performance bottlenecks
- Dependency risks and outdated packages
Generate specific, actionable backlog items with effort estimates."
```

## 3. 🎯 Tenet-Based Technical Debt Evaluation

**Evaluate backlog items against fundamental leyline tenets**:

### Core Tenets to Consider

**Simplicity**: Is the current implementation unnecessarily complex? Look for over-engineered solutions, excessive abstractions, or clever code where boring would work better. Items that restore simplicity often prevent cascading complexity.

**Modularity**: Are components properly isolated with clear boundaries? Identify tightly coupled code, god classes, or modules doing too many things. Fixing modularity issues enables parallel development and easier testing.

**Explicitness**: Is behavior obvious or hidden? Watch for implicit dependencies, magic constants, side effects, or unclear data flow. Making things explicit reduces debugging time and onboarding friction.

**Maintainability**: Would a new developer understand this in six months? Flag cryptic naming, missing documentation, inconsistent patterns, or code that requires archaeology to modify.

### Tenet Violation Impact

When evaluating technical debt, consider which fundamental principles are being violated:
- **High Impact**: Violations that affect system-wide patterns or architectural principles
- **Medium Impact**: Local violations that complicate specific features or modules
- **Low Impact**: Style or convention violations that don't affect functionality

Items that violate multiple tenets or core architectural principles should be prioritized higher, as they tend to generate more technical debt over time.

### 🎯 Technology-Specific Binding Awareness

**Consider technology-specific best practices when evaluating debt**:

Different technologies have their own critical patterns and anti-patterns. When grooming your backlog, consider violations of technology-specific bindings:

**TypeScript/JavaScript**: Look for uses of 'any' without justification, missing type definitions, ignored promise rejections, or direct DOM manipulation in React components. These violations often lead to runtime errors that TypeScript was meant to prevent.

**Go**: Identify ignored errors (the underscore pattern), missing context propagation, goroutine leaks, or improper mutex usage. Go's explicit error handling philosophy means ignored errors often hide critical failures.

**Python**: Watch for missing type hints in public APIs, bare except clauses that swallow errors, or mutable default arguments. These Python-specific issues create debugging nightmares.

**SQL/Database**: Flag missing indexes on foreign keys, SELECT * in production queries, or non-idempotent migrations. Database issues compound quickly under load.

**Security Bindings**: Regardless of technology, prioritize items involving authentication, authorization, data validation, or secret management. Security debt is technical debt with external consequences.

When a backlog item violates both a fundamental tenet AND a technology-specific binding, it deserves higher priority. For example, a Go service that both ignores errors (binding violation) AND has unclear module boundaries (tenet violation) is accumulating debt from multiple directions.

## 4. Stack Rank by Value

**The Bezos Question**: "Will this matter to users in 6 months?"

Priority order:
1. **CRITICAL**: Security/data loss risks, fundamental tenet violations affecting system stability
2. **HIGH**: User-facing bugs, performance issues, architectural principle violations
3. **MEDIUM**: Developer experience, maintainability, local tenet violations
4. **LOW**: Nice-to-haves, optimizations, minor convention violations

**Tenet-Aware Prioritization**:
Items that violate core tenets (simplicity, modularity, explicitness) early in the stack often create compounding technical debt. Prioritize fixing fundamental violations even if they're not immediately user-facing - they affect your ability to deliver everything else.

### 🎯 Remediation Strategy Guidance

**Describe how to fix issues based on tenet violations**:

When creating backlog items, include clear remediation strategies based on which principles are being violated:

**Simplicity Violations - The Path to Boring**:
For over-engineered code, the fix usually involves removing layers, not adding them. Replace clever abstractions with straightforward implementations. Convert configuration into constants if values never change. Replace factories with direct instantiation when there's only one type. The remediation is often deletion - remove the abstraction and inline the logic.

**Modularity Violations - Creating Clear Boundaries**:
For tightly coupled code, identify the seams where modules should separate. Extract god classes into focused components with single responsibilities. Define clear interfaces between modules. Move shared state into explicit dependencies. The fix involves drawing boundaries and moving code to respect them.

**Explicitness Violations - Making the Implicit Obvious**:
For hidden behavior, surface dependencies in function signatures. Replace magic numbers with named constants. Convert side effects into return values. Document assumptions that can't be made explicit in code. The remediation makes invisible behavior visible.

**Maintainability Violations - Writing for Future You**:
For cryptic code, rename variables and functions to describe intent. Extract complex conditionals into well-named functions. Add documentation for non-obvious decisions. Establish consistent patterns within modules. The fix makes code self-documenting.

**Multiple Violation Remediation**:
When an item violates multiple tenets, address them in order: simplicity first (remove unnecessary complexity), then modularity (establish boundaries), then explicitness (surface behavior), and finally maintainability (polish for clarity). This order prevents fixing symptoms while core issues remain.

Include these remediation approaches in backlog items so developers know not just what's wrong, but how to approach fixing it.

## 5. Output Format

```markdown
# BACKLOG.md

## Critical [Fix This Week]
- [L] Fix SQL injection in user input (Security)
- [S] Add rate limiting to API (Security)

## High Priority [This Sprint]
- [M] Reduce homepage load time >2s (Performance)
- [S] Fix flaky payment tests (Quality)

## Medium Priority [This Quarter]
- [L] Refactor authentication module (Tech Debt)
- [M] Add integration test suite (Quality)

## Low Priority [Someday]
- [S] Dark mode support (Feature)
- [S] Optimize bundle size (Performance)

## Archived
- ✅ Implemented user authentication
- ❌ WebSocket support (no longer needed)
```

## Success Metrics

- Every item has clear effort (S/M/L) and category
- Top 5 items could start tomorrow
- No vague wishes like "improve performance"
- Archived section prevents backlog bloat

Remember: **A groomed backlog is a usable backlog. Everything else is wishful thinking.**