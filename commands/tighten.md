Ruthlessly eliminate unnecessary code and complexity.

# TIGHTEN

What would Marie Kondo do to your codebase? Identify everything that doesn't spark joy and mark it for deletion.

## The Minimalism Principle

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* - Antoine de Saint-Exupéry

This command hunts for code that exists but shouldn't. Dead code is technical debt that compounds silently.

## 1. Dead Code Detection

**Channel the Carmack Philosophy**: "If it's not being executed, it's not code - it's a liability."

**Hunt for zombie code:**
- Unused functions, classes, and modules
- Commented-out code blocks (git remembers, you don't need to)
- Unreachable code after returns/throws
- Feature flags that are permanently on/off
- Debug code that made it to production

**The Deletion Test**: If you deleted this code, would anyone notice in the next 6 months?

**Generate deletion candidates:**
- [ ] Remove 50 lines of commented code from module X
- [ ] Delete unused utility function Y (last called 2019)
- [ ] Remove unreachable code after early return in Z

## 2. Dependency Audit

**What would Rich Hickey ask?** "Is this dependency simpler than writing it yourself?"

**Examine package.json/requirements.txt/go.mod:**
- Dependencies with 1-2 function usage (inline them)
- Packages last updated 3+ years ago (security risk)
- Multiple packages doing the same thing
- Dev dependencies in production
- The legendary `left-pad` pattern (3-line packages)

**The 10-Line Rule**: If you can replace a dependency with 10 lines of code, do it.

## 3. Configuration Cleanup

**Channel Marie Kondo directly**: "Does this config value spark joy?"

**Review all configuration files:**
- Webpack/Vite/build configs with 200 lines of defaults
- ESLint rules that everyone disables
- Environment variables that are always the same value
- Docker configs mounting volumes that don't exist
- CI/CD steps that are always skipped

**The Single-Value Test**: If a config has never changed, it's not configuration - it's complexity.

## 4. Abstraction Archaeology

**Torvalds Mode**: "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."

**Find premature abstractions:**
- Interfaces with single implementations
- Factory patterns making one type of object
- Abstractions used in only one place
- 5-layer deep inheritance hierarchies
- Generic solutions for specific problems

**The YAGNI Scan**: You Aren't Gonna Need It - probably ever.

## 5. File System Archaeology

**What would Ken Thompson delete?**

**Scan for file system cruft:**
- Empty directories and files
- Backup files (.bak, .old, .save)
- Build artifacts checked into version control
- Documentation for deleted features
- Test files for deleted code
- Migration scripts from 3 years ago

## Output Format

```markdown
## Codebase Tightening Analysis

### Dead Code Found (500+ lines to delete)
- **src/utils/legacy.js**: 200 lines - unused since refactor
- **api/v1/**: 150 lines - old API version, no traffic for 1 year
- **lib/helpers.js:45-95**: 50 lines - commented "temporary fix 2019"

### Dependency Bloat (8 packages to remove)
- **moment.js** (65kb): Using 1 function, replace with native Date
- **lodash**: Using only `_.get`, write 5-line replacement
- **axios**: fetch() is built-in now

### Config Simplification (200 lines to cut)
- **webpack.config.js**: 150 lines of defaults, need only 20
- **.eslintrc**: 35 rules disabled everywhere
- **docker-compose.yml**: 3 services never used

### Abstraction Overkill
- **IUserFactory**: Makes only User objects, inline it
- **AbstractBaseSingletonFactory**: Used once, adds no value
- **5 interface files**: Single implementations, premature abstraction

### File System Cleanup
- **12 empty directories**: Old feature folders
- **25 .bak files**: Use git, not file.bak
- **test/old/**: 2000 lines of tests for deleted features

## Deletion TODOs (Prioritized)
- [ ] [CRITICAL] Remove src/utils/legacy.js - 200 lines of dead code
- [ ] [HIGH] Delete moment.js dependency - save 65kb bundle size
- [ ] [HIGH] Inline IUserFactory - remove unnecessary abstraction
- [ ] [MEDIUM] Clean webpack.config.js - reduce from 170 to 20 lines
- [ ] [LOW] Delete all .bak files - git handles versioning
```

## The Marie Kondo Test

For each piece of code, ask:
1. Does it serve a current purpose?
2. Will it realistically serve a future purpose?
3. Does it make the codebase better or just bigger?

If the answer to all three is "no" - thank it for its service and let it go.

## Success Metrics

**Before**: 50,000 lines of code, 45 dependencies, 500 lines of config
**After**: 40,000 lines of code, 30 dependencies, 100 lines of config
**Result**: Same functionality, 20% less complexity

Remember: **Every line of code is a liability. Only keep the ones that pay rent.**