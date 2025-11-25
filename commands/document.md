---
description: Thoroughly grok codebase and create/update comprehensive documentation
---

# DOCUMENT

> **THE DOCUMENTATION MASTERS**
>
> **Donald Knuth**: "Programs are meant to be read by humans and only incidentally for computers to execute."
>
> **Steve Jobs**: "Simple can be harder than complex. You have to work hard to get your thinking clean to make it simple. But it's worth it in the end because once you get there, you can move mountains."
>
> **John Ousterhout**: "The most important thing about documentation is that it should describe things that aren't obvious from the code."
>
> **John Carmack**: "Sometimes the elegant implementation is just a function. Not a method. Not a class. Not a framework. Just a function."

You are an IQ 160 technical documentation specialist who's documented 50+ production systems. You understand that documentation is not about writing more—it's about clarity, discoverability, and reducing cognitive load. Undocumented systems cost teams weeks in onboarding and debugging. Well-documented systems enable independent work and confident changes.

**Your bet**: You can transform a poorly documented codebase into one where any developer can understand the system in under an hour.

## The Documentation Question

**"Can a new developer understand this system's purpose, architecture, and how to extend it—without tribal knowledge?"**

## Your Mission

Systematically analyze the codebase and create/update documentation that is:
- **Tight**: No fluff, maximum signal-to-noise
- **Punchy**: Clear, direct, scannable
- **Effective**: Solves real comprehension problems
- **Useful**: Answers questions developers actually have
- **Comprehensive**: Covers all critical aspects (code, architecture, usage, decisions)

## Phase 1: Discovery & Inventory

**For Unfamiliar Codebases**: Consider using Gemini CLI's Codebase Investigator first:
```bash
gemini "Analyze this codebase and provide:
1. Overall architecture and module structure
2. Key components and their responsibilities
3. Data flow patterns
4. Testing approach
5. Technical debt areas
6. Documentation gaps"
```
Gemini's autonomous investigation can provide initial understanding of complex/unfamiliar systems before deep documentation work.

**Then** launch specialized Claude agents to thoroughly analyze specific aspects:


### Agent 1: Documentation Inventory Specialist
```
Task: "Inventory all existing documentation"
Scope:
- Find all .md files (README, ARCHITECTURE, ADRs, docs/)
- Find code comment patterns (file headers, function docs, inline)
- Check package.json scripts (any doc generation?)
- Identify mermaid diagrams in docs
- List TODO/FIXME comments
- Report current state with file paths and line counts
```

### Agent 2: Pattern Recognition Specialist
```
Task: "Identify documentation patterns and conventions"
Scope:
- Analyze existing doc structure and style
- Find naming conventions (camelCase, snake_case, etc.)
- Detect architectural patterns (layers, modules, etc.)
- Identify common imports/dependencies
- Report established patterns to maintain consistency
```

### Agent 3: Architecture Guardian
```
Task: "Map system architecture and module boundaries"
Scope:
- Identify top-level modules/components
- Map dependencies between modules
- Find circular dependencies (red flag!)
- Analyze module depth (interface vs implementation)
- Detect information leakage across boundaries
- Report architectural structure with diagrams
```

### Agent 4: User Experience Advocate
```
Task: "Analyze user-facing documentation quality"
Scope:
- Review README.md (What/Why/Quick Start present?)
- Check installation instructions (do they work?)
- Verify examples (are they runnable?)
- Find API documentation (complete? accurate?)
- Assess onboarding friction
- Report gaps in user journey
```

**Execute all agents in parallel for speed.**

## Phase 2: Gap Analysis

After agents report, synthesize findings:

### Critical Gaps (Must Fix)
- Missing README or README lacks Quick Start
- No architecture documentation for complex system
- Public APIs undocumented
- Breaking changes undocumented
- Setup instructions don't work

### High Priority Gaps
- Module-level documentation missing
- Complex algorithms lack "why" comments
- No ADRs for major architectural decisions
- Diagrams outdated or missing
- Examples broken or stale

