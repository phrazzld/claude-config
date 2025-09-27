Comprehensive quality review: cleanup, then brutal honesty.

# CODE-REVIEW

Two-phase quality review that first cleans up the code, then tears it apart with critical analysis.

## 1. Review Context Gathering

**Determine review scope**:
- Check if reviewing a PR: `gh pr view` or examine PR URL
- If branch review: `git diff main...HEAD` (or appropriate base branch)
- Note changed files, additions, deletions, and affected modules
- For post-task review: `git diff HEAD~1` or check recently modified files

## 2. Phase 1: The Cleanup (Matt Shumer)

**"After successfully completing your goal, ask: Please clean up the code you worked on, remove any bloat you added, and document it very clearly."**

**Cleanup Actions**:
- Remove all console.logs, debug statements, and print debugging
- Delete commented-out code and zombie imports
- Fix inconsistent naming (variables, functions, classes)
- Extract magic numbers and hardcoded strings to constants
- Simplify overly complex logic and nested conditionals
- Add clear documentation for complex sections
- Remove any temporary hacks or workarounds
- Ensure consistent code style and formatting

**Documentation Check**:
- Every public function has a clear purpose comment
- Complex algorithms have step-by-step explanations
- Non-obvious decisions are explained
- Configuration and setup requirements are documented

## 3. Phase 2: The Critical Analysis (Daniel Jeffries)

**"That's great that its 'production ready' but let's pretend it's not. Go back and tell me what you missed, half assed or did wrong. Ferret out any magical code and hallucination bullshit. Analyze it with a critical eye like you are Linus Torvalds on a bender doing a code review. Prove that it works by designing a useful test. Output your understanding of what I just said and your plan once you have analyzed it."**

**Brutal Honesty Questions**:
- What did I miss, half-ass, or completely botch?
- Where's the magical thinking and hallucination bullshit?
- What would make Linus rage-quit this review?
- What edge cases will definitely explode in production?
- Where did I copy-paste without understanding?
- What tests would actually prove this garbage works?
- What assumptions will bite us at 3am on a Sunday?
- Where's the technical debt I'm hiding?

**Linus-Level Analysis**:
- **Security**: What moron would expose user data like this?
- **Performance**: This O(n²) loop is what - a DoS vulnerability you're gifting to attackers?
- **Error Handling**: "It probably won't fail" is not error handling, genius
- **Testing**: These tests test nothing but your ability to write useless tests
- **Architecture**: This coupling is so tight it needs therapy
- **Documentation**: "It's self-documenting" = "I'm too lazy to explain my mess"

## 4. Phase 3: Leyline Binding Validation Expert

**🎯 BINDING COMPLIANCE REVIEW**: Validate all changes against applicable leyline bindings based on file types modified.

### File Type Detection & Binding Application
Analyze the diff to identify file types and apply relevant bindings:

**Automated File Type Detection:**
```bash
# Detect changed file types in current branch
git diff --name-only main...HEAD | while read file; do
  case "$file" in
    *.ts|*.tsx) echo "TypeScript binding validation required" ;;
    *.js|*.jsx) echo "JavaScript binding validation required" ;;
    *.go) echo "Go binding validation required" ;;
    *.py) echo "Python binding validation required" ;;
    *.sql) echo "SQL binding validation required" ;;
    *.rs) echo "Rust binding validation required" ;;
    *.java) echo "Java binding validation required" ;;
    *.rb) echo "Ruby binding validation required" ;;
    *.yaml|*.yml) echo "YAML configuration validation required" ;;
    Dockerfile*) echo "Docker binding validation required" ;;
  esac
done
```

**Technology-Specific Bindings to Validate:**
```yaml
TypeScript/JavaScript (.ts, .tsx, .js, .jsx):
  ✓ No use of 'any' without justification
  ✓ Explicit type annotations where needed
  ✓ Strict null checks compliance
  ✓ No implicit any returns
  ✓ Proper error boundaries in React
  ✓ useEffect dependency arrays complete
  ✓ No direct DOM manipulation in React
  ✓ Async/await over callbacks
  ✓ No var declarations (use const/let)

Go (.go):
  ✓ All errors explicitly handled (no _ ignoring)
  ✓ Context propagation in API calls
  ✓ Interface segregation principle followed
  ✓ Embedded struct composition over inheritance
  ✓ Defer statements for cleanup
  ✓ Goroutine leak prevention
  ✓ Mutex lock/unlock pairs
  ✓ Channel close responsibility clear

Python (.py):
  ✓ Type hints for function signatures
  ✓ Docstrings for public functions
  ✓ No bare except clauses
  ✓ Context managers for resources
  ✓ f-strings over % formatting
  ✓ List comprehensions where appropriate
  ✓ No mutable default arguments

Rust (.rs):
  ✓ Proper error handling with Result<T, E>
  ✓ No unnecessary unwrap() calls
  ✓ Lifetime annotations where needed
  ✓ Prefer borrowing over ownership transfer
  ✓ Use of unsafe blocks justified
  ✓ Match expressions exhaustive

SQL/Migrations (.sql):
  ✓ Foreign key constraints defined
  ✓ Indexes on queried columns
  ✓ NOT NULL constraints by default
  ✓ Consistent naming conventions
  ✓ No SELECT * in production code
  ✓ Transactions for multi-statement operations
  ✓ Idempotent migrations (IF NOT EXISTS)

Docker (Dockerfile):
  ✓ Multi-stage builds for smaller images
  ✓ Non-root user for runtime
  ✓ Specific version tags (no :latest)
  ✓ COPY preferred over ADD
  ✓ Minimal layers through command combining
  ✓ .dockerignore properly configured

Configuration (*.yaml, *.yml, *.json):
  ✓ No hardcoded secrets or credentials
  ✓ Environment-specific values extracted
  ✓ Schema validation where applicable
  ✓ Consistent indentation and formatting
  ✓ Comments for non-obvious settings
```

