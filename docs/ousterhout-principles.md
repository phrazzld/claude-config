# Ousterhout's Philosophy of Software Design

*Integration of John Ousterhout's "A Philosophy of Software Design" with Leyline development principles.*

---

## Core Thesis: Complexity is the Enemy

**Central Principle**: The greatest challenge in software engineering is managing complexity. Complexity is anything that makes software hard to understand or modify. It accumulates from thousands of small decisions.

**Relationship to Leyline Tenets**:
- Directly reinforces and extends the **Simplicity** tenet
- Provides specific vocabulary for identifying and fighting complexity

### Two Sources of Complexity

1. **Dependencies**: Linkages between components where changes to one require changes to another
2. **Obscurity**: When important information about system behavior is not obvious

**Application**: Every design decision should be evaluated by whether it increases or decreases these two factors.

---

## Deep vs Shallow Modules

### Deep Modules
**Definition**: Provide powerful functionality through a simple interface. The interface is significantly simpler than the implementation.

**Formula**: Module Value = Functionality - Interface Complexity

**Example**: Unix file I/O
- Interface: `open()`, `read()`, `write()`, `close()`, `lseek()`
- Implementation: Disk blocks, file systems, caching, permissions, device drivers
- Result: Enormous functionality, tiny interface = deep module

**Relationship to Leyline Tenets**:
- Extends **Modularity** tenet with depth measurement
- Provides concrete evaluation criteria: "Is this module deep or shallow?"

### Shallow Modules
**Definition**: Interface complexity nearly equals implementation complexity. Little value provided.

**Red Flag**: Wrapper classes that expose most of the wrapped object's methods

**Example**:
```python
# Shallow - adds boilerplate, hides nothing
class ItemCollection:
    def __init__(self):
        self._items = []
    def add(self, item): self._items.append(item)
    def get(self, index): return self._items[index]
    def count(self): return len(self._items)
```

**Application**: When creating abstractions, ask "What complexity am I actually hiding?"

---

## Information Hiding and Leakage

### Information Hiding
**Principle**: A module should hide implementation details. Users interact only through its defined interface.

**Relationship to Leyline Tenets**:
- Complements **Explicitness** tenet (hide implementation, expose intention)
- Extends **Modularity** with clear boundary definition

### Information Leakage
**Definition**: When a module's design choices "leak" out, forcing users to know internal implementation.

**Red Flag Example**: Data access layer returns raw database row objects
```python
# BAD: Database schema leaks through abstraction
def get_user(user_id):
    return db.execute("SELECT * FROM users WHERE id = ?", user_id).fetchone()
    # Returns: (1, 'user@email.com', 'John', 'Doe', '2025-01-01')
    # Callers must know database column order!

# GOOD: Implementation hidden behind domain object
def get_user(user_id):
    row = db.execute("SELECT * FROM users WHERE id = ?", user_id).fetchone()
    return User(id=row[0], email=row[1], first_name=row[2], last_name=row[3])
```

**Application**: In code review, ask "If I change this module's implementation, will calling code break?"

---

## Strategic vs Tactical Programming

### Tactical Programming
- **Focus**: Get something working as quickly as possible
- **Result**: Short-term speed, long-term slowdown
- **Warning**: "Tactical tornadoes" leave trails of complexity

### Strategic Programming
- **Focus**: Invest in system design while implementing features
- **Time Investment**: 10-20% of development time on design improvements
- **Result**: Small upfront cost, compounding long-term velocity gains

**Relationship to Leyline Tenets**:
- Extends **Maintainability** tenet with specific time allocation
- Reinforces **Design Never Done** philosophy with investment mindset

**Application**: When completing a task, ask "What small design improvement can I make while I'm here?"

---

## Different Layers, Different Abstractions

**Principle**: Each system layer should provide a simpler abstraction than the layer below it. Layers that merely wrap without changing abstraction are shallow and harmful.

**Red Flag**: Pass-through methods that add no semantic value
```python
# BAD: Business logic layer exposes data access details
class UserService:
    def execute_sql(self, query):
        return self.db.execute(query)

# GOOD: Business logic provides domain-level abstraction
class UserService:
    def register_user(self, email, password):
        # Hides SQL, transactions, validation, hashing
```

**Relationship to Leyline Tenets**:
- Extends **Modularity** with vertical structure guidance
- Complements **Explicitness** by clarifying appropriate abstraction levels

**Application**: When creating a new layer, ensure it changes the vocabulary and concepts from the layer below.

---

## Design Red Flags (Code Review Checklist)

### 1. Information Leakage
- Implementation details visible through interface
- Changes to implementation require changes outside module

### 2. Temporal Decomposition
- Code organized by execution order rather than functionality
- High-level functions that are just sequences of function calls

### 3. Over-exposure / Generic Names
- Classes named `Manager`, `Util`, `Helper`, `Context`
- Suggests unfocused responsibility, likely a dumping ground

### 4. Pass-through Methods
- Methods that only call another method with same signature
- Indicates shallow, leaky abstraction

### 5. Configuration Overload
- Dozens of configuration parameters exposed
- Forces users to understand implementation to configure properly
- Good modules have sensible defaults

