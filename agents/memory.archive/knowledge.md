# Quick Reference Knowledge

This file contains actionable patterns, lessons, and gotchas discovered through development work.

## Code Patterns

### Constants Array Patterns
- **Object array constants**: `[{ value: "key", label: "Display" }] as const` for dropdowns and selects
- **String array constants**: `["item1", "item2", "item3"] as const` for enums and validation
- **Nested object constants**: Complex structures with typed fields for configuration objects
- **Export pattern**: `export const CONSTANT_NAME = [...] as const;` for shared constants
- **Type inference**: Use `as const` to get literal types instead of string[]
- **Naming convention**: SCREAMING_SNAKE_CASE for exported constants, camelCase for local
- **File organization**: Separate constants.ts files for complex configurations

### Environment Variable Feature Flags
- **Server-side environment detection**: Use `process.env.VERCEL_ENV` with fallback to 'development' - supports production/preview/development tiers
- **Client-side environment detection**: Browser-safe hostname-based detection for when `process.env` unavailable
- **Boolean flag pattern**: `const isFeatureEnabled = !!process.env.FEATURE_FLAG_NAME` or `!process.env.DISABLE_FEATURE`
- **Conditional rendering pattern**: `pathname === '/' ? null : <Component />` - perfect template for feature flag conditionals
- **Environment-based ternary**: `process.env.NODE_ENV === 'production' ? prodValue : devValue` for config switching
- **Layout rollback pattern**: Preserve legacy layout structures in git history, enable via environment variable conditionals
- **Feature flag coexistence pattern**: Both implementations exist in same codebase with conditional class names
- **Safe rollback environment variables**: Use `NEXT_PUBLIC_` prefix for client-side access, default to new behavior when undefined
- **Conditional class functions**: `cn("base-classes", flag ? "new-layout" : "legacy-layout")` for style switching
- **Component spacer conditionals**: Only render spacer divs when legacy mode active, eliminates them for new layouts

### CSS Grid Layout System
- **Three-row grid template**: `grid-template-rows: auto 1fr auto` for header/main/footer structure
- **Mobile viewport optimization**: Use both `100vh` and `100dvh` for dynamic viewport height support
- **Grid children safeguards**: `min-width: 0` prevents overflow issues with text and images
- **Legacy layout preservation**: Fixed positioning with manual spacer divs (pre-CSS Grid) perfectly preserved in git history
- **Sticky vs fixed positioning**: Sticky navbar (`sticky top-0`) eliminates need for manual spacing compensation
- **Layout migration history**: Commits a6ed177 (CSS Grid implementation) and d36c467 (navbar/footer updates) contain complete migration patterns

### Security by Default
- **Rules Engine pattern**: Default to fail when no data provided - `return false` instead of `return true` for unknown states
- **Verification principle**: "No data = cannot verify = fail" - restrictive defaults prevent security bypasses
- **Permission inversion**: Change from permissive defaults to restrictive - single line with massive security impact
- **Critical behavior comments**: Document reasoning for security-critical default behaviors in code
- **Question categorization pattern**: Group questions by risk level (required vs optional) rather than adding flags to each individual question
- **Early exit leverage**: Use existing fail-fast logic (stopOnFail) to naturally handle missing required data

### Responsive Design
- **Mobile-first grid**: `grid-cols-1 md:grid-cols-3 lg:grid-cols-4`
- **Container pattern**: `max-w-7xl mx-auto px-4` for wide layouts
- **Button responsive**: `w-full sm:w-auto` for mobile touch targets
- **Flex direction**: `flex-col sm:flex-row` for mobile stacking
- **Text sizing**: `text-2xl md:text-3xl` for responsive typography

### AI Historical Context Integration
- **OpenRouter API configuration**: Use `google/gemini-2.5-flash` model with structured prompts for historical narrative generation
- **Retry logic with exponential backoff**: `calculateBackoffDelay()` with jitter, max 3 attempts for network resilience
- **Server-side action pattern**: Convex internal actions for external API calls with proper error handling and logging
- **Historical context storage**: Store AI-generated context in puzzle records via internal mutations after generation
- **Prompt engineering structure**: System role + user prompt with era establishment → year specifics → creative ending pattern
- **API headers for tracking**: Include `HTTP-Referer` and `X-Title` headers for OpenRouter request identification

### Mobile Input Configuration
- **Numeric keyboard activation**: Use `type="text"` with `inputMode="numeric"` for mobile number keyboards without validation constraints
- **Input accessibility**: `aria-label="Enter your year guess. Use arrow keys to increment or decrement. Use negative numbers for BC years."`
- **Touch target sizing**: `h-12` minimum height for mobile touch targets, `w-full sm:w-auto` responsive width
- **Keyboard navigation**: Arrow keys for increment/decrement with Shift modifier for ±10 year jumps
- **Auto-focus management**: `useEffect` to focus input on mount and after successful submission with `setTimeout` for DOM updates

### Timeline and Hint Display Components
- **SVG timeline with responsive viewBox**: `viewBox="0 25 800 50"` with `preserveAspectRatio="xMidYMid meet"` for consistent scaling
- **Animation optimization**: `useReducedMotion()` hook to respect accessibility preferences and disable animations
- **Memory optimization**: Custom `areHintsDisplayPropsEqual` function for React.memo to prevent unnecessary re-renders
- **Mobile-responsive text**: `text-lg sm:text-xl` and `text-sm sm:text-sm` patterns for adaptive text sizing
- **Progressive hint revelation**: Current hint at top, past hints in reverse chronological order below
- **Proximity feedback integration**: Temperature emojis (🎯🔥♨️🌡️❄️🧊) with accessibility labels for guess feedback

### Data Migration and Backfill Patterns
- **Batch processing with delays**: Process records in configurable batch sizes with delays between batches to avoid API rate limits
- **Dry run capability**: `dryRun` parameter to count and preview changes without execution
- **Test mode for single records**: `testMode` with optional specific record targeting for validation
- **Progress tracking**: Detailed logging with batch progress, success/error counts, and estimated completion times
- **Scheduler-based processing**: Use Convex scheduler (`ctx.scheduler.runAfter`) for delayed execution with staggered processing
- **Query filtering and sorting**: Filter by missing fields, sort by consistent criteria (puzzleNumber), apply limits for controlled processing
- **Error handling with statistics**: Track processed/scheduled/error counts with detailed error logging for debugging

### CLI Tool Architecture for Data Management
- **Commander.js structure**: Subcommands with shared options, validation, and error handling
- **Environment loading**: `dotenv` with `.env.local` file loading for database connection configuration
- **Rich terminal output**: Color-coded status (green/yellow/red), progress indicators, formatted tables
- **Protective mutations**: Check for existing usage (puzzle references) before allowing destructive operations
- **Batch operations**: Support for single record and bulk operations with proper validation
- **Interactive verification**: `verify` and `validate` commands to check system state and data integrity

