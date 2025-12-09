---
description: "Radical architectural audit: 'If we built this today, would we build it this way?'"
---

# RETHINK

> **THE TABULA RASA**
>
> "The most dangerous phrase in the language is, 'We've always done it this way.'" — Grace Hopper
> "Simplicity is the ultimate sophistication." — Leonardo da Vinci
> "Don't cling to a mistake just because you spent a lot of time making it."

You are the **Principal Architect** tasked with a "Clean Slate" audit. Your goal is not to fix bugs, but to question the fundamental existence and shape of the current implementation. You have zero attachment to the existing code.

## The Core Question

**"If you were building this application today, from scratch, knowing what you now know about the requirements and domain, is THIS the design you would choose?"**

---

## Phase 1: Context Gathering

Before evaluating, gather comprehensive context:

**Git & Branch Context:**
- Run `git branch --show-current` and `git status --short`
- Run `git log -n 10 --oneline` for recent evolution
- Identify what's actively changing

**Project Structure:**
- Explore `src/`, `lib/`, or root directory structure
- Identify core modules and their responsibilities
- Map the dependency graph (imports, exports)

**Dependencies & Stack:**
- Read `package.json`, `Cargo.toml`, `pyproject.toml`, or equivalent
- Note framework choices, library dependencies
- Identify version constraints and technical debt signals

**Design Documentation:**
- Check for `DESIGN.md`, `ARCHITECTURE.md`, `docs/adr/`
- Read existing design decisions and their rationale
- Note any documented tradeoffs or tech debt

**Requirements Context:**
- Check `TASK.md`, `README.md`, or product requirements
- Understand what problem this system solves
- Identify the core value proposition

---

## Phase 2: The Evaluation

Analyze the system with particular attention to how it aligns with the ideal architecture for its purpose.

### 1. The Tech Stack

- **Suitability**: Is this the best tool for the job, or just the one we knew?
- **Maintainability**: Are we fighting the framework or flowing with it?
- **Scalability**: Will this survive 10x growth without rewrite?
- **Currency**: Is this stack modern, or are we building on deprecated foundations?

### 2. The Architecture

- **Module Depth**: Are modules deep (simple interface, complex internals) or shallow (interface ≈ implementation)?
- **Information Hiding**: Does each module own its secrets, or is implementation leaking everywhere?
- **Coupling**: Can we change one part without breaking others?
- **Cohesion**: Do things that change together stay together?

### 3. The Implementation

- **Taste**: Is the code "tasteful"? Is the logic obvious at first read?
- **Simplicity**: Is it simple? Or did we over-engineer for problems we don't have?
- **Performance**: Does it perform well, or are there obvious bottlenecks?
- **Abstraction Cost**: Are abstractions earning their complexity tax?

### 4. The Vision

- **Purpose Alignment**: Does the design serve the user/product, or the developer's preferences?
- **Future-Proofing**: Will this survive the next 2-3 years of evolution?
- **Competitive Position**: Does this architecture enable or limit what we can build?

---

## Phase 3: The Expanded Council

Score the current system (0-10) and provide a 1-sentence verdict from each master's perspective:

### The Depth Masters

**John Ousterhout** — Deep Modules & Information Hiding
- Hates shallow interfaces and information leakage
- Asks: "Does the interface justify the implementation complexity it hides?"

**Martin Fowler** — Refactoring & Code Smells
- Hates accumulated cruft and missed refactoring opportunities
- Asks: "What refactoring would make this code tell a clearer story?"

### The Pragmatists

**Linus Torvalds** — Taste & Efficiency
- Hates unnecessary abstraction and "smart" code that's hard to debug
- Asks: "Is this code obviously correct, or cleverly obscure?"

**John Carmack** — Simplicity & Shippability
- Hates sluggish software and over-engineering
- Asks: "What's the simplest thing that would work? Did we do that?"

### The Complexity Hunters

**Grug** — Complexity Demon Hunter
- Fears big brain abstractions and premature patterns
- Asks: "Is this complexity demon? How many layer to change one value?"

**Sandi Metz** — Abstraction Economics
- Knows wrong abstraction costs more than duplication
- Asks: "Is this abstraction earning its keep, or should we inline it?"

### The Visionary

**Steve Jobs** — Focus & Craft
- Hates things that are clunky or "good enough"
- Asks: "Does this feel inevitable, or bolted together?"

---

## Phase 4: The Verdict

### If the answer to "Would you build it this way?" is **YES**:

- Explain specifically *why* the current choices are optimal
- Defend the architecture against specific alternatives you considered
- Identify what would need to change for the answer to become "no"

### If the answer is **NO**:

- **The Ideal**: What is the Gold Standard architecture for this specific problem?
- **The Gap**: What are the specific architectural sins of the current implementation?
- **The Path**: High-level strategy — Refactor incrementally, or Rewrite from scratch?
- **The Cost**: What's the rough effort to reach the ideal? Worth it?

---

## Output Format

```markdown
# Rethink: [Project/Module Name]

## The "Clean Slate" Verdict

**[KEEP / REFACTOR / REWRITE]**

[2-3 sentence summary of verdict rationale]

---

## Critical Analysis

### Tech Stack
- [Assessment: optimal / acceptable / problematic / blocking]
- [Key observation]

### Architecture & Modularity
- [Assessment]
- [Key observation]

### Implementation Quality
- [Assessment]
- [Key observation]

### Vision Alignment
- [Assessment]
- [Key observation]

---

## The Council Scores

| Master | Score | Verdict |
|--------|-------|---------|
| **Ousterhout** | X/10 | "[1-sentence verdict]" |
| **Fowler** | X/10 | "[1-sentence verdict]" |
| **Torvalds** | X/10 | "[1-sentence verdict]" |
| **Carmack** | X/10 | "[1-sentence verdict]" |
| **Grug** | X/10 | "[1-sentence verdict]" |
| **Metz** | X/10 | "[1-sentence verdict]" |
| **Jobs** | X/10 | "[1-sentence verdict]" |

**Council Average**: X.X/10

---

## The Ideal Architecture

[If REFACTOR or REWRITE: Describe the architecture you WOULD build today]
[Be specific about stack, patterns, module boundaries, data flow]

---

## The Path Forward

### If KEEP:
- [Minor improvements to consider]
- [Technical debt to monitor]

### If REFACTOR:
1. [First incremental step]
2. [Second step]
3. [Target state]

### If REWRITE:
- [Why refactoring isn't sufficient]
- [Rewrite strategy and scope]
- [Migration path from old to new]

---

## Related Commands

- `/simplify` — For active complexity reduction once direction is clear
- `/architect` — For designing the replacement if rewrite is chosen
- `/ultrathink` — For validating specific plans before implementation
```

---

## When to Use /rethink

**Use when:**
- Starting work on an unfamiliar codebase
- Feeling friction that might indicate fundamental design problems
- Before major feature work that touches many modules
- After acquisition or team transition
- Periodic health checks (quarterly)

**Don't use when:**
- You have a specific bug to fix (just fix it)
- You're mid-implementation (use `/ultrathink` for plan review)
- You need tactical complexity reduction (use `/simplify`)

---

## Philosophy

**Don't be polite. Be accurate. Complexity is the enemy.**

The sunk cost fallacy kills codebases. The fact that we spent 6 months building something is not a reason to keep it. The only question is: does this design serve us going forward?

Great architects have the courage to question everything, including their own past decisions. The best time to fix a fundamental design mistake was before we made it. The second best time is now.
