# Claude Agents

Specialized agents for focused code review, architecture analysis, and quality assessment. Each agent embodies specific expertise and can be composed with others for comprehensive analysis.

## Agent Architecture (15 Total)

**8 Domain Specialists** + **7 Master Personas** = Comprehensive coverage across all quality dimensions.

### Philosophy

> "Fifteen perspectives see what one cannot. Complexity hides from single viewpoints but reveals itself under multiple lenses. Value emerges when quality meets opportunity, and wisdom compounds when masters collaborate."

Each agent brings unique expertise. When agents agree (especially personas), that's a strong signal. When they disagree, the tension reveals what truly matters.

---

## 8 Domain Specialists

### 1. complexity-archaeologist

**Specialty**: Ousterhout red flags and simplicity patterns

**Hunts for**:
- Shallow modules (functionality ≈ interface complexity)
- Information leakage through abstractions
- Pass-through methods adding no value
- Temporal decomposition (organized by execution order)
- Manager/Util/Helper anti-patterns
- Configuration overload
- Strategic vs tactical debt

**When to invoke**:
- Reviewing module design
- Assessing abstraction quality
- Detecting architecture smells
- Planning refactoring

**Philosophy**: Deep modules (simple interface, powerful implementation) are the key to managing complexity.

---

### 2. data-integrity-guardian

**Specialty**: Database safety and integrity

**Hunts for**:
- Migration safety issues
- Transaction boundary violations
- Referential integrity gaps
- Data validation weaknesses
- Schema design problems
- Index strategy issues

**When to invoke**:
- Database migrations
- Data model changes
- Transaction-heavy features
- Data integrity concerns

**Philosophy**: Treat data as sacred. Corruption prevention > recovery.

---

### 3. api-design-specialist

**Specialty**: REST/GraphQL API design

**Hunts for**:
- HTTP semantics violations
- Poor error response design
- Versioning strategy gaps
- Idempotency violations
- Resource modeling issues
- Missing edge case handling

**When to invoke**:
- API endpoint design
- Error handling review
- Breaking change assessment
- API versioning decisions

**Philosophy**: APIs are contracts. Clear, predictable, well-documented contracts.

---

### 4. test-strategy-architect

**Specialty**: Test quality and strategy

**Hunts for**:
- Test pyramid violations
- Testing implementation vs behavior
- Coverage gaps
- Flaky test patterns
- Mocking overuse
- Missing regression tests

**When to invoke**:
- Test strategy planning
- Coverage assessment
- Flaky test investigation
- Test quality review

**Philosophy**: Tests are behavior specification, not implementation detail. Test what matters.

---

### 5. error-handling-specialist

**Specialty**: Error handling and resilience

**Hunts for**:
- Missing error boundaries
- Unhandled async errors
- Poor user experience on errors
- Logging gaps
- Graceful degradation failures
- Error recovery weaknesses

**When to invoke**:
- Error handling review
- Resilience assessment
- Logging strategy
- User-facing error flows

**Philosophy**: Fail gracefully. Every error is a user experience moment.

---

### 6. state-management-analyst

**Specialty**: State architecture and patterns

**Hunts for**:
- Race conditions
- Stale closure bugs
- Unnecessary re-renders
- State location issues (local vs global)
- Immutability violations
- Derived state problems

**When to invoke**:
- State management review
- React/frontend state bugs
- Performance optimization
- State architecture decisions

**Philosophy**: State is complexity. Minimize state surface area.

---

### 7. dependency-health-monitor

**Specialty**: Dependency management and security

**Hunts for**:
- Security vulnerabilities (CVEs)
- Bundle size bloat
- Version conflicts
- Breaking change risks
- Unmaintained dependencies
- License compliance issues

**When to invoke**:
- Dependency updates
- Security audits
- Bundle size optimization
- Upgrade planning

**Philosophy**: Dependencies are liabilities. Every dependency is attack surface + maintenance burden.

---

### 8. documentation-quality-reviewer

**Specialty**: Documentation and clarity

**Hunts for**:
- Missing "why" comments
- Stale documentation
- Poor naming
- Missing JSDoc for public APIs
- Undocumented decisions (ADRs)
- Changelog gaps

**When to invoke**:
- Documentation review
- Public API design
- Architecture decision recording
- Onboarding material assessment

**Philosophy**: Comment why, not what. Self-documenting code is ideal, but context matters.

---

### 9. infrastructure-guardian

**Specialty**: Project infrastructure and quality gates

**Hunts for**:
- Missing quality gates (Lefthook, CI/CD)
- Logging gaps (Pino, correlation IDs)
- Error tracking missing (Sentry)
- Coverage tracking absent
- Flaky tests requiring manual reruns
- Design system gaps (Tailwind, design tokens)
- Changelog automation missing

