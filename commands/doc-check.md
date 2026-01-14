---
description: Audit and fix documentation across the codebase
---

# DOC-CHECK

> Documentation is design. Missing docs are missing understanding.

## Philosophy (Ousterhout)

**Good documentation reduces cognitive load.** You shouldn't need to read code to understand intent. Docs should make the system feel *smaller*, not bigger.

**Document the abstractions, not the implementation.** Interface docs explain *how to use*. Implementation docs explain *why this way*. Never restate what code already says.

**Deep modules need shallow docs.** A well-designed module hides complexity behind a simple interface. Its documentation should be equally simple: what it does, how to use it, done.

**Shallow modules need deep docs (or deletion).** If you need extensive documentation to explain a module, that's a design smell. Consider: is the abstraction wrong?

**Architecture docs are maps, not inventories.** They show how pieces fit together, where to start reading, which modules are deep vs shallow. They don't list every file.

## Mission

Audit the codebase for documentation that reduces cognitive load. Create what's missing. Update what's stale. Delete what misleads.

## Execution

Launch parallel Task agents to comb through the codebase. Each agent audits one aspect and makes fixes.

### Agent 1: High-Level Docs

```
Task general-purpose:
"Audit high-level project documentation. Apply Ousterhout's standard: docs should reduce cognitive load, not add to it.

## README.md

Check: Does it answer a new engineer's first questions?
- What is this? (one sentence)
- Why does it exist? (the problem it solves)
- How do I run it? (Quick Start that actually works TODAY)
- Where do I go next? (pointer to architecture or key modules)

If README is missing or placeholder: generate from package.json, code structure.
If Quick Start is stale: update with actual working commands.
If it's an inventory of features: rewrite as a map to understanding.

## ARCHITECTURE.md

This is the most important doc. Without it, every new reader must reverse-engineer the system.

Check: Does it make the system feel SMALLER?
- Shows the 3-5 major modules/domains (not every file)
- Explains what each owns and what it DOESN'T own
- Shows data flow: where does data enter? Where does it exit?
- Identifies the deep modules (simple interface, rich behavior)
- Warns about the shallow modules (complexity exposed, use carefully)
- Points to where to start reading code (the entry points)

If missing: CREATE it. Analyze the codebase structure:
- What are the main directories/packages?
- How do they depend on each other?
- What's the runtime flow? (request comes in, goes where, returns what)
- What are the key abstractions?

If exists but is an inventory: rewrite as a map.
If exists but is stale: update to match current structure.

## CLAUDE.md / AGENTS.md

Check: Does it tell an AI assistant how to be effective here?
- Key conventions (naming, patterns, anti-patterns)
- Commands/workflows that exist
- What to avoid
- Where to find things

If missing: generate from observed patterns.

## ADR Infrastructure

Check: Is there a place for architectural decisions?
- docs/adr/ or similar folder
- Template for new ADRs
- At least one ADR (even if it's 'why we chose X framework')

If missing: create folder + template.

Report what you created/updated and WHY it improves understanding."
```

### Agent 2: Module-Level Docs

```
Task general-purpose:
"Audit module-level documentation. Apply Ousterhout's deep module principle.

## Deep vs Shallow Module Detection

**Deep modules** (good): Simple interface, rich implementation.
- Few exports, lots of internal logic
- You can use it without understanding how it works
- Docs needed: just the interface (what it does, how to call it)

**Shallow modules** (smell): Complex interface, thin implementation.
- Many exports, little encapsulation
- You need to understand internals to use it
- Docs needed: more extensive, OR refactor the module

## Audit Process

Identify major directories (src/*, lib/*, packages/*, app/*, etc.)

For each module, assess depth:
- Count exports vs internal logic
- How many files must you read to understand it?
- Is there a clear boundary?

For deep modules without README:
- Create minimal README: what it does, main entry point, key exports
- Don't document internals (they're hidden for a reason)

For shallow modules without README:
- Create README explaining WHY it's complex
- Consider: flag for refactoring instead of documenting around the problem
- Document the essential complexity, not the accidental complexity

For complex modules (10+ files):
- Ensure there's a guide to navigating them
- Show the internal structure as a mini-architecture

Skip: node_modules, .git, build outputs, test fixtures

Report:
- Which modules got READMEs
- Which modules are concerning (shallow, need refactoring not docs)
- Which were already well-documented"
```

