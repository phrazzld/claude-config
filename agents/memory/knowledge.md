# Quick Reference Knowledge

This file contains actionable patterns, lessons, and gotchas discovered through development work.

## Code Patterns

### Responsive Design
- **Mobile-first grid**: `grid-cols-1 md:grid-cols-3 lg:grid-cols-4`
- **Container pattern**: `max-w-7xl mx-auto px-4` for wide layouts
- **Button responsive**: `w-full sm:w-auto` for mobile touch targets
- **Flex direction**: `flex-col sm:flex-row` for mobile stacking
- **Text sizing**: `text-2xl md:text-3xl` for responsive typography

### React Patterns  
- **Form validation**: React Hook Form + Zod with FormField wrappers
- **Loading states**: `disabled={isLoading}` with Loader2 spinner
- **Error handling**: Try/catch with toast.error() for user feedback
- **Mutation flow**: useState for loading, setLoading in finally blocks
- **Modal structure**: Dialog -> Content -> Header + Description + Footer

### API Integration
- **Error responses**: HTTP status check + response structure validation
- **Request headers**: Include proper headers (HTTP-Referer, X-Title for OpenRouter)
- **Logging**: Detailed context (puzzleId, year, attempt) for debugging
- **Auth pattern**: Check session token, validate ownership before operations

### Database/Backend
- **Ownership verification**: `resource.userId !== userId` throws unauthorized
- **Soft delete**: Add `deletedAt` timestamp, preserve all original data
- **Validation**: Minimum length checks, field type validation
- **Timestamps**: Always update `updatedAt` on modifications

### Performance
- **Client filtering**: Use useMemo with proper dependencies for real-time search
- **List rendering**: Avoid store subscriptions in list items - causes mass re-renders
- **Theme changes**: Use CSS variables, not React re-rendering
- **Loading optimization**: aria-hidden="true" aria-busy="true" for skeleton states

## Common Gotchas

### Mobile/CSS Issues
- **Fixed-width elements**: Calculate total width vs mobile viewport (320px min)
- **Overflow debugging**: 3 × 140px buttons = 420px > 320px mobile screen
- **Touch targets**: Use full-width buttons on mobile for easier tapping

### Authentication/IDs
- **Auth context confusion**: User object has `id` field, not `_id`  
- **Database records**: Use `_id` in database queries, `id` for auth context
- **Ownership checks**: `question.userId === user.id as Id<"users">`

### Testing/Development
- **Convex mutations**: Use `._handler` property, not `.handler` for unit tests
- **N+1 performance**: Store hooks in list items cause 367 re-renders → 0 with CSS variables
- **Pattern discovery**: Always use pattern-scout first - prevents reinventing solutions

### API/External Services
- **Third-party auth**: Always add 100% time buffer - provider quirks inevitable
- **Migration tasks**: Need rollback plan + multi-environment testing
- **Performance work**: Set up measurement infrastructure before optimization

## Good Questions to Ask

### Before Implementation
- "What's the mobile experience for this feature?"
- "How does this fail gracefully when the API is down?"
- "What assumptions am I making about user data?"
- "What should happen with duplicate/concurrent requests?"
- "If one item in a batch fails, should the whole operation rollback?"

### During Code Review
- "Are we handling the loading state properly?"
- "What happens when this component receives null/undefined data?"
- "Is this accessible to screen readers?"
- "Will this cause re-renders in parent components?"
- "Are we following the established error handling pattern?"

### Architecture Decisions
- "Does this need to scale beyond the current team size?"
- "What's the rollback strategy if this goes wrong?"
- "Are we over-engineering this for a simple use case?"
- "What similar decisions have we made before and how did they work out?"

## Time Estimation Wisdom

### Consistently Fast (1-5 minutes)
- Convex optional field additions with existing patterns
- Configuration changes with clear precedent  
- Component positioning following established patterns
- Copy/paste implementations with minor modifications

### Consistently Simple (10-15 minutes)
- Modal forms with established component library
- UI features when backend mutations already exist
- Layout changes with existing CSS Grid structure
- Enhanced filtering with existing search patterns

### Consistently Medium (15-45 minutes)  
- External API integrations with discovered patterns
- Convex mutations following established auth patterns
- Multi-task implementations with clear integration hooks
- Comprehensive unit test suites with established testing patterns

### Always Add Buffer For
- Third-party integrations (100% buffer minimum)
- Database migrations (50% buffer for rollback planning)  
- Performance optimization (add measurement setup time)
- E2E test suites (50% buffer for flaky test debugging)

### Trust Pattern-Scout When
- 95%+ confidence = implementation should be trivial
- Exact component locations found = accurate simple estimates
- Same-service API patterns discovered = direct adaptation possible
- Well-organized existing structure = minimal refactoring needed

## Architecture Lessons

### What Works
- **Mobile-first CSS**: Prevents overflow issues, easier to scale up than down
- **Pattern-first development**: Always search for existing solutions before building
- **Simple ownership model**: User-based permissions over complex RBAC for personal tools
- **CSS Grid over complex calculations**: Modern CSS features often simplify assumed complexity
- **No-internal-mocking testing**: Realistic test implementations more valuable than mocks

### What Doesn't Work
- **Store hooks in list items**: Causes mass re-renders (367 → 0 with CSS variables)
- **String concatenation for shell commands**: Creates injection vulnerabilities - use subprocess arrays
- **Complex status models**: Three-state models often unnecessary in single-user systems
- **Over-engineered confidence scoring**: Metadata maintenance exceeds utility value
- **Fixed-width mobile layouts**: Calculate total width requirements vs viewport constraints

### When to Keep It Simple
- Personal tools favor binary states over multi-state models
- Well-organized codebases need minimal changes with modern CSS
- Copy existing patterns rather than creating new ones
- Trust simple solutions when existing structure is already good
- Use established component libraries instead of custom implementations

## Performance Baselines

### Component Rendering
- **Before optimization**: 285ms visual completion, 367 component re-renders
- **After CSS variables**: 185ms completion (35% faster), 0 component re-renders
- **Affected elements**: 1000+ transitioning DOM reduced to ~20

### Development Speed  
- **With pattern-scout**: 10 minutes for comprehensive filtering UI
- **With existing patterns**: 15 minutes for external API integration
- **Without patterns**: 45+ minutes for same complexity features

### Testing Coverage
- **Comprehensive CRUD testing**: 45 minutes for 22 tests with authentication, data preservation, edge cases
- **Unit test setup**: TestConvexDB simulation enables realistic testing without internal mocks
- **Authentication testing**: Multiple user scenarios and permission matrix coverage essential

---

*Updated: Daily as new patterns and lessons are discovered*