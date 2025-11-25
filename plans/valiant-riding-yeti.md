# Plan: Creative Council Commands Suite

## Overview

Create 6 new commands following the "Creative Council" pattern established in `/aesthetic`:
- Masters-based philosophical lenses
- Elevation over correction
- "Default Territory → Intentional Territory" framing
- Soul/vibe assessment with metaphors
- Hero Experiment closing

---

## Command 1: `/performance` - The Performance Council

### The Council

**Core Lenses (Always Applied):**
1. **Brendan Gregg (The Investigator)** - Measure before optimizing. Flame graphs. Systems thinking.
2. **Rich Hickey (The Simplifier)** - Simple Made Easy. Complexity is the performance killer.
3. **Donald Knuth (The Scientist)** - Premature optimization is evil. Profile, don't guess.

**Contextual Masters:**
| Performance Domain | Masters to Invoke |
|-------------------|-------------------|
| Latency/Response | Casey Muratori (Handmade Hero), Jonathan Blow |
| Throughput/Scale | Werner Vogels (Amazon), Jeff Dean (Google) |
| Memory/Resources | Joe Armstrong (Erlang), memory-efficient algorithms |
| Startup/Bundle | Addy Osmani (web performance), Lighthouse philosophy |
| Database | Use The Index Luke, query optimization |

### Phases
1. **Understanding the Machine** - Profile, measure, establish baselines
2. **Summoning the Council** - Load relevant performance philosophy
3. **The Profiling Session** - Analyze with lenses (CPU, Memory, I/O, Network, Bundle)
4. **Perspectives** - Parallel agents: The Measurer, The Simplifier, The Systems Thinker
5. **The Vision** - Soul assessment ("Currently feels like a sloth, wants to feel like a cheetah")
6. **The Optimization Path** - 3 named approaches + Hero Experiment

### Default Territory → Intentional
- N+1 queries → Eager loading with purpose
- No caching → Strategic cache layers
- Blocking operations → Async with intention
- Bundle everything → Code splitting strategy

---

## Command 2: `/security` - The Security Council

### The Council

**Core Lenses (Always Applied):**
1. **Bruce Schneier (The Threat Modeler)** - Think like an attacker. What are we protecting?
2. **OWASP Philosophy (The Checklist)** - Known vulnerabilities, systematic defense
3. **Joe Armstrong (The Resilience Master)** - Let it crash safely. Fail secure.

**Contextual Masters:**
| Security Domain | Masters to Invoke |
|-----------------|-------------------|
| Authentication | OAuth/OIDC philosophy, Zero Trust |
| Data Protection | Encryption at rest/transit, key management |
| Input Validation | Never trust input, sanitize everything |
| Secrets | HashiCorp Vault philosophy, environment separation |
| Infrastructure | Principle of least privilege, defense in depth |

### Phases
1. **Understanding the Attack Surface** - Inventory entry points, data flows
2. **Summoning the Council** - Load security philosophy
3. **The Threat Modeling Session** - STRIDE or similar, with Council questions
4. **Perspectives** - Parallel agents: The Attacker, The Defender, The Auditor
5. **The Vision** - Soul assessment ("Currently feels like an unlocked house, wants to feel like a vault")
6. **The Hardening Path** - Prioritized security improvements + Hero Experiment

### Default Territory → Intentional
- Hardcoded secrets → Environment variables with rotation
- Trust all input → Validate at every boundary
- Implicit permissions → Explicit RBAC
- Hope-based security → Defense in depth

---

## Command 3: `/testing` - The Testing Council

### The Council

**Core Lenses (Always Applied):**
1. **Kent Beck (The Pragmatist)** - Test behavior, not implementation. Red-Green-Refactor.
2. **Martin Fowler (The Architect)** - Testing pyramid. Right tests at right levels.
3. **James Bach (The Explorer)** - Context matters. Exploratory testing. Question assumptions.

**Contextual Masters:**
| Testing Philosophy | Masters to Invoke |
|-------------------|-------------------|
| TDD Purist | Kent Beck, Uncle Bob (discipline) |
| Integration-First | DHH (Rails approach), real dependencies |
| Property-Based | QuickCheck philosophy, generative testing |
| BDD/Acceptance | Cucumber philosophy, user stories as tests |
| Chaos Engineering | Netflix (Chaos Monkey), resilience testing |

### Phases
1. **Understanding the Safety Net** - Current test inventory, coverage patterns
2. **Summoning the Council** - Load testing philosophy
3. **The Testing Session** - Analyze with lenses (Unit, Integration, E2E, Edge cases)
4. **Perspectives** - Parallel agents: The TDD Advocate, The Integration Champion, The Edge Case Hunter
5. **The Vision** - Soul assessment ("Currently feels like walking without a net, wants to feel like confident refactoring")
6. **The Coverage Path** - Testing strategy + Hero Experiment (one critical path to test)

### Default Territory → Intentional
- No tests → Strategic coverage starting with critical paths
- Testing implementation → Testing behavior
- Mocking everything → Real dependencies where valuable
- Random test placement → Pyramid-aware organization

---

## Command 4: `/simplify` - The Simplicity Council

### The Council

**Core Lenses (Always Applied):**
1. **John Ousterhout (The Complexity Hunter)** - Shallow modules are red flags. Information hiding.
2. **Martin Fowler (The Refactorer)** - Small steps. Named patterns. Code smells.
3. **Sandi Metz (The Rule Maker)** - Squint test. Small objects. Tell, don't ask.

