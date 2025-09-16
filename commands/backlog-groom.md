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

## 3. Stack Rank by Value

**The Bezos Question**: "Will this matter to users in 6 months?"

Priority order:
1. **CRITICAL**: Security/data loss risks
2. **HIGH**: User-facing bugs and performance issues
3. **MEDIUM**: Developer experience and maintainability
4. **LOW**: Nice-to-haves and optimizations

## 4. Output Format

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