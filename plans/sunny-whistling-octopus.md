# Plan: Apply Gemini CLI Integration Pattern Across Master-Lens Commands

## Executive Summary

Apply the gemini integration pattern (successfully implemented in `/aesthetic`) to other master-lens commands, adding web-grounded perspectives where they provide unique value.

**Scope**:
1. Rename `backlog-groom.md` → `groom.md`
2. Add Phase 4.5 gemini integration to: `performance`, `security`, `testing`
3. Add Phase 2.5 competitive intelligence to: `groom`
4. Add Phase 2 research to: `simplify`
5. Note: `api-design` already has gemini integration ✓

**Pattern**: Each command gets gemini as "fourth perspective" or "competitive intelligence" that complements local code analysis with current web-grounded context.

---

## Command-by-Command Integration Plan

### 1. GROOM (formerly backlog-groom)

**Current State**:
- 8 parallel Task agents analyzing local codebase
- No gemini integration
- Needs rename: backlog-groom.md → groom.md

**Integration Point**: **Phase 2.5: Competitive Intelligence Scout**

After the 8 local agents complete, add 9th perspective using gemini:

```bash
gemini "Conduct competitive intelligence analysis for this codebase:

## Context
- Tech stack: [detected from Phase 1]
- Domain: [product type]
- Key challenges: [from agent reports]

## Research Mission

1. **Competitive Landscape**: How do competitors solve similar problems?
   - Identify 3-5 direct/adjacent competitors
   - Analyze their approach (libraries, patterns, architecture)
   - What do they do differently?

2. **Ecosystem Evolution**: Has the tech landscape moved beyond our approach?
   - Framework/library updates that change best practices
   - New patterns that supersede current architecture
   - Deprecated approaches we're still using

3. **Best Practice Currency**: What's table stakes vs differentiation now (2025)?
   - Industry standards for [domain]
   - Expected features in [product category]
   - Security/performance baselines

4. **Opportunity Gaps**: What are users asking for in this space?
   - GitHub issues/discussions in similar projects
   - Reddit/HN discussions about pain points
   - Feature requests we haven't considered

Return: Competitive gap analysis, modernization opportunities, user-driven feature ideas."
```

**File Changes**:
1. Rename `/Users/phaedrus/.claude/commands/backlog-groom.md` → `groom.md`
2. Insert Phase 2.5 after line ~[locate after 8 agents complete, before synthesis]

**Rationale**: 8 agents analyze local code deeply; gemini adds external market context about what competitors do, what's changed in ecosystem, and what users want. This grounds prioritization in competitive reality.

---

### 2. PERFORMANCE

**Current State**:
- 3 parallel Task agents (Measurer, Simplifier, Scientist)
- Optional gemini research mentioned but not implemented
- Structure matches aesthetic perfectly

**Integration Point**: **Phase 4.5: Gemini Performance Perspective**

After Phase 4 (3 Task agents), before Phase 5 (synthesis):

```bash
gemini "You are a performance engineering expert channeling Brendan Gregg, Rich Hickey, and Donald Knuth.

Review this [framework] application:

## Context
- Framework: [detected]
- Runtime: [detected]
- Performance baseline: [from Phase 1 measurements]

## Performance Analysis

1. **Profiling & Observability**: What are current best practices for [runtime] profiling?
   - Recommended tools (Chrome DevTools, clinic.js, perf, etc.)
   - APM platforms for this stack
   - Tracing and metrics standards

2. **Framework-Specific Patterns**: Performance patterns for [framework] in 2025
   - Server-side rendering optimizations
   - Bundle splitting strategies
   - Database query patterns
   - Caching layers

3. **Algorithmic Assessment**: Review reported hotspots
   - Are current algorithms optimal?
   - Library recommendations for performance-critical operations
   - Data structure choices

4. **Real-World Benchmarks**: What performance is achievable?
   - Industry benchmarks for [product type]
   - Exemplar sites with similar traffic
   - What's fast enough?

Provide:
- Tooling recommendations
- Framework-specific optimizations
- Algorithmic improvements
- Performance targets grounded in real examples"
```

**File Changes**: Insert Phase 4.5 in `/Users/phaedrus/.claude/commands/performance.md` after parallel agents

---