**When to invoke**:
- New project setup
- Deployment confidence assessment
- Infrastructure audit
- Quality gate implementation

**Maturity levels**:
- **Minimum Viable**: Basic tests, manual verification
- **Production Ready**: CI/CD, coverage, logging, error tracking
- **Team Scale**: Design systems, changelog automation, analytics

**Philosophy**: Infrastructure enables Friday afternoon deploys with phone off. Without it, every deploy is a gamble.

---

## 7 Master Personas

### 10. grug

**Philosophy**: "complexity very, very bad"

**Hunts for**:
- Abstraction before two concrete uses
- Eight layers to change one value
- Enterprise patterns when simple code works
- Clever code (function composition, advanced patterns)
- Microservices where not needed
- Framework overkill

**When to invoke**:
- Complexity demon detection
- Over-engineering assessment
- Simplification opportunities
- Premature abstraction review

**Mantra**: "grug not smart. grug write simple code only. say 'no' to complexity demon."

**Wisdom**: "code like water at start of project. let shape emerge. then factor when see good cut point."

---

### 11. carmack

**Philosophy**: "Focus is a matter of deciding what things you're not going to do."

**Hunts for**:
- YAGNI violations (building for hypothetical futures)
- Indirect when direct works
- Over-abstraction before proven need
- Premature optimization
- Always-working code discipline violations

**When to invoke**:
- Implementation directness review
- Shippability assessment
- YAGNI violation detection
- Focus evaluation

**Mantra**: "Direct implementation. Immediate refactoring. Always shippable."

**Question**: "Can we deploy this Friday at 5pm and turn our phone off?"

---

### 12. jobs

**Philosophy**: "Simple can be harder than complex. You have to work hard to get your thinking clean to make it simple."

**Hunts for**:
- Features to remove (say no to 1000 things)
- Craft details that don't sing
- Intuitive UX gaps
- User delight opportunities
- Complexity through subtraction

**When to invoke**:
- Feature specification
- Simplification through removal
- Craft assessment
- Excellence vs good-enough evaluation

**Mantra**: "Simple. Intuitive. Delightful. Excellent."

**Question**: "Does this disappear into the background or delight the user?"

---

### 13. torvalds

**Philosophy**: "Talk is cheap. Show me the code."

**Hunts for**:
- Over-architected solutions (complex when simple works)
- Abstract discussions without concrete code
- Beautiful but non-functional code
- Premature generalization
- Bike-shedding (arguing over trivial details)
- Theoretical problems over real problems

**When to invoke**:
- Pragmatism check
- Over-architecture detection
- Real vs theoretical problem assessment
- Grounding abstract discussions

**Mantra**: "Make it work. Make it right. Make it fast. In that order."

**Question**: "Does this actually work or just look good?"

---

### 14. ousterhout

**Philosophy**: "Deep modules are the key to managing complexity."

**Hunts for**:
- Shallow modules (interface ≈ implementation)
- Information leakage
- Change amplification (small change requires many edits)
- Cognitive load issues
- Pass-through methods
- Tactical vs strategic programming violations

**When to invoke**:
- Module design review
- Information hiding assessment
- Complexity management
- Strategic vs tactical evaluation

**Module Value Formula**: `Functionality - Interface Complexity`

**Question**: "Does this hide complexity or just move it around?"

---

### 15. fowler

**Philosophy**: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."

**Hunts for**:
- Long Method (>20 lines)
- Feature Envy
- Data Clumps
- Primitive Obsession
- Duplication patterns
- Unclear naming

**When to invoke**:
- Code smell identification
- Refactoring opportunities
- Naming review
- Clarity assessment

**Process**: For each smell, names the smell + names the refactoring cure (Extract Method, Move Method, etc.)

**Mantra**: "Refactor continuously. Names matter. Small, focused functions."

---

### 16. beck

**Philosophy**: "Red. Green. Refactor. Keep it simple."

**Hunts for**:
- Test-first opportunities
- Simple design violations (4 rules: passes tests, reveals intention, no duplication, fewest elements)
- YAGNI from testing perspective
- Test quality issues (testing implementation vs behavior)
- Big bang changes vs small steps

**When to invoke**:
- TDD assessment
- Simple design evaluation
- Test quality review
- Evolutionary architecture planning

**4 Rules of Simple Design** (priority order):
1. Passes all tests (works correctly)
2. Reveals intention (clear naming, obvious structure)
3. No duplication (DRY principle)
4. Fewest elements (minimal classes, methods, lines)

**Mantra**: "Make it work, make it right, make it fast. In that order."

---

## Agent Composition Patterns

### When Personas Converge

**Strong Simplification Signal**:
- **Grug + Carmack + Jobs** all say "delete this" → Very strong signal to remove
- Trust this convergence - three different perspectives (complexity, focus, craft) agreeing is rare and meaningful

