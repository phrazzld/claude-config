# Knowledge Base - Lessons Learned

This file tracks valuable patterns, gotchas, and estimation insights extracted from real task execution.

## Code Patterns

### TypeScript Type Refinement
- **API response transformation**: Convex queries naturally transform raw database types into API response types with computed fields (id, percentage) - embrace this pattern instead of complex type unions
- **Interface over any**: When transforming between database and API types, create explicit interfaces rather than using `any` - type inference works well but explicit interfaces prevent drift

### DRY Principle Application
- **Authentication helpers**: Duplicated `getAuthenticatedUserId` helpers across Convex files should be extracted to `convex/lib/auth.ts` - this pattern appears in 3+ files in full-stack apps
- **Shared utilities location**: Convex projects benefit from `convex/lib/` directory for shared utilities between mutations, queries, and actions

### Migration Patterns
- **Defensive programming preservation**: Well-architected codebases often have proper error handling and type safety already in place - check existing patterns before implementing new ones
- **JSON parsing consistency**: When migrating from string to object formats, defensive JSON parsing with try/catch blocks is a good indicator that migration is already complete

## CI/CD Patterns

### Convex Integration
- **Generated TypeScript files**: Convex projects require `npx convex codegen` in CI pipelines to generate TypeScript definitions that are typically gitignored
- **No push needed**: The `convex codegen` command doesn't require flags for basic type generation - it just generates the necessary .d.ts files
- **Environment variables**: Set CONVEX_DEPLOYMENT to specify which Convex deployment to use for code generation
- **Caching optimization**: Cache Convex generated files using schema files as cache key - significant performance win since codegen is expensive
- **Conditional generation**: Only run `convex codegen` on cache miss to avoid unnecessary work

## Documentation Patterns

### Pattern Discovery
- **Documentation archaeology**: Before writing new docs, use pattern-scout or grep to discover existing documentation conventions in the project
- **Consistency indicators**: Look for emoji usage in headers, section structure patterns, and formatting conventions - consistency suggests mature documentation practices
- **Troubleshooting formats**: Many projects follow problem/symptom/solution structure - adopt the established pattern rather than inventing new ones

### Integration Strategy
- **Cross-referencing**: Well-maintained projects often have interconnected documentation with clear links between related topics
- **Environment separation**: Document dev vs prod configurations clearly, following project's established environment documentation patterns

## Common Gotchas

### Refactoring Safety
- **Test coverage first**: Before extracting shared utilities, verify test coverage exists - refactoring with 76/76 passing tests gives confidence
- **Import path updates**: When extracting helpers to lib/ directories, update all import paths simultaneously to avoid build breakage

### CI Pipeline Issues
- **Missing generated files**: When CI fails on TypeScript errors for "missing" files that exist locally, check if they're generated files that need a build step in CI
- **Invalid command flags**: Don't assume CLI commands support standard flags like `--no-push` without checking documentation first
- **Duplicate steps across jobs**: CI workflows often duplicate steps between test/build jobs - use `replace_all` when editing identical steps to avoid edit conflicts

### Deployment Platform Issues
- **CI pass ≠ deployment success**: CI can pass while deployment fails due to different build environments and processes
- **Platform-specific build commands**: Each deployment platform (Vercel, Netlify, etc.) may require different build command configurations even when CI works
- **Generated files in deployments**: Platforms like Vercel need explicit build commands for projects with code generation steps, even if CI handles it separately

### Task Verification vs Implementation
- **TODO archaeology**: TODO items may be for verification/validation rather than implementation - check if work is already complete before starting implementation
- **Pattern-scout for quick verification**: Use pattern-scout agent to quickly verify if migrations or refactors are already complete before spending time on implementation

## Good Questions to Ask

### Refactoring Planning
- "What authentication patterns are duplicated across this codebase?" - Look for `getAuthenticatedUserId` or similar patterns in multiple files
- "Are there explicit interfaces for API response types or is `any` being used?" - Type safety wins compound over time
- "What shared utilities would benefit from extraction to a lib/ directory?"

### CI Troubleshooting
- "Are there any generated files that might be gitignored but needed for CI?"
- "What build or generation steps happen locally that might be missing in CI?"
- "Does this project use any code generation tools that need to run before type checking?"
- "What expensive operations in CI could benefit from caching?" - Look beyond just dependencies to generated files, compiled assets, etc.

### Deployment Troubleshooting
- "Is the deployment platform using the same build process as CI?" - Different platforms may need explicit build commands
- "What code generation happens locally that the deployment platform might be missing?"
- "Does this deployment platform understand this project's build complexity?" - Simple projects may work with default commands, complex ones need explicit configuration

### Documentation Strategy
- "What existing documentation patterns does this project follow?" - Use pattern-scout or grep to find style consistency before writing new docs
- "How does this project structure troubleshooting sections?" - Look for problem/symptom/solution formats

### Task Validation
- "Is this a TODO for implementation or verification?" - Check if the work described in TODOs is already complete
- "What patterns would indicate this migration/refactor is already done?" - Look for defensive programming, proper error handling, consistent interfaces

## Time Estimation Wisdom

### Code Quality Refactoring
- **Type safety improvements**: 10-20 minutes for replacing `any` types with proper interfaces when transformations are straightforward
- **Utility extraction**: 15-25 minutes for extracting shared helpers from 3-4 files with good test coverage
- **Key factors**: Test coverage quality, import complexity, number of files affected

### CI Pipeline Fixes
- **Simple infrastructure fixes**: 10-30 minutes typical (adding missing build steps, fixing environment variables)
- **Caching optimization**: 5-10 minutes when adding caching to existing expensive operations (like Convex codegen)
- **Key factors**: Whether it's a missing step vs. fundamental architecture issue, familiarity with the CI platform, availability of existing caching patterns to follow

### Documentation Tasks
- **Pattern-following documentation**: 5-10 minutes when following established project patterns and structure
- **Key factors**: Whether existing patterns exist and are discoverable, complexity of the topic being documented

### Deployment Configuration
- **Simple deployment fixes**: 5-15 minutes for configuration file updates (adding build commands, environment variable setup)
- **Key factors**: Whether it's just missing configuration vs. fundamental deployment architecture mismatch, familiarity with deployment platform's configuration format

### Task Verification
- **Pattern-scout verification**: 30 seconds - 2 minutes to determine if work is already complete vs 10-30 minutes for actual implementation
- **Key factors**: Clear patterns to search for, well-organized codebase structure, existence of defensive programming patterns