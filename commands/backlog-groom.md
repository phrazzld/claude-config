Conduct comprehensive multi-perspective codebase analysis to identify improvement opportunities across all quality dimensions.

# GROOM

Step back and see the whole system through seven expert perspectives. What would make this better?

## The Multi-Perspective Discovery Principle

*"The best problems to solve are the ones you find, not the ones you're given."*

Look for opportunities, not just problems. Different perspectives reveal different truths. Complexity archaeologists find different issues than security sentinels. Architecture guardians see what performance pathfinders miss. Product visionaries see value creation opportunities that quality-focused agents overlook.

By analyzing the codebase through multiple specialized lenses — each embodying specific Ousterhout principles and Leyline tenets — we discover both the issues that truly matter AND the opportunities that create value.

## Phase 1: Preparation

### 1. Curate Ruthlessly

The backlog is strategic intent, not historical record. Approach it like a genius product leader:

**Kill without mercy:**
- Completed work belongs in git history and release notes, not BACKLOG.md
- Remove anything you wouldn't realistically tackle in next 6 months
- Delete duplicates, merge related items, eliminate noise
- Ask: "Would future me actually prioritize this?" No = delete

**The backlog shows where you're going, not where you've been.**

### 2. Understand Current Context

Before launching the audit:
- Review BACKLOG.md and PLAN.md for known issues
- Check recent commits for areas of active change
- Note ongoing refactoring or migrations
- Identify critical vs exploratory code areas

## Phase 2: Parallel Multi-Perspective Audit

Launch eight specialized subagents concurrently. Each brings unique expertise and hunts different categories of issues:

### The Eight Perspectives

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
- Secret & credential exposure (git-tracked = CRITICAL, gitignored = LOW)
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

**7. product-visionary** (Feature Value + Market Opportunity)
- Missing core features preventing adoption
- Competitive feature gaps (table stakes vs differentiation)
- Workflow enhancement opportunities (10x improvements, not 10%)
- Monetization and premium features (revenue enablers)
- Integration and ecosystem plays (network effects)
- Innovation and differentiation opportunities (why choose this?)
- Vertical-specific customization (market expansion)
- Platform expansion possibilities (strategic bets)
- **Apply 80/20**: Which 20% of features drive 80% of value?

**8. design-systems-architect** (Design Systems + UI Consistency + Component Architecture)
- Design token system gaps (hardcoded values vs tokens)
- Component architecture issues (duplication, poor composition, shallow modules)
- Visual consistency (typography, spacing, color, layout patterns)
- UI state patterns (loading states, forms, data fetching inconsistencies)
- Frontend tooling (component docs, testing, CSS architecture)
- Reusable component opportunities
- Design system infrastructure

### Launch Protocol

Use Task tool to run all 8 agents in parallel:

**IMPORTANT**: All agents must exclude gitignored content (node_modules, dist, build, .next, vendor, etc.) when searching. Only analyze source code under version control.

```markdown
Launching parallel codebase audit with 7 specialized perspectives...

Task 1: complexity-archaeologist
"Analyze the codebase for Ousterhout red flags and complexity patterns.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: shallow modules, information leakage, pass-through methods, temporal decomposition, generic names (Manager/Util/Helper), configuration overload.
Map tactical debt → strategic refactoring opportunities.
Return: Prioritized findings with file:line, principle violated, remediation, effort+impact."

Task 2: architecture-guardian
"Analyze the codebase for modularity and architectural quality.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: responsibility violations, tight coupling, dependency inversions, circular dependencies, god objects, poor interfaces, boundary violations.
Return: Prioritized findings with coupling/cohesion metrics, concrete fixes, effort+impact."

Task 3: security-sentinel
"Analyze the codebase for security vulnerabilities and defensive coding gaps.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: auth/authz issues, injection vulnerabilities, secret exposure IN GIT-TRACKED FILES (verify with git ls-files), weak crypto, access control bugs, dependency CVEs.
For secrets in gitignored files (.env, .env.local, etc.): Flag as LOW priority defense-in-depth reminder only, NOT critical vulnerabilities.
Cover OWASP Top 10.
Return: Prioritized findings with severity (CRITICAL only for tracked secrets), attack scenario, remediation, effort+risk."

Task 4: performance-pathfinder
"Analyze the codebase for performance bottlenecks and optimization opportunities.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: algorithmic inefficiencies (O(n²)), N+1 queries, missing indexes, bundle bloat, memory leaks, inefficient I/O.
Focus on user-facing impact only.
Return: Prioritized findings with current metrics, user impact, optimization, effort+speedup."

Task 5: maintainability-maven
"Analyze the codebase for maintainability issues and comprehension barriers.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: poor naming, missing documentation, test gaps, inconsistent patterns, complex logic, undocumented debt.
Return: Prioritized findings with developer impact, concrete improvements, effort+benefit."

Task 6: user-experience-advocate
"Analyze the codebase from user perspective for UX issues and product gaps.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: poor error messages, friction points, accessibility issues, missing features, data loss risks, performance UX.
Return: Prioritized findings with user impact, improved experience, effort+value."

Task 7: product-visionary
"Analyze the product for feature opportunities and market gaps.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
Hunt for: missing core features, competitive gaps, workflow enhancements, monetization opportunities, integration plays, differentiation potential, vertical customization, platform expansion.
Apply 80/20 ruthlessly: which 20% of potential features would drive 80% of adoption/retention/revenue?
Focus on what would make users choose and stick with this product beyond just code quality.
Require business justification: adoption driver? retention hook? revenue enabler? competitive gap? workflow unlock?
Return: Prioritized opportunities with market analysis, user value, competitive impact, business case, effort+strategic value."

Task 8: design-systems-architect
"Analyze the frontend for design systems, UI consistency, and component architecture.
EXCLUDE: node_modules, dist, build, .next, vendor, and all gitignored directories.
First: Detect stack from package.json (React/Vue/Svelte, Tailwind/CSS-in-JS, component libraries). Adapt analysis to the stack present.
Hunt for: hardcoded values vs design tokens, component duplication and shallow modules, typography/spacing/color inconsistencies, UI state pattern variations (loading, forms, data fetching), frontend tooling gaps (docs, tests, CSS architecture).
Apply Ousterhout principles: Identify shallow component modules where interface ≈ implementation.
Focus on reusability opportunities, visual consistency, and component composition patterns.
Return: Prioritized findings with stack context, pattern prevalence, refactoring opportunities, effort+impact, migration strategies."
```