### React Hook Optimization Patterns
- **Config object useMemo**: Wrap configuration objects to prevent recreation: `const config = useMemo(() => ({ ...options }), [dep1, dep2])`
- **Stable dependencies**: Use JSON.stringify for complex options: `const optionsKey = JSON.stringify(options)` then `[optionsKey]` in deps
- **useCallback with refs**: Dependencies include refs when using their current value: `[config, dispatch, showTypingIndicator]`
- **Function memoization**: Return functions from useMemo: `return useMemo(() => (amount) => formatCurrency(amount, options), [options])`
- **Debounced functions**: Wrap in useMemo, not useCallback: `const debouncedFn = useMemo(() => { const fn = (...) => {...}; return fn; }, [deps])`

### React Hook Form Patterns
- **Form initialization with zodResolver**: `const form = useForm<T>({ resolver: zodResolver(schema), mode: 'onTouched', defaultValues: {...} })`
- **Memoized form config**: `const formConfig = useMemo(() => ({ resolver: zodResolver(schema), defaultValues: {...}, mode: 'onTouched' as const }), [])`
- **Form structure with sections**: Organize complex forms with section components like `<PersonalInformationSection />`, `<AddressInformationSection />`
- **FormProvider wrapper**: Use `<FormProvider {...form}>` to provide form context to child components
- **Complex validation with superRefine**: Use `.superRefine()` for conditional validation based on other field values
- **Controller for custom inputs**: Use `<Controller />` from react-hook-form for complex UI components that don't work with register
- **FormField with shadcn/ui**: Use `<FormField render={() => <FormItem><FormLabel /><FormControl><Input /></FormControl><FormMessage /></FormItem>} />` pattern
- **Error display with FormMessage**: Automatic error display with `<FormMessage />` component that shows field validation errors
- **Custom hooks for form logic**: Extract form setup, validation, and submission to custom hooks like `useHouseholdFormSetup()`, `useFormSubmission()`
- **Form submission with FormData**: Build FormData in submission handler for API compatibility: `formData.append('field', value)`
- **Watch form changes**: Use `form.watch()` to monitor form state changes and trigger side effects
- **Conditional field visibility**: Show/hide form sections based on form state using `selectedHousehold ? <SelectedSection /> : <AddressSection />`
- **Form reset after success**: Clear form data with `reset({ defaultValues })` after successful submission
- **Loading states during submission**: Use `fetcher.state === 'submitting'` or custom `isSubmitting` state
- **Validation contexts**: Create validation providers like `<FormValidationProvider>` for cross-field validation
- **Real-time validation**: Set `mode: 'onBlur'` and `reValidateMode: 'onChange'` for progressive validation

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

### FSRS Soft Delete Patterns
- **Soft delete data integrity**: Use `deletedAt: Date.now()` to preserve all FSRS fields (stability, difficulty, nextReview, state, etc.)
- **Restoration pattern**: Remove `deletedAt` field via `{ deletedAt: undefined }` to restore questions intact
- **Query filtering pattern**: Use `.filter(q => q.eq(q.field("deletedAt"), undefined))` to exclude deleted questions from review queues
- **Retrievability preservation**: Deleted/restored questions maintain FSRS calculations unchanged - only time passage affects retrievability
- **Test simulation pattern**: Use object spread with `deletedAt` addition/removal to simulate soft delete operations in tests

### FSRS Testing Patterns
- **Mock question factory**: `createMockQuestion(overrides)` pattern with required fields and spread overrides
- **Prioritization simulation**: Extract core logic from queries into testable functions with `retrievability` scoring
- **Time-based scenarios**: Use fixed dates (`new Date('2025-01-16T12:00:00Z')`) for consistent test results
- **FSRS field validation**: Preserve all FSRS state fields (stability, difficulty, elapsedDays, scheduledDays, reps, lapses, state, lastReview, nextReview) through operations
- **Permission test matrix**: Test creator-only permissions across all mutations with scenario-based testing

### Performance
- **Client filtering**: Use useMemo with proper dependencies for real-time search
- **List rendering**: Avoid store subscriptions in list items - causes mass re-renders
- **Theme changes**: Use CSS variables, not React re-rendering
- **Loading optimization**: aria-hidden="true" aria-busy="true" for skeleton states

### File Processing & Validation
- **Multi-stage validation**: Pre-flight → Format compliance → Quality analysis → Auto-processing
- **Comprehensive error extraction**: Parse JSON errors, categorize headers, log structured data
- **Asset path generation**: Use service patterns with retry logic and structured logging
- **File format detection**: Check headers, validate against patterns, support multiple formats
- **Batch processing with rollback**: Track individual results, enable partial success recovery

### CLI Command Architecture
- **Commander.js structure**: Main program → subcommands → action handlers with shared options
- **Rich terminal feedback**: ora spinners + chalk colors + progress indicators
- **Environment handling**: Config hierarchy (flags → files → env → defaults)
- **Mock mode support**: Bypass external dependencies for testing/development
- **Screenshot debugging**: Automated screenshots on errors for browser automation

### Publishing Pipeline Patterns
- **Configuration validation**: Credentials → file existence → format compliance → publishing readiness
- **Playwright automation**: Login → 2FA handling → form filling → file uploads → result extraction
- **Metadata-driven workflow**: YAML parsing → validation → template processing → multi-format output
- **Error recovery tiers**: Auto-fix → semi-auto → manual intervention with actionable feedback
- **Progress reporting**: Stage tracking → detailed logging → final status reports

### Template & Asset Management
- **SVG template processing**: Variable replacement (`{{VAR}}`) + conditional sections + color schemes
- **Multi-format templates**: EPUB, PDF (LaTeX), Kindle with shared metadata
- **Asset organization**: Structured paths (books/slug/covers/ebook/validated/) with status tracking
- **Blob storage patterns**: Batch uploads + path services + URL generation + existence checking

### SessionStorage & State Persistence
- **Browser safety check**: `typeof window !== 'undefined' && typeof window.sessionStorage !== 'undefined'`
- **Safe storage operations**: Try/catch with fallback behavior on quota exceeded errors
- **Structured data interfaces**: Versioned interfaces with `lastUpdated` and `version` fields
- **Validation functions**: Comprehensive type guards with `message is Type` patterns
- **Automatic cleanup**: Quota management with oldest-first removal strategy
- **Key management**: Consistent key generation functions and storage key patterns

### Fact Collection & Validation
- **TypeScript interfaces**: Structured fact collection with validation metadata
- **Readiness assessment**: Confidence scoring (0-100%) with area-based status tracking
- **Missing data detection**: `criticalMissing` arrays for targeted follow-up questions
- **Sufficiency checking**: Boolean determination if enough facts collected for decisions
- **Session persistence**: Automatic fact storage across page refreshes and navigation

### Step-Based Progress Indicators
- **Step interface pattern**: `{ label: string, description: string, icon: ReactNode, index: number }`
- **Visual step rendering**: Circle icon with check state, connected by lines, labeled with description
- **Status-based styling**: `active`, `finished`, and `pending` states with color coding
- **Progress calculation**: `currentStep > stepNumber` determines completion state
- **Icon state management**: Show check icon for completed, step icon for active/pending

