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

## 4. Stack Rank by Value

**The Bezos Question**: "Will this matter to users in 6 months?"

Priority order:
1. **CRITICAL**: Security/data loss risks, fundamental tenet violations affecting system stability
2. **HIGH**: User-facing bugs, performance issues, architectural principle violations
3. **MEDIUM**: Developer experience, maintainability, local tenet violations
4. **LOW**: Nice-to-haves, optimizations, minor convention violations

**Tenet-Aware Prioritization**:
Items that violate core tenets (simplicity, modularity, explicitness) early in the stack often create compounding technical debt. Prioritize fixing fundamental violations even if they're not immediately user-facing - they affect your ability to deliver everything else.

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