Run all 8 in single invocation for true parallelism.

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

Think like a CEO allocating scarce resources. Organize by time horizon and strategic value:

### Now (Sprint-Ready, <2 weeks)
**Unblocked, high-confidence, immediate impact:**
- Security vulnerabilities (CRITICAL/HIGH)
- Data loss scenarios / broken core functionality
- User-facing performance issues (>1s latency)
- High-value features with clear ROI (adoption/retention/revenue)
- Architectural blockers preventing current development

**Require:** file:line, effort estimate, acceptance criteria
**Ask:** "If we only shipped 3 things this month, would this make the list?"

### Next (This Quarter, <3 months)
**Directionally clear, needs refinement:**
- Strategic refactoring that unlocks velocity
- High-impact UX improvements
- Feature opportunities with strong business case
- Technical debt compounding over time
- Performance improvements (>100ms saves)

**Require:** Approach, rough sizing, dependencies
**Ask:** "Does this meaningfully improve our competitive position or development speed?"

### Soon (Exploring, 3-6 months)
**Worth validating, dependency-blocked, or needs design:**
- Ambitious architectural improvements
- Feature ideas requiring user research
- Performance optimizations with unclear ROI
- Maintainability improvements in stable code
- Experimental differentiation plays

**Require:** One-liner sufficient, optional detail
**Ask:** "Is this still compelling if we revisit in 3 months?"

### Later (Someday/Maybe, 6+ months)
**Interesting but not urgent, capture for future consideration:**
- Platform expansion ideas
- Vertical-specific customizations
- Innovation experiments
- Low-priority polish

**Require:** Title only, delete freely on next groom
**Ask:** "Does keeping this idea spark genuine excitement?"

**Apply 80/20 ruthlessly**: Which 20% of items drive 80% of value? Emphasize those, prune the rest.

## Phase 5: Backlog Update

Craft a forward-looking strategic roadmap. Detail matches proximity — rich specs for Now, light bullets for Later:

```markdown
# BACKLOG.md

Last groomed: [DATE]
Analyzed by: 8 specialized perspectives

---

## Now (Sprint-Ready, <2 weeks)

### [Security] SQL Injection in Order Search
**File**: api/orders.ts:89
**Perspectives**: security-sentinel
**Impact**: Database compromise, data exfiltration possible
**Fix**: Use parameterized query: `db.query('SELECT * FROM orders WHERE id = $1', [id])`
**Effort**: 5m | **Risk**: CRITICAL
**Acceptance**: Manual SQL injection test passes, security audit clean

### [Product] User Authentication System
**Scope**: New feature - auth system
**Perspectives**: product-visionary, user-experience-advocate
**Business Case**:
- Blocks 5+ features (saved preferences, collaboration, premium tiers)
- 90% of competitors have auth (table stakes)
- Anonymous users = 10x higher churn
**Implementation**: Auth0/Clerk integration, email + social login
**Effort**: 2d | **Value**: Foundation for $15/mo Pro tier, retention unlock
**Acceptance**: Users can register, login, logout; sessions persist; OAuth works

[... more Now items with full detail]

---

## Next (This Quarter, <3 months)

### [Architecture] Extract UserManager God Object → 5 Focused Modules
**File**: services/UserManager.ts:1-847
**Perspectives**: complexity-archaeologist, architecture-guardian, maintainability-maven
**Why**: 847 lines, 28 methods, 5 responsibilities = maintenance bottleneck
**Approach**: Extract UserAuth, UserProfile, UserPermissions, UserNotifier, UserAnalytics
**Effort**: 8h | **Impact**: Unlocks parallel feature development, halves test complexity

### [Performance] Implement Virtual Scrolling for Large Tables
**Perspectives**: performance-pathfinder, user-experience-advocate
**Why**: Tables with >100 rows freeze UI for 3-5s
**Approach**: React-virtual or tanstack-virtual, lazy load rows
**Effort**: 4h | **Impact**: 3s → <100ms, handles 10k+ rows smoothly

[... more Next items with approach + sizing]

---

## Soon (Exploring, 3-6 months)

- **[Product] Collaboration Features** - Real-time multiplayer editing (needs design review, WebSocket infra)
- **[Architecture] Migrate to Monorepo** - Consolidate 4 repos → 1 turborepo (dependency hell fix, team growing)
- **[Feature] Plugin System** - User-extensible commands (differentiation play, needs API design)
- **[Performance] Server-Side Rendering** - SEO + initial load improvement (Next.js migration, big lift)

[... Soon items = one-liner + optional parenthetical context]

---

## Later (Someday/Maybe, 6+ months)

- **[Platform] Mobile App** - iOS/Android native or React Native
- **[Product] AI-Powered Suggestions** - ML model for workflow optimization
- **[Feature] Visual Workflow Builder** - No-code interface for power users
- **[Integration] Enterprise SSO** - SAML/OAuth for large orgs

[... Later items = title only, delete freely]

---

## Learnings

**From this grooming session:**
- [Capture insights that inform next groom: "UserManager bloat = symptom of missing domain boundaries"]
- [Technical discoveries: "Payment processing N+1 query only hits on enterprise tier"]
- [Product insights: "Users request export more than import, flip prioritization"]

**Keep 2-3 recent learnings, delete old ones**
```

