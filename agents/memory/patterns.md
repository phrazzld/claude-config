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

## Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/__tests__/DarkModeToggle.a11y.test.tsx:14-46 - Comprehensive accessibility testing with axe-core (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:24-50 - Next.js Image mocking pattern with onError support (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/map/__tests__/page.test.tsx:140-169 - Error handling and edge case testing (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/test-utils/component-test-patterns.md:364-434 - Form validation and debounce testing patterns (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/__tests__/TypewriterQuotes.test.tsx:157-191 - Component lifecycle and unmount testing (confidence: 85%)
**Times referenced**: 3
**Last used**: 2025-08-21
**Average confidence**: 91%
**Notes**: Key patterns: 90%+ coverage requires comprehensive mocking, error simulation, edge cases, accessibility testing, and lifecycle management. Use jest.Mock for external dependencies and simulate user interactions.

## Node.js Filesystem Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:11-24 - Complete fs module mocking setup (confidence: 98%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:28-31,54-56 - fs.readdirSync and fs.readFileSync mocking (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:69-74,85-91 - Error simulation for filesystem operations (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:100-116 - Performance testing with large filesystem operations (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 94.5%
**Notes**: Pattern: jest.mock('fs') at top level, cast as jest.Mocked<typeof fs>, mock specific methods with mockReturnValue/mockImplementation. Test both success and error scenarios, including ENOENT errors.

## Gray-matter/Markdown Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:12,16 - gray-matter module mocking setup (confidence: 98%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:33-41,126-147 - Mock frontmatter data and content parsing (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:427-435 - Gray-matter parsing error simulation (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/lib/__tests__/data.test.ts:437-449 - Binary content handling tests (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 93.3%
**Notes**: Pattern: jest.mock('gray-matter'), cast as jest.MockedFunction<typeof matter>, mock with { data: {}, content: '' } structure. Test malformed frontmatter, binary content, and parsing errors.