### 3. SECURITY

**Current State**:
- 3 parallel Task agents (Attacker, Defender, Auditor)
- Optional gemini research mentioned but not implemented
- Structure matches aesthetic

**Integration Point**: **Phase 4.5: Gemini Security Perspective**

```bash
gemini "You are a security expert channeling Bruce Schneier, OWASP guidance, and Joe Armstrong's defensive philosophy.

Review this [framework] application:

## Context
- Framework: [detected]
- Dependencies: [key libraries]
- Attack surface: [from Phase 1]

## Security Analysis

1. **Current Threat Landscape (2025)**: What are active attack patterns for [framework]?
   - OWASP Top 10 updates
   - Framework-specific vulnerabilities
   - Supply chain risks
   - Zero-days in dependencies

2. **Framework Security Patterns**: Best practices for securing [framework]
   - Authentication/authorization patterns
   - Input validation libraries
   - CSRF/XSS protection
   - Security headers

3. **Dependency Audit**: Are current dependencies secure?
   - Known CVEs in package.json
   - Alternative libraries with better security
   - Unmaintained packages to replace

4. **Defense-in-Depth**: Industry standards for [domain]
   - Compliance requirements (SOC2, GDPR, etc.)
   - Security tooling (Snyk, SAST, DAST)
   - Incident response patterns

Provide:
- Current threat assessment
- Framework hardening guide
- Dependency recommendations
- Security roadmap grounded in 2025 standards"
```

**File Changes**: Insert Phase 4.5 in `/Users/phaedrus/.claude/commands/security.md` after parallel agents

---

### 4. TESTING

**Current State**:
- 3 parallel Task agents (Pragmatist, Pyramid-Builder, Explorer)
- NO gemini integration mentioned
- Structure matches aesthetic

**Integration Point**: **Phase 4.5: Gemini Testing Perspective**

```bash
gemini "You are a testing expert channeling Kent Beck, Martin Fowler, and James Bach.

Review this [framework] application:

## Context
- Framework: [detected]
- Current test coverage: [from Phase 1]
- Test frameworks: [detected]

## Testing Analysis

1. **Testing Philosophy Evolution**: What's current best practice (2025)?
   - Test-first vs test-after vs type-driven
   - Unit vs integration vs E2E ratios
   - TDD/BDD/property-based testing trends

2. **Framework Testing Patterns**: How to test [framework] effectively
   - Recommended testing libraries (Vitest, Jest, Playwright, etc.)
   - Component testing patterns
   - API testing strategies
   - Visual regression testing

3. **Coverage vs Confidence**: Industry standards for [product type]
   - What coverage % is reasonable?
   - Critical paths requiring 100% coverage
   - Areas where tests add little value

4. **Testing Infrastructure**: Modern testing tooling
   - CI/CD integration patterns
   - Test parallelization
   - Snapshot testing
   - Mock vs real dependencies

Provide:
- Testing philosophy for this stack
- Tool recommendations
- Coverage targets
- Testing roadmap grounded in 2025 practices"
```

**File Changes**: Insert Phase 4.5 in `/Users/phaedrus/.claude/commands/testing.md` after parallel agents

---

### 5. SIMPLIFY

**Current State**:
- 3 parallel Task agents (Essentialist lenses)
- No gemini integration
- Structure matches aesthetic

**Integration Point**: **Phase 2: Optional Research** (lighter touch than Phase 4.5)

After Summon Council, before Phase 3 analysis:

```markdown
### 2.2 Optional: Research Contemporary Patterns

```bash
gemini "Research modern complexity patterns for [detected framework/stack]:

1. What are current best practices for managing complexity in [framework]?
2. How do exemplar codebases structure [specific domain] features?
3. What patterns have emerged since [old pattern] fell out of favor?
4. Are there new libraries/frameworks that reduce complexity?

