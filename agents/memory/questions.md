# Requirements Questions Memory

This file tracks valuable clarifying questions that prevented rework across projects.

## Structure

Each entry includes:
- **Question**: The actual question asked
- **Domain**: Type of project/feature
- **Value**: 0-100 score based on rework prevented
- **Impact**: What issue it prevented
- **Pattern**: Reusable question template
- **Usage Count**: Times this pattern was valuable

---

## Example Patterns (High-Value Questions)

## API Development: REST Endpoint Design
**Question**: Should this endpoint be idempotent, and how should we handle duplicate requests?
**Value**: 85
**Impact**: Prevented race condition bugs and duplicate processing issues
**Pattern**: "How should [operation] handle duplicate/concurrent requests?"
**Usage Count**: 12

## Data Processing: Input Validation
**Question**: What should happen when the system receives malformed or incomplete data?
**Value**: 90
**Impact**: Prevented crashes and data corruption, clarified error handling strategy
**Pattern**: "What's the failure behavior for invalid [input type]?"
**Usage Count**: 18

## Authentication: Session Management
**Question**: What should happen to active user sessions when permissions change?
**Value**: 75
**Impact**: Prevented security vulnerability where revoked users maintained access
**Pattern**: "How should active [sessions/connections] handle [permission/state] changes?"
**Usage Count**: 8

## Search Features: Query Behavior
**Question**: Should search be case-sensitive, and should it support partial matches?
**Value**: 60
**Impact**: Prevented UX confusion and rework of search implementation
**Pattern**: "What are the exact matching rules for [search/filter/query]?"
**Usage Count**: 15

## Batch Operations: Transaction Boundaries
**Question**: If one item in a batch fails, should the entire operation rollback or continue?
**Value**: 95
**Impact**: Prevented data inconsistency and complex recovery scenarios
**Pattern**: "What's the transaction boundary and failure behavior for batch [operation]?"
**Usage Count**: 10

## Performance: Scale Requirements
**Question**: What's the expected data volume and concurrent user load in production?
**Value**: 80
**Impact**: Prevented architecture rework when initial design couldn't scale
**Pattern**: "What are the specific performance targets for [metric] at [scale]?"
**Usage Count**: 14

## Integration: External Dependencies
**Question**: What happens when the external service is unavailable or times out?
**Value**: 85
**Impact**: Prevented production outages from unhandled dependency failures
**Pattern**: "What's the fallback behavior when [external service] is unavailable?"
**Usage Count**: 11

## Data Migration: Rollback Strategy
**Question**: How do we rollback if the migration fails partway through?
**Value**: 90
**Impact**: Prevented data loss and extended downtime during failed migration
**Pattern**: "What's the rollback strategy if [migration/deployment] fails?"
**Usage Count**: 7

---

## Domain-Specific Patterns

### E-commerce
- "How should the system handle inventory conflicts during concurrent checkouts?"
- "What happens to cart contents when prices change?"
- "Should tax calculation happen at cart-time or checkout-time?"

### Real-time Systems
- "What's the maximum acceptable latency for updates?"
- "How should the system handle message ordering conflicts?"
- "What's the strategy for handling network partitions?"

### File Processing
- "What's the maximum file size we need to support?"
- "Should processing be synchronous or asynchronous?"
- "How do we handle partial failures in multi-file uploads?"

### Reporting/Analytics
- "What's the data freshness requirement (real-time vs batch)?"
- "How should the system handle retroactive data corrections?"
- "What are the data retention and archival requirements?"

---

<!-- New question patterns will be added below this line as they prove valuable -->