## Script Testing Patterns (Migration Scripts)
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:244-250 - Module exports for testability (confidence: 95%)
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:240-242 - Main execution guard pattern (confidence: 95%)
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:34-45,107-114 - Filesystem operation with error handling (confidence: 90%)
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:129-137 - Continue on error pattern (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 92.5%
**Notes**: Pattern: Export functions for testing with module.exports. Use require.main === module guard for CLI execution. Handle errors gracefully with try/catch and continue processing.

## CLI Testing Infrastructure
**Locations**:
- /Users/phaedrus/Development/vanity/jest.config.js:10-25 - Jest module mocking configuration (confidence: 95%)
- /Users/phaedrus/Development/vanity/jest.config.js:42-58 - Coverage thresholds for testing (confidence: 90%)
- /Users/phaedrus/Development/vanity/jest.config.js:61-66 - Test file patterns and transforms (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: Standard Jest setup with moduleNameMapper for mocking, setupFilesAfterEnv for test setup, testMatch for finding test files. Supports both Node.js and browser environments.

## Image Error Handling Testing
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:24-50 - Mock Image component with onError callback testing (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:122-125 - Image onError handler with logger.warn (confidence: 95%)
- /Users/phaedrus/Development/vanity/jest.setup.js:238-244 - Global next/image mock setup (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 93.3%
**Notes**: Pattern: Mock next/image to return testable element with onError prop. Test image error by triggering onError callback. Use data-testid for reliable testing. Mock logger to verify error handling.

## Mock Component Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:16-21 - Mock utility functions with jest.fn().mockReturnValue (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/map/__tests__/page.test.tsx:13-18 - Mock data fetching functions (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/__tests__/TypewriterQuotes.test.tsx:23-40 - Mock modules with complex behavior (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/test-utils/dynamic-import-helpers.tsx:42-62 - Dynamic import mocking patterns (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91.3%
**Notes**: Use jest.mock() at module level. Mock with jest.fn().mockReturnValue() for simple returns. Use jest.fn().mockImplementation() for complex behavior. Clear mocks in beforeEach().

## Coverage Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/jest.config.js:42-59 - Coverage threshold configuration (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/test-utils/component-test-patterns.md:300-350 - Comprehensive test organization for coverage (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/map/__tests__/page.test.tsx:89-169 - Edge cases and error scenarios testing (confidence: 90%)
- /Users/phaedrus/Development/vanity/CONTRIBUTING.md:276,414 - Coverage requirements: 85% general, 90% core (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: 90% coverage requires: all code paths, error scenarios, edge cases, user interactions, theme variations, accessibility tests, lifecycle methods, and prop variations.

## Accessibility Testing with 90%+ Coverage
**Locations**:
- /Users/phaedrus/Development/vanity/src/test-utils/a11y-helpers.tsx:33-96 - checkA11y and checkA11yInBothThemes helpers (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/__tests__/DarkModeToggle.a11y.test.tsx:34-45 - Custom axe configuration testing (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/test-utils/a11y-helpers.tsx:159-203 - Configurable a11y rules for different component types (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/test-utils/a11y-helpers.tsx:111-153 - Responsive accessibility testing (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91.3%
**Notes**: Use checkA11y() and checkA11yInBothThemes() helpers. Test with a11yRules.basic for components. Include keyboard navigation, focus management, and ARIA attributes in tests.

## Audiobook Field Handling Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/lib/data.ts:30 - Boolean cast with default false (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/types/reading.ts:38,54,69 - Optional boolean field in interfaces (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:221-235 - Conditional emoji display in hover overlay (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/commands/reading.ts:154-161,389-391 - inquirer.prompt boolean confirm + frontmatter assignment (confidence: 90%)
- /Users/phaedrus/Development/vanity/scripts/generate-static-data.js:51 - Missing audiobook handling (confidence: 80%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91%
**Notes**: Pattern: `(data.audiobook as boolean) || false` for parsing. Always optional boolean with false default. UI shows "🎧 Audiobook" in hover overlay. CLI uses inquirer confirm prompt.

## Hover Effects and CSS Transitions
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:91,96-98,135-151 - Minimalist hover overlay with smooth transitions (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:139-141 - Button hover with scale and shadow effects (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/globals.css:241-244 - Project card hover with scale and shadow (confidence: 85%)
- /Users/phaedrus/Development/vanity/src/app/globals.css:159,186 - Link underline hover animation (confidence: 80%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 87.5%
**Notes**: Preferred pattern: 0.2s-0.3s ease transitions, subtle scale transforms (1.01-1.05), box-shadow changes. ReadingCard shows best practices for overlay hover states.

## CSS Transition Performance Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/globals.css:66-70 - Global theme transitions with performance optimization (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/globals.css:77-82 - Reduced motion respect (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/globals.css:84-87 - GPU acceleration for theme transitions (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:50-58 - GPU acceleration and animation state management (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 92.5%
**Notes**: Use cubic-bezier(0.4, 0, 0.2, 1) timing, respect prefers-reduced-motion, use transform-gpu for 60fps, avoid animating layout properties.

## Accessibility Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/globals.css:137-139 - Focus-visible outline styles (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:148 - Semantic aria-label with state (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/test-utils/a11y-helpers.tsx:33-44 - Accessibility testing pattern (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:98 - Meaningful title attributes (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91.3%
**Notes**: Use focus-visible for keyboard navigation, aria-labels should describe current state and action, test with jest-axe. Primary colors for focus rings.

## Icon/Emoji Overlay Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:216-230 - Audiobook emoji indicator in overlay (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:151-188 - Icon state management with animations (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 92.5%
**Notes**: ReadingCard shows perfect pattern for conditional emoji display in hover overlay. Use rgba colors and gap spacing for icon+text combinations.

## Animation State Management
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:59-65 - Click spam prevention with animation state (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:67-86 - Intersection observer for performance (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:63,96-97 - Simple hover state management (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: Use React state for hover/animation tracking, implement spam click prevention, defer animations until visible for performance.

## Screen Reader Compatible Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/DarkModeToggle.tsx:96 - aria-hidden for decorative elements (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/test-utils/a11y-helpers.tsx:159-203 - Comprehensive a11y rule configurations (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 92.5%
**Notes**: Use aria-hidden="true" for decorative elements, test with multiple a11y rule sets, consider color-contrast and button-name rules.

## File Deletion Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:131 - fs.unlinkSync with error handling (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/lib/editor.ts:1,37,48 - unlinkSync import and cleanup usage (confidence: 90%)
- /Users/phaedrus/Development/vanity/scripts/validate-security-pipeline.js:72 - fs.unlinkSync simple usage (confidence: 80%)
- /Users/phaedrus/Development/vanity/scripts/analyze-bundle.js:110 - fs.unlinkSync simple usage (confidence: 80%)
**Times referenced**: 2
**Last used**: 2025-08-21
**Average confidence**: 86.3%
**Notes**: Prefer fs.unlinkSync over async for CLI operations. Always use try/catch. Continue on error for batch operations.

## User Confirmation Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/cli/commands/place.ts:125-135 - inquirer.prompt confirm pattern (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/commands/place.ts:146-156 - overwrite confirmation pattern (confidence: 90%)
- /Users/phaedrus/Development/vanity/cli/commands/project.ts:176-186 - confirm creation pattern (confidence: 90%)
- /Users/phaedrus/Development/vanity/cli/commands/project.ts:197-207 - overwrite confirmation pattern (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91.3%
**Notes**: Standard pattern: inquirer.prompt with type: 'confirm', message with chalk.yellow for warnings

## CLI Color/Logging Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:22-28 - manual chalk implementation (confidence: 85%)
- /Users/phaedrus/Development/vanity/cli/commands/reading.ts:104+ - chalk import with consistent colors (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/commands/quote.ts:34+ - chalk color patterns (confidence: 90%)
**Times referenced**: 2
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: Green for success (✅), red for errors (✖), yellow for warnings/cancellation, cyan for headers, gray for details

## Error Handling Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:129-137 - try/catch with continue on error (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/lib/editor.ts:45-55 - cleanup on error pattern (confidence: 90%)
- /Users/phaedrus/Development/vanity/cli/commands/reading.ts:414+ - prompt cancellation handling (confidence: 85%)
**Times referenced**: 2
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: Always cleanup resources on error. Handle prompt cancellations gracefully. Continue processing on non-critical errors.

## Authentication Patterns
**Locations**: 
- (No patterns discovered yet)
**Times referenced**: 0
**Last used**: Never
**Average confidence**: N/A
**Notes**: Patterns will be added as discovered

## API Endpoint Patterns
**Locations**:
- (No patterns discovered yet)
**Times referenced**: 0
**Last used**: Never
**Average confidence**: N/A
**Notes**: REST/GraphQL endpoint structures

## Component Patterns
**Locations**:
- (No patterns discovered yet)
**Times referenced**: 0
**Last used**: Never
**Average confidence**: N/A
**Notes**: UI component implementations

## ReadingsList Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:114 - Tests audiobook badge display (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:118-139 - Column header sorting tests (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:141-164 - Reading item selection tests (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:166-180 - Search term highlighting tests (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:182-214 - Empty state testing (confidence: 85%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 91%
**Notes**: Key patterns: Test audiobook indicators with textContent.toContain('🎧 Audiobook'), test sorting via fireEvent.click on column headers, test selection with role="button" queries, test search highlighting with getAllByRole('mark')

## Status Badge Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:452-479 - Dropped status removal verification (confidence: 98%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:130-141 - Audiobook indicator testing (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:245-261 - Badge styling verification (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:143-157 - Binary status testing (reading/finished) (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 94.5%
**Notes**: Pattern: Use queryByText(/paused/i) and queryByText(/dropped/i) with .not.toBeInTheDocument() to verify removed statuses. Test audiobook badges with getByText('🎧 Audiobook'). Only test binary states: "Currently Reading" and "Finished"

## Audiobook Indicator Testing Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingsList.tsx:370-374 - Badge implementation in list view (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingsList.test.tsx:80-81,114 - Test data setup and verification (confidence: 95%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/__tests__/ReadingCard.test.tsx:161-183,245-261 - Hover state and visibility testing (confidence: 90%)
- /Users/phaedrus/Development/vanity/src/app/components/readings/ReadingCard.tsx:221-235 - Card hover overlay implementation (confidence: 90%)
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 92.5%
**Notes**: Test pattern: Mock data with audiobook: true, verify with container.textContent.toContain('🎧 Audiobook'), test hover states for card overlays, use blue badge styling (bg-blue-100 dark:bg-blue-900/50)

---

## Example Pattern Format (for reference)

<!-- This shows how patterns will be recorded when discovered:

## React Hook Pattern: Custom useFetch
**Locations**:
- src/hooks/useFetch.ts:12-45 - Main implementation (confidence: 95%)
- src/hooks/useApi.ts:23-67 - Similar pattern with auth (confidence: 82%)
- components/Dashboard/data.ts:89-120 - Usage example (confidence: 70%)
**Times referenced**: 8
**Last used**: 2025-08-21
**Average confidence**: 82.3%
**Notes**: Preferred pattern for API calls with loading states and error handling

-->

<!-- New patterns will be added as discovered -->