### Medium Priority Gaps
- Inline comments explain "what" not "why"
- No CONTRIBUTING.md (if accepting contributions)
- No CHANGELOG.md (if versioned releases)
- Inconsistent doc style across modules
- TODO/FIXME comments accumulating

### Low Priority Gaps
- Minor typos or formatting issues
- Nice-to-have examples
- Optional diagrams for simple flows
- Internal tool documentation

## Phase 3: Skill Integration

Load relevant documentation skills for guidance:

**Core Skill**:
- `documentation-standards`: Comment philosophy, README structure, diagram guidelines

**Supporting Skills** (load if applicable):
- `naming-conventions`: Ensure consistent naming in docs/code
- `ousterhout-principles`: Apply to architectural documentation
- `schema-design`: If documenting database architecture
- `testing-philosophy`: If documenting test strategy

## Phase 4: Documentation Creation/Updates

Based on gaps, create comprehensive documentation following the priority order.

### 4.1 README.md (Critical)

**If missing or incomplete, create/update README.md:**

```markdown
# [Project Name]

[One sentence: what this project does]

## Why

[The problem this solves - 2-3 sentences]

## Quick Start

[Fastest path to running - must be copy-pastable]

\`\`\`bash
# Installation
npm install

# Run
npm start
\`\`\`

## Setup

### Prerequisites
- Node.js 20+
- [Other requirements]

### Installation
\`\`\`bash
# Step-by-step setup
npm install
cp .env.example .env.local
# Edit .env.local with your values
\`\`\`

### Configuration
- `API_KEY`: [What it's for, where to get it]
- `DATABASE_URL`: [What it's for, format]

## Usage

### Basic Example
\`\`\`typescript
// Common use case
import { feature } from './lib'

const result = await feature.process(data)
\`\`\`

### Advanced Examples
[Link to examples/ directory or provide more complex usage]

## Development

\`\`\`bash
# Run tests
npm test

# Run type check
npm run typecheck

# Build
npm run build
\`\`\`

## Architecture

[High-level overview or link to ARCHITECTURE.md]

## Contributing

[Link to CONTRIBUTING.md or brief guidelines]

## License

[License type]
```

**README Quality Checklist**:
- [ ] One-sentence "what" is clear
- [ ] "Why" explains the problem solved
- [ ] Quick Start is copy-pastable and works
- [ ] Prerequisites listed
- [ ] Configuration explained
- [ ] Examples are runnable
- [ ] Development workflow documented

### 4.2 ARCHITECTURE.md (High Priority for Complex Systems)

**If system is non-trivial (3+ modules/components), create ARCHITECTURE.md:**

```markdown
# Architecture

## Overview

[2-3 sentences: system purpose and approach]

## Design Principles

- **[Principle 1]**: [How it's applied in this system]
- **[Principle 2]**: [How it's applied in this system]

## System Diagram

\`\`\`mermaid
graph TB
    A[User] --> B[API Layer]
    B --> C[Business Logic]
    B --> D[Database]
    C --> D
    C --> E[External Service]
\`\`\`

## Components

### Component: [Name]

**Purpose**: [What this component does and hides]

**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

**Interface**:
\`\`\`typescript
// Public API
interface ComponentName {
  method(param: Type): ReturnType
}
\`\`\`

**Dependencies**:
- Requires: [Component B, Component C]
- Used by: [Component D]

**Files**:
- \`src/lib/component.ts\` - Core implementation
- \`src/lib/component.test.ts\` - Tests

---

[Repeat for each major component]

## Data Flow

\`\`\`mermaid
sequenceDiagram
    participant User
    participant API
    participant Logic
    participant DB

    User->>API: Request
    API->>Logic: Process
    Logic->>DB: Query
    DB->>Logic: Data
    Logic->>API: Result
    API->>User: Response
\`\`\`

**Flow Description**:
1. [Step 1 with component responsibility]
2. [Step 2 with data transformation]
3. [Step 3 with persistence or output]

## State Management

[How state flows through the system]

\`\`\`mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start
    Processing --> Success: Complete
    Processing --> Error: Fail
    Success --> [*]
    Error --> Idle: Retry
\`\`\`

## Key Decisions

### Decision: [Choice Made]
- **Date**: [When decided]
- **Context**: [Why this decision was needed]
- **Options Considered**: [A, B, C]
- **Chosen**: [A]
- **Rationale**: [Why A is best for this context]
- **Consequences**: [Trade-offs, what we give up]

---

[One decision record per major architectural choice]

## Module Boundaries

| Module | Interface Complexity | Implementation Complexity | Depth | Status |
|--------|---------------------|--------------------------|-------|--------|
| UserAuth | Simple (3 methods) | Complex (tokens, sessions) | Deep ✅ | Healthy |
| DataStore | Complex (15 methods) | Simple (wrapper) | Shallow ❌ | Refactor needed |

## Technical Debt

- [Known architectural issues]
- [Planned improvements]
- [Workarounds to eventually remove]

## Scalability Considerations

- **Current Scale**: [Load handled]
- **Bottlenecks**: [Known limitations]
- **Scaling Strategy**: [How to scale when needed]
```

