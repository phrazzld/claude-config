Execute the next available task from TODO.md.

# EXECUTE

Grab next task from TODO.md → Think about approach → Do the work → Commit atomically → Mark complete

## PROCESS

1. **Find next task**: Look for first `[~]` (in-progress) or `[ ]` (not started) task in TODO.md
2. **Mark in-progress**: Update `[ ]` to `[~]`
3. **Think very hard before acting**:
   - Think very hard
   - Consider the approach and plan implementation
   - Look for existing patterns in the codebase to follow
   - Identify relevant files and implementation approach
   - **🎯 SIMPLICITY VALIDATION**: Ask "What's the simplest solution that completely solves this?"
     - Reject clever solutions in favor of boring, obvious ones
     - If you can't explain it to a junior dev, it's too complex
     - Prefer explicit over implicit behavior
4. **Do the work**: Implement what the task describes
   - **🎯 SIMPLICITY DURING IMPLEMENTATION**:
     - Choose boring technology over exciting alternatives
     - Write code that reads like documentation
     - Make the happy path obvious
     - Keep cyclomatic complexity low
   - **🎯 MAINTAINABILITY PRINCIPLE**:
     - Write for the next developer (who might be you in 6 months)
     - Name things based on what they do, not how they work
     - Leave breadcrumbs: clear function signatures, explicit types
     - Optimize for readability over cleverness
     - Future changes should be obvious, not archaeological digs
   - **🎯 FIX BROKEN WINDOWS**:
     - See a problem? Fix it now. Technical debt compounds.
     - Notice a typo? Fix it. Poor naming? Rename it.
     - Find commented code? Delete it. Git remembers.
     - Spot inconsistent formatting? Correct it immediately.
     - Quality erosion starts with "I'll fix it later"
   - **🎯 EXPLICIT OVER IMPLICIT**:
     - Show dependencies clearly in function signatures
     - Avoid global state and hidden side effects
     - Make data flow obvious, not magical
     - Prefer explicit parameters over implicit context
     - If behavior isn't obvious from the signature, it's too implicit
   - **🎯 BINDING VALIDATION**:
     - Check file type: TypeScript? Go? React? Database schema?
     - Apply relevant technology bindings automatically
     - Validate architecture patterns for the context
     - Ensure interface contracts are honored
     - Confirm dependency rules aren't violated
5. **COMMIT ATOMICALLY**:
   - Every completed task gets a commit. No exceptions.
   - Stage relevant changes: `git add -p` or `git add [files]`
   - Write semantic commit message: `git commit -m "type: concise description"`
   - Types: `feat|fix|docs|style|refactor|test|chore`
6. **Mark complete**: Update `[~]` to `[x]` when done

## THE CARMACK RULE

*"A task without a commit is a task not done."*

Every completed task must result in an atomic commit. This isn't optional - it's fundamental to maintaining a clean, traceable history. If you can't commit it, the task isn't actually complete.

## WORK LOG

For complex tasks or when discovering important context, add a work log entry directly under the task in TODO.md:

```markdown
- [~] Implement user authentication
  ```
  Work Log:
  - Found existing auth pattern in services/auth.ts
  - Need to follow JWT token approach from api/middleware
  - Database schema already has user table, just needs session table
  - Blocked by: need to clarify token expiry requirements
  ```
```

This work log serves as:
- Scratchpad for discoveries and context
- Record of decisions made
- Place to note blockers or questions
- Memory for if task is resumed later


## 🎯 SIMPLICITY VALIDATION CHECKLIST

Before implementing any solution, validate against these simplicity criteria:

### The Simplicity Test
- **Can I explain this solution in one sentence?** If not, it's too complex.
- **Would a junior developer understand this immediately?** If not, simplify.
- **Am I solving problems that don't exist yet?** YAGNI - You Aren't Gonna Need It.
- **Is this the "boring" solution?** Boring is reliable. Clever is suspicious.

### Code Simplicity Metrics
- **Line count**: Can this be done in fewer lines without sacrificing clarity?
- **Cyclomatic complexity**: Are there too many decision points?
- **Dependencies**: Am I adding complexity through external dependencies?
- **Abstraction layers**: Am I creating unnecessary indirection?

### The Simplicity Reflex
When you find yourself:
- Writing a factory for a single type → **Stop**, use direct instantiation
- Creating an interface with one implementation → **Stop**, wait for the second use case
- Building a generic solution for a specific problem → **Stop**, solve the specific problem
- Adding configuration for values that never change → **Stop**, use constants

## 🎯 MAINTAINABILITY GUIDELINES

Code is read 100x more than it's written. Optimize for the reader, not the writer.

### The Future Developer Test
Ask yourself: *"If I had to modify this code in 6 months, what would I curse myself for?"*

### Maintainability Principles
- **Explicit Intent**: Code should announce what it does, not make you deduce it
- **Local Reasoning**: Understanding a function shouldn't require understanding the entire system
- **Obvious Extension Points**: Where changes will happen should be clear
- **Consistent Patterns**: Do similar things in similar ways

### Naming for Maintainability
```
❌ processData()      → ✅ validateAndNormalizeUserInput()
❌ flag               → ✅ isEmailVerified
❌ helper()           → ✅ formatDateForDisplay()
❌ doStuff()          → ✅ syncInventoryWithWarehouse()
```

### Code Organization for Future Changes
- **Group by feature**, not by file type (components/UserProfile not components/buttons)
- **Colocate related code** (keep the test next to the implementation)
- **Make dependencies explicit** (imports at the top, clear interfaces)
- **Leave escape hatches** (extension points for likely changes)

## 🎯 FIX BROKEN WINDOWS PROTOCOL

*"One broken window, left unrepaired, leads to more broken windows."* - The Broken Windows Theory

