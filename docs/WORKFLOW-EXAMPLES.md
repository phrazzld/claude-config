# Workflow Examples: A Day in the Life

This guide shows real-world scenarios demonstrating the compounding engineering workflow system in action.

## Introduction

The compounding engineering workflow transforms how quality accumulates in your codebase. Three core mechanisms enable this:

1. **Git Worktrees**: Parallel development in isolated environments, each with separate Claude sessions
2. **Learning Codification**: Every bug, pattern, and insight becomes executable artifact (code → tests → skills → commands → agents → docs)
3. **15-Agent Composition**: 8 domain specialists + 7 master personas provide comprehensive quality coverage

**The Result**: Every unit of work makes future work easier, faster, and higher quality.

---

## Scenario 1: New Feature Development (Full Pipeline)

**Timeline**: Monday morning, fresh feature request

**Request**: "Add email notification system for order confirmations"

### 9:00 AM - Understanding the Codebase

```bash
/prime
```

Claude reads README, CLAUDE.md, package.json, examines project structure. You now have full context.

### 9:15 AM - Research & Specification

```bash
/spec
```

**Behind the scenes**: Jobs + domain experts launch in parallel
- **Jobs**: "Do we need this? What's the simplest version? Can we say no?"
- **api-design-specialist**: "RESTful endpoint design, idempotency, error responses"
- **infrastructure-guardian**: "Email service provider, rate limiting, monitoring"

**Output**: Comprehensive spec in TASK.md addressing:
- User value (Jobs: "Confirmation reduces support tickets by 40%")
- API design (RESTful `/orders/:id/notify` endpoint)
- Infrastructure needs (SendGrid integration, structured logging)

### 10:30 AM - Architecture Design

```bash
/architect
```

**Output**: DESIGN.md with:
- Module breakdown (EmailService, NotificationQueue, TemplateRenderer)
- Data flow diagrams
- Interface contracts
- Ousterhout module depth analysis

### 11:00 AM - Planning with Complexity Review

```bash
/plan
```

**Behind the scenes**: Grug complexity review activates

**Grug's feedback**:
```
⚠️  COMPLEXITY DEMON ALERT

grug see in DESIGN.md:
- TemplateRenderer abstract base class with 3 concrete implementations
- EmailQueueManager with dependency injection framework

grug say: you not need this yet! you have ONE email template (order confirm).
one email provider (SendGrid). why abstract before see second use?

RECOMMENDATION:
- Make it work: Simple sendOrderConfirmation(order) function
- Make it right: Add tests
- Make it fast: Profile if needed
- Abstract: When you have SECOND real use case

complexity demon want make you build framework. grug say make working code.
```

**Result**: Plan updated. Removed premature abstractions. TODO.md has 8 focused tasks instead of 15.

### 11:30 AM - Implementation

```bash
/execute
```

Working through TODO.md tasks...

**After implementation completes**: Carmack + Ousterhout review in parallel

**Carmack's review**:
```
DIRECTNESS: ✅ Good
- sendOrderConfirmation() does exactly what name says
- No indirection layers
- Always shippable (feature flag controlled)

YAGNI: ⚠️  One issue
- Line 47: retry logic with exponential backoff
- This is YAGNI - no evidence we need retries yet
- Recommendation: Remove. Add when we see actual failures.
```

**Ousterhout's review**:
```
MODULE DEPTH: ✅ Excellent
- EmailService interface: 1 method (simple)
- Implementation: 50 lines (substantial)
- Value = High functionality - Low interface complexity

INFORMATION HIDING: ✅ Good
- SendGrid API key hidden in implementation
- Template rendering internals encapsulated
- Callers only see sendOrderConfirmation(order)
```

### 2:00 PM - Codification Moment

**Auto-prompt appears**:

```
✨ LEARNING CODIFICATION OPPORTUNITY DETECTED

Pattern identified: Email sending with structured logging and error handling

This pattern could recur. Codify as:
[ ] Code abstraction: Extract sendEmail(template, data) utility
[ ] Test: Add email sending test helper
[ ] Skill: Create email-integration skill template
[ ] Docs: Document email patterns in INFRASTRUCTURE.md

Recommend: Code abstraction (HIGH confidence - email used elsewhere)
```

**You accept**: Extract `sendEmail()` utility, add tests

### 2:30 PM - Ship It

```bash
/git-pr
```