### Architecture Binding Compliance
**Core Architecture Principles:**
```yaml
hex-domain-purity:
  ✓ Domain logic free from infrastructure concerns
  ✓ Pure functions in business logic
  ✓ No database queries in domain layer
  ✓ No HTTP concerns in business rules

component-isolation:
  ✓ Single responsibility per module
  ✓ Clear input/output boundaries
  ✓ No circular dependencies detected
  ✓ Testable in isolation

interface-contracts:
  ✓ Backward compatibility maintained
  ✓ Version changes documented
  ✓ No breaking changes without version bump
  ✓ Contract tests present

dependency-inversion:
  ✓ Dependencies point inward
  ✓ Abstractions don't depend on details
  ✓ High-level modules independent of low-level
  ✓ Dependency injection used appropriately
```

### Binding Violation Detection
**Scan for common violations:**
- **Type Safety**: Any use of dynamic types without justification
- **Error Handling**: Swallowed exceptions or ignored errors
- **Architecture**: Business logic mixed with infrastructure
- **Dependencies**: Circular references or inverted dependencies
- **Testing**: Untestable code due to tight coupling
- **Performance**: Missing indexes, N+1 queries, unbounded loops

### Binding Review Output
```markdown
## Leyline Binding Compliance Report

### Files Reviewed & Applicable Bindings
- `src/api/handler.ts` → TypeScript, hex-domain-purity, interface-contracts
- `internal/service/user.go` → Go, component-isolation, dependency-inversion
- `migrations/001_users.sql` → SQL, database constraints

### ✅ Binding Compliance Passed
- TypeScript strict mode compliance in all .ts files
- Proper error handling in Go services
- Foreign key constraints in database migrations

### ❌ Binding Violations Detected
- **[HIGH]** `src/api/handler.ts:45` - Using 'any' type without justification
- **[HIGH]** `internal/service/user.go:89` - Error ignored with underscore
- **[MEDIUM]** `src/domain/order.ts:23` - Database query in domain layer
- **[MEDIUM]** `migrations/002_orders.sql` - Missing index on foreign key
- **[LOW]** `src/utils/helper.js` - No type annotations in utility functions

### Remediation Requirements
Each violation must be addressed before merge:
1. Replace 'any' with proper types or add justification comment
2. Handle all errors explicitly in Go code
3. Move database queries to repository layer
4. Add index on orders.user_id foreign key
5. Add JSDoc type annotations to JavaScript utilities
```

## 5. Phase 4: Tenet Compliance Review

**🎯 CORE TENET VALIDATION**: Evaluate all code changes against fundamental leyline tenets.

### Simplicity Tenet Review
**"Prefer the simplest design that solves the problem completely"**

**Simplicity Violations to Detect:**
- Clever code where boring would work
- Unnecessary abstractions (factories for single types)
- Over-engineered solutions to simple problems
- Premature optimization without metrics
- Complex inheritance where composition would suffice
- Configuration for values that never change

**Simplicity Score:**
```markdown
✅ SIMPLE: Can explain in one sentence, junior dev would understand
⚠️ MODERATE: Some complexity justified by requirements
❌ COMPLEX: Over-engineered, needs simplification
```

### Explicitness Tenet Review
**"Explicit over implicit - make behavior obvious"**

**Implicit Behavior to Flag:**
- Hidden dependencies not visible in signatures
- Side effects not obvious from function names
- Global state mutations
- Magic numbers without context
- Implicit type conversions
- Undocumented assumptions

**Explicitness Checklist:**
- [ ] All dependencies visible in function signatures
- [ ] Return types clearly specified
- [ ] Side effects obvious from naming
- [ ] No hidden global state access
- [ ] Configuration explicit and documented

### Modularity Tenet Review
**"Build independent, focused components"**

**Modularity Violations:**
- God classes/modules doing everything
- Tight coupling between unrelated components
- Circular dependencies
- Mixed concerns in single module
- Lack of clear boundaries
- Components not testable in isolation

