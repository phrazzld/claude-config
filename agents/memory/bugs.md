# Bug Memory Database

This file maintains a persistent memory of encountered bugs and their solutions.

## Structure

Each entry follows this format:
- **Fingerprint**: Key identifying characteristics
- **First seen**: Date first encountered
- **Times encountered**: How often we've seen this
- **Solution**: What fixed it
- **Files affected**: Where the issue occurred
- **Prevention**: How to avoid in future

---

## Example Entry (Remove after first real bug)

## [TypeError]: Cannot read property 'x' of undefined
**Fingerprint**: Accessing nested object property without null checks
**First seen**: 2024-01-01
**Times encountered**: 1
**Solution**: Add optional chaining (?.) or null checks before property access
**Files affected**: api/user.service.ts
**Prevention**: Use TypeScript strict null checks, add validation at API boundaries

---

## [Performance]: N+1 Subscription Anti-Pattern in List Components
**Fingerprint**: Each item in a mapped list subscribes to global store causing mass re-renders on state change
**First seen**: 2025-08-27 (vanity project)
**Times encountered**: 1
**Solution**: 
1. Remove individual store subscriptions (useTheme/useStore hooks) from list item components
2. Replace inline theme-dependent styles with CSS custom properties
3. Wrap components with React.memo to prevent prop-based re-renders
4. Use CSS cascade for theme changes instead of React re-rendering

**Files affected**: 
- src/app/components/readings/ReadingCard.tsx (367 instances)
- src/app/components/quotes/QuotesList.tsx (unused subscription)
- src/store/ui.ts (theme store)

**Prevention**: 
- ESLint rule added to warn against store hooks in *Card.tsx, *Item.tsx, *List*.tsx files
- Use CSS variables for theme-dependent styles
- Subscribe to stores at list container level, not item level
- Performance test: Theme toggle should not trigger item re-renders

**Performance impact**:
- Before: 285ms visual completion, 367 component re-renders
- After: 185ms visual completion (35% faster), 0 component re-renders
- Affected 1000+ transitioning DOM elements reduced to ~20

---

## [Testing]: Convex Mutation Handler Access Error
**Fingerprint**: Attempting to access Convex mutation handler function with .handler property returns undefined during unit testing
**First seen**: 2025-08-28
**Times encountered**: 1
**Solution**: Use `._handler` property instead of `.handler` to access the actual mutation function. Convex mutations expose their handler via `_handler`, not `handler`. Pattern: `mutationName._handler(ctx, args)`
**Files affected**: 
- /Users/phaedrus/Development/scry/convex/questions.crud.test.ts (discovered during test implementation)
- Any Convex unit tests that need to invoke mutations directly
**Prevention**: 
- Document the `._handler` pattern in testing patterns memory
- Always use `._handler` for Convex mutation testing
- Consider this an internal API that may change - verify pattern with Convex documentation updates
- Add to testing guidelines: Convex mutations use `_handler` property for direct invocation in tests

**Debug Process**:
- Initial attempt: `updateQuestion.handler(ctx, args)` returned undefined
- Inspection revealed `_handler` property existed
- `updateQuestion._handler(ctx, args)` worked correctly
- Pattern confirmed across all mutation functions

**Testing Impact**:
- Critical for unit testing Convex mutations
- Enables proper test coverage of business logic
- Allows realistic database simulation without mocking internal components
- Supports comprehensive CRUD operation testing

---

<!-- New bugs will be added below this line -->