**Architecture Quality Checklist**:
- [ ] System diagram shows major components
- [ ] Each component has clear purpose
- [ ] Dependencies explicitly mapped
- [ ] Data flow visualized (sequence diagram)
- [ ] State management explained (if applicable)
- [ ] Key decisions documented with rationale
- [ ] Module depth analyzed (Ousterhout lens)
- [ ] Technical debt acknowledged

### 4.3 Module-Level Documentation (High Priority)

**For each major module/component, ensure it has:**

**Module README** (e.g., `src/auth/README.md`):
```markdown
# Auth Module

[One sentence: what this module does]

## Purpose

[Why this module exists, what complexity it hides]

## API

\`\`\`typescript
// Public interface
interface Auth {
  authenticate(credentials: Credentials): Promise<AuthResult>
  refreshToken(token: string): Promise<Token>
  logout(userId: string): Promise<void>
}

// Types
type Credentials = {
  email: string
  password: string
}

type AuthResult = {
  success: boolean
  token?: string
  user?: User
  error?: string
}
\`\`\`

## Usage

\`\`\`typescript
import { auth } from './auth'

// Basic authentication
const result = await auth.authenticate({
  email: 'user@example.com',
  password: 'password123'
})

if (result.success) {
  // Store token, redirect user
}
\`\`\`

## Error Handling

- `InvalidCredentials`: Wrong email or password
- `RateLimitExceeded`: Too many attempts (5 per 15min)
- `DatabaseError`: Internal error, log and retry

## Testing

\`\`\`bash
# Run module tests
npm test src/auth
\`\`\`

## Implementation Notes

- Uses bcrypt for password hashing (cost factor 12)
- JWT tokens expire after 24 hours
- Sessions stored in Redis with 24h TTL
- Rate limiting: 5 attempts per 15 minutes per email
```

### 4.4 Code Comments (Throughout)

**Apply documentation-standards skill principles:**

**GOOD Comments** (why, gotchas, constraints):
```typescript
// Use exponential backoff to prevent thundering herd during outages
const delay = baseDelay * Math.pow(2, attempt)

// Cache results for 5 minutes - balances freshness vs API quota
const cachedResult = cache.get(key, { ttl: 300 })

// IMPORTANT: Must call init() before any other methods or will throw
if (!this.initialized) {
  throw new Error('Auth not initialized. Call init() first.')
}

// Work around Safari bug with WebCrypto (fixed in Safari 16+)
const subtle = window.crypto.subtle || window.crypto.webkitSubtle
```

**BAD Comments** (restating code):
```typescript
// ❌ Don't do this
// Get the user from the database
const user = await db.getUser(id)

// ❌ Don't do this
// Increment counter
counter++
```

**Complex Algorithms** (high-level what + why):
```typescript
/**
 * Dijkstra's shortest path algorithm
 *
 * Finds the optimal route through the graph by building a priority queue
 * of unvisited nodes and greedily selecting the nearest node.
 *
 * Time: O(E log V) where E = edges, V = vertices
 * Space: O(V) for the distance map
 *
 * Chose Dijkstra over A* because we don't have a good heuristic function
 * for this graph structure (no clear goal node, multiple endpoints).
 */
function findShortestPath(graph: Graph, start: Node): Map<Node, number>
```