PR created with auto-generated description showing:
- Feature summary
- Design decisions (Grug's simplification)
- Test coverage (15 tests added)
- Codification (sendEmail utility extracted)

**Compounding Effect**: Next email feature (password reset) takes 30 minutes instead of 4 hours because sendEmail() utility exists.

---

## Scenario 2: Parallel Development (Worktrees in Action)

**Timeline**: Tuesday, working on 3 features simultaneously

### 10:00 AM - Main Feature: Authentication System

**Main worktree** (`/Users/phaedrus/Development/myapp/`)

```bash
/prime
/plan
/execute  # Working on auth...
```

### 10:30 AM - Urgent: Review Teammate's PR

**Problem**: You're mid-implementation. Can't switch branches without stashing.

**Solution**: Worktree

```bash
/git-worktree-review 42
```

**Behind the scenes**:
1. Creates worktree at `../myapp-pr-42/`
2. Checks out PR #42
3. Runs initial checks (build, tests, lint)

**New terminal window**, navigate to `../myapp-pr-42/`, start new Claude session:

```bash
cd ../myapp-pr-42
c  # Start new Claude session
```

This Claude session has zero knowledge of your auth work. Clean context.

### 10:45 AM - Review Complete

You provide feedback on PR #42, close terminal.

### 11:00 AM - New Feature Request: Payment Integration

**Problem**: You're still mid-auth implementation. Payment is urgent but independent.

**Solution**: Another worktree

```bash
/git-worktree-create feature/stripe-payment
```

**Behind the scenes**:
1. Creates branch `feature/stripe-payment`
2. Creates worktree at `../myapp-stripe-payment/`
3. Sets up environment (.env copied)
4. Installs dependencies

**New terminal window**, navigate to worktree, start new Claude session:

```bash
cd ../myapp-stripe-payment
c
/prime
/spec    # Jobs + api-design-specialist analyze Stripe integration
/plan
/execute
```

### Current State: 3 Simultaneous Workstreams

**Terminal 1** (main worktree): Auth implementation (in progress)
**Terminal 2** (PR review worktree): PR #42 reviewed (done, ready to clean up)
**Terminal 3** (payment worktree): Stripe integration (in progress)

**Zero context switching**. No git stash. No mental overhead.

### 3:00 PM - Cleanup

```bash
/git-worktree-cleanup
```

**Behind the scenes**:
1. Lists all worktrees
2. Identifies stale ones (PR #42 review - merged)
3. Safety checks (uncommitted changes? unpushed commits?)
4. Removes worktree + local branch

**Compounding Effect**: Parallel work becomes natural. Productivity multiplies because you're never blocked by context switching.

---

## Scenario 3: Bug Investigation & Resolution

**Timeline**: Wednesday afternoon, production bug reported

**Bug Report**: "Users seeing stale data after updating profile"

### 2:00 PM - Debug Specialist Routing

```bash
/debug
```

**You describe**: "React profile page showing old data after successful update. API returns new data, but UI doesn't update."

**Behind the scenes**: `/debug` analyzes bug type

```
Bug category detected: STATE MANAGEMENT
Routing to: state-management-analyst
```

**state-management-analyst investigation**:

```
DIAGNOSIS: Race condition in async state update

Evidence from ProfilePage.tsx:68-72:
```tsx
const handleSave = async () => {
  const updated = await api.updateProfile(form)
  setProfile(updated)  // ⚠️  RACE CONDITION
}

useEffect(() => {
  api.getProfile().then(setProfile)  // Overwrites update if slow
}, [])
```

ROOT CAUSE: useEffect fetch racing with handleSave update
- If initial fetch resolves after update, old data overwrites new
- Stale closure: useEffect doesn't know about update

SOLUTION: Cancellation token pattern
```

### 2:30 PM - Implement Fix

```tsx
// ✅ Fixed with cleanup
useEffect(() => {
  let cancelled = false
  api.getProfile().then(data => {
    if (!cancelled) setProfile(data)
  })
  return () => { cancelled = true }
}, [])
```

### 3:00 PM - Codification Moment

**Auto-prompt appears**:

```
✨ LEARNING CODIFICATION OPPORTUNITY DETECTED

Bug root cause: Async race condition without cleanup
Broader implications: Affects all components with async useEffect

Codify as (multi-layer defense):
[✓] Code: Extract useAsyncEffect hook (cancellation built-in)
[✓] Tests: Regression test for this exact scenario
[✓] Agent: Update error-handling-specialist checklist
[✓] ESLint: Configure react-hooks/exhaustive-deps rule
[✓] Docs: Add REACT.md section on async cleanup
```

**You accept all**:

**Layer 1 - Code**:
```tsx
// hooks/useAsyncEffect.ts
export function useAsyncEffect(
  effect: (signal: AbortSignal) => Promise<void>,
  deps: DependencyList
) {
  useEffect(() => {
    const controller = new AbortController()
    effect(controller.signal)
    return () => controller.abort()
  }, deps)
}

// Usage (now safe by default)
useAsyncEffect(async (signal) => {
  const data = await api.getProfile({ signal })
  setProfile(data)
}, [])
```

**Layer 2 - Tests**:
```tsx
// hooks/useAsyncEffect.test.ts
it('cancels async operations on unmount', async () => {
  const { unmount } = renderHook(() =>
    useAsyncEffect(async (signal) => {
      await delay(100)
      expect(signal.aborted).toBe(false)
    }, [])
  )
  unmount()
  await delay(150)
  // Test passes - operation was cancelled
})
```

**Layer 3 - Agent Update**:
```markdown
# error-handling-specialist.md

## Review Checklist
- [x] Async cleanup on component unmount
  - Check: Does useEffect with async return cleanup function?
  - Check: Does async operation respect AbortSignal?
  - Pattern: Use useAsyncEffect hook (prevents race conditions)
```

**Layer 4 - ESLint**:
```json
// .eslintrc.json
{
  "rules": {
    "react-hooks/exhaustive-deps": "error",
    "react-hooks/rules-of-hooks": "error"
  }
}
```

**Layer 5 - Documentation**:
```markdown
# REACT.md

## Async State Management Patterns

### ⚠️  Avoid: Uncontrolled async in useEffect
Race conditions occur when async operations complete after unmount.

### ✅ Use: useAsyncEffect hook
Built-in cancellation prevents stale state updates.
```

### 3:30 PM - Sync to Other CLIs

```bash
/sync-configs
```

**Behind the scenes**:
- Updates `~/.codex/agents/error-handling-specialist.md`
- Updates `~/.gemini/system-instructions/error-handling-specialist.txt`

**Result**: Codex and Gemini CLIs now enforce same pattern

### Result: Bug Can Never Happen Again

**5-layer defense**:
1. Hook makes safe pattern default
2. Test catches regression
3. Agent flags violations in code review
4. ESLint catches at dev time
5. Docs educate team

**Compounding Effect**: One bug fixed = entire class of bugs prevented forever. Next time similar bug attempted, caught by 5 different mechanisms before reaching production.

---

## Scenario 4: Codebase Grooming (15-Agent Comprehensive Audit)

**Timeline**: Thursday, monthly grooming session

### 9:00 AM - Launch Comprehensive Audit

```bash
/groom
```

**Behind the scenes**: All 15 agents launch in parallel

**8 Domain Specialists analyzing**:
- complexity-archaeologist → shallow modules
- data-integrity-guardian → migration safety
- api-design-specialist → HTTP semantics
- test-strategy-architect → test pyramid
- error-handling-specialist → error boundaries
- state-management-analyst → race conditions
- dependency-health-monitor → CVEs, bundle size
- documentation-quality-reviewer → stale docs
- infrastructure-guardian → missing quality gates

**7 Master Personas applying timeless principles**:
- grug → complexity demon hunting
- carmack → YAGNI violations
- jobs → features to remove
- torvalds → over-architecture
- ousterhout → shallow modules
- fowler → code smells
- beck → test quality

### 9:15 AM - Cross-Validation Signal (Critical Priority)

**4 agents flag same issue**:

```
⚠️  CRITICAL PRIORITY (4 agents flagged)

FILE: services/OrderProcessor.ts

complexity-archaeologist:
  - Shallow module (interface complexity ≈ implementation)
  - 12 public methods, most are pass-throughs

architecture-guardian:
  - God object (420 lines, 8 responsibilities)
  - Violates Single Responsibility Principle

maintainability-maven:
  - Cognitive load: HIGH (comprehension barrier)
  - 3 developers asked "what does this do?"

ousterhout:
  - Module value NEGATIVE
  - Formula: Functionality(3) - Interface Complexity(8) = -5
```

**Diagnosis**: OrderProcessor is a God object pretending to be a module.

### 9:30 AM - Persona Consensus (Very Strong Signal)

**3 master personas agree on same feature**:

```
🔴 VERY STRONG SIGNAL (Grug + Carmack + Jobs agree)

FEATURE: Advanced order scheduling system (services/scheduler/)

grug:
  "grug see 8 files. 400 lines. used by zero other code.
   grug check git log: 6 months old. zero commits.
   this dead code. complexity demon living here. DELETE."

carmack:
  "Feature flag shows <0.1% usage. YAGNI violation.
   Question: Can we deploy without this Friday 5pm? YES.
   Recommendation: DELETE. Add back if actual need emerges."

jobs:
  "Saying no to 1000 things. This is one of them.
   User value: NONE (no user touches this)
   Craft: NEGATIVE (maintenance burden)
   Recommendation: DELETE."
```

**When all three personas agree to delete**: Very strong signal. Trust it.

### 9:45 AM - Infrastructure Gap Detection

**infrastructure-guardian findings**:

```
MATURITY LEVEL: Production Ready (6/9 requirements met)

✅ CI/CD pipeline (GitHub Actions)
✅ Structured logging (Pino)
✅ Error tracking (Sentry)
✅ Test coverage reporting (Vitest)
✅ Git hooks (Lefthook)
✅ Linting + formatting (ESLint + Prettier)

❌ MISSING (Team Scale infrastructure):
  ❌ Test coverage PR comments (no visibility)
  ❌ Coverage threshold enforcement (can merge with 0%)
  ❌ Design token system (Tailwind but no tokens)

RECOMMENDATION:
1. Add vitest-coverage-action to GitHub Actions
2. Set coverage threshold: 50% (current baseline)
3. Establish design tokens in tailwind.config.ts
```

### 10:00 AM - Competitive Intelligence (Gemini CLI)

**Behind the scenes**: `/groom` invokes `gemini` CLI for research

```bash
gemini "Research competitor feature sets for order management SaaS in 2025"
```

**Gemini returns** (with Google Search grounding):

```
COMPETITIVE INTELLIGENCE:

Feature gap identified: Bulk order import via CSV
- Competitor A: Has it (high user satisfaction)
- Competitor B: Has it (mentioned in 40% of reviews)
- Competitor C: Just added it (announced last month)

User evidence:
- Reddit r/ecommerce: "Switched to CompetitorA for CSV import"
- G2 reviews: 15 mentions of "wish had bulk import"

Technical implementation (from open source examples):
- CSV parsing (Papa Parse library)
- Validation + preview before import
- Background job processing
- Est. effort: 3-5 days
```

### 10:30 AM - Comprehensive BACKLOG.md Generated

**Output** organized by priority:

```markdown
# BACKLOG.md

## 🔴 Critical Priority (multiple agents flagged)

### Refactor OrderProcessor God Object
**Flagged by**: complexity-archaeologist, architecture-guardian, maintainability-maven, ousterhout
**Issue**: Shallow module with 12 public methods, negative value formula
**Recommendation**: Split into OrderValidator, OrderPersistence, OrderNotifier
**Effort**: 2-3 days
**Impact**: Reduces cognitive load, enables parallel dev

## 🔴 Very Strong Signal (Persona Consensus)

### DELETE: Advanced Scheduler System
**Consensus**: Grug + Carmack + Jobs all recommend deletion
**Rationale**: <0.1% usage, 400 lines dead code, zero value
**Action**: Delete services/scheduler/, remove feature flag
**Effort**: 1 hour
**Impact**: Removes maintenance burden, simplifies codebase

## 🟡 High Priority (2 agents flagged)

### Add Test Coverage PR Comments
**Flagged by**: infrastructure-guardian, test-strategy-architect
**Issue**: No visibility into coverage changes
**Recommendation**: vitest-coverage-action, 50% threshold
**Effort**: 2 hours
**Impact**: Prevents coverage regression

## 🔵 Competitive Intelligence

### Build Bulk Order CSV Import
**Source**: Gemini CLI research (competitor gap analysis)
**User evidence**: Reddit, G2 reviews
**Effort**: 3-5 days
**Impact**: Competitive parity, reduces churn risk

## 🟢 Specialized Concerns

### Update Dependencies with CVEs
**Flagged by**: dependency-health-monitor
**Vulnerabilities**: 3 high, 7 moderate
**Action**: Update axios, lodash, express
**Effort**: 1 day (testing required)
```

### Result: Strategic Roadmap

**From 15 perspectives**, you now have:
- Critical issues (must fix)
- Strong signals (persona consensus)
- Infrastructure gaps (quality gates)
- Competitive gaps (market intelligence)
- Prioritized by impact + effort

**Compounding Effect**: Multi-perspective analysis reveals what single viewpoint misses. God object identified. Dead code discovered. Competitive gaps surfaced. All in 30 minutes.

---

## Scenario 5: PR Feedback Integration (Automated Enforcement)

**Timeline**: Friday, PR feedback received

### 10:00 AM - PR Review Feedback

**Reviewer comment on PR #87**:

```
@phaedrus - You're not checking authentication on the DELETE endpoint.
This is the 3rd time I've mentioned this in different PRs.

Please add auth check.
```

### 10:15 AM - Implement Fix

```bash
/git-respond
```

**You provide reviewer comment**, Claude implements fix:

```typescript
// ✅ Added auth check
router.delete('/api/orders/:id',
  authenticateUser,  // Added
  async (req, res) => {
    // ... delete logic
  }
)
```

### 10:30 AM - Codification Auto-Prompt Appears

**Behind the scenes**: `/git-respond` detects pattern

```
🔄 FEEDBACK REVEALS AGENT GAP

Pattern: "Auth check missing on endpoints"
Impact: CRITICAL (security)
Gap: security-sentinel should catch this

Codify as:
[✓] Agent checklist: Update security-sentinel
[✓] Sync: Propagate to Codex & Gemini CLIs
[ ] ESLint rule: Custom rule for endpoint auth (optional)

Recommend: Agent update (prevents this class of issue)
```

**You accept**:

**Agent Update**:
```markdown
# agents/security-sentinel.md

## Review Checklist

### Authentication & Authorization
- [x] **Endpoint auth verification**
  - Every API endpoint has auth middleware
  - Specific check: Express routes must have authenticateUser/authorize
  - Red flag: router.METHOD without auth middleware
  - Exception: Public endpoints (must be explicitly documented as public)

### Before Approving
Run:
```bash
rg "router\.(get|post|put|delete|patch)" --type ts | rg -v "authenticateUser|authorize|PUBLIC"
```

If matches found: Flag for auth review
```

### 10:45 AM - Sync to Other CLIs

```bash
/sync-configs
```

**Behind the scenes**:
- Updates `~/.codex/agents/security-sentinel.md`
- Updates `~/.gemini/system-instructions/security-sentinel.txt`

### Next Week: Automated Enforcement

**New PR #94** (different developer):

```typescript
// Missing auth (same mistake)
router.delete('/api/products/:id', async (req, res) => {
  // ... delete logic
})
```

**Developer runs**:
```bash
/groom  # Before submitting PR
```

**security-sentinel flags immediately**:

```
🔴 SECURITY ISSUE DETECTED

FILE: routes/products.ts:42
ISSUE: DELETE endpoint missing authentication middleware

router.delete('/api/products/:id', async (req, res) => {
                                   ^^^^^^^^^^^^^^^^^^^^
                                   No authenticateUser middleware

RECOMMENDATION:
router.delete('/api/products/:id',
  authenticateUser,  // Add this
  async (req, res) => {
    // ...
  }
)
```

**Developer fixes before PR submission**. Reviewer never sees it.

### Result: PR Feedback → Automated Enforcement

**Compounding Effect**:
- **Before**: Reviewer gives feedback, system doesn't learn
- **After**: Agent catches issue automatically, reviewer never repeats themselves
- **Time saved**: 5 minutes per PR × 10 PRs/month = 50 minutes/month
- **Quality improved**: Zero instances of this bug class reach production

---

## Scenario 6: Week-End Review (Compounding Visualized)

**Timeline**: Friday end of day, reflection

### Monday: Starting Point

**Codebase state**:
- No email sending capability
- Manual PR reviews (no automation)
- Auth bug shipped to production
- Context switching hell (git stash, branch juggling)
- God object in OrderProcessor

**Quality debt**:
- 3 classes of bugs recurring
- PR reviews catch same issues repeatedly
- Parallel work blocked by context switching
- No infrastructure for automated quality

### Friday: Compounding Accumulated

**Codebase state**:
- Email sending: `sendEmail()` utility (reusable)
- Git worktrees: 3 parallel workstreams (zero context switching)
- Auth bug: Fixed + 5-layer defense (can't recur)
- OrderProcessor: Refactored (God object eliminated)
- security-sentinel: Updated (catches auth issues automatically)

**Quality improvements**:

**Patterns Extracted → Reused**:
1. `sendEmail()` utility
   - Used 5 times this week
   - Saved: 30 min × 5 = 2.5 hours
2. `useAsyncEffect()` hook
   - Used 3 times this week
   - Prevented: 3 potential race condition bugs
3. Stripe payment integration
   - Reusable pattern for future payment providers

**Bugs → Regression Tests + Prevention**:
1. Async race condition
   - Regression test: Catches if reintroduced
   - useAsyncEffect hook: Makes safe pattern default
   - Agent checklist: Flags violations in review
2. Missing auth checks
   - security-sentinel: Automated detection
   - Zero instances reached PR review this week

**PR Feedback → Automated Enforcement**:
1. Auth check pattern
   - Was: 3 manual reviews
   - Now: security-sentinel catches automatically
2. Test coverage visibility
   - Was: Manual check
   - Now: PR comments show delta

**Parallel Work Enabled**:
1. Main: Auth system (3 days)
2. Worktree 1: Payment integration (2 days, overlapped)
3. Worktree 2: PR review (30 min, didn't block main work)
   - **Total**: 5 days of work in 3 calendar days

**Infrastructure Maturity**:
- **Monday**: Production Ready (6/9)
- **Friday**: Team Scale (9/9)
  - Coverage PR comments ✅
  - Coverage threshold ✅
  - Design tokens ✅

### Compounding Metrics

**Time Savings**:
- Pattern reuse: 2.5 hours saved
- Worktree parallelization: 2 days saved
- Automated PR checks: 50 min/month saved (projected)

**Quality Improvements**:
- Bug classes prevented: 3
- Regression tests added: 8
- Agent checklists updated: 2
- Infrastructure gaps closed: 3

**Knowledge Codified**:
- Code abstractions: 3
- Reusable hooks: 1
- Test helpers: 2
- Skills created: 0 (patterns not yet at 3 occurrences)
- Agent updates: 2
- Documentation sections: 3

### The Compounding Effect

**Every unit of work made subsequent work easier**:

```
Monday work → Tuesday reuse (2.5 hours saved)
              ↓
Wednesday bug → 5-layer defense (entire bug class prevented)
              ↓
Thursday grooming → Strategic roadmap (15 perspectives)
              ↓
Friday PR feedback → Automated enforcement (reviewer never repeats)
```

**Visual**:

```
Quality Trajectory

High ▲                                              *
     |                                          *
     |                                      *
     |                                  *
     |                              *
     |                          *
     |                      * (Compounding curve)
     |                  *
     |              *
     |          *
     |      *
     |  *
Low  └──────────────────────────────────────────────▶ Time
     Mon   Tue   Wed   Thu   Fri

     * = Quality improvements accumulating
```

**Calm, Confident Friday 5pm Deploy**:
- All tests passing (8 new regression tests)
- Coverage above threshold (enforced by CI)
- Security checked (automated)
- Infrastructure mature (Team Scale)
- Parallel work shipped (worktrees)

**The compounding loop**:
1. Work produces learnings
2. Learnings codified into artifacts
3. Artifacts make future work easier
4. Easier work produces more learnings
5. Repeat → exponential quality growth

---

## Command Composition Showcase

### `/execute` Composition

**Visual flow**:

```
User: /execute

  ↓

📋 Task Selection (from TODO.md)

  ↓

🔍 Complexity Assessment
- Count files affected
- Assess scope
- Allocate reasoning effort

  ↓

⚙️  Implementation
- Make changes
- Write tests
- Update docs

  ↓

👥 Quality Review (Parallel)
┌────────────┴────────────┐
│                         │
🎯 Carmack              📚 Ousterhout
- Directness            - Module depth
- YAGNI                 - Information hiding
- Shippability          - Interface complexity
│                         │
└────────────┬────────────┘

  ↓

🔄 Synthesis
- Conflicts? (e.g., Carmack says "simple" but Ousterhout says "shallow")
- Resolution (evaluate trade-offs)
- Consensus highlights

  ↓

✨ Codification Prompt (default: codify)
- Can be enforced (hook/agent/skill/docs)
- Broad implications (affects multiple areas)
- Actionable (clear codification target)

  ↓

✅ Task Complete
```

**Key insight**: Two perspectives (directness + depth) catch issues single perspective misses.

### `/groom` Composition

**Visual flow**:

```
User: /groom

  ↓

🚀 Launch 15 Agents in Parallel
┌────────────────┬────────────────┐
│                │                │
8 Specialists    │    7 Personas
│                │                │
complexity       │    grug
data-integrity   │    carmack
api-design       │    jobs
test-strategy    │    torvalds
error-handling   │    ousterhout
state-mgmt       │    fowler
dependency       │    beck
docs             │
infrastructure   │
│                │                │
└────────────────┴────────────────┘

  ⏱️  15-30 minutes (parallel execution)

  ↓

📊 Cross-Validation Analysis

1 agent flags    = Specialized concern
2+ agents flag   = 🔴 HIGH PRIORITY (cross-cutting issue)

Example:
┌─────────────────────────────────┐
│ OrderProcessor.ts               │
│                                 │
│ complexity-archaeologist ✓      │
│ architecture-guardian    ✓      │
│ maintainability-maven    ✓      │
│ ousterhout               ✓      │
│                                 │
│ = CRITICAL (4 agents)           │
└─────────────────────────────────┘

  ↓

🤝 Persona Consensus Detection

When Grug + Carmack + Jobs agree:
  = VERY STRONG SIGNAL

Example: All three say "DELETE feature X"
  → Extremely high confidence
  → Rare agreement across perspectives
  → Trust this signal

  ↓

🔬 Gemini CLI Research

gemini "Research competitor features for [domain]"
  ↓
Google Search grounding
  ↓
Competitive intelligence
Market trends
User sentiment

  ↓

📋 Comprehensive BACKLOG.md

Generated with sections:
- 🔴 Critical Priority (3+ agents)
- 🔴 Very Strong Signal (persona consensus)
- 🟡 High Priority (2 agents)
- 🔵 Competitive Intelligence
- 🟢 Specialized Concerns

  ↓

✅ Strategic Roadmap Complete
```

**Key insight**: 15 perspectives reveal issues no single viewpoint could see. Cross-validation quantifies priority. Persona consensus provides rare, high-confidence signals.

---

## Codification Examples (The Compounding Mechanism)

### Example A: Bug → Multi-Layer Codification

**Scenario**: `setState`-during-render bug discovered in React component

**Codification cascade**:

```
🐛 Bug: Component crashes with "Cannot update during render"

  ↓

🔬 Root Cause Analysis
- setState() called inside render function
- Violation: Side effects must be in useEffect

  ↓

🏗️  Multi-Layer Codification

Layer 1: CODE (Most Permanent)
  ✓ Extract useAsyncEffect hook
  ✓ Built-in cancellation prevents race conditions
  ✓ Reusable across all async effects
  Location: hooks/useAsyncEffect.ts
  Impact: Makes safe pattern the default

Layer 2: TESTS
  ✓ Regression test for exact scenario
  ✓ Hook unit tests (cancellation, cleanup)
  ✓ Integration test (component using hook)
  Location: hooks/useAsyncEffect.test.ts
  Impact: Catches if bug reintroduced

Layer 3: AGENT CHECKLIST
  ✓ Update error-handling-specialist
  ✓ Add: "Check async cleanup on unmount"
  ✓ Pattern: Recommend useAsyncEffect
  Location: agents/error-handling-specialist.md
  Impact: Flags violations in code review

Layer 4: LINTING
  ✓ Enable react-hooks/exhaustive-deps
  ✓ Enable react-hooks/rules-of-hooks
  Location: .eslintrc.json
  Impact: Catches at dev time (immediate feedback)

Layer 5: DOCUMENTATION
  ✓ Add REACT.md section on async patterns
  ✓ Explain why pattern needed
  ✓ Show before/after examples
  Location: docs/REACT.md
  Impact: Educates team, prevents misunderstanding

  ↓

🔄 Sync to Other CLIs
  /sync-configs
  ✓ Codex: agents/error-handling-specialist.md
  ✓ Gemini: system-instructions/error-handling-specialist.txt

  ↓

🛡️  5-Layer Defense Established

Developer attempts setState-during-render:
  1. ESLint flags immediately (Layer 4)
  2. If bypassed: Hook makes pattern safe (Layer 1)
  3. If custom implementation: Test fails (Layer 2)
  4. If in PR: Agent flags (Layer 3)
  5. If confused: Docs explain (Layer 5)

  ↓

✅ Bug Can Never Happen Again
```

**Key insight**: Each layer defends differently. More permanent layers (code, tests) prevent at root. Less permanent layers (agents, docs) catch edge cases and educate.

### Example B: Pattern → Skill

**Scenario**: 3rd time implementing "Convex function with validation"

**Codification flow**:

```
🔁 Pattern Detected

Occurrence 1: users.createUser()
  - Zod validation
  - Error handling
  - Return type

Occurrence 2: orders.createOrder()
  - Zod validation (same pattern)
  - Error handling (same pattern)
  - Return type (same pattern)

Occurrence 3: products.createProduct()
  - Same pattern, clear reuse value
  - learning-codifier triggers

  ↓

📊 Codification Decision

Questions:
- Does this reveal a gap? YES (repeated manual setup)
- Can it be automated? YES (multi-step workflow)
- What's the best target? SKILL (reusable workflow)
→ Codify as skill

  ↓

🎯 Codification Decision

Pattern type: Multi-step workflow (5+ steps)
Best fit: SKILL (executable template)

  ↓

🏗️  Skill Creation

Location: ~/.claude/skills/convex-validated-function/

Structure:
convex-validated-function/
├── SKILL.md                 # Skill instructions
├── templates/
│   ├── mutation.ts          # Mutation template
│   ├── query.ts             # Query template
│   └── action.ts            # Action template
├── examples/
│   ├── users.ts             # Real example (users)
│   ├── orders.ts            # Real example (orders)
│   └── products.ts          # Real example (products)
└── tests/
    └── validation.test.ts   # Test template

  ↓

📝 SKILL.md Content

---
name: Convex Validated Function
description: Create type-safe Convex function with Zod validation
category: backend
tags: [convex, validation, zod, typescript]
---

# Convex Validated Function

Creates mutation/query/action with:
- Zod schema validation
- Type-safe inputs/outputs
- Error handling
- Return type inference

## Usage

/use-skill convex-validated-function

## Template Variables

- FUNCTION_NAME: Name of function
- FUNCTION_TYPE: mutation | query | action
- INPUT_SCHEMA: Zod schema
- RETURN_TYPE: TypeScript type

## Example

Input: "Create authenticated user update mutation"
Output: Mutation with auth, validation, error handling

  ↓

⚡ Usage Next Time

Developer: "Create Convex function to delete expired sessions"

Command: /use-skill convex-validated-function

  ↓ (30 seconds)

Generated:
```typescript
// convex/sessions.ts
import { mutation } from './_generated/server'
import { z } from 'zod'

const deleteExpiredSessionsInput = z.object({
  beforeDate: z.string().datetime(),
})

export const deleteExpiredSessions = mutation({
  args: deleteExpiredSessionsInput,
  handler: async (ctx, args) => {
    const { beforeDate } = args

    // Validation
    const parsedDate = new Date(beforeDate)
    if (isNaN(parsedDate.getTime())) {
      throw new Error('Invalid date format')
    }

    // Delete logic
    const expired = await ctx.db
      .query('sessions')
      .filter(q => q.lt(q.field('expiresAt'), parsedDate.getTime()))
      .collect()

    for (const session of expired) {
      await ctx.db.delete(session._id)
    }

    return { deleted: expired.length }
  },
})
```

  ↓

📊 Time Saved

Before skill: 30 minutes
- Look up Convex docs
- Write Zod schema
- Implement validation
- Add error handling
- Write tests

After skill: 30 seconds
- /use-skill convex-validated-function
- Answer prompts
- Review generated code

Savings: 30 min → 30 sec (60x faster)

  ↓

🔄 Compounding Effect

Week 1: Create skill (30 min investment)
Week 2: Use 2 times (save 60 min)
Week 3: Use 3 times (save 90 min)
Week 4: Use 1 time (save 30 min)

Total: 30 min invested, 180 min saved = 6x ROI in 1 month
```

**Key insight**: Patterns become executable templates. One-time investment yields exponential returns as pattern recurs.

---

## Before/After Comparisons

### Before Compounding Workflow

**Monday**: Bug fix takes 2 hours
- Fix the immediate issue
- Move on to next task
- Same bug type occurs next week

**Tuesday**: Similar bug takes 2 hours again
- "Didn't we fix this before?"
- Fix again, slightly differently
- No learning captured

**Wednesday**: PR reviewer says "check auth" for 10th time
- Add auth check
- Reviewer repeats same feedback next PR
- Pattern continues indefinitely

**Thursday**: Manual testing before every deploy
- Run through checklist
- Catch some issues
- Miss some issues
- Stressful process

**Friday**: Stressed, uncertain, manual everything
- Can't deploy confidently at 5pm
- Phone stays on all weekend
- System feels fragile

**Overall Quality Trajectory**: Flat or declining

```
Quality
  ▲
  │  * * * * * * * * *  (Flat - no compounding)
  │
  └──────────────────────▶ Time
```

### After Compounding Workflow

**Monday**: Bug fix takes 2 hours, becomes regression test
- Fix immediate issue
- Codification prompt: Extract pattern
- Create regression test
- Update agent checklist
- 5-layer defense established

**Tuesday**: Similar bug caught by test before it ships (0 hours)
- Developer writes code with bug
- Test fails immediately
- Developer fixes during development
- Bug never reaches PR review

**Wednesday**: security-sentinel flags auth check (auto-caught)
- Developer forgets auth check
- Runs `/groom` before PR
- security-sentinel flags issue
- Fixed before human reviewer sees it

**Thursday**: CI runs all quality gates (confident deploy)
- Tests run automatically
- Coverage checked
- Linting enforced
- Security scanned
- Deploy with confidence

**Friday**: Calm, confident, compounding quality
- Deploy at 5pm
- Phone off
- System feels robust
- Quality trajectory ascending

**Overall Quality Trajectory**: Exponential growth

```
Quality
  ▲                            *
  │                        *
  │                    *
  │                *
  │            *  (Compounding curve)
  │        *
  │    *
  │  *
  └──────────────────────────▶ Time
```

### Specific Comparisons

| Scenario | Before | After | Time Saved |
|----------|--------|-------|------------|
| Email feature | 4 hours (full implementation) | 30 min (reuse sendEmail utility) | 3.5 hours |
| Race condition bug | 2 hours (fix + test) | 0 hours (caught by useAsyncEffect) | 2 hours |
| Auth missing in PR | 10 min (reviewer comment) | 0 min (agent catches) | 10 min |
| Parallel work | Blocked (context switching) | Enabled (worktrees) | 2 days saved |
| Monthly audit | 4 hours (manual) | 30 min (/groom with 15 agents) | 3.5 hours |
| PR feedback loop | 3 iterations (same issue) | 0 iterations (automated) | 30 min |

**Cumulative Monthly Savings**: 40+ hours

**Quality Improvements**:
- Bug classes prevented: 5+
- Regression tests added: 20+
- Agent checklists updated: 5+
- Patterns codified: 10+
- Infrastructure gaps closed: 3+

---

## Tips & Best Practices

### Accept Codification Prompts Liberally

**Why**: Builds muscle memory for recognizing patterns

**When prompted**:
```
✨ LEARNING CODIFICATION OPPORTUNITY DETECTED
```

**Don't overthink**:
- Default: Accept and codify
- If it reveals a gap → Codify
- If bug has broad implications → Codify

**Example**: useAsyncEffect hook
- Could have said "not needed yet"
- Accepting saved 3 bugs this week
- ROI immediate

### Run `/groom` Monthly

**Why**: Comprehensive audit from 15 perspectives

**When**:
- End of month
- Before major release
- When system feels "off"

**What to expect**:
- 30 minutes runtime
- 50-100 findings
- Critical issues surfaced
- Strategic roadmap generated

**Act on results**:
- 🔴 Critical priority: This sprint
- 🟡 High priority: This month
- 🔵 Competitive intelligence: Roadmap

### Use Worktrees for Parallel Work

**Pattern**: One worktree per workstream

**Good uses**:
- Main: Feature A (multi-day)
- Worktree 1: PR review (30 min)
- Worktree 2: Feature B (multi-day, independent)

**Avoid**: Too many worktrees (3-4 max)

**Cleanup**: `/git-worktree-cleanup` weekly

### Trust Persona Consensus

**Strong signals** (3 personas agree):

**Grug + Carmack + Jobs say "DELETE"**:
- Very high confidence
- Rare convergence
- Different perspectives align
- Trust this signal

**Example decision tree**:
```
1 persona says delete    → Consider
2 personas say delete    → Strong consideration
3 personas say delete    → Very strong signal (do it)
```

**When personas disagree**:
- Jobs: "Remove feature" (simplicity)
- Expert: "Feature required" (domain need)
- → Validate user value (talk to users)

### Sync Configs Regularly

**When to run `/sync-configs`**:
- After creating new agent
- After modifying agent checklists
- After adding new command
- After significant philosophy updates
- Monthly (catch drift)

**Ensures**:
- Codex CLI has same quality bar
- Gemini CLI has same agent perspectives
- Consistent workflow across tools

**Verify sync**:
```bash
# Check Codex agents
ls ~/.codex/agents/

# Check Gemini system instructions
ls ~/.gemini/system-instructions/

# Should match ~/.claude/agents/ count
```

### Codify at Right Level

**Hierarchy** (descending permanence):
1. **Code**: Abstractions, utilities, hooks
2. **Tests**: Regression tests, test helpers
3. **Skills**: Multi-step workflow templates
4. **Commands**: Automated workflows
5. **Agents**: Review checklists, patterns
6. **Docs**: Explanations, decisions
7. **Philosophy**: Principles, values

**Decision guide**:
- Repeated logic with clear reuse value → Code abstraction
- Bug with broad implications → Code + tests + agent
- Multi-step workflow → Skill
- Process manual + repetitive → Command
- PR feedback reveals agent gap → Agent checklist
- Non-obvious decision → Docs (ADR)

---

## FAQ

### Q: When should I codify?

**A**: Default codify. Justify not codifying.

**Signs to codify** (any one is enough):
- "I learned something that could prevent future issues"
- "This could happen elsewhere"
- "Feedback revealed a gap in the system"
- "This workflow should be automated"

**When NOT to codify** (requires explicit justification):
- Already codified elsewhere (cite the exact path)
- Truly unique edge case (explain why)
- External constraint beyond system control

### Q: How do I choose between code abstraction vs test vs skill?

**A**: Hierarchy guides you - prefer more permanent forms.

**Decision tree**:

```
Is it a bug?
  YES → Code (fix) + Test (regression) + Agent (prevent)
  NO  ↓

Is it repeated logic with clear reuse value?
  YES → Code abstraction
  NO  ↓

Is it a multi-step workflow?
  YES → Skill
  NO  ↓

Does it reveal an agent gap?
  YES → Agent checklist update
  NO  ↓

Is it a decision rationale?
  YES → Documentation (ADR)
```

**Examples**:
- Race condition bug → Code (useAsyncEffect) + Test + Agent
- CSV parsing pattern → Code (parseCsv utility)
- Convex function creation → Skill (template)
- Auth check feedback → Agent (security-sentinel)
- Architecture choice → Docs (ADR)

### Q: What if agents disagree?

**A**: Tension reveals trade-offs. Evaluate context.

**Common tensions**:

**Jobs vs Expert**:
- Jobs: "Remove feature" (simplicity)
- Expert: "Feature required" (domain knowledge)
- Resolution: Validate user value (data, interviews)

**Grug vs Ousterhout**:
- Grug: "Too complex, delete abstraction"
- Ousterhout: "Deep module, good abstraction"
- Resolution: Check interface simplicity (if interface simple, trust Ousterhout)

**Beck vs Torvalds**:
- Beck: "Write tests first" (TDD)
- Torvalds: "Ship now, test later" (pragmatism)
- Resolution: Context-dependent
  - New feature: Beck (test first)
  - Bug fix: Torvalds (ship quickly)
  - Critical path: Beck (test first)

**Trust convergence**:
- 2 personas agree → Strong signal
- 3 personas agree → Very strong signal (rare)

### Q: How many worktrees is too many?

**A**: 3-4 maximum. Beyond that, cognitive overhead increases.

**Good**:
- Main: Primary feature (multi-day)
- Worktree 1: PR review (short-lived)
- Worktree 2: Independent feature (multi-day)

**Too many** (avoid):
- 5+ worktrees open simultaneously
- Forgotten worktrees (use `/git-worktree-cleanup`)
- Worktrees for trivial changes (just use main)

**Best practice**: Clean up weekly

### Q: Should I run `/groom` on every PR?

**A**: No. `/groom` is monthly comprehensive audit. Use `/execute` for PR-level quality.

**Command purposes**:

**`/execute`** (per-task quality):
- Carmack + Ousterhout review
- Focused on current changes
- Fast (2-5 minutes)
- Run: Every significant change

**`/groom`** (comprehensive audit):
- All 15 agents
- Entire codebase
- Slow (15-30 minutes)
- Run: Monthly, before major release

**Don't**: Run `/groom` on every PR (overkill, slow)
**Do**: Run `/execute` on every task

### Q: What if codification prompt appears but pattern isn't clear?

**A**: Skip it. False negatives okay, false positives waste time.

**When to skip**:
- Pattern unclear ("I don't see how this recurs")
- Confidence low (learning-codifier says "MEDIUM")
- One-off scenario ("This is edge case")

**When to accept**:
- Pattern has clear prevention value
- Broad implications ("This affects multiple areas")
- Can be enforced (hook/agent/skill/docs)

**Default**: Accept and codify. Justify skipping, not codifying.

### Q: How do I sync agent changes to active projects?

**A**: `/sync-configs` syncs to Codex/Gemini, but not to other repos.

**For project-specific agents**:
- Add to `project/.claude/agents/`
- Document in `project/CLAUDE.md`
- Not synced globally (intentional)

**For global agents**:
- Modify `~/.claude/agents/`
- Run `/sync-configs`
- Available in all projects

### Q: Can I create my own agents?

**A**: Yes! Follow the agent template.

**Template** (`~/.claude/agents/my-agent.md`):

```markdown
# Agent Name

**Specialty**: One-line description

**Hunts for**:
- Specific issue 1
- Specific issue 2
- Specific issue 3

**When to invoke**:
- Scenario 1
- Scenario 2

**Philosophy**: Core principle in one sentence

## Review Checklist

- [ ] Check 1 (specific, actionable)
- [ ] Check 2 (specific, actionable)
- [ ] Check 3 (specific, actionable)

## Red Flags

- Pattern 1 to avoid
- Pattern 2 to avoid

## Examples

### ❌ Anti-pattern
[Code example of what NOT to do]

### ✅ Correct pattern
[Code example of what TO do]
```

**Then**: Run `/sync-configs` to propagate

---

## Conclusion

The compounding engineering workflow transforms software development from repetitive manual labor into a self-improving system.

**Three mechanisms**:
1. **Git Worktrees**: Parallel development without context switching
2. **Learning Codification**: Bugs become prevention, patterns become tools
3. **15-Agent Composition**: Multi-perspective quality coverage

**The compounding loop**:
```
Work → Learnings → Codification → Easier Future Work → More Learnings → ...
```

**Every unit of work**:
- Fixes immediate problem
- Prevents future occurrences
- Builds reusable artifacts
- Educates the system

**The result**:
- Quality compounds exponentially
- Bugs can't recur
- Patterns become tools
- PR reviews automate
- Deploy with confidence

**Start today**:
1. Use `/git-worktree-create` for next parallel task
2. Accept next codification prompt
3. Run `/groom` this month
4. Trust persona consensus
5. Watch quality compound

**Welcome to compounding engineering.**
