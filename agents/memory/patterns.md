# Pattern Memory Database

This file maintains a persistent memory of code patterns and their locations in the codebase.

## Structure

Each pattern entry includes:
- **Locations**: Specific file:line references with confidence scores
- **Times referenced**: How often this pattern is looked up
- **Last used**: When last referenced (YYYY-MM-DD format)
- **Average confidence**: Weighted average of all location confidence scores
- **Notes**: Important context or preferences

---

## Responsive Grid Layout Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:84,175 - Card grid with md:grid-cols-2 lg:grid-cols-3 responsive breakpoints (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:55 - Stats grid with grid-cols-2 md:grid-cols-4 for mobile-first design (confidence: 98%)
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:30,121 - Dashboard grid using md:grid-cols-2 lg:grid-cols-4 for quick actions and lg:grid-cols-3 for main layout (confidence: 95%)
- /Users/phaedrus/Development/scry/app/deployments/page.tsx:33 - Simple responsive grid with grid-cols-1 md:grid-cols-4 pattern (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 95.3%
**Notes**: Primary responsive pattern uses grid-cols-1 for mobile, md:grid-cols-2/3/4 for tablet+, lg:grid-cols-3/4 for desktop. Cards/stats use 2 cols mobile, 4 cols desktop. Main dashboard uses 3-column layout with sidebar pattern.

## Container and Spacing Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/navbar.tsx:27 - max-w-7xl mx-auto px-4 py-4 container pattern with responsive padding (confidence: 98%)
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:19-20 - container mx-auto px-4 py-8 with nested max-w-7xl mx-auto for content centering (confidence: 95%)
- /Users/phaedrus/Development/scry/app/deployments/page.tsx:21,29 - container mx-auto p-8 simpler container pattern (confidence: 90%)
- /Users/phaedrus/Development/scry/app/globals.css:102-107 - CSS Grid layout system with min-height viewport handling (confidence: 95%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Standard container pattern: max-w-7xl mx-auto for wide layouts, container mx-auto for full-width, px-4 for mobile horizontal padding. Uses CSS Grid layout-grid class for min-height 100vh/100dvh mobile viewport handling.

## Mobile-First Breakpoint System (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/navbar.tsx:28 - text-2xl md:text-3xl responsive text sizing (confidence: 98%)
- /Users/phaedrus/Development/scry/app/page.tsx:29,31,34,43 - Complex responsive header with sm:p-8 md:p-16, gap-2 sm:gap-3, hidden sm:block patterns (confidence: 95%)
- /Users/phaedrus/Development/scry/app/not-found.tsx:22 - flex-col sm:flex-row responsive flex direction (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:282 - TabsList with grid w-40 grid-cols-2 for compact mobile tabs (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Tailwind mobile-first approach: base styles for mobile, sm: (640px+) for small screens, md: (768px+) for tablets, lg: (1024px+) for desktop. Uses hidden sm:block for mobile-hidden elements, responsive text sizing, gap spacing, and flex direction changes.

## Button Responsive Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-flow.tsx:155,198,207 - w-full buttons for mobile-friendly touch targets (confidence: 98%)
- /Users/phaedrus/Development/scry/components/ui/button.tsx:7-36 - Complete button variant system with size variations (sm, default, lg, icon) (confidence: 95%)
- /Users/phaedrus/Development/scry/app/page.tsx:43 - Icon-responsive pattern: h-4 w-4 sm:mr-2 (shows icon spacing only on larger screens) (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:235-241 - Responsive button width: w-full sm:w-auto for mobile-first approach (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Mobile-first button approach: w-full for mobile touch-friendly buttons, sm:w-auto for desktop. Button sizes: sm (h-8), default (h-10), lg (h-12), icon (size-10). Icons use conditional spacing/visibility with sm: breakpoints.

## Modal and Dialog Responsive Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:126 - DialogContent with sm:max-w-[525px] responsive max-width (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-generation-skeleton.tsx:14 - Card with w-full max-w-md mx-auto centering pattern (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-flow.tsx:147,186 - max-w-md w-full centered content containers (confidence: 90%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:45 - DropdownMenuContent with w-64 fixed width for user menu (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Modal pattern: full-width on mobile (w-full), constrained max-width on larger screens (sm:max-w-[525px]). Uses mx-auto centering with max-width containers (max-w-md, max-w-lg). Dropdown menus use fixed pixel widths (w-64, w-40) for consistency.

## CSS Grid Layout System (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/globals.css:102-107 - .layout-grid CSS Grid with grid-template-rows: auto 1fr auto and min-height viewport (confidence: 98%)
- /Users/phaedrus/Development/scry/app/layout.tsx:38-42 - Layout structure using layout-grid for header, main, footer (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/card.tsx:23 - Card header grid with auto-rows-min grid-rows-[auto_auto] and conditional grid-cols-[1fr_auto] (confidence: 90%)
- /Users/phaedrus/Development/scry/app/globals.css:333 - Mobile viewport handling with min-height: 100dvh fallback (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Uses CSS Grid for main layout with sticky header/footer. layout-grid class provides auto 1fr auto rows for proper content stretching. Handles mobile viewport with 100dvh fallback. Card components use CSS Grid for complex layouts with conditional columns.

## Navigation Responsive Behavior (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/navbar.tsx:26-32 - Sticky navbar with max-width container and responsive logo sizing (confidence: 98%)
- /Users/phaedrus/Development/scry/components/conditional-navbar.tsx:6-14 - Conditional navbar rendering based on pathname (confidence: 95%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:45-98 - Dropdown user menu with responsive layout and truncation (confidence: 95%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:53 - Flex layout with min-w-0 flex-1 for text truncation in constrained spaces (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Navigation uses sticky positioning with proper z-index (z-40). Responsive logo sizing (text-2xl md:text-3xl). User dropdown menu handles text overflow with truncate and min-w-0 flex-1 pattern. Conditional rendering hides navbar on homepage.

## Responsive Typography Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/globals.css:325-327 - .text-hero class with clamp(3.5rem, 10vw, 7rem) fluid typography (confidence: 98%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:28 - text-2xl md:text-3xl responsive text sizing (confidence: 95%)
- /Users/phaedrus/Development/scry/app/globals.css:40-48 - CSS custom properties for consistent font scale (confidence: 90%)
- /Users/phaedrus/Development/scry/app/globals.css:115-143 - Typography hierarchy with consistent spacing (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Uses clamp() for fluid typography on hero elements. Standard responsive pattern: smaller text on mobile, larger on desktop. CSS custom properties provide consistent type scale. Typography includes proper line-height and spacing variables.

## Flex Layout Responsive Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/not-found.tsx:22 - flex-col sm:flex-row for responsive flex direction (confidence: 98%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:32,46,53 - Complex flex layouts with items-center justify-between and gap spacing (confidence: 95%)
- /Users/phaedrus/Development/scry/app/page.tsx:31 - gap-2 sm:gap-3 responsive gap spacing (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/card.tsx:23 - Grid/flex hybrid with has-data-[slot=card-action]:grid-cols-[1fr_auto] conditional layout (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Primary flex pattern: flex-col on mobile, sm:flex-row on tablet+. Uses responsive gap spacing (gap-2 sm:gap-3). Complex layouts combine flexbox with conditional grid columns. Proper use of items-center, justify-between, and space distribution.

## Performance Testing and Benchmarking Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:1-786 - Complete performance benchmarking suite with statistical analysis (confidence: 98%)
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:1-393 - HTML report generation for performance results (confidence: 95%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/testAudioFileDownloads.ts:1-662 - Audio download performance verification script (confidence: 95%)
- /Users/phaedrus/Development/brainrot/apps/web/docs/PERFORMANCE_BASELINE.md:1-206 - Performance baseline documentation with SLOs (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Comprehensive performance testing suite using performance.now(), statistical metrics (p50, p95, p99), concurrency testing (1, 5, 10), multi-environment support, HTML/JSON reports, checksum verification, and SLO definitions. Measures TTFB, transfer speed, success rates, and response times.

## API Performance Measurement Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:155-231 - benchmarkDirectUrl function with TTFB and transfer speed calculation (confidence: 98%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:245-332 - benchmarkApiEndpoint with API response timing (confidence: 95%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:346-424 - benchmarkProxyEndpoint with proxy performance metrics (confidence: 95%)
- /Users/phaedrus/Development/brainrot/apps/web/app/api/download/route.ts:310-362 - Request timing with Date.now() and duration logging (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Pattern uses performance.now() for high-precision timing, Date.now() for basic request duration, calculates TTFB, transfer speed (KB/s), measures API vs proxy endpoint performance, includes checksum verification for integrity, and structured logging with correlation IDs.

## Statistical Performance Metrics Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:578-664 - StatisticalMetrics interface and calculateStats function (confidence: 98%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:49-80 - PerformanceMetrics and BenchmarkResult interfaces (confidence: 95%)
- /Users/phaedrus/Development/brainrot/apps/web/docs/PERFORMANCE_BASELINE.md:39-57 - Performance baseline metrics table format (confidence: 90%)
- /Users/phaedrus/Development/brainrot/apps/web/docs/PERFORMANCE_BASELINE.md:126-144 - SLO definitions with percentiles (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Comprehensive metrics including min/max/avg/median/p95, success rates, TTFB, transfer speed, content length, grouping by dimensions (book/category/test type/concurrency), statistical analysis with sorted arrays, and SLO thresholds for different environments.

## Concurrency and Load Testing Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:471-558 - Concurrent request testing with configurable parallelism (confidence: 98%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:346-424 - Series testing with individual timing (confidence: 95%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:245-332 - Single request baseline measurement (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.3%
**Notes**: Supports 1, 5, 10 concurrent requests using Promise.all(), measures aggregate and individual request metrics, includes TTFB, transfer speed, success rates, and response times for each concurrency level. Critical for understanding service behavior under load.

## HTML Report Generation Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:1-393 - Complete HTML report with embedded CSS and JavaScript (confidence: 98%)
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:89-150 - Chart.js integration for performance visualization (confidence: 95%)
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:299-393 - Dynamic table generation with filtering (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.3%
**Notes**: Self-contained HTML with embedded CSS and Chart.js, responsive design, sortable tables, metric filtering, color-coded performance indicators, and export capabilities. Suitable for sharing performance results with stakeholders.

## Log Parsing and Aggregation Patterns
**Locations**:
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:19-86 - JSON log parsing and metric aggregation (confidence: 98%)
- /Users/phaedrus/Development/brainrot/tools/legacy-scripts/benchmark-downloads.ts:667-722 - Structured logging with correlation IDs (confidence: 95%)
- /Users/phaedrus/Development/brainrot/apps/web/scripts/benchmark-report-generator.ts:151-225 - Data transformation for visualization (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.3%
**Notes**: Parses newline-delimited JSON logs, aggregates metrics by dimensions (book, category, test type, concurrency), calculates statistical summaries, and transforms data for Chart.js visualization. Handles large log files efficiently with streaming.

## Form Input Validation Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/question-form.tsx:132-150 - Textarea with character limits and validation (confidence: 98%)
- /Users/phaedrus/Development/scry/components/question-form.tsx:76-94 - Input with length validation and error display (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-form.tsx:96-130 - Dynamic array field management for quiz options (confidence: 90%)
- /Users/phaedrus/Development/scry/components/question-form.tsx:152-186 - Select field with form integration (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Uses React Hook Form with Zod validation, FormField wrapper for consistent styling, error message display below inputs, character count indicators for textareas, and dynamic field arrays for quiz options. All fields properly integrated with form state.

## Mutation State Management Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:127-156 - useMutation with loading states and error handling (confidence: 98%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:45-78 - Custom hook with mutation orchestration (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-form.tsx:188-220 - Form submission with mutation integration (confidence: 90%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:48-80 - Destructive action with confirmation (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Standard pattern: useMutation hook, loading state for button disabling, error handling with toast messages, success callbacks for UI updates. Destructive actions require explicit confirmation. Custom hooks encapsulate complex mutation logic.

## API Route Parameter Handling
**Locations**:
- /Users/phaedrus/Development/scry/app/api/generate-quiz/route.ts:23-45 - POST request body parsing with validation (confidence: 98%)
- /Users/phaedrus/Development/scry/app/api/quiz/complete/route.ts:15-35 - Request body extraction and type checking (confidence: 95%)
- /Users/phaedrus/Development/scry/app/api/generate-quiz/route.ts:46-65 - Error response formatting (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.3%
**Notes**: Extract request body using await request.json(), validate with TypeScript types, handle parsing errors gracefully, return structured error responses with appropriate HTTP status codes. Use try/catch blocks for robust error handling.

## Auth Context Usage Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:89-95 - useUser hook with loading and error states (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:30-36 - Authenticated queries with sessionToken (confidence: 95%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:23-30 - User validation in custom hooks (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:98-104 - Conditional rendering based on auth state (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: useUser() returns user object with loading state, sessionToken used for authenticated Convex queries, early returns for loading states, conditional UI rendering based on authentication. User object has 'id' field (not '_id').

## Convex Query Integration Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:30-45 - useQuery with skip condition and pagination (confidence: 98%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:31-44 - Query dependency management (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:96-102 - Single resource query with error handling (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:46-52 - Loading state management (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: useQuery with "skip" for conditional queries, loading states handled at component level, error boundaries for query failures, pagination with hasMore/loadMore pattern. Queries automatically re-run when dependencies change.

## Spaced Repetition Integration Patterns
**Locations**:
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:45-78 - FSRS scheduling with automatic rating (confidence: 98%)
- /Users/phaedrus/Development/scry/convex/spacedRepetition.ts:42-75 - Rating calculation from correctness (confidence: 95%)
- /Users/phaedrus/Development/scry/components/unified-quiz-flow.tsx:156-183 - Quiz completion with spaced repetition (confidence: 90%)
- /Users/phaedrus/Development/scry/hooks/use-polling-query.ts:15-45 - Time-based query polling for reviews (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: FSRS algorithm automatically rates answers (correct=Good, incorrect=Again), schedules next review based on memory model, polling queries handle time-based updates, seamless integration with quiz flow. No manual difficulty rating required.

## UI Component Composition Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:103-126 - Dialog with form integration (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:102-170 - Card layout with action buttons (confidence: 95%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:81-159 - AlertDialog with confirmation flow (confidence: 90%)
- /Users/phaedrus/Development/scry/components/question-form.tsx:42-74 - Form with shadcn/ui components (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Consistent use of shadcn/ui primitives, Dialog/AlertDialog for modals, Card components for content display, Form components with proper field integration, action buttons positioned in appropriate sections (header, footer).

## Error Handling and Toast Patterns
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:139-155 - Mutation error handling with specific messages (confidence: 98%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:62-77 - Error classification and user feedback (confidence: 95%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:58-79 - Destructive action error handling (confidence: 90%)
- /Users/phaedrus/Development/scry/app/api/generate-quiz/route.ts:46-65 - API error response formatting (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Use toast.error() for user-facing errors, classify errors (network, validation, authorization), provide specific error messages, handle API errors gracefully, show success confirmations for important actions. Consistent error UX across app.

## Schema Evolution Best Practices
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Using pattern-scout agent to find existing patterns before implementing new functionality to accelerate development
**Solution**: Always run pattern-scout to discover relevant existing patterns before starting implementation. This prevents reinventing solutions and provides proven patterns to follow.
**Example**:
Task execution showed that using pattern-scout to find Convex schema patterns made schema field addition trivial (2 minutes vs expected longer time). Pattern discovery provides confidence in implementation approach.
**Files**: /Users/phaedrus/Development/chrondle/convex/schema.ts:45-46

## Question Display Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:102-170 - Card-based question display with stats grid (confidence: 98%)
- /Users/phaedrus/Development/scry/components/question-history.tsx:42-113 - Question history with interaction timeline (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:96-102 - Grid layout with search filtering (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:120-167 - Question metadata display pattern (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Questions displayed in Card components with hover effects. Uses grid layout (grid-cols-1 gap-4) for question list. Each card shows question text, topic, type, accuracy, attempts, last review, and creation date. Stats displayed in responsive grid (grid-cols-2 md:grid-cols-4 gap-4).

## Button Action Patterns (Scry Codebase)  
**Locations**:
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:83-90 - Destructive button with icon and confirmation (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:176-183 - Outline button for load more functionality (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:250-272 - Modal action buttons (Cancel outline + Save default) (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/button.tsx:11-23 - Button variant system (default, destructive, outline, secondary, ghost, link) (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Button variants: outline for secondary actions, destructive for delete operations, default for primary actions. Icons use Lucide React with consistent sizing (w-4 h-4). Loading states show Loader2 with animate-spin. Buttons disable during async operations.

## AlertDialog Confirmation Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:81-159 - Complete AlertDialog implementation with email confirmation (confidence: 98%)
- /Users/phaedrus/Development/scry/components/ui/alert-dialog.tsx:9-143 - AlertDialog component structure and styling (confidence: 95%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:97-134 - Input validation within AlertDialog (confidence: 95%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:136-157 - AlertDialog footer with Cancel/Action buttons (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: AlertDialog structure: Trigger -> Content -> Header + Description + Footer. Cancel button uses outline variant, Action button matches operation type (destructive for delete). Input validation inline with error messages. Loading states disable all interactions.

## User Permission and Ownership Check Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/convex/spacedRepetition.ts:54 - Standard ownership verification: question.userId !== userId (confidence: 98%)
- /Users/phaedrus/Development/scry/convex/questions.ts:96,250,305,343 - Consistent ownership pattern across mutations (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:127-133 - Frontend error handling for unauthorized access (confidence: 90%)
- /Users/phaedrus/Development/scry/convex/questions.ts:248,302,340 - Ownership verification after resource fetch (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Ownership pattern: fetch resource first, then check if (!resource || resource.userId !== userId) throw new Error("Resource not found or unauthorized"). Frontend handles unauthorized errors with specific toast messages. No role-based permissions - simple user ownership model.

## Button Placement and Styling Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:103-119 - Action buttons in card header (top-right with flex-shrink-0) (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:250-272 - Modal footer buttons (space-x-2, Cancel + Action) (confidence: 95%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:136-157 - AlertDialog footer (Cancel + Destructive action) (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:174-184 - Centered load more button (flex justify-center) (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 91.3%
**Notes**: Card action buttons positioned in header (top-right) with flex-shrink-0. Modal/dialog footers use space-x-2 gap with Cancel (outline) + Action button. Load more buttons centered with full width on mobile (w-full sm:w-auto). Consistent icon sizing (w-4 h-4) with mr-2 spacing.

## Conditional UI Rendering Based on Ownership
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Implementing edit/delete action buttons that should only appear for content owned by the current user
**Solution**: Use conditional rendering with ownership check: `{question.userId === user.id && (<ActionButtons />)}`. This pattern ensures action buttons only appear for content the user owns.
**Example**: Adding edit/delete buttons to question cards that only show for questions the current user created. Pattern prevents unauthorized access attempts and provides clean UX.
**Files**: /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:103-119

## Auth Context User ID Field Disambiguation
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Confusion between user._id vs user.id when working with auth context vs database records
**Solution**: Auth context user object has `id` field, not `_id`. Database records use `_id`. When checking ownership, use `user.id` from auth context and cast as `Id<"users">` for type safety.
**Example**: TypeScript caught the issue when using `user._id` instead of `user.id` for ownership checks. Proper pattern: `question.userId === user.id as Id<"users">`
**Files**: /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:105

## Icon-Only Button Styling Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Creating compact action buttons with icons only (no text) in constrained spaces like card headers
**Solution**: Use ghost variant with specific sizing: `variant="ghost" size="sm" className="h-8 w-8 p-0"`. This creates a square button with proper icon positioning and hover states.
**Example**: Edit/delete buttons in question card headers need to be compact but still accessible. Ghost variant provides subtle hover effects without overwhelming the card design.
**Files**: /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:107-115

## Delete Confirmation with Item Preview Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Providing confirmation dialogs for delete actions that show what will be deleted to prevent accidental deletions
**Solution**: Include a preview of the item being deleted in the AlertDialog description. Truncate long content with ellipsis and use proper typography hierarchy.
**Example**: Question deletion shows the question text (truncated) in the confirmation dialog so users can verify they're deleting the correct item. Improves safety and user confidence.
**Files**: /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:127-135

## Backend Mutation Integration with Frontend Loading States
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Providing immediate feedback during async operations while preventing duplicate submissions
**Solution**: Use mutation.isPending for loading states, disable buttons/forms during operations, show spinners with Loader2 icon, handle both success and error cases with appropriate feedback.
**Example**: Delete button shows spinner and disables during deletion, then provides success/error feedback. Prevents accidental double-clicks and gives clear status updates.
**Files**: /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:107,147-165

## Loading State Management Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:73,103-135 - useState for loading state with mutation integration (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:32-34,99-124 - Component-level loading state for delete operations (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:297-304 - Loading UI with Loader2 spinner and disabled buttons (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:171,192,215,255,261 - Form field disabling during loading (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Pattern: useState for loading state, setLoading(true) before async operation, setLoading(false) in finally block. During loading: disable form fields/buttons, show Loader2 with animate-spin, change button text to "Loading..." or similar. Consistent across all CRUD operations.

## Immediate UI Feedback Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:99-110 - Button disabling and spinner on click (confidence: 85%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:103-117 - Form submission loading state (confidence: 85%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:51-54 - Loading skeleton while data fetches (confidence: 80%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:10-40 - No optimistic updates - waits for server response (confidence: 75%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 81.3%
**Notes**: Current pattern provides immediate visual feedback through loading states but NO optimistic updates. UI waits for server response before showing changes. Uses Loader2 spinners, button disabling, and form field disabling for feedback. No cache manipulation or immediate data updates found.

## Error Recovery and Rollback Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:121-134 - Error handling with specific toast messages (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:110-122 - Delete error handling with UI state reset (confidence: 85%)
- /Users/phaedrus/Development/scry/hooks/use-quiz-interactions.ts:34-37 - Graceful error handling with null return (confidence: 80%)
- /Users/phaedrus/Development/scry/components/delete-account-dialog.tsx:58-79 - Destructive action error recovery (confidence: 80%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 83.8%
**Notes**: Error handling pattern: try/catch blocks, specific error messages via toast.error(), loading state reset in finally blocks. NO automatic rollback mechanisms found - relies on server state as source of truth. UI resets to previous state only through loading state cleanup, not optimistic rollbacks.

## Dashboard Layout Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:10-47 - Two-column layout with main content (lg:col-span-2) and sidebar (confidence: 98%)
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:14-37 - Tabs pattern for content switching (Recent Quizzes vs All Questions) (confidence: 95%)
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:40-43 - Sidebar with vertically stacked components using space-y-6 (confidence: 95%)
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:27-68 - Widget card structure with header and content sections (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Dashboard uses grid gap-6 lg:grid-cols-3 layout. Main content area spans 2 columns with tabbed interface. Sidebar uses space-y-6 for vertical spacing. Container with max-width centering (max-w-7xl mx-auto). Icons paired with tab labels.

## Stats Widget Display Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:55-80 - Grid-based stats display (grid-cols-2 md:grid-cols-4 gap-4) (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:56-79 - Stat item structure: value + label with color coding (confidence: 95%)
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:82-89 - Empty state with background and center text (confidence: 90%)
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:44-49 - Large number display with description text (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Stats displayed in responsive grid (2 cols mobile, 4 cols desktop). Each stat: large colored number (text-2xl font-bold) with small gray label below (text-sm text-gray-600). Colors: blue, green, purple, orange for different metrics. Empty states use bg-gray-50 rounded container.

## Review Indicator Widget Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:27-68 - Complete review widget with polling and CTA (confidence: 98%)
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:44-49 - Large count display with conditional text (confidence: 95%)
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:51-57 - Conditional CTA button based on count (confidence: 90%)
- /Users/phaedrus/Development/scry/hooks/use-polling-query.ts:15-45 - Polling pattern for time-sensitive data (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Review indicator shows due count with polling (60s interval). Large number display (text-4xl font-bold) with conditional singular/plural text. Shows "Start Review Session" button only when count > 0. Uses Target icon with consistent shadcn/ui card structure.

## Quick Action CTA Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:52-56 - Full-width primary CTA (Button asChild with Link) (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:59-64 - Primary CTA with icon in empty state (confidence: 95%)
- /Users/phaedrus/Development/scry/components/empty-states.tsx:48-53 - Multiple CTA pattern (primary + outline secondary) (confidence: 90%)
- /Users/phaedrus/Development/scry/app/page.tsx:37-46 - Header CTA with responsive text/icon (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: CTAs use Button asChild with Link for navigation. Full-width buttons (className="w-full") for primary actions. Icons with consistent sizing (h-4 w-4). Empty states often include CTAs. Responsive patterns hide text on small screens, show icons only.

## Recent Activity Display Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:74-101 - Card-based activity list with metadata (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:84-93 - Activity item metadata (score, timestamp) with icons (confidence: 95%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:95-97 - Color-coded performance indicator (confidence: 90%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:103-107 - Pagination hint text (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Recent activity uses Card components with hover effects. Each item shows title, metadata row with icons (Trophy, Calendar), and color-coded score. Uses date-fns formatDistanceToNow for relative timestamps. Performance colors: green (≥80%), yellow (≥60%), red (<60%).

## Navigation Between Dashboard Sections (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:17-27 - Tabbed navigation with icons for content switching (confidence: 95%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:65-82 - Dropdown navigation with consistent menu items (confidence: 90%)
- /Users/phaedrus/Development/scry/app/page.tsx:37-46,82-89 - Dashboard link in header and footer contexts (confidence: 90%)
- /Users/phaedrus/Development/scry/components/empty-states.tsx:54-59 - Cross-navigation between empty states (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 90%
**Notes**: Dashboard navigation uses Tabs component for section switching. Navbar dropdown includes Dashboard, My Quizzes, Review, Settings. Navigation links use consistent button styling (outline variant). Empty states provide cross-navigation between sections.

## Empty State Patterns for Dashboard (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:44-70 - Complete empty state with icon, text, and CTA (confidence: 98%)
- /Users/phaedrus/Development/scry/components/empty-states.tsx:10-28 - Reusable empty state pattern with consistent structure (confidence: 95%)
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:82-89 - Simple empty state with background styling (confidence: 90%)
- /Users/phaedrus/Development/scry/components/review-indicator.tsx:59-63 - Positive completion message ("all caught up") (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Empty states use Card with center alignment and py-12 padding. Structure: icon (w-16 h-16 in gray-100 circle), heading (text-lg font-semibold), description (text-gray-500), CTA button. Positive states use encouraging language. Icons from Lucide React with consistent sizing.

## External API Integration in Convex Actions
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Implementing external API calls (OpenRouter) within Convex actions with proper error handling and logging
**Solution**: Pattern-scout to find existing API integration patterns, adapt HTTP headers and request structure, implement comprehensive error handling with both HTTP status and response structure validation, use existing configuration constants
**Example**: OpenRouter API integration with proper HTTP-Referer, X-Title headers, comprehensive error handling (HTTP status + malformed response), detailed logging for debugging, environment variable validation
**Files**: /src/app/api/historical-context/route.ts (existing pattern), convex action implementation (new)

## Pattern Discovery for API Integrations
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Using pattern-scout to find existing API integration patterns before implementing new external API calls
**Solution**: Search for existing API implementations of the same service (OpenRouter) to discover proper headers, error handling, request structure, and response processing patterns
**Example**: Found existing OpenRouter implementation with exact header patterns (HTTP-Referer, X-Title), model configuration, and error handling structure that could be directly adapted for Convex action context
**Files**: /src/app/api/historical-context/route.ts:pattern-discovery

## Convex Action Error Handling Best Practices
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Implementing robust error handling in Convex actions for external API calls
**Solution**: Two-tier error handling: (1) HTTP status code validation with response.ok check, (2) Response structure validation for expected fields, detailed logging with context (puzzleId, year, attempt) for debugging
**Example**: HTTP status error handling + malformed response detection + comprehensive logging enables effective debugging and monitoring of external API integrations
**Files**: convex action implementation

## Configuration Constants Pattern for AI Integration
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Using existing configuration constants (AI_CONFIG) for prompt templates and model settings in new implementations
**Solution**: Leverage existing AI_CONFIG with prompt templates, model configuration, and settings rather than hardcoding values in new implementations
**Example**: AI_CONFIG provided prompts and google/gemini-2.5-flash model configuration that could be reused for historical context generation without duplicating configuration
**Files**: constants file with AI_CONFIG

## Search and Filter Input Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:117-127 - Search input with icon and placeholder text (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:88-95 - Client-side filtering with toLowerCase() search (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:28,123-124 - useState for search query management (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/input.tsx:7-26 - Base input component with consistent styling (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Search pattern: useState for query, Input with Search icon positioned absolute left-3, client-side filtering with includes() and toLowerCase(). Real-time filtering on every keystroke. Placeholder text describes searchable fields. Icon uses h-4 w-4 with text-gray-400 color.

## Table vs Card View Toggle Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:280-302 - Tabs component for view switching with icons (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:173-221 - Card view implementation with responsive grid (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:224-275 - Table view with shadcn/ui Table components (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:283-290 - TabsList with LayoutGrid and List icons (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: View toggle uses Tabs with TabsList grid w-40 grid-cols-2. Icons: LayoutGrid for cards, List for table. Card view uses md:grid-cols-2 lg:grid-cols-3 responsive grid. Table view uses shadcn Table components with TableHeader/Body/Row/Cell. Both views share same data props interface.

## Date Formatting and Relative Time Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:9,90,113 - formatDistanceToNow from date-fns for relative timestamps (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:29-37 - Intl.DateTimeFormat for absolute date/time formatting (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:74-85 - Custom formatRelativeTime function with days/hours/minutes (confidence: 90%)
- /Users/phaedrus/Development/scry/components/question-history.tsx:3,97 - date-fns formatDistanceToNow with addSuffix option (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Two approaches: date-fns formatDistanceToNow({addSuffix: true}) for "X ago" format, or custom relative time with Math.floor calculations. Intl.DateTimeFormat for precise timestamps in tables. date-fns preferred for user-friendly relative times. Both handle Date objects and timestamps.

## Pagination and Load More Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:29,97-99,233-242 - useState loadedCount with handleLoadMore function (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:38-41 - useQuery with dynamic limit parameter (confidence: 95%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:126-130 - hasMore indicator with count display (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:235-241 - Centered load more button with responsive width (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Pagination pattern: useState for loadedCount (initial 30), increment by 30 on load more. Conditional button display based on data.length >= loadedCount. Button styling: outline variant, centered with flex justify-center, responsive w-full sm:w-auto. hasMore from backend indicates more available.

## Loading Skeleton Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:39-89 - Card skeleton with structured layout matching real cards (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:92-136 - Table skeleton with proper TableHeader/Body structure (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:49-56 - Simple centered loading with Loader2 spinner (confidence: 90%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:82-89 - Array.from pattern for multiple skeleton items (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Two skeleton approaches: structured skeletons matching exact layout (preferred for complex layouts), or simple Loader2 spinner. Skeleton components use shadcn/ui Skeleton with proper sizing. Array.from({length: count}) pattern for multiple items. Export skeleton components for reuse across views.

## Dropdown Filter Menu Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/dropdown-menu.tsx:85-108 - DropdownMenuCheckboxItem for multi-select filters (confidence: 98%)
- /Users/phaedrus/Development/scry/components/ui/dropdown-menu.tsx:111-143 - DropdownMenuRadioGroup/RadioItem for single-select filters (confidence: 95%)
- /Users/phaedrus/Development/scry/components/navbar.tsx:34-98 - Complete dropdown implementation with menu items and separators (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/dropdown-menu.tsx:146-163,166-177 - DropdownMenuLabel and DropdownMenuSeparator for organization (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Filter dropdown structure: DropdownMenu -> Trigger -> Content -> (Label + Items + Separators). CheckboxItem for multi-select with checked prop, RadioGroup/RadioItem for single-select. Icons with size-4 sizing. Use DropdownMenuSeparator to group related options. Proper keyboard navigation built-in.

## Performance Score Color Coding Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:93-94,117-118 - Ternary operator color coding for performance scores (confidence: 98%)
- /Users/phaedrus/Development/scry/components/quiz-questions-grid.tsx:132-134,188-189 - Accuracy percentage calculation and display (confidence: 95%)
- /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:200-204,247-252 - Consistent score display with percentage calculation (confidence: 90%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:82-122 - Performance colors: green ≥80%, yellow ≥60%, red <60% (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 93.3%
**Notes**: Color coding: green-600 for ≥80%, yellow-600 for ≥60%, red-600 for <60%. Percentage calculation: Math.round((score / total) * 100). Display pattern: "X/Y (Z%)" format. Used consistently across cards, tables, and compact views. Null/undefined accuracy shows "—" or similar placeholder.

## Enhanced History Listing with Comprehensive Filtering
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Creating comprehensive history/listing pages with search, filtering, sorting, and dual view modes (table/card) while leveraging existing patterns
**Solution**: Combine search input patterns, dropdown filter menus, table/card view toggles, performance color coding, and loading skeletons. Use useMemo for efficient filtering/sorting operations. Apply Badge variant adaptations for different UI contexts.
**Example**: Quiz history page with search by topic, time/score filters, card/table toggle, responsive design, empty state differentiation. Pattern-scout provided 93%+ confidence patterns that enabled rapid implementation (~10 minutes).
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx

## Search Icon Positioning Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Positioning search icons consistently within input fields across different components
**Solution**: Use absolute positioning with left-3 for icon placement, add padding-left to input (pl-10) to account for icon space. Icon styling: absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4.
**Example**: Search input in quiz history page uses consistent icon positioning pattern found in quiz-questions-grid component. Creates familiar UX across different search interfaces.
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:search-input

## Time-Based Filter Calculations Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Implementing time-based filtering (last 7 days, 30 days, etc.) with date-fns calculations
**Solution**: Use date-fns subDays function to calculate cutoff dates, compare timestamps with Date.getTime() for filtering. Pattern: `isAfter(itemDate, subDays(new Date(), days))` for "within last X days" logic.
**Example**: Quiz history filtering by "Last 7 days", "Last 30 days", "Last 3 months" uses date-fns calculations to determine which items fall within the selected timeframe.
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:time-filter-logic

## Score Category Classification Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Categorizing quiz/test scores into performance tiers for filtering and display
**Solution**: Use threshold-based categorization: Excellent (≥80%), Good (60-79%), Needs Improvement (<60%). Consistent across filtering logic and color coding. Handle null/undefined scores appropriately.
**Example**: Quiz history filter allows filtering by score categories using established performance thresholds. Same thresholds used for color coding ensure UI consistency.
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:score-categorization

## Empty State Differentiation Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Distinguishing between "no data exists" vs "no results match current filters" empty states for better UX
**Solution**: Track filter state and show different empty states: "No quizzes found" for no data, "No quizzes match your filters" for filtered results. Include clear filter reset actions in filtered empty states.
**Example**: Quiz history shows different messages and actions when user has no quiz history vs when filters hide existing results. Helps users understand whether they need to take quizzes or adjust filters.
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:empty-state-logic

## Efficient Filtering with useMemo Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Implementing client-side filtering and sorting that doesn't cause unnecessary re-renders on every keystroke
**Solution**: Use useMemo with proper dependency arrays for filtering/sorting operations. Dependencies include search query, filter states, sort criteria, and data array. Prevents expensive operations from running when unrelated state changes.
**Example**: Quiz history filtering by search, time, score with real-time updates using useMemo dependency on [data, searchQuery, timeFilter, scoreFilter, sortBy, sortOrder]. Maintains performance even with large datasets.
**Files**: /Users/phaedrus/Development/scry/components/quiz-history-views.tsx:filtering-optimization

## Shared Component Organization Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/app/dashboard/page.tsx:1-2,125,150 - Direct component imports with @/components/ prefix (confidence: 98%)
- /Users/phaedrus/Development/scry/app/quizzes/quiz-history-client.tsx:48,201 - Same components imported in different pages (confidence: 95%)
- /Users/phaedrus/Development/scry/components/index.ts:1-11 - Central export file for reusable components (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/ - UI primitives organized in ui/ subfolder (confidence: 95%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Components organized flat in /components/ with direct imports using @/components/component-name. UI primitives in /components/ui/ subfolder. Some reusable components exported from index.ts file. QuizStatsRealtime and QuizHistoryRealtime used across multiple pages with direct import pattern. Auth components in /components/auth/ subfolder.

## Component Export Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx:9 - Named export function QuizStatsRealtime() (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:17 - Named export function with props interface (confidence: 95%)
- /Users/phaedrus/Development/scry/components/empty-states.tsx:10,30,67,92,148 - Multiple named exports from single file (confidence: 90%)
- /Users/phaedrus/Development/scry/components/index.ts:1-11 - Re-export pattern for barrel exports (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Primary pattern is named exports (export function ComponentName). No default exports found in components. Multiple related components can be exported from single file (empty-states.tsx). Some components re-exported from index.ts for convenience. TypeScript interfaces defined inline with components.

## Component Props Interface Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx:12-15 - Interface with optional props and defaults (confidence: 98%)
- /Users/phaedrus/Development/scry/components/question-history.tsx:8-11 - Interface with required and optional props (confidence: 95%)
- /Users/phaedrus/Development/scry/components/empty-states.tsx:6-8 - Simple interface with className prop (confidence: 90%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:50-62 - Complex interface with multiple required props (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 92%
**Notes**: Pattern: Define interface above component with ComponentNameProps naming convention. Use optional props with default values in function parameters. Include className?: string for styling flexibility. Required props come first, optional props after. No prop spreading patterns found.

## Component File Naming Conventions (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx - kebab-case with descriptive names (confidence: 98%)
- /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx - kebab-case following same pattern (confidence: 98%)
- /Users/phaedrus/Development/scry/components/ui/button.tsx - UI primitives use single word when possible (confidence: 95%)
- /Users/phaedrus/Development/scry/components/auth/auth-modal.tsx - Subfolder organization for related components (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-27
**Average confidence**: 95.3%
**Notes**: Consistent kebab-case naming (quiz-stats-realtime.tsx). Descriptive names indicating component purpose. UI primitives in ui/ subfolder use simpler names (button.tsx, card.tsx). Related components grouped in subfolders (auth/, icons/). Function names use PascalCase matching file purpose.

## Component Refactoring with Minimal File Operations
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Refactoring shared components to reduce duplication when components are already well-organized and reused across multiple locations
**Solution**: Use pattern-scout to assess current organization, identify truly shared components, move to logical subfolder (shared/), update imports with MultiEdit for efficiency, create barrel exports for cleaner imports
**Example**: Moving QuizStatsRealtime and QuizHistoryRealtime to /components/shared/ folder with index.ts barrel export, updating all imports from dashboard and quiz-history-client pages, leveraging existing flat component structure
**Files**: /Users/phaedrus/Development/scry/components/shared/quiz-stats-realtime.tsx, /Users/phaedrus/Development/scry/components/shared/quiz-history-realtime.tsx

## Pattern-Scout Effectiveness for Component Assessment
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Using pattern-scout to assess component organization and reuse patterns before implementing refactoring changes
**Solution**: Pattern-scout provides confidence levels about component organization and reuse patterns. High confidence (98%) indicates components are already well-organized and extensively reused, making refactoring straightforward.
**Example**: Pattern-scout revealed components were already well-organized and reused across multiple locations, indicating the codebase structure was sound and only needed minor organizational improvements
**Files**: Pattern-scout assessment results

## Barrel Export Patterns for Component Organization
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Creating cleaner import statements for shared components using barrel export pattern
**Solution**: Create index.ts file in shared component folders to re-export components, enabling imports like `from '@/components/shared'` instead of individual file paths
**Example**: Created /components/shared/index.ts with exports for QuizStatsRealtime and QuizHistoryRealtime, enabling cleaner imports in consuming components
**Files**: /Users/phaedrus/Development/scry/components/shared/index.ts

## MultiEdit for Efficient Import Updates
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Updating multiple import statements efficiently when refactoring component locations
**Solution**: Use MultiEdit tool to update imports across multiple files simultaneously, reducing manual editing and potential for errors in import path updates
**Example**: Updated imports in both dashboard page and quiz-history-client page from individual component imports to shared barrel export imports using MultiEdit
**Files**: Multiple files with import statement updates

---

## Convex Internal Mutation Implementation Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Implementing Convex internal mutations with comprehensive validation, error handling, and proper return formats
**Solution**: Pattern: args validation → document verification → patch operation → timestamp update → success return. Always include validation for document existence, field type checking, and minimum requirements. Use descriptive error messages matching codebase conventions.
**Example**: updateHistoricalContext mutation with args validation (puzzleId, historicalContext), document fetch with null check, minimum length validation, patch operation with updatedAt timestamp, structured return with success status and ID
**Files**: /convex/puzzles.ts:mutation-implementation

## Task Dependency Management in Multi-Step Implementation
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Managing logical dependencies between tasks where foundational work must be completed before dependent tasks can succeed
**Solution**: Identify task dependencies upfront, complete foundational tasks first (internal mutations before actions), then complete dependent tasks in logical order. This enables smooth integration and prevents blocking.
**Example**: Internal mutation implementation before action integration - mutation had to exist before action could call it via ctx.runMutation. Completing mutation first enabled seamless action integration.
**Files**: Multi-task implementation sequence

## Pattern-Driven Multi-Task Efficiency
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Completing multiple related tasks efficiently when pattern-scout provides clear implementation templates and patterns
**Solution**: When pattern discovery reveals comprehensive templates, identify all related tasks that can be completed using the same patterns. Complete them together rather than individually to maximize efficiency and maintain consistency.
**Example**: Found Convex patterns enabled completion of 5 related tasks: mutation creation, validation implementation, error handling, action integration, and logging - all following discovered pattern templates
**Files**: Pattern-scout discovery enabling multi-task completion

## TODO-Driven Integration Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 75
**Context**: Using existing TODO comments in codebase as integration hooks for new functionality
**Solution**: Look for TODO comments that indicate planned integration points. These provide clear guidance on where new functionality should connect and often include the exact integration pattern needed.
**Example**: TODO comment in action file specified exact mutation call pattern and import structure needed, making integration straightforward once mutation was implemented
**Files**: Action file with TODO integration guidance

## Mobile Overflow Debug Pattern for Fixed-Width Elements
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Identifying and fixing mobile layout overflow issues caused by fixed-width elements that exceed small screen constraints
**Solution**: Pattern: Calculate total width requirements (3 × 140px buttons = 420px) vs mobile viewport (320px min), replace fixed widths with responsive patterns: w-full sm:w-[140px] min-w-[120px]. Use flex-col sm:flex-row for mobile stacking.
**Example**: Filter controls with 3 fixed-width buttons (140px each) caused overflow on 320px screens. Fixed with w-full mobile, constrained desktop width, and vertical stacking pattern.
**Files**: /Users/phaedrus/Development/scry/components/quiz-filter-controls.tsx

## Pattern-Scout Confidence for Mobile Audit Efficiency
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Using high-confidence pattern analysis to avoid unnecessary changes during mobile responsiveness audits
**Solution**: When pattern-scout reports 93-95% confidence in existing responsive patterns, focus audit efforts on specific low-confidence areas rather than broad changes. High confidence indicates existing components already follow mobile-first patterns.
**Example**: Pattern analysis showed existing components were already responsive (93-95% confidence), allowing targeted focus on the one overflow issue rather than broad refactoring.
**Files**: Pattern-scout analysis results for mobile audit

## Responsive Button Width Pattern for Mobile Touch Targets
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Ensuring buttons provide adequate touch targets on mobile while maintaining desktop layout integrity
**Solution**: Use responsive width pattern: w-full for mobile (full-width touch-friendly), sm:w-[fixed] for desktop (constrained width), min-w-[value] for minimum usable size. Prevents overflow while maintaining usability.
**Example**: Filter buttons use w-full sm:w-[140px] min-w-[120px] pattern - full width on mobile for easy tapping, fixed width on desktop for consistent layout, minimum width prevents excessive shrinking.
**Files**: /Users/phaedrus/Development/scry/components/quiz-filter-controls.tsx

## Container Flex Direction Responsive Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Adapting container layouts to stack vertically on mobile while maintaining horizontal layout on larger screens
**Solution**: Use flex-col sm:flex-row pattern for containers that need different orientations based on screen size. Mobile-first approach stacks elements vertically by default, then switches to horizontal at small breakpoint (640px+).
**Example**: Filter controls container changed from fixed flex-row to flex-col sm:flex-row to stack buttons vertically on mobile, preventing horizontal overflow while maintaining desktop layout.
**Files**: /Users/phaedrus/Development/scry/components/quiz-filter-controls.tsx

## Mobile Audit Time Efficiency Through Pattern Recognition
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 92
**Context**: Completing mobile responsiveness audits quickly by leveraging existing pattern analysis rather than manual inspection
**Solution**: Use pattern-scout to analyze current responsive patterns first. High confidence scores (93-95%) indicate well-implemented mobile-first design. Focus audit time on specific low-confidence or newly identified issues rather than broad review.
**Example**: 5-7 minute audit completion vs estimated longer time. Pattern analysis revealed most components already responsive, enabling focused fix on one specific overflow issue.
**Files**: Mobile audit workflow pattern

## WCAG 2.1 AA Accessibility Compliance Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/form.tsx:114-119 - Form accessibility: aria-describedby, aria-invalid, proper ID association (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/button.tsx:7-8 - Focus management: focus-visible:ring-2 focus-visible:ring-gray-300 focus-visible:ring-offset-2 (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/loading-skeletons.tsx:9,36,54,77 - Loading state announcements: aria-hidden="true" aria-busy="true" (confidence: 85%)
- /Users/phaedrus/Development/scry/components/ui/dialog.tsx:75 - Screen reader support: <span className="sr-only">Close</span> (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 90%
**Notes**: Strong foundational accessibility through Radix UI primitives. Form controls have proper ARIA labeling and association. Focus management implemented for interactive elements. Screen reader text provided for icon-only buttons. Loading states properly announced. However, gaps exist in CRUD operations and modal focus trapping.

## Form Accessibility Implementation Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/form.tsx:94-104 - Label association: htmlFor={formItemId} with proper ID linking (confidence: 98%)
- /Users/phaedrus/Development/scry/components/ui/form.tsx:125-135 - Description linking: id={formDescriptionId} with aria-describedby (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/form.tsx:138-155 - Error message association: id={formMessageId} with ARIA support (confidence: 95%)
- /Users/phaedrus/Development/scry/components/ui/input.tsx:13 - Input validation states: aria-invalid:ring-red-500/20 aria-invalid:border-red-500 (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 94.5%
**Notes**: Excellent form accessibility implementation using React Hook Form integration. All form fields have proper label association, description linking, and error message connection. Visual validation states reflect ARIA attributes. Form controls automatically receive appropriate IDs and ARIA attributes.

## Button and Interactive Element Accessibility (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/button.tsx:7-8 - Comprehensive focus management: focus-visible:ring-2 with proper ring offset (confidence: 95%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:237,231 - Loading state accessibility: disabled={isLoading} with proper state management (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/dialog.tsx:75 - Icon button accessibility: sr-only text for close buttons (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/button.tsx:8 - Disabled state handling: disabled:pointer-events-none disabled:opacity-50 (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 90%
**Notes**: Strong focus management with visible focus indicators. Disabled states properly prevent interaction and provide visual feedback. Icon-only buttons include screen reader text. However, missing some ARIA labels for complex button actions in CRUD components.

## Modal and Dialog Accessibility Patterns (Scry Codebase)
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/dialog.tsx:61-65 - Dialog content structure with proper semantic markup (confidence: 85%)
- /Users/phaedrus/Development/scry/components/ui/alert-dialog.tsx:55-59 - AlertDialog with proper focus management through Radix primitives (confidence: 85%)
- /Users/phaedrus/Development/scry/components/question-edit-modal.tsx:82-91 - Form reset and state management in modals (confidence: 80%)
- /Users/phaedrus/Development/scry/components/ui/dialog.tsx:112-114 - Proper dialog title with DialogPrimitive.Title (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 85%
**Notes**: Basic modal accessibility provided by Radix UI primitives including focus trapping and escape key handling. Proper semantic structure with DialogTitle. However, missing explicit ARIA labels for complex modal actions and lacking focus restoration patterns in some cases.

## Loading State and Screen Reader Support (Scry Codebase)  
**Locations**:
- /Users/phaedrus/Development/scry/components/ui/loading-skeletons.tsx:9,36,54,77,91 - Consistent loading state pattern: aria-hidden="true" aria-busy="true" (confidence: 95%)
- /Users/phaedrus/Development/scry/app/loading.tsx:9 - Page-level loading with aria-busy and aria-hidden (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/dialog.tsx:75 - Screen reader text: <span className="sr-only">Close</span> (confidence: 90%)
- /Users/phaedrus/Development/scry/components/ui/alert.tsx:30 - Alert role: role="alert" for important messages (confidence: 95%)
**Times referenced**: 1
**Last used**: 2025-08-27
**Average confidence**: 92.5%
**Notes**: Excellent loading state accessibility with consistent aria-busy and aria-hidden patterns. Screen reader text provided for icon-only elements. Alert role used for important system messages. However, some async operations lack live region announcements for status updates.

## React Component Prop Threading Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Threading data through multiple React component layers when data is available at a parent but needed deep in the component tree
**Solution**: Use optional parameters in interfaces and function signatures to maintain backward compatibility while adding new data flow. Pattern: ParentComponent (has data) → IntermediateComponent (passes through) → TargetComponent (uses data)
**Example**: Puzzle number available in GameIsland needed to be threaded through GameLayout → GameInstructions → useShareGame → generateShareText. Used puzzleNumber?: number pattern throughout the chain.
**Files**: /Users/phaedrus/Development/chrondle/src/components/GameLayout.tsx, GameInstructions.tsx, useShareGame.ts, generateShareText.ts

## Hook Parameter Expansion with Backward Compatibility
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Adding new parameters to existing React hooks while maintaining compatibility with existing usage
**Solution**: Use optional parameters with meaningful defaults. Update hook interface to include new optional parameter, update implementation to handle both old and new usage patterns. Provide default behavior when new parameter is omitted.
**Example**: useShareGame hook expanded to accept puzzleNumber parameter while maintaining compatibility with existing calls that don't provide it. Optional parameter allows gradual adoption.
**Files**: /Users/phaedrus/Development/chrondle/src/hooks/useShareGame.ts

## Utility Function Input Validation Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Adding input validation to utility functions that accept optional parameters to ensure robust behavior
**Solution**: Validate optional parameters at function entry, provide sensible defaults or early returns for invalid inputs. Use TypeScript's optional parameter syntax (param?: type) combined with runtime validation for defensive programming.
**Example**: generateShareText function validates puzzleNumber parameter, uses default behavior when not provided or invalid. Prevents runtime errors and provides predictable output.
**Files**: /Users/phaedrus/Development/chrondle/src/lib/generateShareText.ts

## TypeScript Interface Evolution for Data Flow
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Evolving TypeScript interfaces to support new data requirements while maintaining existing functionality
**Solution**: Add optional properties to interfaces rather than required ones to maintain backward compatibility. Use systematic approach: update interfaces → update implementations → update calls. TypeScript compiler helps catch incomplete updates.
**Example**: Added puzzleNumber?: number to multiple component prop interfaces, enabling type-safe prop threading without breaking existing component usage.
**Files**: Multiple interface files in /Users/phaedrus/Development/chrondle/src/

## Component Data Flow Architecture Pattern
**First seen**: 2025-08-27
**Last used**: 2025-08-27
**Times referenced**: 1
**Effectiveness**: 92
**Context**: Understanding and working with existing component data flow architecture to add new data paths efficiently
**Solution**: Map out existing data flow before implementing changes. Identify the shortest path from data source to consumption point. Use existing patterns (prop passing, hook parameters) rather than introducing new architectures for consistency.
**Example**: Successfully mapped GameIsland → GameLayout → GameInstructions → useShareGame → generateShareText data flow, added puzzle number threading using established prop-passing patterns.
**Files**: Component chain in Chrondle application

## Convex Database Testing with Test Implementation Pattern
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Testing Convex backend mutations with comprehensive CRUD operations following Leyline no-internal-mocking principle
**Solution**: Create TestConvexDB class that simulates real database operations without mocking internal components. Implement full database interface (insert, patch, query, get) with proper ID generation, timestamps, and session management. Use createTestContext to provide proper mutation context.
**Example**: 22 tests covering updateQuestion, softDeleteQuestion, restoreQuestion with permission validation, soft delete behavior, FSRS data preservation, and edge cases. TestConvexDB provided realistic database simulation enabling thorough testing.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:12-109

## Convex Mutation Handler Access Pattern
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Accessing the actual handler function from Convex mutation objects for unit testing
**Solution**: Convex mutations expose their handler via `_handler` property, not `handler`. Use `mutationName._handler(ctx, args)` pattern to invoke mutation functions in tests with proper context and arguments.
**Example**: `updateQuestion._handler(ctx, { sessionToken, questionId, question })` correctly invokes the mutation. Initial attempt with `handler` property failed, `_handler` discovered through debugging process.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:185,297,374

## Authentication Context Simulation for Testing
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Creating realistic authentication context for testing Convex mutations that require session validation
**Solution**: Implement test session management in TestConvexDB with insertSession/querySession methods. In createTestContext, implement db.query('sessions') to return proper session lookup functionality that matches real Convex query patterns.
**Example**: Session creation with userId, token, expiresAt fields, then query implementation that finds sessions by token for authentication validation in mutations.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:20-32,89-106

## FSRS Data Preservation Testing Pattern
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 90
**Context**: Verifying that CRUD operations preserve complex spaced repetition data (FSRS fields) during updates
**Solution**: Set up test data with complete FSRS fields (stability, difficulty, state, review times), capture original values before operation, perform update, then verify all FSRS fields remain unchanged while confirming editable fields were updated.
**Example**: Test verified that updating question text/topic preserved all 9 FSRS fields (nextReview, stability, fsrsDifficulty, elapsedDays, scheduledDays, reps, lapses, state, lastReview) while allowing content changes.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:515-557

## Comprehensive Permission Testing Coverage
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Testing creator-only permission model across all CRUD operations with multiple user scenarios
**Solution**: Set up multiple test users and questions with different ownership. Test all operations (update, delete, restore) against both owned and non-owned resources. Include authentication edge cases (invalid tokens, expired sessions, missing tokens).
**Example**: Every mutation tested against: valid user with owned resource, valid user with non-owned resource, invalid session token, expired session, missing session. Comprehensive coverage of authorization matrix.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:211-221,316-325,394-405

## Soft Delete State Testing Pattern
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Testing soft delete functionality that preserves data while marking items as deleted with proper state transitions
**Solution**: Test soft delete operation preserves all original data while adding deletedAt timestamp. Test that operations on deleted items are properly rejected. Test restore operation removes deletedAt and adds updatedAt. Verify state transitions are atomic.
**Example**: Soft delete preserves question content and FSRS data while adding deletedAt. Updates/deletes rejected on deleted items. Restore removes deletedAt, adds updatedAt, preserves all other data.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:294-314,365-392,419-441

## Edge Case and Concurrency Testing Pattern
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 85
**Context**: Testing mutation behavior under edge conditions and concurrent operations to ensure robust error handling
**Solution**: Test non-existent resources, already-deleted items, empty/invalid inputs, expired sessions, concurrent operations using Promise.allSettled. Focus on graceful degradation and proper error messages.
**Example**: Concurrent update and delete operations tested with Promise.allSettled, expired session simulation with past expiresAt timestamps, empty string validation for required fields.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:490-512,470-488,234-257

## Leyline No-Internal-Mocking Testing Principle
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 98
**Context**: Following Leyline testing philosophy of only mocking external systems (database) without mocking internal components
**Solution**: Create realistic test implementation of external system (TestConvexDB) that behaves like real database but doesn't mock internal business logic. Test actual mutation functions with realistic context and data flow.
**Example**: TestConvexDB implements full database interface (insert, patch, query, get) with proper ID generation, timestamps, and relationships. Mutations tested with real business logic against realistic data layer.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:10-12,74-108

## Time Estimation for Comprehensive Unit Testing
**First seen**: 2025-08-28
**Last used**: 2025-08-28
**Times referenced**: 1
**Effectiveness**: 95
**Context**: Successfully completing comprehensive unit test suites for CRUD mutations in reasonable time frames
**Solution**: When following established testing patterns and having clear requirements, comprehensive unit test coverage (22 tests) for CRUD operations can be achieved in ~45 minutes including debugging time.
**Example**: Complete test suite covering 3 mutations with permission validation, data preservation, soft delete behavior, edge cases, and authentication scenarios completed in 45 minutes total.
**Files**: /Users/phaedrus/Development/scry/convex/questions.crud.test.ts:complete-test-suite

<!-- New patterns will be added as discovered -->