### Conditional Button Disabling
- **Multiple condition pattern**: `disabled={isLoading || !inputMessage.trim() || !sufficientFacts}`
- **Data validation pattern**: `disabled={currentData.length === 0}` for export buttons
- **Loading state pattern**: `disabled={isSubmitting}` with loading spinner
- **Form validation pattern**: `disabled={!form.isValid}` with error display

### Progress Display Patterns
- **Numeric progress**: "2 of 4 facts verified" using `${current} of ${total}` format
- **Fact counting**: Use `.factCount` from structured data for real-time progress
- **Status indicators**: Color-coded badges (`text-blue-600` checking, `text-green-600` complete)
- **Inline notifications**: Progress banners with `animate-in fade-in slide-in-from-top-2` transitions

### Always-Visible Progress Indicators
- **Persistent status display**: Show progress continuously, not gated behind buttons or actions
- **Amber/warning state pattern**: Use `text-amber-600` and warning icons for incomplete states
- **Icon-based status visualization**: Clock icons for in-progress, checkmark for complete
- **Auto-redirect detection**: When system redirects automatically, eliminate "continue" button assumptions
- **SessionStorage integration pattern**: `const [facts, setFacts] = useState(() => getFacts(orgId))` for React state initialization

### Text Processing & Pattern Matching
- **State abbreviation regex**: Use negative lookbehind to exclude common words: `/\b(?<!in |or |me |to )[A-Z]{2}\b/g`
- **Natural language parsing**: Account for context - "IN" in "in California" vs "Indiana" requires sophisticated exclusion
- **Data extraction validation**: Always test patterns against realistic text, not just ideal cases
- **Common word exclusions**: Build exclusion lists for ambiguous patterns (in, or, me, to, if, is, etc.)

### AI Prompt Engineering
- **Behavior control through instructions**: Small text changes can fundamentally alter AI behavior patterns
- **Fact-gathering patterns**: "Gather facts before determination" vs "make inference" changes entire workflow
- **Instruction clarity prevents tool misuse**: Explicit constraints prevent premature tool calling
- **Sequential requirement patterns**: Force information gathering before decision-making tools

### Server-Side Tool Validation
- **Server-side fact extraction**: Extract facts from tool parameters rather than sessionStorage in edge runtime environments
- **Early return validation pattern**: Check fact sufficiency before expensive tool operations with clear user messaging
- **Tool parameter parsing**: Use tool call parameters as data source for validation instead of external storage
- **Edge runtime constraints**: Cannot access browser storage APIs (sessionStorage/localStorage) in server-side tools
- **Fact counting validation**: Simple numeric checks (e.g., `facts.length >= 3`) for tool gating logic

### API Route Testing
- **SSE route testing**: Mock at HTTP boundary using `setupMockFetch`, test SSE headers (`text/event-stream`, `Cache-Control: no-cache`, `Connection: keep-alive`)
- **Stream response testing**: Use `ReadableStream` with controller to simulate SSE events, parse `event: type\ndata: {...}\n\n` format
- **Tool execution testing**: Test tool result events with proper event types (`tool_result`, `content_manipulation`)
- **Authentication testing**: Mock `getAccessTokenFromRequest` to test both authenticated and unauthenticated flows
- **Error event testing**: Verify error events return 200 status (SSE requirement) with proper error data structure
- **Correlation ID testing**: Ensure all SSE events include correlation IDs for request tracing

### SSE Hook Testing
- **MockEventSource pattern**: Create mock class with event simulation methods (`triggerMessage`, `triggerComplete`, `triggerError`)
- **Connection lifecycle testing**: Test CONNECTING → OPEN → CLOSED states with proper cleanup
- **Dual request mode**: Test both GET (no history) and POST (with history) request patterns
- **Event buffering testing**: Verify events are buffered until complete, then processed as batch
- **Fetch stream parsing**: Test parsing of SSE format from fetch response streams for POST requests
- **Connection reuse testing**: Ensure no duplicate connections when one already exists

### Vitest Environment Configuration
- **Environment specification critical**: Use `environment: 'jsdom'` in vitest.config.ts for DOM testing, not default 'node'
- **Test execution failures**: Environment mismatch causes cryptic errors - wrong environment prevents tests from running
- **Mock utilities require DOM**: `setupMockFetch` and similar utilities need browser-like environment to function properly
- **Configuration verification**: Always verify vitest environment matches test requirements before debugging other issues

### Task Completion Discovery
- **Check existing coverage first**: Always examine existing test files before writing new tests - task may already be complete
- **Pattern scout effectiveness**: Use pattern search tools to quickly identify existing implementations and test coverage
- **Test coverage validation**: Run existing tests to verify functionality already works as expected
- **Quick task verification**: For simple tasks, spend initial minutes verifying current state before implementation

### Rollback Strategy Patterns
- **Complete implementation preservation**: Keep entire legacy implementation in git history for exact restoration
- **Environment variable rollback switches**: Use feature flags that can instantly revert to previous behavior
- **Coexisting implementations**: Both old and new code exist in same codebase, toggled by environment variables
- **Zero-downtime rollbacks**: Environment variable changes enable instant rollback without code deployment
- **Gradual rollout support**: Environment-based flags enable percentage-based or user-based feature rollouts

### Unit Testing Patterns (Vitest)
- **Test file structure**: `describe()` blocks with shared `beforeEach`/`afterEach` setup and cleanup
- **Mock utilities**: Use `setupMockFetch` and `cleanupMockFetch` for HTTP boundary mocking
- **Result type validation**: Use `isOk(result)` and `isErr(result)` pattern with type guards for API responses
- **Shared test data**: Create immutable constants with `Object.freeze()` for consistent test data across tests
- **Test isolation**: Clean up stores, mocks, and state in `afterEach` to prevent test interdependence
- **Custom store cleanup**: Generic cleanup functions with type casting to handle any store type
- **Vitest environment**: Use `jsdom` environment for DOM-based tests, configured in vite.config.ts
- **Mock console**: Include console mocking in test setup to prevent test pollution
- **Test data factories**: Use helper functions to create test data with sensible defaults and override patterns
- **Comprehensive edge cases**: Test boundary conditions, error states, and malformed inputs
- **Security testing**: Dedicated security test suites for authentication and authorization utilities
- **Performance testing**: Include realistic load testing for critical paths like cookie parsing
- **Immutability verification**: Test that operations don't mutate original data structures
- **Custom actions integration**: Test store extensions and custom business logic alongside core functionality