### 6. Shallow Modules
- Interface complexity ≈ implementation complexity
- Wrapper classes that expose wrapped object's methods

**Application**: Use these red flags as code review criteria alongside existing Leyline tenet checks.

---

## Interface Design Principles

1. **Make it simple**: Interface significantly simpler than implementation
2. **Hide the details**: Don't expose implementation decisions
3. **Define 'what' not 'how'**: Interface describes what module does, not how
4. **Hard to misuse**: Guide developers toward correct usage
5. **Consistency**: Naming conventions, parameter ordering

**Relationship to Leyline Tenets**:
- Extends **Explicitness** with interface-specific guidance
- Reinforces **Maintainability** through misuse prevention

---

## Comments as Design Documentation

### Ousterhout's Controversial Stance
**Thesis**: "Good code doesn't need comments" is a fallacy. Code cannot fully capture designer's intent.

**What Comments Should Document**:
1. **Reasoning**: Why was this approach chosen?
2. **Invariants**: Assumptions that must hold (e.g., "list is always sorted")
3. **Units**: Time units, measurement units (e.g., `timeout_ms`)
4. **Contracts**: What function does, parameters, return values, exceptions
5. **Non-obvious decisions**: Anything surprising or counterintuitive

**What Comments Should NOT Document**:
- What the code does (code should be self-explanatory)
- Obvious information

**Relationship to Leyline Tenets**:
- Extends **Maintainability** with documentation strategy
- Complements **Explicitness** by capturing intent that code cannot express

**Application**: Before writing a comment, ask "Does this explain something code cannot?"

---

## Integration with Leyline Tenets

### Mapping Overview

| Ousterhout Concept | Primary Leyline Tenet | How It Extends |
|-------------------|----------------------|----------------|
| Complexity Management | Simplicity | Specific vocabulary: dependencies + obscurity |
| Deep Modules | Modularity | Depth metric: functionality - interface complexity |
| Information Hiding/Leakage | Explicitness + Modularity | Hide implementation, expose intention |
| Strategic Programming | Maintainability + Design Never Done | 10-20% design investment guideline |
| Abstraction Layers | Modularity | Each layer must change abstraction level |
| Interface Design | Explicitness + Modularity | Hard to misuse, simple to understand |
| Comments as Documentation | Maintainability + Explicitness | Capture intent code cannot express |
| Red Flags | All Tenets | Concrete violation indicators |

### New Concepts Introduced

1. **Module Depth as Design Metric**: Quantifiable way to evaluate module quality
2. **Tactical Debt Awareness**: Explicit recognition of strategic vs tactical tradeoffs
3. **Abstraction Layer Discipline**: Requirement that layers change conceptual level
4. **Information Leakage Detection**: Specific pattern for identifying abstraction failures
5. **10-20% Design Investment Rule**: Concrete time allocation for strategic work

---

## Practical Application in Commands

### /spec Command
- **Add**: Design twice consideration - explore multiple approaches before committing
- **Add**: Interface-first thinking - define simple interfaces before implementation
- **Check**: Are we creating deep or shallow modules?

### /plan Command
- **Add**: Strategic vs tactical tradeoff identification
- **Add**: Module depth evaluation during planning
- **Check**: Are we grouping by functionality or execution order? (avoid temporal decomposition)

### /execute Command
- **Add**: Complexity check - does this increase dependencies or obscurity?
- **Add**: Deep module validation - am I hiding significant complexity?
- **Check**: Red flags - generic names, pass-through methods, information leakage

### /git-code-review Command
- **Add**: Shallow module detection
- **Add**: Information leakage checking
- **Add**: Pass-through method identification
- **Add**: Configuration overload detection
- **Check**: Run through all six red flags

### /backlog-groom Command
- **Add**: Prioritize by complexity reduction impact
- **Add**: Identify tactical debt items for strategic paydown
- **Check**: Which items reduce dependencies? Which reduce obscurity?

---

## Key Takeaways for Daily Development

1. **Adopt Strategic Mindset**: Dedicate 10-20% of time to design improvement, not just feature completion

2. **Question Every Abstraction**: "Is this module deep or shallow? What complexity am I hiding?"

3. **Hunt Information Leaks**: "If I change this implementation, will calling code break?"

4. **Name Precisely**: Avoid `Manager`, `Util`, `Helper` - find names that describe specific responsibility

5. **Write Meaningful Comments**: Document reasoning, invariants, and intent - not what code does

6. **Refactor to Deepen**: When encountering shallow modules, pull complexity from callers to deepen them

7. **Different Layers, Different Abstractions**: Each layer must change vocabulary and concepts

8. **Recognize Tactical Debt**: Know when you're taking shortcuts vs investing in design

---

## Further Reading

- **Book**: "A Philosophy of Software Design" by John Ousterhout (2nd Edition)
- **Related**: David Parnas on information hiding (1972)
- **Related**: Fred Brooks on essential vs accidental complexity
- **Complement**: KISS, YAGNI, and Single Responsibility principles

---

*This document bridges Ousterhout's specific vocabulary and concepts with Leyline's existing tenet framework, providing actionable guidance for daily development work and code review.*