### Agent 3: Decision Records

```
Task general-purpose:
"Scan for undocumented architectural decisions. Ousterhout: 'The key design decisions are the ones that are non-obvious.'

## What Makes a Decision Worth Recording?

**Record if:**
- Future readers will ask 'why?' (non-obvious choice)
- Alternatives were seriously considered (tradeoffs exist)
- The decision constrains future options (architectural)
- Getting it wrong would be expensive to fix

**Don't record:**
- Obvious choices (using npm for a Node project)
- Easily reversible decisions
- Implementation details (not architectural)

## Audit Process

Scan git history (last 20 commits):
- Major refactors: what decision drove them?
- New dependencies: why this one, not alternatives?
- Pattern changes: what problem was being solved?

Scan codebase for non-obvious patterns:
- Custom abstractions: why not use a library?
- Unusual file structure: what's the organizing principle?
- Integration patterns: why this approach?

For each significant undocumented decision:
- Create ADR with: Context, Decision, Consequences
- Focus on the WHY, not the WHAT (code shows the what)
- Include what was NOT chosen and why

Focus areas:
- Database/storage choices
- Auth patterns
- API design (REST vs GraphQL, versioning)
- State management (why this approach?)
- Build/deploy configurations
- Major dependency choices

Report:
- ADRs created (with brief summary of each decision)
- Decisions flagged for user attention (need human context)"
```

### Agent 4: State & Flow Docs

```
Task general-purpose:
"Audit documentation for stateful components and complex flows. Ousterhout: 'Complexity is anything that makes software hard to understand or modify.'

## Why Diagrams Matter

State machines and data flows are where bugs hide. A diagram forces you to enumerate all states and transitions. Missing states become visible. Impossible transitions become obvious.

**Diagram if:**
- More than 3 states
- Non-linear transitions (can go backward, can skip)
- Error states that need handling
- Async operations with race conditions

**Don't diagram:**
- Simple boolean flags
- Linear progressions (step 1, 2, 3, done)
- Well-abstracted state (XState already IS the diagram)

## Audit Process

Look for undocumented complexity:

**State machines:**
- React useState/useReducer with multiple related states
- Redux slices with status enums
- XState machines (already good, but ensure they're findable)
- Hand-rolled state patterns (status: 'idle' | 'loading' | 'error')

**Data flows:**
- API request → transform → store → render chains
- Event propagation across components
- Background job lifecycles

For each undocumented stateful component:
- Generate Mermaid stateDiagram-v2
- Place NEAR the code (same file or adjacent .md)
- Include: all states, all transitions, error states

For complex data flows:
- Generate Mermaid sequenceDiagram or flowchart
- Show the happy path first
- Show error/edge paths
- Identify where state lives at each step

Focus areas (high bug potential):
- Auth flows (login, logout, refresh, expiry)
- Payment/transaction flows
- Form submission (validation, retry, success)
- Real-time/websocket (connect, disconnect, reconnect)

Report:
- Diagrams generated (with what complexity they document)
- Complex flows still undocumented (need more context)"
```

## Output

After all agents complete, summarize:

```markdown
## Doc-Check Complete

### Created
- README.md (generated project overview)
- docs/adr/template.md
- src/auth/README.md
- docs/auth-flow.md (state diagram)

### Updated
- README.md (added Quick Start section)
- CLAUDE.md (added missing conventions)

### Flagged (User Action Needed)
- ADR needed: Why we chose Convex over Prisma
- Complex flow: Payment webhook handling needs diagram

### Already Good
- ARCHITECTURE.md (current)
- src/api/README.md (complete)
```

If docs were created/updated, commit:
```bash
git add -A && git commit -m "docs: update project documentation"
```

## When to Run

- Before any thinktank invocation (ensures reviewers have context)
- After major features (capture new architecture)
- Periodically as maintenance

## Guiding Principle

**"Write the document that makes the codebase smaller."**

Every doc you create should reduce the number of things a reader needs to hold in their head. If a doc adds complexity, it's wrong.

- ARCHITECTURE.md should make the system feel like 5 pieces, not 500.
- Module READMEs should let you use the module without reading the code.
- ADRs should answer "why?" before anyone asks.
- State diagrams should make bugs visible before they're written.

Documentation gaps are context gaps. When thinktank reviews code without docs, it's reviewing in a vacuum. This command ensures every review has the context it needs—and that the context is actually helpful.
