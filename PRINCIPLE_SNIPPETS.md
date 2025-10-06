# Leyline Principle Snippets for Natural Embedding

> Working reference for integrating principles into slash commands conversationally

## Core Tenets (Compact Forms)

### Simplicity
**One-liner**: "Prefer the simplest solution that solves the problem completely"

**Natural embedding**:
- "Boring beats clever. Obvious beats terse."
- "Complexity is like debt—it accrues interest. Each abstraction, component, or dependency can break and needs maintenance."
- "Choose the simplest design with the fewest moving parts. If you can't explain it in one sentence, simplify."
- "Question every piece of code not solving an immediate need. Do we have evidence we'll need this?"

**Warning signs**:
- "Premature abstraction before seeing patterns 3+ times"
- "Designing for imagined future requirements without concrete use cases"
- "Over-engineering—elaborate frameworks for simple problems"

### Modularity
**One-liner**: "Build independent, focused components with clear boundaries"

**Natural embedding**:
- "Each module should do one thing well—describable in one sentence without 'and'"
- "Define clear boundaries with well-defined interfaces hiding implementation details"
- "Minimize coupling through abstract interfaces, not concrete implementations"
- "Could someone use this correctly without understanding how it works internally?"

**Warning signs**:
- "God objects knowing too much about the system"
- "Tangled dependencies creating a complex web instead of clear hierarchy"
- "Changes frequently breaking seemingly unrelated parts"
- "Circular dependencies (A→B→C→A)"

### Explicitness
**One-liner**: "Make behavior obvious—explicit over implicit"

**Natural embedding**:
- "Dependencies visible in function signatures, not hidden globals"
- "Side effects obvious from naming (update, delete, save = verbs signaling mutation)"
- "No magic behavior triggered by naming conventions or reflection"
- "If you change implementation and calling code breaks, you have leakage"

**Warning signs**:
- "Hidden dependencies through global state or singletons"
- "Magic methods triggering based on conventions"
- "Undocumented assumptions about execution context"

### Maintainability
**One-liner**: "Write for yourself in 6 months, not for the compiler"

**Natural embedding**:
- "Code is read far more than written—prioritize clarity over cleverness"
- "Names should reveal purpose, not mechanism. 'calculateTotalWithTax' not 'processData'"
- "Document the 'why' behind decisions, not the 'what' (code shows what)"
- "Consistency reduces cognitive load—follow established patterns"

**Warning signs**:
- "Cryptic names (a, temp, data, thing, x)"
- "Clever code requiring mental gymnastics to understand"
- "Inconsistent patterns for similar operations"

### Testability
**One-liner**: "If testing is hard, the design has coupling problems"

**Natural embedding**:
- "Test pain is diagnostic—fix the design, not the test"
- "Components should be testable in isolation with clearly defined dependencies"
- "Separate business logic from infrastructure (databases, HTTP, file systems)"
- "Make dependencies explicit through injection—no hidden globals"
- "Heavy mocking signals excessive coupling"

**Warning signs**:
- "Tests requiring extensive setup or complex mocking"
- "Testing one component requires instantiating many others"
- "Tests break when refactoring unrelated code"

### Automation
**One-liner**: "Manual repetitive tasks are bugs in your process"

**Natural embedding**:
- "After performing a task manually twice, invest in automating it"
- "Automation is executable documentation forcing explicit process definition"
- "Machines handle reliable execution; humans handle creative problem-solving"
- "Quality gates should be automated—make the right way the easy way"

**Warning signs**:
- "Performing same task manually >2 times without automation"
- "Documentation with 'remember to...' for multi-step procedures"
- "'Works on my machine' problems from manual setup"

### Design Never Done
**One-liner**: "Design is continuous refinement, not one-time activity"

**Natural embedding**:
- "Codebases drift toward complexity—make simplification continuous practice"
- "After major phases, review module boundaries and refactor toward simpler design"
- "Regularly ask: 'How could this be simplified?'"
- "Invest 10-20% in design improvement, not just feature completion"

### Observability
**One-liner**: "Make system behavior visible, don't debug blind"

**Natural embedding**:
- "Add logging, metrics, tracing to understand actual behavior"
- "Instrument data flow, capture state at transitions"
- "Log inputs/outputs of failing functions with structured logging"
- "Can't fix what you can't see—visibility first, fixes second"

### Fix Broken Windows
**One-liner**: "Fix quality issues immediately (<2min fixes)"