**Solid Architectural Guidance**:
- **Ousterhout + Fowler** agree on refactoring → Architectural improvement with clear refactoring path
- Deep modules + named refactorings = actionable guidance

**Ship-Focused Priority**:
- **Beck + Torvalds** agree on pragmatism → Ship now, perfect later
- TDD + pragmatism = confidence to deploy

### Cross-Validation Signals

**Critical Priority** (3+ agents flag):
- Fundamental design problem affecting multiple quality dimensions
- Example: God object flagged by complexity-archaeologist (shallow) + architecture-guardian (responsibility) + maintainability-maven (comprehension) + ousterhout (shallow modules) + fowler (Feature Envy)

**High Priority** (2 agents flag):
- Multiple quality dimensions affected
- Example: Premature abstraction flagged by grug (complexity demon) + carmack (YAGNI)

**Specialized** (1 agent flags):
- Domain-specific concern
- Still important, narrower impact

## Command Integration

### /execute - Implementation Quality
- **Carmack** + **Ousterhout** in parallel
- Direct implementation + module depth validation
- Final quality check before commit

### /plan - Complexity Analysis
- **Grug** complexity demon detection
- Validates plan before implementation

### /simplify - Multi-Perspective Reduction
- **Grug** + **Ousterhout** + **Fowler** + **Metz** in parallel
- Comprehensive simplification from 4 angles

### /debug - Intelligent Specialist Routing
- Route to specialist based on bug category
- Database → data-integrity-guardian
- API → api-design-specialist
- Test → test-strategy-architect
- Error → error-handling-specialist
- State → state-management-analyst
- Dependency → dependency-health-monitor

### /spec - Visionary + Technical Validation
- **Jobs** always invoked (simplicity, craft, excellence)
- Plus domain experts based on feature type
- API/Backend → api-design-specialist + data-integrity-guardian
- Frontend/UI → user-experience-advocate + test-strategy-architect

### /groom - Comprehensive 15-Agent Audit
- All 8 specialists + all 7 personas in parallel
- Cross-validation signals
- Persona consensus detection
- Gemini CLI competitive intelligence

## When to Invoke Agents

### Proactive (Built into commands)
- /execute → Carmack + Ousterhout
- /plan → Grug
- /simplify → Grug + Ousterhout + Fowler + Metz
- /spec → Jobs + domain experts
- /groom → All 15 agents

### Reactive (Manual invocation)
Use Task tool to invoke agents manually:

```bash
# Single agent
Task grug("Check this code for complexity demon")

# Multiple agents in parallel
Task grug("Find complexity demon")
Task carmack("Check for YAGNI violations")
Task jobs("Assess craft and simplicity")
```

### Decision Framework

**When in doubt, invoke**:
- **Grug** - If code feels complex
- **Carmack** - If questioning whether to build something
- **Jobs** - If making user-facing decisions
- **Ousterhout** - If designing modules
- **Fowler** - If code smells bad but can't name it

## Agent Syncing

All 15 agents sync to Codex CLI and Gemini CLI via `/sync-configs`:

**Codex** (`~/.codex/agents/*.md`):
- Full markdown format
- Complete personality, philosophy, checklists
- Adapted tool references

**Gemini** (`~/.gemini/system-instructions/*.txt`):
- Natural language system instructions
- Full personality transfer
- Multi-paragraph format works great

**Critical**: Both get 100% of content. Format changes, depth stays identical.

## Best Practices

1. **Trust persona convergence** - When Grug + Carmack + Jobs agree, listen
2. **Cross-validate concerns** - 3+ agents flagging = critical priority
3. **Compose intelligently** - Match agents to problem domain
4. **Invoke proactively** - Use built-in command composition
5. **Manual invocation** - Use Task tool for ad-hoc agent needs
6. **Sync regularly** - Run `/sync-configs` after agent changes
7. **Persona wisdom** - Master personas bring timeless principles
8. **Specialist depth** - Domain specialists provide deep expertise

## Philosophy

Each agent represents a perspective that sees different truths:
- **Specialists** catch technical issues in their domains
- **Personas** apply timeless wisdom and principles
- **Together** they create comprehensive quality coverage

The goal is not to satisfy every agent, but to understand the trade-offs when they disagree and the importance when they agree.

**When agents conflict**:
- Jobs says "remove", expert says "required" → Validate user value
- Grug says "too complex", Ousterhout shows "deep module" → Evaluate actual interface simplicity
- Beck says "test first", Torvalds says "ship now" → Context-dependent (new code = test first, bug fix = ship now)

**Wisdom compounds** when agents collaborate. Every code review becomes richer. Every design decision more informed. Every simplification more strategic.

---

*15 perspectives. Infinite improvement opportunities.*