**Module Health Check:**
```yaml
Single Responsibility: Each module has one clear purpose
Loose Coupling: Modules interact through interfaces
High Cohesion: Related functionality grouped together
Clear Boundaries: Obvious what belongs where
Independent Testing: Can test without dependencies
```

### Maintainability Tenet Review
**"Write for the future developer (probably you in 6 months)"**

**Maintainability Red Flags:**
- Cryptic variable names (a, temp, data, thing)
- Missing documentation for complex logic
- Inconsistent patterns in similar code
- No clear extension points for likely changes
- Copy-paste code that should be extracted
- Deep nesting making code hard to follow

**Future Developer Test:**
```markdown
✅ MAINTAINABLE: Clear intent, obvious extension points, well-documented
⚠️ UNCLEAR: Needs some documentation or refactoring
❌ CRYPTIC: Would require archaeology to modify
```

### Tenet Compliance Scoring Matrix

| Tenet | Weight | Pass Criteria | Current Score |
|-------|--------|--------------|---------------|
| **Simplicity** | 30% | No unnecessary complexity | ✅/⚠️/❌ |
| **Explicitness** | 25% | All behavior obvious | ✅/⚠️/❌ |
| **Modularity** | 25% | Clean boundaries | ✅/⚠️/❌ |
| **Maintainability** | 20% | Future-proof code | ✅/⚠️/❌ |

### Tenet Review Output
```markdown
## Tenet Compliance Assessment

### 🎯 Simplicity (Score: 7/10)
✅ Straightforward implementation in UserService
✅ Clear, linear flow in authentication logic
❌ Over-engineered factory pattern in NotificationBuilder
❌ Unnecessary abstraction layers in data access

### 🎯 Explicitness (Score: 8/10)
✅ Clear function signatures with typed parameters
✅ Explicit error handling throughout
⚠️ Some magic numbers in rate limiting logic
❌ Hidden dependency on global config in Logger

### 🎯 Modularity (Score: 6/10)
✅ Clean separation of API and business logic
⚠️ Some coupling between user and auth modules
❌ Circular dependency between order and inventory
❌ God class in ApplicationController

### 🎯 Maintainability (Score: 7/10)
✅ Well-documented public APIs
✅ Consistent naming conventions
⚠️ Complex nested logic in payment processing
❌ Copy-pasted validation logic across controllers

### Overall Tenet Compliance: 70% (NEEDS IMPROVEMENT)

### Critical Tenet Violations Requiring Fix:
1. Simplify NotificationBuilder - remove factory pattern
2. Extract magic numbers to named constants
3. Break circular dependency between order/inventory
4. Extract shared validation logic to utilities
```

## 6. Categorize Findings

### BLOCKERS (This Will Burn In Production)
- Security vulnerabilities that will get us pwned
- Data loss scenarios that will lose customer data
- Performance issues that will take down the server
- Breaking changes with no migration path
- Unhandled errors that will crash everything

### IMPROVEMENTS (Should Fix Before Someone Notices)
- Code that works but makes no sense
- Missing tests for critical paths
- Performance optimizations we're ignoring
- Documentation that's wrong or missing
- Technical debt we're accumulating

### POLISH (Nice To Have If We Cared)
- Style inconsistencies
- Better naming conventions
- Refactoring opportunities
- Enhanced logging

## 5. Generate TODO.md Items

**Add all BLOCKERS with Linus-level clarity**:
```markdown
## Code Review Blockers - [Branch/PR Name] [Date]

- [ ] [CRITICAL] Fix SQL injection in user search - currently concatenating user input like it's 1999
- [ ] [CRITICAL] Add ANY tests for payment processing - zero coverage on code handling actual money
- [ ] [CRITICAL] Fix O(n²) algorithm in notifications - will melt server with >1000 users
- [ ] [CRITICAL] Handle network timeouts - currently just praying the network never fails
```

## 6. Output Summary

```markdown
## Review Summary

### What I Half-Assed
- [Honest admission of shortcuts taken]
- [Features that barely work]
- [Code I copied without understanding]

### Magical Thinking & Hallucination Bullshit
- [Assumptions that are definitely wrong]
- [Code that works by accident]
- [Things I pretended to understand]

### What Would Make Linus Rage
- [The absolutely broken garbage]
- [Security holes you could drive a truck through]
- [Performance disasters waiting to happen]

### Tests That Would Actually Prove It Works
- [Specific test cases that would expose the bugs]
- [Edge cases I'm definitely not handling]
- [Load tests that would break everything]

### Merge Decision: [BLOCKED/APPROVED]
[Clear explanation of why this should or shouldn't merge]
```

## Success Criteria

✓ Code is cleaned up and properly documented
✓ Brutal honest assessment completed
✓ All magical thinking exposed
✓ BLOCKERS identified with clear explanations
✓ TODO.md updated with critical items
✓ No sugar-coating or false confidence