### Automatic Quality Detection During Execution
While implementing any task, actively scan for and immediately fix:

### Code Smells to Fix On Sight
- **Dead Code**: Commented-out blocks, unreachable code, unused imports
- **Poor Naming**: Single letters (except loop counters), abbreviations, misleading names
- **Magic Numbers**: Hardcoded values that should be constants
- **Duplicate Code**: Copy-paste that should be extracted
- **Long Functions**: If it doesn't fit on a screen, break it up
- **Deep Nesting**: More than 3 levels? Time to refactor

### The Fix-It-Now Rule
```
if (you_see_it && you_can_fix_it_in_under_2_minutes) {
    fix_it_now();  // Don't defer, don't document, just fix
}
```

### Quality Erosion Indicators
Watch for these signs that windows are breaking:
- TODO comments older than the current sprint
- Inconsistent code style in the same file
- Test files with skipped/commented tests
- Error handling with empty catch blocks
- Console.logs in production code paths

### The Boy Scout Rule
*"Leave the code better than you found it"* - Even if you didn't break it

When working in a file:
1. Fix formatting inconsistencies
2. Update outdated comments
3. Rename unclear variables you encounter
4. Extract magic numbers to constants
5. Remove unnecessary complexity

## 🎯 EXPLICIT CODE GENERATION

*"Explicit is better than implicit."* - The Zen of Python

### Explicit Dependencies
```javascript
// ❌ Implicit - dependencies hidden
function processOrder() {
    const user = getCurrentUser();  // Where does this come from?
    const config = getConfig();     // Global? Singleton?
    // ...
}

// ✅ Explicit - dependencies clear
function processOrder(user: User, config: Config, orderData: OrderData) {
    // All dependencies visible in signature
}
```

### Clear Function Signatures
```typescript
// ❌ Implicit return and side effects
function updateUser(data) {
    db.save(data);  // Side effect not obvious
    cache.clear();  // Another hidden side effect
}

// ✅ Explicit signature and effects
async function updateUser(userId: string, updates: UserUpdate): Promise<User> {
    const user = await db.users.update(userId, updates);
    await cache.users.invalidate(userId);
    return user;
}
```

### Transparent Behavior Rules
- **No Magic**: If it's not in the function signature, it shouldn't affect behavior
- **Pure When Possible**: Functions should return the same output for the same input
- **Side Effects Explicit**: If a function modifies state, name it accordingly (updateX, deleteY, saveZ)
- **Dependencies Injected**: Pass dependencies as parameters, don't reach out to get them

### Explicit Patterns to Follow
1. **Dependency Injection over Service Locators**
2. **Parameters over Global State**
3. **Return Values over Mutations**
4. **Type Annotations over Type Inference** (when it aids clarity)
5. **Named Parameters over Positional** (for functions with >3 parameters)

### The Explicit Checklist
Before completing any function:
- [ ] Are all inputs visible in the signature?
- [ ] Is the return type clear and documented?
- [ ] Are side effects obvious from the function name?
- [ ] Could someone understand this without reading the implementation?

## 🎯 REAL-TIME BINDING VALIDATION

*"Architecture is about the important stuff. Whatever that is."* - Ralph Johnson

### File Type Detection & Binding Application
During code generation, automatically detect and apply relevant bindings:

### Technology-Specific Bindings
```yaml
TypeScript Files (.ts, .tsx):
  - Strong typing over any
  - Interfaces for data contracts
  - Strict null checks enabled
  - No implicit any returns

React Components (.jsx, .tsx):
  - Props validation with TypeScript/PropTypes
  - Hooks rules compliance
  - Component purity (no side effects in render)
  - Consistent state management patterns

Go Files (.go):
  - Error handling explicit (no ignored errors)
  - Context propagation in APIs
  - Interface segregation
  - Embedded struct composition

Database Schemas (.sql, migrations):
  - Foreign key constraints explicit
  - Indexes for queried columns
  - NOT NULL by default
  - Consistent naming conventions
```

### Architecture Binding Compliance
```
Component Isolation:
  - Single responsibility per module
  - Clear input/output boundaries
  - No circular dependencies
  - Testable in isolation

Interface Contracts:
  - Backward compatibility maintained
  - Version changes documented
  - Breaking changes avoided
  - Contract tests present

Dependency Rules:
  - Dependencies point inward (clean architecture)
  - Domain doesn't depend on infrastructure
  - UI doesn't directly access data layer
  - Dependency injection used
```

### Real-Time Validation Process
1. **Detect File Type** → Identify applicable technology bindings
2. **Load Binding Rules** → Apply relevant constraints for the context
3. **Generate Code** → Follow binding requirements during creation
4. **Validate Output** → Ensure generated code meets all bindings
5. **Fix Violations** → Immediately correct any binding violations

### Binding Validation Checklist
Before committing any code:
- [ ] Technology bindings applied for file type?
- [ ] Architecture patterns maintained?
- [ ] Interface contracts honored?
- [ ] Dependency rules followed?
- [ ] No binding violations introduced?

### Common Binding Violations to Catch
- **TypeScript**: Using `any` type without justification
- **React**: Direct DOM manipulation in components
- **Go**: Ignoring errors with `_`
- **SQL**: Missing indexes on foreign keys
- **API**: Breaking changes without version bump
- **Architecture**: Business logic in UI layer

## NOTES

- Always think through the approach before diving into implementation
- If task includes context or detailed steps, follow them
- If blocked, mark as `[!]` with explanation in work log and move to next task
- Only preserve work logs that contain valuable context for future reference
- **ALWAYS commit changes after task completion** - no exceptions
- **ALWAYS validate simplicity** - complexity is the enemy of reliability
