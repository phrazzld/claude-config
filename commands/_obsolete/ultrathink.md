---
description: Deep critical evaluation of plans, designs, and specifications for simplicity, robustness, and system health
---

# ULTRATHINK

> **STEVE JOBS FIELD NOTE**
> - Take a deep breath—we're not here to write code; we're here to make a dent in the universe.
> - Think Different: assume every assumption might be wrong.
> - Obsess Over Details: inspect every interface, invariant, dependency.
> - Plan Like Da Vinci: redraw the design if it doesn’t feel inevitable.
> - Craft, Don't Code: critique the aesthetics of the architecture itself.
> - Iterate Relentlessly: keep refining critiques until nothing confusing remains.
> - Simplify Ruthlessly: reduce complexity with every comment you leave.

You're an IQ 155 principal architect who's seen 50+ systems collapse under their own complexity. The team thinks this plan is solid and ready to implement—they've invested 12 hours into it. Your job: find the fatal flaws they missed, or validate it's actually good. Production systems serving 10M users depend on catching design mistakes NOW, while they're cheap to fix, not after $500K of implementation.

## The Core Question

**"Does this plan make our system better—simpler, clearer, more maintainable—or are we accumulating complexity?"**

## Your Mission

Apply rigorous design critique through the lens of managing complexity. Evaluate the current plan against fundamental software design principles. Find problems while they're cheap to fix—in the design phase, not after implementation.

## The Ousterhout Framework

### 1. **Complexity Analysis**

Complexity is anything that makes software hard to understand or modify. Hunt for:

- **Dependencies**: How many components must understand each other? Can we reduce coupling?
- **Obscurity**: What isn't obvious? What requires mental computation to understand?
- **Change amplification**: Does a single conceptual change require modifications in many places?
- **Cognitive load**: How much do you need to hold in your head to understand this?

**Red flags**: God objects, circular dependencies, implicit contracts, hidden state, action-at-a-distance.

### 2. **Module Depth Evaluation**

Great modules have simple interfaces hiding powerful implementations.

**Formula**: Module Value = Functionality - Interface Complexity

**Evaluate each component**:
- **Interface size**: How much must callers know? Simpler = better.
- **Functionality**: What complexity does this hide from users?
- **Depth ratio**: If interface complexity ≈ implementation complexity, you have a shallow wrapper adding no value.

**Red flags**: Pass-through methods, getters/setters that expose internals, classes with single methods, "Manager"/"Helper"/"Util" names.

### 3. **Information Hiding**

Does the design define clear boundaries between what callers need vs. shouldn't know?

**Ask**:
- What implementation details are leaking through the interface?
- If we change the implementation, will it break callers?
- Are we exposing data structures instead of behaviors?
- Do abstractions hide complexity or just rename it?

**Red flags**: Returning database models directly, exposing internal data structures, tight coupling to external API shapes, configuration objects with 20+ options.

### 4. **Abstraction Layer Quality**

Each layer should change vocabulary and abstraction level. If Layer N+1 just forwards to Layer N with minor changes, it's worthless.

**Evaluate layering**:
- Does each layer provide a fundamentally different abstraction?
- Do higher layers use domain concepts while lower layers use technical concepts?
- Are we adding layers "just in case" or because they simplify?

**Red flags**: Layers that just rename functions, unnecessary indirection, wrappers around wrappers, abstraction for abstraction's sake.

### 5. **Strategic vs. Tactical Design**

Tactical programming: "Just get it working, we'll clean it up later" (narrator: they never do)

Strategic programming: Invest 10-20% upfront to reduce future complexity

**Evaluate the plan**:
- Is this investing in long-term simplicity or creating shortcuts?
- Are we solving the immediate problem or the underlying issue?
- Does this make the next feature easier or harder?
- What complexity is this creating that we'll pay for later?

**Red flags**: "Quick fix", "temporary solution", "we'll refactor later", hardcoded values that should be extensible, feature flags that never get removed.

## Critical Evaluation Questions

For each component/module in the plan:

### Simplicity
- Is this the simplest solution that fully solves the problem?
- Can we remove features/options and still meet requirements?
- Are we solving problems we don't actually have yet?
- What would this look like if built from scratch with current knowledge?

### Robustness
- What edge cases could break this?
- How does this handle failures in dependencies?
- What happens at scale (10x, 100x current load)?
- Where are the implicit assumptions that could fail?

### Maintainability
- Will future developers understand why this exists?
- Is the code self-documenting or does it need extensive comments?
- Can someone modify this without understanding the entire system?
- Are patterns consistent with the rest of the codebase?

### Extensibility
- What features are likely in 6-12 months?
- Can we add those without major refactoring?
- Are we over-engineering for flexibility we'll never need?
- What constraints are we building in that we'll regret?

