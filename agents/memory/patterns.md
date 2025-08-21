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

## Error Handling Patterns
**Locations**:
- (No patterns discovered yet)
**Times referenced**: 0
**Last used**: Never
**Average confidence**: N/A
**Notes**: Try/catch, error boundaries, validation

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