### Rate Limiting & Request Throttling Patterns
- **Timestamp tracking pattern**: Store request timestamps in database tables with indexed date fields (like Scry's `attemptedAt`, `generatedAt`)
- **Time-based window checking**: Use `Date.now()` comparisons with configurable window periods (e.g., "max 5 requests per hour")
- **User-based rate limiting**: Track requests by `userId` field in database queries with time filters
- **IP-based rate limiting**: Log and filter by client IP from request headers (`x-forwarded-for`, `x-real-ip`)
- **Convex action rate limiting**: Implement rate checks in Convex mutations before expensive operations (AI calls, email sends)
- **Error handling for limits**: Return specific error messages and retry information when limits exceeded
- **Exponential backoff pattern**: Client-side retry logic with increasing delays after rate limit hits
- **Request counting with cleanup**: Use periodic cleanup of old timestamps to prevent unbounded growth
- **Different limits per operation**: Separate rate limits for different actions (quiz generation, email sending, authentication)
- **Polling pattern for time-based updates**: Use `usePollingQuery` hook pattern for real-time rate limit status updates

## Common Gotchas

### Environment Variable & Feature Flag Gotchas
- **Client-side process.env limitations**: `process.env` only available server-side; use client-side alternatives for browser context
- **Environment variable caching**: Next.js caches environment variables at build time - runtime changes require rebuild
- **Feature flag race conditions**: Components may render before environment detection completes - handle loading states
- **Layout system rollback complexity**: CSS Grid vs fixed positioning requires different navbar/footer implementations - can't just toggle CSS
- **Git history preservation**: Legacy layout implementations preserved in specific commits - need exact component restoration, not just CSS changes
- **Environment variable defaults**: Flags should default to new behavior when undefined for forward compatibility
- **Client-side environment variable access**: Must use `NEXT_PUBLIC_` prefix for browser availability
- **Conditional rendering performance**: Environment checks on every render can impact performance - memoize when possible

### Security & Default Behavior
- **Permissive defaults are dangerous**: Rules engines that default to "allow" when data is missing create security holes
- **"Cannot verify" should fail**: When unable to evaluate a condition, failing is safer than assuming success
- **Single-line security impact**: Changing one default can fundamentally alter system security posture
- **Default behavior inversion**: Moving from `return true` to `return false` for unknown states requires careful testing
- **Hidden required fields**: Security fixes expose previously unnoticed required fields in existing test data (forProfitEntity, forProfitSuccessor)

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
- **Environment specification**: Wrong vitest environment ('node' vs 'jsdom') causes test execution failures
- **Security fix TDD**: Test-driven approach catches edge cases in security-critical default changes (missing field requirements)

### API/External Services
- **Third-party auth**: Always add 100% time buffer - provider quirks inevitable
- **Migration tasks**: Need rollback plan + multi-environment testing
- **Performance work**: Set up measurement infrastructure before optimization

### File Processing & KDP Pipeline
- **Cover validation timing**: Technical validation → quality analysis → auto-processing to avoid rework
- **Browser automation failures**: Always take screenshots on errors, implement retry with exponential backoff
- **ISBN handling**: Validate format → check existing assignment → generate placeholders for missing
- **Metadata inheritance**: Deep merge objects, direct assign arrays, preserve existing timestamps

### SessionStorage & State Management
- **Storage quota errors**: Implement cleanup-retry pattern when quota exceeded
- **Cross-tab consistency**: SessionStorage is tab-specific, use localStorage for cross-tab data
- **JSON serialization**: Handle dates and complex objects with custom serializers
- **Browser environment**: Always check `typeof window !== 'undefined'` before storage operations

### Text Processing & Natural Language
- **State code extraction gotcha**: Common words like "in", "or", "me" are also valid state codes
- **Regex exclusions**: Simple word boundary checks insufficient - need context-aware exclusion patterns
- **Edge case testing**: Always test extraction patterns with realistic conversational text
- **False positive prevention**: Build explicit exclusion lists for ambiguous patterns

### AI Prompt Engineering Gotchas
- **Implicit behavior assumptions**: AI may infer allowed behaviors from tool availability alone
- **Tool calling eagerness**: Without explicit constraints, AI tends to use tools prematurely
- **Instruction order matters**: Sequential requirements must be explicit, not assumed from context
- **Behavior drift over conversations**: Initial instructions may be forgotten without reinforcement

### Server-Side Tool Validation Gotchas
- **Edge runtime storage limitations**: Cannot use sessionStorage or localStorage in server-side tool functions
- **Initial development assumptions**: Solutions that work in client-side React don't always translate to server-side tools
- **Data source adaptation**: Must extract validation data from tool parameters when browser storage unavailable
- **Runtime environment confusion**: Edge runtime != browser environment for storage access patterns

### Progress Indicator Gotchas
- **Auto-redirect assumptions**: Don't build "continue" buttons when system auto-redirects after completion
- **Button-gated progress**: Hiding progress behind actions reduces user guidance and clarity
- **SessionStorage initialization**: React state must handle initial undefined values gracefully
- **Browser safety in components**: Always check `typeof window !== 'undefined'` before sessionStorage access

### API Route Testing Gotchas
- **SSE status requirement**: SSE endpoints must return 200 status even for errors (send error as event data)
- **EventSource mock complexity**: Need to simulate connection states, event dispatching, and cleanup
- **Stream processing timing**: Use proper async delays when testing event sequences
- **Authentication error handling**: Mock failures should still return SSE format, not throw exceptions
- **Correlation ID consistency**: All events in a single request must share the same correlation ID

### Test Environment Gotchas
- **Vitest environment mismatch**: Tests fail to execute when environment is 'node' but test utilities need 'jsdom'
- **Cryptic environment errors**: Wrong test environment causes confusing failures that mask real test issues
- **Mock utility dependencies**: `setupMockFetch` and browser mocks require DOM environment to function
- **Configuration troubleshooting order**: Check vitest environment before debugging individual test failures

### FSRS Soft Delete Gotchas
- **Retrievability time-sensitivity**: Deleted questions lose review priority over time even when restored - factor deletion duration into testing
- **Query index assumptions**: Ensure `by_user_active` index exists for efficient deleted question filtering
- **FSRS field assumptions**: Legacy questions without FSRS data need special handling in soft delete operations
- **State transition edge cases**: Questions in different FSRS states (new/learning/review/relearning) all require deletion filtering

### Task Completion Discovery Gotchas
- **Assumption of incompleteness**: Don't assume tasks need implementation without checking existing state first
- **Test coverage blind spots**: Running specific test suites may miss broader coverage already in place
- **Pattern search limitations**: Quick searches might miss comprehensive test coverage if naming conventions differ
- **Time estimation over-confidence**: Even "already complete" tasks take time to verify and document

### Rollback Strategy Gotchas
- **Incomplete legacy preservation**: Partial restoration creates compatibility issues - need complete implementations
- **Environment variable deployment timing**: Changes may not take effect until next build/deployment
- **Feature flag testing coverage**: Must test both enabled and disabled states thoroughly
- **Legacy component dependencies**: Old implementations may depend on deprecated patterns or libraries
- **Git history archaeology**: Finding exact implementation requires careful commit history analysis

### Rate Limiting Implementation Gotchas
- **Database timestamp cleanup**: Without periodic cleanup, rate limiting tables grow unbounded over time
- **Race condition windows**: Multiple simultaneous requests can bypass rate limits if not properly synchronized
- **Time zone considerations**: Use UTC timestamps consistently to avoid rate limit confusion across time zones
- **Request counting accuracy**: Ensure rate limit counters are atomic and don't allow double-counting
- **Error message information leakage**: Rate limit error messages should not reveal system architecture details
- **IP address spoofing**: Client IP headers can be manipulated - use server-side IP detection when possible
- **Cached rate limit status**: Rate limit checks must query real-time data, not cached values
- **Cross-service rate limiting**: Different services (API, email, AI) need coordinated rate limiting strategies

## Good Questions to Ask

### Environment Variable & Feature Flag Questions
- "Does this feature flag need to work client-side or server-side (or both)?"
- "What's the rollback strategy if the feature flag causes issues?"
- "How do we handle the loading state while environment detection completes?"
- "Are we preserving the old implementation completely or just key differences?"
- "What happens if the environment variable changes after build time?"
- "Does this layout change require different components or just different CSS?"
- "Should the feature flag default to new behavior or old behavior?"
- "How do we test both enabled and disabled states of this flag?"
- "Are there any dependencies between the old and new implementations?"
- "What's the performance impact of checking environment variables on every render?"

### Security & Default Behavior
- "What should happen when we can't verify the condition - pass or fail?"
- "Are we defaulting to permissive or restrictive behavior for unknown states?"
- "What's the security impact if this check is bypassed or fails?"
- "Is 'no data provided' the same as 'verification passed'?"
- "Which fields are actually required vs optional for this security check?"

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

### Publishing Pipeline Questions
- "What validation can be automated vs requires human judgment?"
- "How do we handle partial failures in multi-step workflows?"
- "What debug information is needed when automation fails?"
- "Can this process run unattended or needs human confirmation?"

### Fact Collection Questions
- "What constitutes sufficient information for a decision?"
- "How do we handle conflicting or inconsistent facts?"
- "What are the minimum required facts vs nice-to-have facts?"
- "How do we validate fact accuracy and completeness?"

### Text Processing Questions
- "What common words might conflict with my extraction patterns?"
- "How do I test this pattern against realistic user input?"
- "What false positives could this regex produce in natural conversation?"
- "Should I use exclusion lists or more sophisticated context-aware parsing?"

### AI Prompt Engineering Questions
- "What behaviors might the AI assume are allowed without explicit instruction?"
- "How can I enforce sequential workflows in AI interactions?"
- "What tools might be called prematurely without proper constraints?"
- "Are my instructions clear enough to prevent unintended behavior patterns?"

### Server-Side Tool Validation Questions
- "What runtime environment will this tool execute in (browser vs server vs edge)?"
- "Can I access browser storage APIs in this execution context?"
- "What data sources are available for validation in server-side tools?"
- "How do I extract validation data when browser storage is unavailable?"

### Progress Indicator Questions
- "Does the user need to take action to continue, or does the system auto-advance?"
- "Should progress be visible at all times or only when requested?"
- "What happens if the user refreshes the page during the process?"
- "How do we handle progress state when the browser environment is undefined?"

### API Route Testing Questions
- "How do I simulate SSE event streams in tests without real network connections?"
- "What edge cases exist for authentication failures in SSE endpoints?"
- "How do I test event ordering and buffering in streaming responses?"
- "What happens when the client disconnects mid-stream?"

### Test Environment Questions
- "Does this test need DOM APIs or is a Node.js environment sufficient?"
- "Are we using browser-specific mocks that require jsdom environment?"
- "What test utilities are we using and what environment do they expect?"
- "Is the vitest environment configuration matching our test requirements?"

### FSRS Soft Delete Questions
- "How long can questions be deleted before FSRS scheduling becomes invalid?"
- "Should deleted questions affect user statistics or review counts?"
- "Do we need a permanent delete option or is soft delete sufficient?"
- "How do we handle questions deleted before FSRS implementation existed?"
- "Should restored questions resume their original review schedule immediately?"

### Task Completion Discovery Questions
- "What test coverage already exists for this functionality?"
- "Are there existing implementations that already solve this problem?"
- "What patterns can I search for to verify current state?"
- "Is this task actually requesting verification rather than implementation?"
- "What would success look like if this feature already works correctly?"

### Rollback Strategy Questions
- "What's the exact scope of changes that need to be rolled back?"
- "Do we need to preserve the old implementation completely or just key differences?"
- "How quickly can we switch back if issues arise?"
- "What testing do we need for both the new and old implementations?"
- "Are there any data migration or state considerations for rollbacks?"
- "How do we handle users who were in the middle of using the feature during rollback?"

### Rate Limiting Questions
- "What's the appropriate time window for this rate limit (per minute, hour, day)?"
- "Should rate limits be per user, per IP, or both?"
- "What's the desired user experience when rate limits are hit?"
- "How do we handle legitimate users who hit rate limits accidentally?"
- "Should rate limiting be configurable or hardcoded?"
- "What data needs to be cleaned up to prevent unbounded storage growth?"
- "How do we coordinate rate limits across different services (API, email, AI)?"
- "Should rate limit status be visible to users proactively?"
- "How do we test rate limiting without affecting real user experience?"
- "What metrics do we need to monitor rate limiting effectiveness?"

## Time Estimation Wisdom

### Consistently Fast (1-5 minutes)
- Convex optional field additions with existing patterns
- Configuration changes with clear precedent  
- Component positioning following established patterns
- Copy/paste implementations with minor modifications
- **AI instruction text updates**: Simple find/replace with clear before/after requirements
- **Security default inversions**: Single-line changes with clear before/after behavior
- **Environment variable additions**: Simple boolean flags with existing conditional patterns

### Consistently Simple (10-15 minutes)
- Modal forms with established component library
- UI features when backend mutations already exist
- Layout changes with existing CSS Grid structure
- Enhanced filtering with existing search patterns
- **Basic utility modules following existing templates** (like storage.ts → factTracking.ts)
- **Server-side tool validation**: Adding fact checking with parameter extraction patterns
- **Always-visible progress indicators**: Following existing sessionStorage + React state patterns
- **Test creation with existing patterns**: Following established test patterns and mock utilities
- **Security rules engine fixes**: Question categorization approach with TDD (30 min actual vs 2-3 hour estimates)
- **FSRS soft delete validation**: Adding deletedAt filtering to existing queries with established patterns
- **Task verification when already complete**: Checking existing test coverage and running validation (10 min actual)
- **Environment variable feature flags**: Simple conditional rendering with existing patterns (15 min actual)
- **Safe rollback implementations**: Using environment variables for instant rollback capability
- **Basic rate limiting**: Implementing request counting with existing timestamp patterns and database queries (10-15 min with established patterns)

### Consistently Medium (15-45 minutes)  
- External API integrations with discovered patterns
- Convex mutations following established auth patterns
- Multi-task implementations with clear integration hooks
- Comprehensive unit test suites with established testing patterns
- **API route testing**: Following SSE/fetch patterns with mock setup
- **Hook testing with mocks**: EventSource and stream simulation patterns
- **FSRS data integrity tests**: Comprehensive scheduling validation across delete/restore cycles
- **Layout rollback systems**: Complete component restoration from git history with environment flag integration (30-45 min with preserved legacy patterns)
- **Complex rollback strategies**: Multiple component interactions with preserved git history implementations
- **Comprehensive rate limiting**: Multi-service coordination, error handling, cleanup strategies (30-45 min with existing database patterns)

### Environment Variable & Feature Flag Timing
- **Simple boolean feature flags**: 5-10 minutes with existing conditional rendering patterns
- **Environment detection integration**: 10-15 minutes combining server-side and client-side detection
- **Layout system rollbacks**: 30-45 minutes when complete legacy implementations preserved in git history
- **Component restoration from git**: 15-20 minutes extracting and adapting historical component versions
- **Multi-environment testing**: Add 100% buffer for testing across development/preview/production environments
- **Rollback system implementation**: 20-30 minutes for complete environment-based rollback capability
- **Feature flag coexistence setup**: 15-25 minutes implementing both old and new code paths with conditional switching

### Publishing Pipeline Timing
- **Cover validation system**: 2-4 hours (multi-format support, quality analysis)
- **CLI command integration**: 1-2 hours (following Commander.js patterns)
- **Playwright automation**: 3-6 hours (2FA handling, error recovery, screenshot debugging)
- **Template processing**: 1-2 hours (SVG generation, variable replacement)

### SessionStorage & Fact Collection Timing
- **Basic fact tracking utility**: 15-30 minutes (following storage.ts patterns)
- **Comprehensive validation functions**: 30-45 minutes (type guards + edge cases)
- **Readiness assessment logic**: 45-60 minutes (area-based confidence scoring)
- **SessionStorage integration**: 15-20 minutes (browser safety + error handling)

### Text Processing & Pattern Matching
- **Simple regex patterns**: 5-10 minutes for straightforward extraction
- **Context-aware extraction**: 15-25 minutes when excluding common word conflicts
- **Natural language parsing**: 30-45 minutes for sophisticated disambiguation
- **Pattern testing with edge cases**: Add 50% buffer for realistic text validation

### AI Prompt Engineering Timing
- **Simple instruction updates**: 2-5 minutes for clear behavioral constraints
- **Sequential workflow design**: 15-30 minutes to design proper instruction flow
- **Complex behavior modification**: 30-60 minutes to test and refine AI responses
- **Cross-conversation consistency**: 45+ minutes to ensure behavior persistence

### Server-Side Tool Validation Timing
- **Basic tool gating**: 10-15 minutes when adapting from existing validation patterns
- **Parameter extraction logic**: 5-10 minutes for simple fact counting validation
- **Runtime environment adaptation**: Add 25% buffer when switching from client-side assumptions
- **Early return patterns**: 2-5 minutes to implement with clear user messaging

### Progress Indicator Timing
- **Always-visible progress displays**: 5-10 minutes when following existing sessionStorage patterns
- **Icon-based status visualization**: 2-5 minutes using established icon libraries (lucide-react)
- **SessionStorage React integration**: 5-8 minutes for safe browser environment handling
- **Auto-redirect detection**: 2-3 minutes to remove unnecessary button assumptions

### API Route Testing Timing
- **SSE endpoint test setup**: 10-15 minutes following existing fetchWithSchema patterns
- **MockEventSource creation**: 15-20 minutes for comprehensive event simulation
- **Stream parsing tests**: 5-10 minutes with ReadableStream mocks
- **Authentication flow testing**: 5-8 minutes mocking getAccessTokenFromRequest
- **Tool execution testing**: 8-12 minutes for tool result event validation

### Test Environment Configuration Timing
- **Environment specification fixes**: 1-2 minutes to update vitest.config.ts environment setting
- **Environment troubleshooting**: 5-10 minutes to identify wrong environment as cause of test failures
- **Mock utility setup with correct environment**: 2-3 minutes when environment is properly configured
- **Configuration verification**: 1 minute to verify test environment matches requirements

### FSRS Soft Delete Testing Timing
- **Basic soft delete tests**: 10-15 minutes following existing CRUD test patterns
- **FSRS field preservation tests**: 5-10 minutes with object spread validation patterns
- **Review queue filtering tests**: 15-20 minutes simulating query logic with time-based scenarios
- **Retrievability calculation tests**: 8-12 minutes using mock questions with FSRS state

### Task Completion Discovery Timing
- **Existing test coverage verification**: 5-10 minutes examining test files and running relevant suites
- **Pattern scout discovery**: 3-5 minutes using search tools to identify existing implementations
- **Current state validation**: 5-10 minutes running tests and verifying functionality works as expected
- **Documentation and verification**: 10 minutes to document findings and confirm task completion status

### Rollback Strategy Implementation Timing
- **Environment variable rollback setup**: 15-20 minutes implementing feature flag with safe defaults
- **Complete implementation coexistence**: 25-35 minutes making both old and new code paths work together
- **Git history component restoration**: 20-30 minutes extracting and adapting legacy components
- **Cross-environment rollback testing**: 10-15 minutes testing rollback across different environments
- **Documentation and rollback procedures**: 5-10 minutes documenting rollback steps and procedures

### Rate Limiting Implementation Timing
- **Basic request counting**: 10-15 minutes with existing timestamp patterns and database schema
- **Multi-service rate limiting**: 20-30 minutes coordinating limits across API endpoints, email, AI services
- **User experience enhancements**: 15-25 minutes adding countdown timers, retry messaging, graceful degradation
- **Rate limit testing**: 15-20 minutes testing edge cases, cleanup, and monitoring integration
- **Database cleanup automation**: 10-15 minutes implementing periodic cleanup of old rate limit data

### Always Add Buffer For
- Third-party integrations (100% buffer minimum)
- Database migrations (50% buffer for rollback planning)  
- Performance optimization (add measurement setup time)
- E2E test suites (50% buffer for flaky test debugging)
- Browser automation (200% buffer for platform quirks and anti-bot measures)
- **Text processing with ambiguous patterns** (100% buffer for false positive debugging)
- **Security-critical default changes** (25% buffer for comprehensive testing)
- **SSE testing with complex event sequences** (50% buffer for timing issues)
- **Test environment configuration issues** (Add 25% when tests use DOM-specific utilities)
- **FSRS scheduling edge cases** (25% buffer for time-dependent calculation validation)
- **Task discovery and verification** (Add 25% buffer for thorough existing coverage analysis)
- **Layout rollback systems** (50% buffer for cross-component compatibility when restoring legacy implementations)
- **Environment-dependent feature flags** (25% buffer for edge cases where environment detection fails)
- **Rollback system implementation** (100% buffer for thorough testing of both forward and backward compatibility)
- **Rate limiting across multiple services** (50% buffer for coordination complexity and testing race conditions)

### Trust Pattern-Scout When
- 95%+ confidence = implementation should be trivial
- Exact component locations found = accurate simple estimates
- Same-service API patterns discovered = direct adaptation possible
- Well-organized existing structure = minimal refactoring needed
- **Comprehensive test coverage found** = task may already be complete, verify first
- **Complete git history preservation** = legacy implementations can be restored exactly
- **Environment variable patterns established** = feature flag implementation becomes straightforward
- **Existing rate limiting components found** = timestamp tracking and database patterns can be directly adapted

## Architecture Lessons

### What Works
- **Environment-based feature flags**: Using environment variables for feature toggles enables safe rollbacks and staged deployments
- **Git history preservation**: Maintaining complete legacy implementations in git history enables exact restoration
- **CSS Grid layout systems**: Three-row grid template (auto/1fr/auto) eliminates content overlap and manual spacing
- **Conditional rendering patterns**: Path-based or environment-based conditional rendering provides clean feature flag implementation
- **Security-first defaults**: Failing when unable to verify prevents security bypasses
- **Restrictive rule engines**: Default to deny/fail rather than allow/pass for unknown conditions
- **Mobile-first CSS**: Prevents overflow issues, easier to scale up than down
- **Pattern-first development**: Always search for existing solutions before building
- **Simple ownership model**: User-based permissions over complex RBAC for personal tools
- **CSS Grid over complex calculations**: Modern CSS features often simplify assumed complexity
- **No-internal-mocking testing**: Realistic test implementations more valuable than mocks
- **Service-based architecture**: Dependency injection enables testing, configurability, reuse
- **Multi-stage validation**: Separate concerns (format → compliance → quality) for better debugging
- **SessionStorage for persistence**: Simple client-side data persistence across page refreshes
- **Structured fact interfaces**: Type-safe data collection with validation and readiness assessment
- **Template-driven development**: Following existing patterns (storage.ts) prevents architectural drift
- **Explicit AI instruction constraints**: Clear behavioral boundaries prevent tool misuse and workflow violations
- **Server-side parameter extraction**: Using tool call parameters as validation data source when storage unavailable
- **Always-visible progress indicators**: Continuous status display improves user guidance over button-gated progress
- **HTTP boundary mocking**: Mock fetch/EventSource rather than internal dependencies for more realistic tests
- **SSE event buffering**: Buffer streaming events until completion for better UX and error handling
- **Proper test environment configuration**: Matching vitest environment to test requirements prevents execution failures
- **FSRS soft delete preservation**: Maintaining all scheduling fields through delete/restore ensures algorithm continuity
- **Query-level deletion filtering**: Filtering deleted questions at the database query level prevents accidental inclusion
- **Existing coverage verification**: Checking test coverage before implementation prevents duplicate work and reveals completed tasks
- **Constants array organization**: Dedicated constants.ts files with typed arrays and proper exports
- **Complete rollback system preservation**: Keeping entire legacy implementations enables instant rollback capability
- **Environment variable coexistence**: Both implementations in same codebase with conditional switching eliminates deployment risk
- **Zero-downtime rollbacks**: Environment variable changes enable instant rollback without code changes or deployments
- **Timestamp-based rate limiting**: Using existing database timestamp patterns for simple, effective request throttling
- **Database-driven rate limits**: Leveraging existing user-based queries and timestamp indexes for efficient rate limit checking

### What Doesn't Work
- **Client-side process.env assumptions**: Environment variables only available server-side in Next.js
- **Runtime environment variable changes**: Next.js caches env vars at build time - runtime changes ignored
- **Fixed positioning with manual spacers**: CSS Grid eliminates need for manual spacing calculations
- **Incomplete legacy preservation**: Partial restoration of old systems creates compatibility issues
- **Permissive security defaults**: Defaulting to "allow" when unable to verify creates vulnerabilities
- **Store hooks in list items**: Causes mass re-renders (367 → 0 with CSS variables)
- **String concatenation for shell commands**: Creates injection vulnerabilities - use subprocess arrays
- **Complex status models**: Three-state models often unnecessary in single-user systems
- **Over-engineered confidence scoring**: Metadata maintenance exceeds utility value
- **Fixed-width mobile layouts**: Calculate total width requirements vs viewport constraints
- **Monolithic validation**: Combining all validation logic makes debugging failures impossible
- **Direct localStorage for facts**: SessionStorage better for conversation-scoped data
- **Manual storage operations**: Automatic persistence reduces bugs and improves UX
- **Simple word boundary regex for state codes**: Matches common words like "in", "or", "me"
- **Implicit AI behavioral assumptions**: AI will use available tools without explicit constraints
- **Assuming browser storage in server tools**: Edge runtime cannot access sessionStorage/localStorage
- **Button-gated progress indicators**: Hide important status information behind user actions
- **"Continue button" assumptions for auto-redirecting flows**: System may redirect automatically without user action
- **Internal dependency mocking**: Mocking internal functions reduces test value vs mocking at system boundaries
- **Real network connections in tests**: SSE tests should use mocks, not actual EventSource connections
- **Wrong test environment**: Using 'node' environment when tests need DOM APIs causes execution failures
- **Hard delete in learning systems**: Permanent deletion breaks FSRS algorithm continuity and user progress tracking
- **Assuming tasks need implementation**: Many "tasks" are actually verification requests for already-complete functionality
- **Inline constants in components**: Scatter configuration, reduce reusability, no type safety
- **Partial legacy implementation preservation**: Creates compatibility issues and incomplete rollback capability
- **Complex rollback mechanisms**: Simple environment variable toggles more reliable than complex migration scripts
- **Client-side rate limiting**: Client-side checks can be bypassed - rate limiting must be server-side
- **In-memory rate limit storage**: Server restarts reset limits - persistent storage required for consistency

### When to Keep It Simple
- **Environment variables for feature flags** - simpler than complex feature flag services
- **Git history for rollbacks** - preserve complete implementations rather than trying to recreate
- **Conditional rendering for feature toggles** - leverage existing patterns rather than complex state management
- **CSS Grid over manual positioning** - modern layout systems eliminate complex calculations
- Personal tools favor binary states over multi-state models
- Well-organized codebases need minimal changes with modern CSS
- Copy existing patterns rather than creating new ones
- Trust simple solutions when existing structure is already good
- Use established component libraries instead of custom implementations
- Follow existing CLI patterns rather than inventing new argument structures
- Leverage existing validation patterns rather than building custom validators
- **Use template files as blueprints** - following established patterns prevents bugs and ensures consistency
- **Simple text replacements for AI instruction updates** - clear requirements eliminate complexity
- **Parameter-based validation over storage** - simpler and works across runtime environments
- **Single-line security fixes** - simple default changes often have massive positive impact
- **Always-visible progress over complex state management** - permanent display eliminates complexity
- **Mock at system boundaries** - HTTP/EventSource mocking simpler than internal dependency mocking
- **Check test environment first** - verify vitest configuration before debugging complex test failures
- **Soft delete over hard delete** - preserves data integrity and enables user error recovery in learning systems
- **Verify existing coverage before implementing** - check for completed work before building new solutions
- **Extract constants to dedicated files** - improves maintainability and enables reuse across components
- **Environment variable rollback switches** - simpler than complex rollback mechanisms or deployment-based rollbacks
- **Complete implementation coexistence** - both versions in same codebase simpler than maintaining separate branches
- **Database timestamp rate limiting** - use existing patterns rather than external rate limiting services
- **User-based rate limits** - leverage existing authentication patterns rather than complex IP tracking

## Performance Baselines

### Component Rendering
- **Before optimization**: 285ms visual completion, 367 component re-renders
- **After CSS variables**: 185ms completion (35% faster), 0 component re-renders
- **Affected elements**: 1000+ transitioning DOM reduced to ~20

### Development Speed  
- **With pattern-scout**: 10 minutes for comprehensive filtering UI
- **With existing patterns**: 15 minutes for external API integration
- **Without patterns**: 45+ minutes for same complexity features
- **Following template files**: 15 minutes for complete utility module with tests
- **AI instruction text updates with clear requirements**: 3 minutes actual vs 5-10 minute estimates
- **Server-side tool validation with patterns**: 10 minutes vs 20+ minutes without examples
- **Security default inversions**: 2 minutes actual vs 2-5 minute estimates
- **Security rules engine fixes with TDD**: 30 minutes actual vs 2-3 hour estimates (question categorization approach)
- **Always-visible progress indicators**: 8 minutes actual vs 10-15 minute estimates
- **Test creation with established patterns**: 12 minutes actual vs 15-20 minute estimates
- **FSRS soft delete implementation**: 15 minutes actual vs 30-45 minute estimates (with existing patterns)
- **Task verification with existing coverage**: 10 minutes actual vs 30-45 minute implementation estimates
- **Environment variable feature flags**: 15 minutes actual vs 30-45 minute estimates (with conditional rendering patterns)
- **Layout rollback with git history**: 25 minutes actual vs 60-90 minute estimates (when legacy implementation preserved)
- **Complete rollback system implementation**: 15 minutes actual vs 45-60 minute estimates (with environment variable patterns)
- **Basic rate limiting with existing patterns**: 12 minutes actual vs 30-45 minute estimates (with timestamp tracking patterns)

### Testing Coverage
- **Comprehensive CRUD testing**: 45 minutes for 22 tests with authentication, data preservation, edge cases
- **Unit test setup**: TestConvexDB simulation enables realistic testing without internal mocks
- **Authentication testing**: Multiple user scenarios and permission matrix coverage essential
- **SSE endpoint testing**: 30 minutes for complete test suite with MockEventSource patterns
- **Hook testing with mocks**: 25 minutes for comprehensive event simulation and state testing
- **Test environment fixes**: 2 minutes to correct vitest environment vs 15+ minutes debugging wrong environment
- **FSRS soft delete testing**: 20 minutes for complete data integrity validation with time-based scenarios
- **Existing coverage analysis**: 5 minutes to identify comprehensive test coverage vs hours of duplicate implementation
- **Environment flag testing**: 15 minutes to test across multiple environment scenarios with proper mocking
- **Rate limiting test coverage**: 20 minutes for comprehensive edge case testing with existing database patterns

### Publishing Pipeline Performance
- **Cover validation**: <30s for complete technical + quality analysis
- **Metadata parsing**: <5s for YAML + schema validation + ISBN checks
- **Template processing**: <10s for SVG generation + variable replacement
- **Build performance**: Maintain <15s with 99%+ cache hit rate during development

### SessionStorage Operations
- **Basic read/write**: <1ms for typical conversation data (<10KB)
- **Large conversations**: <10ms for conversations up to 500KB
- **Storage cleanup**: <50ms for removing 5+ old conversations
- **Browser safety checks**: <0.1ms for environment detection

### Text Processing Performance
- **Simple regex extraction**: <1ms for typical conversation text (<50KB)
- **Context-aware processing**: <5ms with exclusion list checks
- **Pattern validation**: <10ms for comprehensive edge case testing
- **False positive checking**: <2ms for common word exclusion patterns

### AI Prompt Engineering Performance
- **Simple instruction validation**: <1s to verify behavioral changes take effect
- **Text replacement operations**: <0.1s for straightforward find/replace updates
- **Workflow constraint testing**: <5s to confirm sequential behavior enforcement
- **Behavior persistence verification**: <10s to test across multiple AI interactions

### Server-Side Tool Validation Performance
- **Parameter extraction**: <0.1ms for simple fact counting from tool parameters
- **Early return validation**: <1ms for basic sufficiency checks before expensive operations
- **Tool gating logic**: <5ms for comprehensive fact validation with clear error messages
- **Runtime adaptation**: <10ms overhead when switching validation approaches

### Progress Indicator Performance
- **SessionStorage fact retrieval**: <1ms for typical fact collection data
- **React state initialization**: <0.1ms with sessionStorage fallback patterns
- **Icon rendering**: <5ms for status-based icon switching (clock ↔ checkmark)
- **Browser environment checks**: <0.1ms for safe sessionStorage access

### API Route Testing Performance
- **MockEventSource setup**: <1ms for complete event simulation infrastructure
- **SSE event parsing**: <5ms for parsing multiple events from stream
- **Stream processing tests**: <10ms for complete request/response cycle simulation
- **Authentication mock setup**: <0.1ms for token validation patterns

### Test Environment Performance
- **Environment detection**: <0.1ms to identify correct vitest environment needed
- **Configuration updates**: <1s to update vitest.config.ts environment setting
- **Test execution with correct environment**: <5s for typical test suite vs infinite hang with wrong environment
- **Mock utility initialization**: <10ms when environment properly supports DOM APIs

### FSRS Soft Delete Performance
- **Soft delete operation**: <5ms to add deletedAt timestamp to question
- **Restore operation**: <5ms to remove deletedAt field from question
- **Query filtering**: <10ms overhead for deletedAt filtering in review queries with proper indexing
- **FSRS calculation preservation**: <1ms to maintain all scheduling fields through delete/restore operations

### Task Completion Discovery Performance
- **Pattern search execution**: <2s to search codebase for existing test coverage patterns
- **Test suite execution**: <10s to run relevant test suites and verify functionality
- **Coverage analysis**: <5s to analyze test coverage and identify comprehensive existing implementations
- **Verification documentation**: <5s to document findings and confirm task completion status

### Environment Variable & Feature Flag Performance
- **Environment variable lookup**: <0.1ms for process.env access
- **Client-side environment detection**: <1ms for hostname-based detection
- **Feature flag conditional evaluation**: <0.1ms for boolean condition checks
- **Component switching**: <5ms for conditional rendering between layout systems
- **Git history component restoration**: <1s to extract and adapt legacy component implementations
- **Rollback system execution**: <0.1ms for environment variable toggle to switch implementations
- **Coexistence overhead**: <5ms additional render time when both implementations present in bundle

### Rate Limiting Performance
- **Request count checking**: <5ms with proper database indexing on userId and timestamp fields
- **Rate limit enforcement**: <10ms including database query and validation logic
- **Cleanup operations**: <50ms for removing expired rate limit entries (daily batch operation)
- **Multi-service coordination**: <15ms when checking rate limits across multiple endpoints
- **User experience updates**: <100ms for displaying countdown timers and retry information

---

*Updated: Daily as new patterns and lessons are discovered*