**Contextual Masters:**
| Simplification Domain | Masters to Invoke |
|----------------------|-------------------|
| Module Design | Ousterhout (deep modules), Unix philosophy |
| Object Design | Sandi Metz (POODR), Alan Kay |
| Functional | Rich Hickey (values), immutability |
| Naming | Intent-revealing names, domain language |
| Dead Code | Marie Kondo approach (does it spark joy?) |

### Phases
1. **Understanding the Complexity** - Module inventory, dependency graph, complexity metrics
2. **Summoning the Council** - Load ousterhout-principles skill
3. **The Simplification Session** - Analyze with lenses (Depth, Coupling, Cohesion, Naming)
4. **Perspectives** - Parallel agents: The Depth Checker, The Coupling Analyzer, The Naming Critic
5. **The Vision** - Soul assessment ("Currently feels like a tangled mess, wants to feel like a well-organized toolbox")
6. **The Simplification Path** - Refactoring strategy + Hero Experiment

### Default Territory → Intentional
- Pass-through methods → Deep modules with real logic
- Manager/Helper/Util names → Intent-revealing names
- Scattered configuration → Centralized, typed config
- Implicit dependencies → Explicit interfaces

---

## Command 5: `/api-design` - The Interface Council

### The Council

**Core Lenses (Always Applied):**
1. **Roy Fielding (The Constraint Master)** - REST is constraints, not URLs. HATEOAS. Statelessness.
2. **Stripe API Philosophy (The Empathist)** - Developer experience. Consistency. Predictability.
3. **GraphQL Philosophy (The Negotiator)** - Ask for what you need. Schema as contract.

**Contextual Masters:**
| API Style | Masters to Invoke |
|-----------|-------------------|
| REST | Fielding, Richardson Maturity Model |
| GraphQL | Facebook philosophy, schema-first |
| RPC/gRPC | Google, Protocol Buffers, efficiency |
| Webhooks | Event-driven, idempotency |
| SDK/Client | Stripe, Twilio (great DX examples) |

### Phases
1. **Understanding the Interface** - Endpoint inventory, schema analysis
2. **Summoning the Council** - Load relevant API philosophy
3. **The Design Session** - Analyze with lenses (Consistency, Discoverability, Error Handling, Versioning)
4. **Perspectives** - Parallel agents: The Consumer, The Maintainer, The Evolver
5. **The Vision** - Soul assessment ("Currently feels like reading assembly, wants to feel like speaking a language")
6. **The Interface Path** - Design improvements + Hero Experiment

### Default Territory → Intentional
- Inconsistent naming → Predictable conventions
- Generic error messages → Actionable error responses
- No versioning → Intentional evolution strategy
- Hidden capabilities → Discoverable API (HATEOAS or docs)

---

## Implementation Order

Implementing 5 commands (excluding `/review` for now):

1. **`/performance`** - User mentioned, high standalone value
2. **`/simplify`** - Builds on existing ousterhout-principles skill
3. **`/testing`** - Complements quality-check command
4. **`/security`** - High risk domain, standalone value
5. **`/api-design`** - Specialized but valuable for API projects

---

## Common Structure (Template)

Each command follows this pattern:

```markdown
---
description: [Domain] through the lens of [masters] (elevate, not audit)
---

# THE [DOMAIN] COUNCIL

> **THE [DOMAIN] MANIFESTO**
> - "[Quote 1]" — *Master 1*
> - "[Quote 2]" — *Master 2*
> - "[Quote 3]" — *Master 3*

You are the **Visionary [Role]**...

## The Council (Your Lenses)

### Core Lenses (Always Applied)
[3 masters with questions they ask]

### Contextual Masters
[Table of domain → masters]

## Phase 1: Understanding the [Domain Noun]
[Technical discovery with domain-specific commands]

## Phase 2: Summoning the Council
[Load relevant skills]

## Phase 3: The [Domain] Session
[Analysis with Council questions, Default → Intentional tables]

## Phase 4: Perspectives
[Parallel agents with philosophical framing]

## Phase 5: The Vision
[Soul assessment with metaphors, Elevation Roadmap with 3 named paths]

## Phase 6: The Closing Encouragement
[Hero Experiment + inspiring close]

## Success Criteria
[Checklist]

## The Anti-Convergence Principle
[Domain-specific defaults to avoid]
```

---

## Files to Create

1. `/Users/phaedrus/.claude/commands/performance.md`
2. `/Users/phaedrus/.claude/commands/simplify.md`
3. `/Users/phaedrus/.claude/commands/testing.md`
4. `/Users/phaedrus/.claude/commands/security.md`
5. `/Users/phaedrus/.claude/commands/api-design.md`

---

## Success Criteria

For each command:
- [ ] Follows Creative Council template structure
- [ ] 3 core lenses + contextual masters table
- [ ] Domain-specific technical discovery phase
- [ ] "The Council asks:" guiding questions throughout
- [ ] Default Territory → Intentional Territory tables
- [ ] Soul Assessment with domain-appropriate metaphors
- [ ] 3 named elevation paths (1 anchor + 2 contextual)
- [ ] Hero Experiment specific to domain
- [ ] Anti-convergence principle for domain
- [ ] Parallel agents with philosophical personas