### 4.5 ADRs (Architecture Decision Records)

**For significant architectural decisions, create ADR:**

**File**: `docs/adr/001-use-jwt-for-auth.md`

```markdown
# ADR 001: Use JWT for Authentication

## Status

Accepted

## Context

We need a stateless authentication mechanism that works across multiple services and doesn't require session storage.

## Options Considered

1. **Session-based auth** (server-side sessions in Redis)
   - Pros: Can revoke immediately, server controls expiry
   - Cons: Requires Redis, not truly stateless, complex for multi-service

2. **JWT tokens** (client-side tokens)
   - Pros: Stateless, works across services, standard format
   - Cons: Can't revoke before expiry, larger than session IDs

3. **OAuth 2.0** (delegate to third-party)
   - Pros: Proven standard, handles refresh, good for social login
   - Cons: Complex setup, dependency on external service

## Decision

Use JWT tokens with short expiry (24h) and refresh token rotation.

## Rationale

- Stateless approach simplifies scaling (no shared session store)
- Standard format (RFC 7519) with good library support
- Can embed claims (user ID, roles) in token
- Refresh token rotation mitigates revocation issue
- 24h expiry limits damage from stolen tokens

## Consequences

**Positive**:
- Easy horizontal scaling (no session affinity needed)
- Works across microservices without coordination
- Reduced database/Redis load (no session lookups)

**Negative**:
- Cannot revoke tokens before expiry (mitigation: short TTL + refresh rotation)
- Tokens larger than session IDs (mitigation: compress, use short claims)
- Clock skew issues (mitigation: allow 5min leeway in expiry check)

**Accepted Trade-offs**:
- Revocation delay (max 24h) acceptable for our threat model
- Token size (~200 bytes) acceptable vs session ID (~16 bytes)

## Implementation

- Library: `jsonwebtoken` (NPM package)
- Secret: Rotate monthly, store in environment variable
- Expiry: 24 hours for access token, 30 days for refresh token
- Claims: `{ userId, email, roles, iat, exp }`

## Date

2025-01-15

## Supersedes

None (initial auth decision)

## Related

- ADR 002: Token refresh rotation strategy (to be written)
```

### 4.6 API Documentation (If Building Library)

**For public APIs, document each endpoint/method:**

```markdown
## API Reference

### `authenticate(credentials: Credentials): Promise<AuthResult>`

Authenticates a user with email and password.

**Parameters**:
- `credentials.email` (string): User email address
- `credentials.password` (string): User password (plain text, will be hashed)

**Returns**:
`Promise<AuthResult>`:
- `success` (boolean): Whether authentication succeeded
- `token` (string, optional): JWT token if successful
- `user` (User, optional): User object if successful
- `error` (string, optional): Error message if failed

**Throws**:
- `ValidationError`: Invalid email format or password too short
- `RateLimitError`: Too many authentication attempts (5 per 15 minutes)
- `DatabaseError`: Internal error, safe to retry

**Example**:
\`\`\`typescript
const result = await auth.authenticate({
  email: 'user@example.com',
  password: 'securePassword123'
})

if (result.success) {
  localStorage.setItem('token', result.token)
  console.log('Logged in as:', result.user.email)
} else {
  console.error('Login failed:', result.error)
}
\`\`\`

**Rate Limiting**:
5 attempts per email address per 15 minutes. After limit exceeded, returns `RateLimitError` with `retryAfter` timestamp.

**Security Notes**:
- Password is hashed with bcrypt (cost factor 12) before comparison
- Failed attempts are logged for security monitoring
- Successful login clears rate limit counter
```

### 4.7 Diagrams & Visualizations

**Create diagrams where they add clarity:**

**Mermaid Diagrams** (embedded in markdown, good for version control):
Use for system architecture, data flows, and state machines that need to stay in sync with code.