### Formatting Guidance

**Now items need:**
- Category, file:line, perspectives, business/technical impact
- Concrete fix/implementation approach
- Effort estimate + acceptance criteria
- Multi-agent flags = surface prominently

**Next items need:**
- Category, scope, perspectives
- Why it matters (business case or technical rationale)
- High-level approach + dependencies
- Rough effort sizing

**Soon items need:**
- Title + one-line context (optional)
- Brevity over comprehensiveness

**Later items need:**
- Title only
- Delete freely if not exciting anymore

**Value-first lens for features:**
- Adoption driver? Retention hook? Revenue enabler?
- Competitive gap? Workflow unlock? Differentiation?
- What's the 20% of features that drive 80% of value?

**Velocity-first lens for technical work:**
- Does this unlock faster feature development?
- Does this prevent future bugs/incidents?
- Does this reduce cognitive load for team?

## Success Criteria

You've groomed well if:

✅ **Forward-Only**: No completed/archived section — backlog shows where you're going, not where you've been
✅ **Ruthlessly Curated**: Every item passes "would future me work on this in 6 months?" test
✅ **Time-Organized**: Clear Now/Next/Soon/Later structure with detail matching proximity
✅ **Comprehensive Coverage**: All 8 perspectives analyzed the codebase
✅ **Value-First**: Business case for features, velocity case for technical work
✅ **80/20 Applied**: Emphasis on high-leverage items, aggressive pruning of low-impact work
✅ **Principle Traceability**: Each issue links to violated principles or strategic opportunity
✅ **Cross-Validation**: Multi-agent issues surfaced and prioritized
✅ **Strategic Mix**: Critical fixes + velocity unlocks + revenue drivers + differentiation plays
✅ **Effort-Estimated**: Now/Next items have realistic sizing

The backlog should feel like a strategic roadmap that excites you about the future, not a graveyard of abandoned ideas.

## Philosophy

> "Eight perspectives see what one cannot. Complexity hides from single viewpoints but reveals itself under multiple lenses. Value emerges when quality meets opportunity."

Each specialized agent embodies different wisdom:
- **Complexity archaeologist**: Ousterhout's depth philosophy
- **Architecture guardian**: Modularity and clean architecture
- **Security sentinel**: Defensive programming and OWASP
- **Performance pathfinder**: User-facing speed and efficiency
- **Maintainability maven**: Code for humans, not machines
- **User experience advocate**: Friction-free user journeys
- **Product visionary**: Market opportunities and feature value
- **Design systems architect**: UI consistency and component quality

Together, they see the whole system — both what needs fixing AND what's worth building.

**The Curator's Mindset:**

A great backlog is not comprehensive — it's strategic. Like a museum curator, you select what deserves attention and ruthlessly exclude what doesn't. Completed work belongs in git history. Abandoned ideas belong in the void. The backlog holds only what competes for your finite attention.

Time horizons enforce reality. "Now" means sprint-ready. "Later" means genuinely excited about someday. Everything else gets deleted or promoted. Detail matches proximity because distant futures don't need pixel-perfect specs.

Value beats completeness. Better to ship 3 high-impact items than 30 marginal ones. The 80/20 rule is your weapon against backlog bloat: identify the 20% of work that drives 80% of value, emphasize that, prune the rest.

The backlog is alive — it evolves with learning, market shifts, technical discoveries. Learnings section captures what you learned this groom to inform the next. Each grooming session refines your understanding of what actually matters.

---

*Run this command periodically (monthly/quarterly) to maintain strategic clarity and discover high-leverage opportunities.*
