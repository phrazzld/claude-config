Conduct comprehensive multi-perspective codebase analysis to identify improvement opportunities across all quality dimensions.

# GROOM

Step back and see the whole system through six expert perspectives. What would make this better?

## The Multi-Perspective Discovery Principle

*"The best problems to solve are the ones you find, not the ones you're given."*

Look for opportunities, not just problems. Different perspectives reveal different truths. Complexity archaeologists find different issues than security sentinels. Architecture guardians see what performance pathfinders miss.

By analyzing the codebase through multiple specialized lenses — each embodying specific Ousterhout principles and Leyline tenets — we discover the issues that truly matter.

## Phase 1: Preparation

### 1. Clean the Slate

First, refresh existing BACKLOG.md. Remove noise, keep signal:
- Move completed items to "Completed / Archived" section at bottom
- Remove obsolete tasks (would you work on this next quarter?)
- Consolidate duplicate or related items
- Keep everything in one unified BACKLOG.md — no separate archive files

This creates a clean foundation for comprehensive analysis.

### 2. Understand Current Context

Before launching the audit:
- Check BACKLOG.md and PLAN.md for known issues
- Review recent commits for areas of active change
- Note any ongoing refactoring or migrations
- Identify critical vs exploratory code areas

## Phase 2: Parallel Multi-Perspective Audit

Launch six specialized subagents concurrently. Each brings unique expertise and hunts different categories of issues:

### The Six Perspectives

**1. complexity-archaeologist** (Ousterhout Red Flags + Simplicity)
- Shallow module detection (functionality ≈ interface complexity)
- Information leakage through abstractions
- Pass-through methods adding no value
- Temporal decomposition (organized by execution order)
- Manager/Util/Helper anti-patterns
- Configuration overload
- Strategic vs tactical debt mapping

**2. architecture-guardian** (Modularity + Explicitness)
- Single responsibility violations
- Tight coupling analysis
- Dependency direction validation (high→low only)
- Circular dependency detection
- God object identification
- Interface quality assessment
- Module boundary violations

**3. security-sentinel** (Security Bindings + OWASP)
- Authentication & authorization gaps
- Input validation & injection vulnerabilities
- Secret & credential exposure
- Error handling security (info disclosure)
- Weak cryptography patterns
- Access control issues (IDOR, privilege escalation)
- Dependency vulnerabilities

**4. performance-pathfinder** (Performance + Efficiency)
- Algorithmic complexity issues (O(n²) traps)
- Database query optimization (N+1 queries, missing indexes)
- Frontend performance (bundle size, re-renders)
- Memory leaks & resource management
- Network & I/O optimization
- Asset optimization opportunities

**5. maintainability-maven** (Maintainability Tenet)
- Naming quality (unclear, misleading, inconsistent)
- Documentation gaps (missing "why", stale docs, no contracts)
- Test coverage analysis
- Code consistency (error handling, async patterns, structure)
- Comprehension barriers (complex conditionals, magic numbers)
- Technical debt documentation

**6. user-experience-advocate** (Product Value First)
- Error message quality
- User friction points (loading states, confusing flows)
- Accessibility issues (WCAG compliance)
- Missing high-value features
- Data loss prevention
- Performance as UX
- Empty states

### Launch Protocol

Use Task tool to run all 6 agents in parallel:

```markdown
Launching parallel codebase audit with 6 specialized perspectives...

Task 1: complexity-archaeologist
"Analyze the codebase for Ousterhout red flags and complexity patterns.
Hunt for: shallow modules, information leakage, pass-through methods, temporal decomposition, generic names (Manager/Util/Helper), configuration overload.
Map tactical debt → strategic refactoring opportunities.
Return: Prioritized findings with file:line, principle violated, remediation, effort+impact."

Task 2: architecture-guardian
"Analyze the codebase for modularity and architectural quality.
Hunt for: responsibility violations, tight coupling, dependency inversions, circular dependencies, god objects, poor interfaces, boundary violations.
Return: Prioritized findings with coupling/cohesion metrics, concrete fixes, effort+impact."

Task 3: security-sentinel
"Analyze the codebase for security vulnerabilities and defensive coding gaps.
Hunt for: auth/authz issues, injection vulnerabilities, secret exposure, weak crypto, access control bugs, dependency CVEs.
Cover OWASP Top 10.
Return: Prioritized findings with severity, attack scenario, remediation, effort+risk."

Task 4: performance-pathfinder
"Analyze the codebase for performance bottlenecks and optimization opportunities.
Hunt for: algorithmic inefficiencies (O(n²)), N+1 queries, missing indexes, bundle bloat, memory leaks, inefficient I/O.
Focus on user-facing impact only.
Return: Prioritized findings with current metrics, user impact, optimization, effort+speedup."

Task 5: maintainability-maven
"Analyze the codebase for maintainability issues and comprehension barriers.
Hunt for: poor naming, missing documentation, test gaps, inconsistent patterns, complex logic, undocumented debt.
Return: Prioritized findings with developer impact, concrete improvements, effort+benefit."

Task 6: user-experience-advocate
"Analyze the codebase from user perspective for UX issues and product gaps.
Hunt for: poor error messages, friction points, accessibility issues, missing features, data loss risks, performance UX.
Return: Prioritized findings with user impact, improved experience, effort+value."
```

Run all 6 in single invocation for true parallelism.

## Phase 3: Synthesis & Cross-Validation

### 1. Collect & Merge Findings

When all agents return, collect their findings:
- Group issues by file/module
- Identify issues flagged by multiple perspectives (high priority signal)
- Note principle violations (which tenets/bindings affected)
- Calculate aggregate impact scores

### 2. Cross-Validation Signals

**Critical Priority** — Issues flagged by 3+ agents:
- Indicates fundamental design problem affecting multiple quality dimensions
- Example: God object flagged by complexity-archaeologist (shallow module) + architecture-guardian (responsibility violation) + maintainability-maven (comprehension barrier)

**High Priority** — Issues flagged by 2 agents:
- Multiple quality dimensions affected
- Example: Poor error handling flagged by security-sentinel (info disclosure) + user-experience-advocate (user confusion)

**Specialized** — Issues flagged by 1 agent:
- Domain-specific concern
- Still important, but narrower impact

### 3. Principle Mapping

For each issue, document which principles violated:
- **Ousterhout**: Shallow module, information leakage, pass-through, temporal decomp, generic naming, config overload
- **Leyline Tenets**: Simplicity, Modularity, Explicitness, Maintainability, etc.
- **Bindings**: Specific implementation standards

This creates traceability from issue → principle → fix rationale.

## Phase 4: Prioritization

Organize findings into clear priority tiers:

### Immediate Concerns (Fix Now)
- Security vulnerabilities (CRITICAL/HIGH severity)
- Data loss scenarios
- Broken core functionality
- Performance issues causing >1s user-facing latency
- Accessibility blockers

**Criteria**: User-facing impact + risk severity

### High-Value Improvements (Fix Soon)
- Architectural issues blocking future development
- God objects and tight coupling in core modules
- Missing tests for financial/critical logic
- Significant UX friction (confusing workflows, poor errors)
- Performance improvements saving >100ms

**Criteria**: Developer velocity + user experience improvement

### Technical Debt Worth Paying (Schedule)
- Complexity patterns compounding over time
- Maintainability issues slowing development
- Shallow modules that should be deepened
- Inconsistent patterns across codebase
- Missing documentation on complex logic

**Criteria**: Long-term velocity + code health

### Nice to Have (Opportunistic)
- Minor naming improvements
- Additional test coverage in stable code
- Performance micro-optimizations
- UX polish

**Criteria**: Low effort + positive impact when touching that code anyway

## Phase 5: Backlog Update

Update the ONE consolidated BACKLOG.md file. No archive files, no document clutter — everything lives here:

```markdown
# BACKLOG.md

Last groomed: [DATE]
Analyzed by: 6 specialized perspectives

## Immediate Concerns

### [Security] SQL Injection in Order Search
**File**: api/orders.ts:89
**Perspectives**: security-sentinel
**Severity**: CRITICAL
**Impact**: Database compromise, data exfiltration possible
**Violation**: Input validation gap
**Fix**: Use parameterized query: `db.query('SELECT * FROM orders WHERE id = $1', [id])`
**Effort**: 5m | **Risk**: CRITICAL

[... more immediate concerns]

## High-Value Improvements

### [Architecture] UserManager God Object
**File**: services/UserManager.ts:1-847
**Perspectives**: complexity-archaeologist, architecture-guardian, maintainability-maven
**Impact**: Blocks feature development, hard to test, maintenance bottleneck
**Violations**:
- Ousterhout: God object with 28 methods
- Modularity: 5+ responsibilities (auth, profile, permissions, notifications, analytics)
- Maintainability: 847 lines, comprehension barrier
**Fix**: Extract UserAuth, UserProfile, UserPermissions, UserNotifier, UserAnalytics
**Effort**: 8h | **Impact**: 847 lines → 5 focused 150-line modules

[... more high-value improvements]

## Technical Debt Worth Paying

### [Complexity] Payment Processing Temporal Decomposition
**File**: payment/workflow.ts:23-156
**Perspectives**: complexity-archaeologist
**Impact**: Change amplification — small changes require edits across many locations
**Violation**: Ousterhout temporal decomposition (organized by execution order)
**Fix**: Reorganize by functionality (validation, transformation, persistence)
**Effort**: 3h | **Impact**: Reduces change amplification

[... more technical debt]

## Nice to Have

### [Maintainability] Improve Variable Naming in Parser
**File**: utils/parser.ts:45
**Perspectives**: maintainability-maven
**Impact**: Minor comprehension barrier
**Fix**: Rename `data` → `rawOrders`, `result` → `validatedOrders`, `temp` → `enrichedOrders`
**Effort**: 10m | **Impact**: Clear data flow

[... more nice-to-haves]

## Completed / Archived
[Completed items stay here - keep most recent ~10-20 for context, prune older ones]
[Track what's been done and decisions made]
```

### Format Requirements

Each backlog item must include:
1. **Category** in brackets: [Security], [Architecture], [Performance], [Maintainability], [UX], [Complexity]
2. **Title**: Clear, specific description
3. **File**: Precise file:line reference
4. **Perspectives**: Which agents flagged this (multi-agent = higher priority)
5. **Impact**: User/developer effect
6. **Violations**: Specific principles/tenets violated
7. **Fix**: Concrete remediation approach
8. **Effort + Impact/Risk/Benefit**: Time estimate + outcome

## Success Criteria

You've groomed well if:

✅ **Single Source of Truth**: All backlog items in ONE consolidated BACKLOG.md — no archive files
✅ **Comprehensive Coverage**: All 6 perspectives analyzed the codebase
✅ **Actionable Items**: Every item has file:line + concrete fix approach
✅ **Clear Priorities**: Most important issues obvious from organization
✅ **Principle Traceability**: Each issue links to violated principles
✅ **Cross-Validation**: Multi-agent issues surfaced and prioritized
✅ **Balanced Mix**: Quick wins + strategic improvements + critical fixes
✅ **Real Needs**: Reflects actual user and developer pain, not theoretical concerns

The backlog should feel like a strategic map of opportunities, energizing the team about what's possible.

## Philosophy

> "Six perspectives see what one cannot. Complexity hides from single viewpoints but reveals itself under multiple lenses."

Each specialized agent embodies different wisdom:
- **Complexity archaeologist**: Ousterhout's depth philosophy
- **Architecture guardian**: Modularity and clean architecture
- **Security sentinel**: Defensive programming and OWASP
- **Performance pathfinder**: User-facing speed and efficiency
- **Maintainability maven**: Code for humans, not machines
- **User experience advocate**: Product value above all

Together, they see the whole system.

---

*Run this command periodically (monthly/quarterly) to maintain codebase health and discover strategic improvement opportunities.*