**Natural embedding**:
- "See a problem, fix it now—don't defer quality issues"
- "Dead code, poor names, magic numbers—fix on sight"
- "Technical debt compounds like interest—pay it down continuously"
- "Leave code better than you found it (Boy Scout Rule)"

### Product Value First
**One-liner**: "Every technical decision must serve demonstrable user value"

**Natural embedding**:
- "Reject technically interesting solutions lacking clear user benefits"
- "Evaluate approaches based on user outcomes, not engineering preferences"
- "Ask: 'Does this solve real user problems or satisfy engineering curiosity?'"
- "Focus on what users need, not what's technically elegant"

## Ousterhout Principles (Compact Forms)

### Design Twice
"Explore 2-3 fundamentally different alternatives before committing. The best design emerges from comparison, not from your first idea."

### Deep Modules
"Great modules = simple interface hiding powerful implementation. Module Value = Functionality - Interface Complexity. If interface complexity ≈ implementation complexity, you have a shallow abstraction adding little value."

### Information Hiding
"Define clear boundaries—what callers need to know (interface) vs. what they shouldn't (implementation). If changing implementation breaks callers, details are leaking through your interface."

### Strategic Programming
"Invest 10-20% in design that reduces future complexity, not just feature completion. Tactical programming gets it working but accumulates debt. Strategic programming pays compound interest."

### Complexity Management
"Complexity = Dependencies + Obscurity. Dependencies are linkages between code pieces. Obscurity is non-obvious information. Both increase system complexity—minimize them aggressively."

## Ousterhout Red Flags (Compact Catalog)

### 1. Information Leakage
"Implementation details visible through interfaces. If changing internals breaks callers, you have leakage."
- Example: Returning raw DB rows exposes schema to callers
- Fix: Return domain objects hiding data structure

### 2. Temporal Decomposition
"Code organized by execution order (step1, step2), not functionality. Creates change amplification."
- Example: High-level functions that are just doStep1(); doStep2(); doStep3();
- Fix: Organize by module responsibility, not execution sequence

### 3. Over-exposure / Generic Names
"Manager, Util, Helper, Context without domain context. Suggest unfocused responsibility, become dumping grounds."
- Example: UserManager, DataUtil, HelperService
- Fix: Name based on domain purpose (UserAuthenticator, PriceCalculator)

### 4. Pass-through Methods
"Methods only calling another method with same signature. Each layer should transform, not just forward."
- Example: class A { foo() { return b.foo(); } }
- Fix: Each abstraction layer must change vocabulary and add value

### 5. Configuration Overload
"Dozens of parameters forcing users to understand implementation. Good modules hide internal knobs."
- Example: 15-parameter constructor requiring deep implementation knowledge
- Fix: Provide sensible defaults, hide complexity behind simple interface

### 6. Shallow Modules
"Interface complexity ≈ implementation complexity. Low value abstraction."
- Example: Wrapper class exposing most of wrapped object's methods
- Fix: Either simplify interface or merge with underlying module

## Binding Patterns (Technology-Agnostic)

### Domain Purity (Hexagonal Architecture)
"Keep business logic pure—no databases, HTTP, or file systems in domain code. Domain defines interfaces (ports); infrastructure implements them (adapters)."

### Avoid Premature Abstraction
"Wait until you see the same pattern 3+ times before abstracting. Each abstraction adds complexity—it must earn its place."

### Continuous Refactoring
"Simple refactorings compound into architectural improvements. Make simplification continuous, not event-driven."

### Immutability by Default
"Never modify data after creation—create new structures instead. Mutable state creates unpredictable changes hard to trace."

### Fail Fast
"Invalid states should be immediately visible through explicit validation. Don't let problems propagate silently."

## Context-Specific Integration Examples

### For Specification/Planning
"Design Twice—explore 2-3 fundamentally different approaches. Deep Module Thinking—specify interfaces first, hide complexity. Strategic Specification—invest in design reducing future complexity."

### For Implementation/Execution
"Simplicity: boring > clever. Maintainability: write for yourself in 6 months. Explicitness: dependencies visible in signatures. Fix Broken Windows: see problem <2min? Fix now."

### For Review/Quality
"Check for Ousterhout red flags: information leakage, temporal decomposition, shallow modules. Validate principle compliance: simplicity, explicitness, modularity, maintainability."

### For Debugging
"Observability first—don't debug blind. Explicitness—document actual vs expected behavior. Simplicity—choose simplest fix solving problem completely."

### For Architecture
"Modularity: independent components with clear boundaries. Domain Purity: business logic separate from infrastructure. Layered Architecture: each layer changes abstraction level."
