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

**Technology-Specific Bindings to Validate:**
```yaml
TypeScript/JavaScript (.ts, .tsx, .js, .jsx):
  ✓ No use of 'any' without justification
  ✓ Explicit type annotations where needed
  ✓ Strict null checks compliance
  ✓ No implicit any returns
  ✓ Proper error boundaries in React

Go (.go):
  ✓ All errors explicitly handled (no _ ignoring)
  ✓ Context propagation in API calls
  ✓ Interface segregation principle followed
  ✓ Embedded struct composition over inheritance
  ✓ Defer statements for cleanup

Python (.py):
  ✓ Type hints for function signatures
  ✓ Docstrings for public functions
  ✓ No bare except clauses
  ✓ Context managers for resources

SQL/Migrations (.sql):
  ✓ Foreign key constraints defined
  ✓ Indexes on queried columns
  ✓ NOT NULL constraints by default
  ✓ Consistent naming conventions
  ✓ No SELECT * in production code
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

## 5. Categorize Findings

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