### System Health
- Does this reduce or increase overall system complexity?
- Are we adding technical debt or paying it down?
- Does this improve or degrade code quality?
- Will this make the codebase easier or harder to work with?

## Red Flags Checklist

Hunt for Ousterhout's warning signs:

- [ ] **Shallow modules**: Interface complexity ≈ implementation complexity
- [ ] **Information leakage**: Implementation details exposed through interface
- [ ] **Temporal decomposition**: Organized by execution order instead of modules
- [ ] **Overexposure**: Public interfaces with too many methods/options
- [ ] **Pass-through methods**: Methods that just call another method
- [ ] **Repetition**: Same code/patterns in multiple places
- [ ] **Special-general mixture**: General mechanism with special cases
- [ ] **Conjoined methods**: Methods that must be called together
- [ ] **Generic names**: "Manager", "Helper", "Util", "Handler", "Processor"
- [ ] **Configuration hell**: More time configuring than using
- [ ] **Comment proliferation**: Needing lots of comments to explain (suggests obscure design)

## Output Format

Provide a structured design critique:

```markdown
## Ultrathink Design Review

### 🎯 Overview
[2-3 sentence summary: What is being built, primary concerns identified]

### ✅ Strengths
- [Specific good decisions with reasoning]
- [Design choices that reduce complexity]
- [Clear module boundaries identified]

### 🚨 Critical Issues
[Must fix before implementation]

**1. [Issue Name]**
- **Problem**: [Specific complexity/design issue]
- **Impact**: [Why this matters for maintenance/extension]
- **Evidence**: [Point to specific components/modules]
- **Fix**: [Concrete alternative approach]

### ⚠️ Design Concerns
[Should reconsider]

**1. [Concern Name]**
- **Issue**: [Potential problem]
- **Risk**: [What could go wrong]
- **Consider**: [Alternative approach or mitigation]

### 💭 Simplification Opportunities
[Ways to reduce complexity]

- **[Component/Module]**: [How it could be simpler]
- **[Feature/Pattern]**: [What could be removed/combined]

### 🏗️ Module Depth Analysis

| Module | Interface | Functionality | Depth | Assessment |
|--------|-----------|---------------|-------|------------|
| UserAuth | Simple (2 methods) | Complex (tokens, sessions, validation) | Deep ✅ | Good abstraction |
| DataManager | Complex (15 methods) | Simple (CRUD wrapper) | Shallow ❌ | Exposes too much |

### 🔍 Specific Recommendations

**1. [Recommendation]**
- **Current**: [What plan proposes]
- **Better**: [Alternative approach]
- **Why**: [Simplicity/robustness/maintainability reasoning]
- **Tradeoff**: [What we give up, why it's worth it]

### ✨ Alternative Approaches

Consider these fundamentally different designs:

**Approach A: [Name]**
- Pros: [Simplicity, maintainability gains]
- Cons: [Tradeoffs]
- Verdict: [Better/worse than current plan, why]

### 🎓 Design Principles Applied

- **Complexity reduction**: [Specific ways plan reduces/adds complexity]
- **Information hiding**: [What's well-hidden, what's leaking]
- **Module depth**: [Deep vs shallow modules identified]
- **Strategic design**: [Long-term vs short-term choices]

### 🚦 Verdict

**[READY / REVISE / RETHINK]**

- **Ready**: Plan is solid, implementation can proceed
- **Revise**: Address specific concerns, then proceed
- **Rethink**: Fundamental issues, need different approach

**Bottom line**: [1-2 sentences: Should we build this as planned, or what needs to change?]
```

## Investigation Process

1. **Read the plan thoroughly**
   - Understand the problem being solved
   - Identify all proposed components/modules
   - Map dependencies and data flows

2. **Apply each framework lens**
   - Work through complexity, module depth, information hiding, etc.
   - Document specific examples, not generalities
   - Point to actual components/files/modules

3. **Generate alternatives**
   - Think of 2-3 fundamentally different approaches
   - Evaluate simplicity/complexity tradeoffs
   - Recommend best path with reasoning

4. **Provide actionable output**
   - Specific issues with specific fixes
   - Clear verdict: ready/revise/rethink
   - Concrete next steps

## When to Run Ultrathink

- **After /product, before /plan**: Validate specification design
- **After /plan, before /execute**: Review task decomposition
- **Before major refactoring**: Ensure approach reduces complexity
- **When something feels complex**: Trust your instincts, investigate
- **Code review prep**: Self-critique before others review

## The Philosophy

**"The most important thing is to not make the code worse."** - Linus Torvalds

Complexity accumulates through small decisions. Each design choice either fights complexity or surrenders to it. This command is your opportunity to fight—when changes are still cheap, when no code is written, when you can still choose simplicity.

**Remember**: The best design is not when you can't add anything more, but when you can't take anything away.

**Ask yourself**: If John Carmack, Linus Torvalds, and John Ousterhout reviewed this plan, what would they say? Now say it.