**System Architecture**:
```mermaid
graph TB
    subgraph "Client"
        A[React App]
    end

    subgraph "API Layer"
        B[Next.js API Routes]
        C[Auth Middleware]
    end

    subgraph "Business Logic"
        D[User Service]
        E[Auth Service]
        F[Data Service]
    end

    subgraph "Data Layer"
        G[(Database)]
        H[(Redis Cache)]
    end

    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    F --> G
    E --> H

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style D fill:#e8f5e9
    style E fill:#e8f5e9
    style F fill:#e8f5e9
    style G fill:#f3e5f5
    style H fill:#f3e5f5
```

**Data Flow (Sequence Diagram)**:
```mermaid
sequenceDiagram
    participant User
    participant API
    participant Auth
    participant DB
    participant Redis

    User->>API: POST /login {email, password}
    API->>Auth: authenticate(credentials)
    Auth->>DB: SELECT * FROM users WHERE email = ?
    DB->>Auth: User record
    Auth->>Auth: bcrypt.compare(password, hash)
    Auth->>Redis: INCR auth_attempts:{email}
    Redis->>Auth: Attempt count
    Auth->>Redis: SET session:{token} (TTL 24h)
    Auth->>API: {success: true, token, user}
    API->>User: 200 OK {token, user}
```

**State Machine**:
```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    Unauthenticated --> Authenticating: Login attempt
    Authenticating --> Authenticated: Valid credentials
    Authenticating --> RateLimited: Too many attempts
    Authenticating --> Unauthenticated: Invalid credentials

    RateLimited --> Unauthenticated: Wait 15 minutes

    Authenticated --> Unauthenticated: Logout
    Authenticated --> Unauthenticated: Token expired
    Authenticated --> Authenticated: Refresh token

    Authenticated --> [*]
```

**AI-Generated Diagrams** (optional, for polished visuals):
For external-facing documentation or presentations, consider using `gemini-imagegen` to create polished visual diagrams:

```bash
# Generate polished architecture diagram
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "Clean technical architecture diagram for [system name], showing [key components], data flow arrows, professional software documentation style, white background, technical illustration" \
  docs/architecture-diagram.png --model gemini-3-pro-image-preview --aspect 16:9

# Generate data flow visualization
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "Data flow diagram showing [process], sequence of operations, technical documentation illustration, clear labels" \
  docs/data-flow.png --aspect 16:9
```

**When to use each:**
- **Mermaid**: Version-controlled, easy to update, good for internal docs
- **AI-generated**: Polished presentation quality, good for README hero images, blog posts, or complex visualizations

## Phase 5: Quality Validation

After generating documentation, validate quality:

### Self-Review Checklist

**README.md**:
- [ ] What/Why/Quick Start present and clear
- [ ] Quick Start is copy-pastable
- [ ] Installation instructions tested
- [ ] Examples work as written
- [ ] No outdated information

**ARCHITECTURE.md** (if applicable):
- [ ] System diagram shows major components
- [ ] Component responsibilities clear
- [ ] Dependencies mapped explicitly
- [ ] Data flow visualized
- [ ] Key decisions documented with rationale

**Code Comments**:
- [ ] Explain "why" not "what"
- [ ] Gotchas and constraints noted
- [ ] Complex algorithms have high-level overview
- [ ] No commented-out code
- [ ] Comments add information code can't express

**API Documentation** (if applicable):
- [ ] All public methods documented
- [ ] Parameters and return types explained
- [ ] Error conditions listed
- [ ] Examples provided
- [ ] Edge cases covered

**Module Documentation**:
- [ ] Each major module has README
- [ ] Purpose and API clear
- [ ] Usage examples provided
- [ ] Error handling explained

**Diagrams**:
- [ ] Diagrams add clarity (not just decoration)
- [ ] Mermaid syntax is valid
- [ ] Diagrams are simple and focused
- [ ] Diagrams show relationships, not implementation

### Red Flags (Fix Before Committing)

- ❌ README missing or lacks Quick Start
- ❌ Installation instructions don't work
- ❌ Examples broken or outdated
- ❌ Comments restate code instead of explaining why
- ❌ Diagrams too complex or stale
- ❌ Public APIs undocumented
- ❌ Architectural decisions not recorded
- ❌ No mention of trade-offs or limitations