Focus on helping identify if complexity is accidental (outdated patterns) vs essential (problem domain)."
```

**Rationale**: Lighter integration than Phase 4.5 because complexity analysis is mostly local. Gemini helps identify if patterns are outdated.

**File Changes**: Insert Phase 2.2 in `/Users/phaedrus/.claude/commands/simplify.md` as optional research

---

### 6. API-DESIGN

**Current State**: Already has gemini integration at Phase 2 ✓

**Action**: None needed. This command already follows the pattern.

---

## Technical Implementation

### File Operations Summary

**Rename**:
1. `backlog-groom.md` → `groom.md`

**Insert Phase 4.5** (after parallel Task agents, before synthesis):
1. `/Users/phaedrus/.claude/commands/performance.md`
2. `/Users/phaedrus/.claude/commands/security.md`
3. `/Users/phaedrus/.claude/commands/testing.md`

**Insert Phase 2.5** (competitive intelligence after 8 agents):
1. `/Users/phaedrus/.claude/commands/groom.md` (renamed file)

**Insert Phase 2.2** (optional research):
1. `/Users/phaedrus/.claude/commands/simplify.md`

### Gemini Prompt Pattern

All prompts follow this structure:
```bash
gemini "You are [expert] channeling [masters].

Review this [framework] application:

## Context
[Pass key findings from earlier phases]

## [Domain] Analysis
1-4 specific research questions

Provide:
- Specific recommendations
- Tool/library suggestions
- Industry benchmarks
- Roadmap grounded in 2025 practices"
```

### Error Handling (Standard Pattern)

All integrations include fallback:
```markdown
**If Gemini CLI unavailable**:
```markdown
## Gemini [Domain] Perspective (Unavailable)

Gemini CLI not available. Proceeding with Task agent perspectives only.
To enable: Ensure gemini CLI installed and GEMINI_API_KEY set in ~/.secrets.
```
```

---

## Rationale

### Why These Commands?

**Performance/Security/Testing**: Already have 3 parallel Task agents (Essentialist, Humanist, Architect equivalents). Natural fit for "fourth perspective" pattern from aesthetic.

**Groom**: Has 8 agents but missing external competitive context. Gemini adds market intelligence.

**Simplify**: Lighter integration (optional research) because complexity is mostly local analysis.

**API-Design**: Already complete ✓

### Why This Pattern?

**Consistency**: All master-lens commands now follow same integration pattern
**Complementary**: Local analysis (Claude) + web grounding (Gemini)
**Graceful**: Commands work without gemini; it's an enhancement not requirement
**Proven**: Aesthetic command demonstrates this works well

### Trade-offs

**Performance**: Adds 3-5 min per command (acceptable for deep reviews)
**Dependency**: Requires gemini CLI (already installed, graceful fallback)
**Variation**: Gemini's web grounding means responses stay current (feature, not bug)

---

## Success Metrics

Integration succeeds when:

✅ **Pattern consistency**: All 5 commands follow same integration approach
✅ **Four perspectives**: Performance, Security, Testing have 4th perspective like Aesthetic
✅ **Competitive intelligence**: Groom has market context from gemini
✅ **Graceful degradation**: All commands work without gemini
✅ **Web grounding**: Gemini provides current (2025) best practices and tools
✅ **File rename**: backlog-groom.md successfully renamed to groom.md

---

## Implementation Order

Recommended sequence:

1. **Rename**: backlog-groom.md → groom.md (simplest, no command logic changes)
2. **Performance**: Phase 4.5 integration (proven pattern from aesthetic)
3. **Security**: Phase 4.5 integration (same pattern)
4. **Testing**: Phase 4.5 integration (same pattern)
5. **Groom**: Phase 2.5 competitive intelligence (slightly different insertion point)
6. **Simplify**: Phase 2.2 optional research (lightest touch)

Can be done in one batch or iteratively. Each is independent.

---

## Critical Files

**To Rename**:
- `/Users/phaedrus/.claude/commands/backlog-groom.md` → `groom.md`

**To Modify** (add Phase 4.5):
- `/Users/phaedrus/.claude/commands/performance.md`
- `/Users/phaedrus/.claude/commands/security.md`
- `/Users/phaedrus/.claude/commands/testing.md`

**To Modify** (add Phase 2.5):
- `/Users/phaedrus/.claude/commands/groom.md` (after rename)

**To Modify** (add Phase 2.2):
- `/Users/phaedrus/.claude/commands/simplify.md`

**Already Complete**:
- `/Users/phaedrus/.claude/commands/api-design.md` ✓
- `/Users/phaedrus/.claude/commands/aesthetic.md` ✓
