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

## File Deletion Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:131 - fs.unlinkSync with error handling (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/lib/editor.ts:1,37,48 - unlinkSync import and cleanup usage (confidence: 90%)
- /Users/phaedrus/Development/vanity/scripts/validate-security-pipeline.js:72 - fs.unlinkSync simple usage (confidence: 80%)
- /Users/phaedrus/Development/vanity/scripts/analyze-bundle.js:110 - fs.unlinkSync simple usage (confidence: 80%)
**Times referenced**: 1
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
**Times referenced**: 1
**Last used**: 2025-08-21
**Average confidence**: 90%
**Notes**: Green for success (✅), red for errors (✖), yellow for warnings/cancellation, cyan for headers, gray for details

## Error Handling Patterns
**Locations**:
- /Users/phaedrus/Development/vanity/scripts/migrate-reading-status.js:129-137 - try/catch with continue on error (confidence: 95%)
- /Users/phaedrus/Development/vanity/cli/lib/editor.ts:45-55 - cleanup on error pattern (confidence: 90%)
- /Users/phaedrus/Development/vanity/cli/commands/reading.ts:414+ - prompt cancellation handling (confidence: 85%)
**Times referenced**: 1
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

## Testing Patterns
**Locations**:
- (No patterns discovered yet)
**Times referenced**: 0
**Last used**: Never
**Average confidence**: N/A
**Notes**: Unit tests, integration tests, mocks

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