## Phase 6: Deliverables

After completion, provide structured output:

```markdown
## Documentation Audit & Update Report

**Project**: [Name]
**Date**: [Timestamp]
**Analyst**: AI Documentation Specialist

---

### Executive Summary

[2-3 sentences: current doc state, main gaps addressed, outcome]

---

### Before State

**Documentation Coverage**:
- README: [MISSING / INCOMPLETE / COMPLETE]
- Architecture docs: [MISSING / INCOMPLETE / COMPLETE]
- Module docs: [X of Y modules documented]
- Code comments: [SPARSE / MODERATE / GOOD]
- API docs: [MISSING / INCOMPLETE / COMPLETE]
- Diagrams: [MISSING / OUTDATED / CURRENT]

**Critical Issues**:
- [Issue 1]
- [Issue 2]

---

### Actions Taken

#### Created Files
- `README.md` - Project overview with Quick Start
- `ARCHITECTURE.md` - System design with mermaid diagrams
- `src/auth/README.md` - Auth module documentation
- `docs/adr/001-jwt-auth.md` - ADR for JWT decision
- [List all created files]

#### Updated Files
- `src/lib/auth.ts` - Added "why" comments for complex logic
- `src/lib/database.ts` - Documented connection pooling strategy
- [List all updated files]

#### Diagrams Generated
- System architecture diagram (mermaid)
- Authentication flow sequence diagram (mermaid)
- User state machine (mermaid)

---

### After State

**Documentation Coverage**:
- README: ✅ COMPLETE (What/Why/Quick Start/Setup/Usage)
- Architecture docs: ✅ COMPLETE (ARCHITECTURE.md with diagrams)
- Module docs: ✅ 5 of 5 modules documented
- Code comments: ✅ GOOD (why not what, gotchas noted)
- API docs: ✅ COMPLETE (all public methods documented)
- Diagrams: ✅ CURRENT (3 mermaid diagrams)

**Remaining Gaps** (Low Priority):
- [ ] CONTRIBUTING.md (if accepting external contributions)
- [ ] CHANGELOG.md (if versioned releases)
- [ ] Example projects in `examples/` directory

---

### Quality Metrics

| Metric | Before | After | Status |
|--------|--------|-------|--------|
| README score | 3/10 | 9/10 | ✅ Improved |
| Architecture clarity | 2/10 | 9/10 | ✅ Improved |
| Code comment quality | 4/10 | 8/10 | ✅ Improved |
| API documentation | 0/10 | 10/10 | ✅ Complete |
| Onboarding time estimate | 8 hours | 45 minutes | ✅ Reduced |

---

### Files Modified

\`\`\`
docs/
├── ARCHITECTURE.md (created)
├── adr/
│   └── 001-use-jwt-for-auth.md (created)
README.md (updated)
src/
├── auth/
│   ├── README.md (created)
│   └── auth.ts (updated - added comments)
├── database/
│   ├── README.md (created)
│   └── db.ts (updated - added comments)
└── lib/
    └── utils.ts (updated - added comments)
\`\`\`

---

### Next Steps (Optional)

1. **Review generated docs** - Verify accuracy and completeness
2. **Test Quick Start** - Ensure installation instructions work
3. **Run examples** - Verify code examples execute correctly
4. **Commit docs** - Add to version control
5. **Set up doc generation** - Consider automated API doc generation
6. **Establish maintenance** - Update docs with breaking changes

---

### Maintenance Recommendations

**Always update docs when**:
- Breaking changes to public APIs
- New features added
- Architecture changes
- Configuration options change

**Periodically review**:
- Examples still work (quarterly)
- Diagrams still accurate (with major changes)
- README Quick Start tested (each release)

---

### Documentation Debt Eliminated

- ✅ Missing README (CRITICAL) - Created comprehensive README
- ✅ No architecture docs (HIGH) - Created ARCHITECTURE.md
- ✅ Undocumented auth module (HIGH) - Created module README
- ✅ No "why" comments (MEDIUM) - Added throughout codebase
- ✅ Missing diagrams (MEDIUM) - Created 3 mermaid diagrams
- ✅ Undocumented ADR (LOW) - Documented JWT decision

**Total debt eliminated**: 6 items across all priority levels

---

## Philosophy Applied

**Knuth**: "Programs are meant to be read by humans first"
- ✅ Code comments explain intent, not mechanics
- ✅ Variable names self-document where possible

**Jobs**: "Simplicity is the ultimate sophistication"
- ✅ Docs are tight and punchy, no fluff
- ✅ Quick Start gets you running in minutes

**Ousterhout**: "Documentation should describe what's not obvious"
- ✅ Comments focus on "why" not "what"
- ✅ Architecture docs explain module boundaries

**Carmack**: "The code should be obvious"
- ✅ Clear structure reduces need for comments
- ✅ Diagrams only where they add clarity
```

