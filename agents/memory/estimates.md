# Task Estimation Memory

This file tracks task estimates vs actual completion times to improve future estimation accuracy.

## Structure

Each entry includes:
- **Task Type**: Category of work
- **Estimated Complexity**: Initial estimate  
- **Actual Time**: How long it really took
- **Accuracy**: How close the estimate was
- **Factors**: What affected the estimate
- **Learning**: Pattern to remember
- **Times referenced**: How often this pattern is consulted
- **Last used**: When this pattern was last referenced (YYYY-MM-DD)

---

## Example Patterns (From Common Projects)

## API Development: CRUD Endpoints
**Estimated**: MEDIUM (4-8 hours)
**Actual**: 3 hours
**Accuracy**: 75% (overestimated)
**Factors**: Existing patterns made it faster, good ORM abstractions
**Learning**: CRUD with existing patterns is usually SIMPLE (2-4 hours)
**Confidence Adjustment**: Reduce CRUD estimates by 25% when patterns exist
**Times referenced**: 0
**Last used**: Never

## Authentication: OAuth2 Integration
**Estimated**: MEDIUM (8 hours)
**Actual**: 16 hours  
**Accuracy**: 50% (underestimated)
**Factors**: Provider documentation issues, session management complexity, testing edge cases
**Learning**: Third-party auth is always COMPLEX minimum
**Confidence Adjustment**: Double auth-related estimates, add buffer for provider quirks
**Times referenced**: 0
**Last used**: Never

## Database: Schema Migration
**Estimated**: SIMPLE (2 hours)
**Actual**: 5 hours
**Accuracy**: 40% (underestimated)
**Factors**: Rollback strategy needed, data validation issues, staging environment testing
**Learning**: Migrations need rollback plan and multi-environment testing
**Confidence Adjustment**: Add 50% buffer to all migration estimates
**Times referenced**: 0
**Last used**: Never

## Frontend: Component with Design System
**Estimated**: MEDIUM (4 hours)
**Actual**: 2 hours
**Accuracy**: 50% (overestimated)
**Factors**: Design system had most patterns, just composition needed
**Learning**: With good design system, UI work is usually SIMPLE
**Confidence Adjustment**: Reduce UI estimates by 50% when design system exists
**Times referenced**: 0
**Last used**: Never

## Performance: Query Optimization
**Estimated**: MEDIUM (4 hours)
**Actual**: 8 hours
**Accuracy**: 50% (underestimated)
**Factors**: Needed profiling setup first, multiple iterations to hit target
**Learning**: Performance work needs measurement infrastructure first
**Confidence Adjustment**: Add measurement setup time to performance tasks
**Times referenced**: 0
**Last used**: Never

## Testing: E2E Test Suite
**Estimated**: COMPLEX (2 days)
**Actual**: 3 days
**Accuracy**: 67% (underestimated)
**Factors**: Test data setup complexity, flaky test debugging, CI integration
**Learning**: E2E tests always have hidden complexity in setup and stability
**Confidence Adjustment**: Add 50% buffer for test infrastructure and debugging
**Times referenced**: 0
**Last used**: Never

---

## Patterns by Complexity Level

### Consistently SIMPLE (1-2 hours)
- README updates
- Configuration changes
- Adding single API endpoint with existing pattern
- UI components with design system
- Bug fixes with clear reproduction

### Consistently MEDIUM (4-8 hours)
- New feature with 2-3 components
- Database table with basic CRUD
- Integration tests for feature
- API client wrapper
- Refactoring within single module

### Consistently COMPLEX (1-3 days)
- Authentication implementation
- Payment integration
- Database migration with data transformation
- Cross-service communication
- Performance optimization with measurement

### Consistently VERY_COMPLEX (3+ days)
- Architectural refactoring
- Distributed system changes
- Security audit and fixes
- Multi-tenant implementation
- Breaking API migration

---

## Adjustment Factors

### Add 50% Buffer When:
- Working with unfamiliar technology
- Integrating third-party services
- Database migrations involved
- Cross-browser compatibility required
- Security requirements present

### Add 100% Buffer When:
- Distributed systems involved
- Breaking changes required
- Multiple team coordination needed
- Compliance requirements present
- Performance SLAs defined

### Reduce by 25% When:
- Strong existing patterns available
- Similar feature already implemented
- Good test coverage exists
- Working in familiar codebase
- Clear requirements with no ambiguity

---

<!-- New estimation patterns will be added below this line as they prove accurate or inaccurate -->