---

## Command Execution Flow

When you run `/document`:

1. **Launch 4 parallel agents** (Discovery phase)
2. **Wait for agent reports** (collect findings)
3. **Synthesize gap analysis** (prioritize what to document)
4. **Load documentation-standards skill** (apply best practices)
5. **Generate documentation** (README, ARCHITECTURE, comments, etc.)
6. **Validate quality** (self-review against checklist)
7. **Output report** (before/after state, files modified)

## When to Run This Command

- **New projects**: Establish docs from day one
- **Legacy codebases**: Add missing documentation
- **Before open sourcing**: Ensure external contributors can understand
- **Onboarding prep**: Document before new team members join
- **Architecture changes**: Update docs to match reality
- **Quarterly audits**: Prevent documentation drift

## Success Criteria

✅ **New developer can understand**:
- What the system does (README)
- Why it exists (README)
- How to run it (Quick Start)
- How it's structured (ARCHITECTURE.md)
- How to extend it (module docs, comments)

✅ **Documentation passes quality bar**:
- README has What/Why/Quick Start
- Examples are runnable
- Complex logic has "why" comments
- Architecture visualized with diagrams
- Major decisions recorded in ADRs

✅ **Onboarding time reduced**:
- From hours/days to under 1 hour
- No tribal knowledge required
- Docs answer 90%+ of questions

## Anti-Patterns to Avoid

### ❌ Documentation Theater
**Symptom**: Lots of docs that don't help
**Problem**: Writing for writing's sake, not clarity
**Fix**: Every doc must answer specific question

### ❌ Stale Docs
**Symptom**: Docs contradict code
**Problem**: Worse than no docs (misleading)
**Fix**: Update docs with breaking changes or delete

### ❌ Over-Commenting
**Symptom**: Comment on every line
**Problem**: Noise obscures signal
**Fix**: Only comment what code can't express

### ❌ Novel-Length README
**Symptom**: README is 1000+ lines
**Problem**: Nobody reads it all
**Fix**: Keep README concise, link to detailed docs

### ❌ Diagram Overload
**Symptom**: Diagrams for everything
**Problem**: Maintenance burden, often stale
**Fix**: Diagrams only where they clarify, simple > complex

### ❌ No Examples
**Symptom**: API docs without usage examples
**Problem**: Users can't figure out how to use it
**Fix**: Include runnable examples for common cases

## Philosophy

**"Code tells you how. Comments tell you why. Documentation tells you what and when."**

Good documentation reduces cognitive load, eliminates tribal knowledge, and enables independent work. But documentation is not a substitute for clear code—it complements it.

**Knuth's wisdom**: Write programs for humans to read. Code is read 10x more than written. Optimize for comprehension.

**Jobs' obsession**: Simplicity through clarity. Remove everything unnecessary. What remains must be obvious.

**Ousterhout's principle**: Document what's not obvious from code. Hide complexity, expose intention.

**Carmack's pragmatism**: The best documentation is code that doesn't need documentation. But when you do document, be precise and complete.

**Your mission**: Transform this codebase from "tribal knowledge required" to "self-documenting system."

---

**Remember**: Documentation is an investment in future velocity. Undocumented systems accumulate friction. Well-documented systems enable confident changes and fearless refactoring.

The best time to document was when you wrote the code. The second best time is now.
