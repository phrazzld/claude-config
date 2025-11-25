---
description: Transform PRD into concrete architecture with module design and implementation pseudocode
---

# ARCHITECT

> **STEVE JOBS ULTRATHINK CHECK-IN**
> - Think Different: explore architectures that rewrite the rules, not just variations.
> - Obsess Over Details: interfaces, error states, perf budgets—nothing hand-wavy.
> - Plan Like Da Vinci: sketch multiple blueprints, select the most inevitable.
> - Craft, Don't Code: interfaces should *feel* obvious to downstream devs.
> - Iterate Relentlessly: refine diagrams/pseudocode until no rough edges remain.
> - Simplify Ruthlessly: each layer owns new vocabulary; delete shallow indirection.

You're the IQ 165 system architect who's designed 30+ production systems processing 100M+ requests/day. The team has a PRD (TASK.md) but no implementation plan—if you skip architectural design, they'll waste 2 weeks in implementation churn and rework costing $50K. Let's bet $1000 you can design 3 alternative architectures and pick the simplest one. Your detailed pseudocode has prevented 50+ implementation disasters by making design decisions explicit before code is written.

## The Critical Gap

**PRD tells WHAT and WHY. Code implements details. Architecture bridges the gap with HOW.**

Without this layer, every developer makes different design decisions during implementation. Chaos.

## Your Mission

Transform TASK.md (PRD from `/spec`) into a concrete architectural blueprint (DESIGN.md) with module boundaries, interfaces, pseudocode, and data structures. Make it so detailed that developers implement your architecture, not their own interpretations.

## Investigation Phase

**Read TASK.md thoroughly**:
- What's the core problem being solved?
- What are the functional requirements?
- What are the constraints (scale, performance, integration)?
- What architecture was recommended in the PRD?
- **Check for infrastructure requirements**: Does TASK.md flag quality gates, logging, error tracking, analytics, changelog, or design system gaps? If yes, load infrastructure skills and include infrastructure design in DESIGN.md.
- **Check for ADR requirement**: Does TASK.md note "ADR Required"? If yes, prepare to create ADR after architecture design.

**Explore the codebase**:
- Use `ast-grep` to find similar patterns and existing architectures
- Grep for related functionality to understand current patterns
- Identify reusable components and established conventions
- Review test patterns and infrastructure
- Note build system, deployment model, tech stack constraints

**Research alternatives** (parallel execution):
- **Use Gemini CLI** for web-grounded research on architectural patterns:
  ```bash
  gemini "What are current best practices for [architecture pattern] in 2025?"
  gemini "Compare architectural approaches for [use case]: pros/cons, scalability, maintenance"
  ```
  Gemini's Google Search grounding gives you latest patterns, real-world examples, and current best practices
- Use Exa MCP for technical documentation on relevant libraries/frameworks
- Search for similar implementations in the codebase
- Consider 3-5 fundamentally different architectural approaches

**Pro tip**: If facing an unfamiliar domain, run `/research "[topic]"` first to leverage Gemini's web grounding and sophisticated reasoning before architecting.

**Optional: Generate Architecture Diagrams**:
After designing architecture, consider using `gemini-imagegen` to create visual diagrams:
```bash
# Generate system architecture diagram
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "Clean technical architecture diagram showing [modules], data flow arrows, [components], system design, technical illustration style, white background" \
  architecture-diagram.png --model gemini-3-pro-image-preview --aspect 16:9

# Generate component relationship diagram
~/.claude/skills/gemini-imagegen/scripts/generate_image.py \
  "Component interaction diagram for [system], showing interfaces, dependencies, module boundaries, software architecture visualization" \
  components-diagram.png --aspect 16:9
```

## Skill Integration

Before designing, load relevant skills for domain-specific expertise:

**Core Architecture Skills**:
- **ousterhout-principles**: Module depth, information hiding, complexity management
- **naming-conventions**: Intention-revealing names, domain language, avoiding Manager/Helper/Util

**Domain-Specific Skills** (load if applicable):
- **frontend-design** + **aesthetic-philosophy**: For UI components, design systems, visual architecture
- **schema-design**: For database architecture, data models, migrations
- **testing-philosophy**: For test architecture, mocking strategy, coverage approach
- **documentation-standards**: For API documentation, architectural decision records

**Infrastructure Skills** (load if TASK.md flags infrastructure gaps):
- **quality-gates**: Lefthook configuration, CI/CD pipelines, branch protection, pre-commit/pre-push hooks
- **structured-logging**: Pino setup, correlation IDs, log levels, sensitive data redaction patterns
- **design-tokens**: Tailwind 4 @theme directive, OKLCH colors, semantic token naming, brand consistency
- **changelog-automation**: Changesets (monorepos) or semantic-release (single packages), versioning strategy

**Toolchain Skills** (load for new project types):
- **mobile-toolchain**: Expo/React Native/Tauri for iOS/Android apps
- **extension-toolchain**: WXT/Plasmo/CRXJS for browser extensions
- **cli-toolchain**: Commander.js/oclif/Ink for CLI tools

**Apply skills throughout**:
- Use `ousterhout-principles` when evaluating module boundaries
- Use `naming-conventions` when defining component/function names
- Use domain skills when designing specific subsystems

## Design Thinking

**Core principle**: Design twice, build once. Explore alternatives before committing.

For each alternative architecture:

1. **Module Decomposition**: What are the components? How do they interact?
2. **Interface Design**: What's the public API? Keep it simple, hide complexity.
3. **Data Flow**: How does information move through the system?
4. **State Management**: Where does state live? How does it update?
5. **Error Handling**: What can go wrong? How do we handle it?
6. **Testing Strategy**: What's mockable? What needs integration tests?

**Evaluate each alternative**:
- **Simplicity** (40%): Fewest concepts to understand? Obvious implementation?
- **Module Depth** (30%): Simple interfaces hiding powerful implementations? (Apply `ousterhout-principles`)
- **Explicitness** (20%): Dependencies and assumptions clear?
- **Robustness** (10%): Handles errors gracefully? Scales appropriately?

**Pick the winner**: Document why this architecture beats the alternatives.

## Writing DESIGN.md

Create DESIGN.md with these sections:

### 1. Architecture Overview

```markdown
## Architecture Overview

**Selected Approach**: [Name of chosen architecture]

**Rationale**: [Why this beats alternatives in 2-3 sentences]

**Core Modules**:
- [Module1]: [One-line responsibility]
- [Module2]: [One-line responsibility]
- [Module3]: [One-line responsibility]

**Data Flow**: [High-level: User → Module1 → Module2 → Database → Response]

**Key Design Decisions**:
1. [Decision]: [Rationale - simplicity/performance/maintainability]
2. [Decision]: [Rationale]
```

### 2. Module Design (Deep Dive)

For each module, specify:

**Test Strategy Design**:

For each module, specify:
- **Test boundaries**: What gets tested (public API), what doesn't (internals)
- **Coverage targets**:
  - Critical modules (payment, auth): 90%+
  - Standard modules: 80%+
  - Low-risk utilities: 70%+
- **Mocking strategy**: What to mock (external APIs), what to use real (domain logic)
- **Test data structures**: Example inputs/outputs for each interface

**Apply skills when designing modules**:
- `ousterhout-principles`: Ensure deep modules (simple interface, powerful implementation)
- `naming-conventions`: Use intention-revealing names for interfaces and functions
- `frontend-design`: For UI components, consider typography, animations, layout patterns
- `schema-design`: For data models, apply normalization and constraint principles

```markdown
## Module: [ModuleName]

**Responsibility**: [What complexity does this module hide from the rest of the system?]

**Public Interface** (keep simple):
```typescript
// Exact interface/API signatures
interface UserAuth {
  authenticate(credentials: Credentials): Promise<AuthResult>
  refreshToken(token: string): Promise<Token>
  logout(userId: string): Promise<void>
}
```

**Internal Implementation** (hidden complexity):
- Token generation using JWT
- Session management with Redis
- Password hashing with bcrypt
- Rate limiting per user

**Dependencies**:
- Requires: Database, Redis, ConfigService
- Used by: AuthController, AuthMiddleware

**Data Structures**:
```typescript
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
```

**Error Handling**:
- InvalidCredentials → return { success: false, error: "Invalid email/password" }
- DatabaseError → log error, return generic failure message
- RateLimitExceeded → return 429 with retry-after header
```

### 3. Implementation Pseudocode

**Critical algorithms in pseudocode** (not real code, but close):

```markdown
## Core Algorithms

### User Authentication Flow

```pseudocode
function authenticate(credentials):
  1. Validate input format
     - email matches regex pattern
     - password length >= 8 chars
     - if invalid: return error

  2. Check rate limiting
     - key = "auth_attempts:{email}"
     - attempts = redis.get(key) || 0
     - if attempts > 5: return rate limit error
     - redis.incr(key, ttl=15min)

  3. Query user from database
     - user = db.query("SELECT * FROM users WHERE email = ?", email)
     - if not found: return invalid credentials error

  4. Verify password
     - match = bcrypt.compare(password, user.password_hash)
     - if !match: return invalid credentials error

  5. Generate session token
     - token = jwt.sign({ userId: user.id, email: user.email }, secret, { expiresIn: '24h' })
     - session = { userId: user.id, token, createdAt: now() }
     - redis.set("session:{token}", session, ttl=24h)

  6. Return success
     - return { success: true, token, user: sanitize(user) }
```

### Token Refresh Flow
[Additional pseudocode for other critical paths]
```

### 4. File Organization

```markdown
## File Organization

```
src/
  auth/
    AuthService.ts       # Main authentication logic (implements UserAuth interface)
    AuthController.ts    # HTTP endpoints (POST /auth/login, /auth/refresh, /auth/logout)
    AuthMiddleware.ts    # Request authentication middleware
    types.ts             # TypeScript types (Credentials, AuthResult, etc.)
    auth.test.ts         # Unit tests for AuthService
    auth.integration.test.ts  # Integration tests for full auth flow

  database/
    UserRepository.ts    # User data access (abstracts database queries)

  redis/
    SessionStore.ts      # Session management (abstracts Redis operations)
```

**Modification to existing files**:
- `src/types/index.ts` - Add User type export
- `src/middleware/index.ts` - Register AuthMiddleware
- `src/routes/index.ts` - Add auth routes
```

### 5. Integration Points

```markdown
## Integration Points

**Database Schema**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

**Redis Keys**:
- `auth_attempts:{email}` - Rate limiting counter (TTL: 15min)
- `session:{token}` - Session data (TTL: 24h)

**External APIs**: None

**Environment Variables**:
- `JWT_SECRET` - Secret for signing tokens
- `REDIS_URL` - Redis connection string
- `DATABASE_URL` - PostgreSQL connection string
```

### 6. State Management

```markdown
## State Management

**Client State**:
- Token stored in localStorage
- User object stored in React Context (AuthContext)
- Authentication state: { isAuthenticated, user, loading }

**Server State**:
- Sessions in Redis (ephemeral, 24h TTL)
- User data in PostgreSQL (persistent)
- No in-memory state (stateless servers for horizontal scaling)

**State Update Flow**:
1. Login → Server creates session → Client stores token
2. Page refresh → Client reads token → Server validates → User restored
3. Logout → Server deletes session → Client clears token
```

### 7. Error Handling Strategy

```markdown
## Error Handling Strategy

**Error Categories**:
1. **Validation Errors** (4xx): Return to user with specific message
2. **Authentication Errors** (401): Clear session, redirect to login
3. **Authorization Errors** (403): Show "Access Denied" message
4. **Server Errors** (5xx): Log details, show generic error to user
5. **Network Errors**: Retry with exponential backoff

**Error Response Format**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password",
    "retryable": true
  }
}
```

**Logging**:
- All authentication attempts (success/failure) → audit log
- Server errors → error tracking service (Sentry)
- Rate limit hits → metrics (Datadog)
```

### 8. Testing Strategy

```markdown
## Testing Strategy

**Unit Tests** (fast, isolated):
- `AuthService.authenticate()` with mocked database and Redis
- Password validation logic
- Token generation/verification
- Error handling paths

**Integration Tests** (slower, real dependencies):
- Full auth flow with test database and Redis
- Token refresh with expired tokens
- Rate limiting behavior
- Concurrent authentication attempts

**E2E Tests**:
- User login flow in browser
- Session persistence across page refreshes
- Logout clears session

**Mocking Strategy**:
- Mock external services (email, SMS) in unit tests
- Use test database/Redis for integration tests
- Minimize mocking - heavy mocking indicates coupling problems
```

### 9. Performance Considerations

```markdown
## Performance Considerations

**Expected Load**:
- 1000 authentications/min peak
- 50ms p95 response time target
- 99.9% uptime requirement

**Optimizations**:
- Redis for fast session lookups (< 1ms)
- Database connection pooling (max 20 connections)
- JWT tokens to avoid database hits on every request
- Index on users.email for fast lookups

**Scaling Strategy**:
- Horizontal: Stateless servers behind load balancer
- Database: Read replicas for user queries
- Redis: Redis Cluster for session storage
```

### 10. Security Considerations

```markdown
## Security Considerations

**Threats Mitigated**:
- Brute force attacks → Rate limiting (5 attempts per 15min)
- Password leaks → bcrypt hashing (cost factor 12)
- Token theft → Short-lived tokens (24h), HTTPS only
- Session hijacking → Secure, HttpOnly cookies
- Timing attacks → Constant-time password comparison

**Security Best Practices**:
- Never log passwords or tokens
- Sanitize user data in responses (remove password_hash)
- Use prepared statements (prevent SQL injection)
- Validate all inputs (email format, password strength)
- Set security headers (HSTS, CSP, X-Frame-Options)
```

### 11. Infrastructure Design

**If TASK.md flagged infrastructure gaps**, design infrastructure alongside feature architecture:

```markdown
## Infrastructure Design

**Quality Gates** (apply `quality-gates` skill):
```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,tsx}"
      run: pnpm eslint --fix {staged_files}
      stage_fixed: true
    format:
      glob: "*.{ts,tsx,json,md,css}"
      run: pnpm prettier --write {staged_files}
      stage_fixed: true
    typecheck:
      run: pnpm tsc --noEmit

pre-push:
  commands:
    test:
      run: pnpm test
```

**Structured Logging** (apply `structured-logging` skill):
```typescript
// utils/logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: {
    paths: ['password', 'apiKey', 'token', '*.secret'],
    censor: '[REDACTED]',
  },
})

// Usage with correlation IDs
export function withRequestId<T>(fn: (logger: Logger) => T): T {
  const requestId = generateRequestId()
  const childLogger = logger.child({ requestId })
  return fn(childLogger)
}
```

**Error Tracking** (Sentry integration):
```typescript
// utils/sentry.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // Redact sensitive data
    if (event.request) {
      delete event.request.cookies
      delete event.request.headers?.authorization
    }
    return event
  },
})
```

**Design System** (apply `design-tokens` skill):
```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Brand colors (OKLCH for perceptual uniformity) */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.7 0.15 180);

  /* Typography */
  --font-display: "Clash Display", sans-serif;
  --font-body: "Inter", sans-serif;

  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}
```

**Changelog Automation** (apply `changelog-automation` skill):
```bash
# For monorepos: Changesets
pnpm add -D @changesets/cli
pnpm changeset init

# For single packages: semantic-release
pnpm add -D semantic-release @semantic-release/git @semantic-release/changelog
```

**CI/CD Pipeline**:
```yaml
# .github/workflows/ci.yml
name: CI

on: [pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test
      - run: pnpm build
```
```

### 12. Alternative Architectures Considered

**Apply `ousterhout-principles` when evaluating alternatives**: Which architecture minimizes complexity? Which has the deepest modules (simplest interfaces hiding most functionality)?

```markdown
## Alternative Architectures Considered

### Alternative A: Monolithic Auth Module
- **Pros**: Simple, one file
- **Cons**: Poor separation of concerns, hard to test
- **Ousterhout Analysis**: Shallow module - interface complexity ≈ implementation complexity
- **Verdict**: Rejected - violates modularity principles

### Alternative B: Microservice
- **Pros**: Independent deployment, dedicated scaling
- **Cons**: Network latency, operational complexity, overkill for current scale
- **Ousterhout Analysis**: Adds network dependency (complexity source), distributed state management (obscurity)
- **Verdict**: Rejected - premature optimization, increases overall system complexity

### Alternative C: Serverless Functions
- **Pros**: Auto-scaling, pay-per-use
- **Cons**: Cold starts (100ms+), vendor lock-in, harder debugging
- **Ousterhout Analysis**: Hidden cold start complexity leaks into interface (unpredictable latency)
- **Verdict**: Rejected - cold starts hurt UX, information leakage through performance

**Selected**: Modular monolith with clear boundaries (can extract later if needed)
- **Ousterhout Justification**: Deep modules with simple interfaces, minimal dependencies, obvious behavior
- **Skills Applied**: `ousterhout-principles` for module evaluation, `naming-conventions` for component naming
```

## Quality Validation

Before finalizing DESIGN.md, verify:

**✅ Clarity**: Can a developer implement this without making architectural decisions?
**✅ Completeness**: Are all modules, interfaces, and data structures defined?
**✅ Pseudocode**: Are critical algorithms detailed enough to translate to code?
**✅ Simplicity**: Is this the simplest architecture that meets requirements?
**✅ Deep Modules**: Do modules hide complexity behind simple interfaces?
**✅ Explicit Dependencies**: Are all integrations and assumptions documented?
**✅ Infrastructure Design**: If TASK.md flagged infrastructure gaps, is infrastructure designed (quality gates, logging, error tracking, design tokens, changelog)?

**Red Flags**:
- Vague interfaces ("handle authentication") → Make concrete
- Missing pseudocode for complex logic → Add it
- Unclear module boundaries → Refine responsibilities
- Hand-waving integration points → Specify exactly
- "We'll figure it out later" → No, figure it out now

### Architecture Validation (Multi-Agent Review)

After writing DESIGN.md, run parallel validation (optional but recommended for complex features):

```
Task architecture-strategist("Review DESIGN.md for architectural soundness and alignment with codebase patterns")
Task pattern-recognition-specialist("Verify module boundaries match existing codebase conventions")
```

Review agent findings:
- **Critical issues**: Refine DESIGN.md immediately
- **Suggestions**: Note in DESIGN.md "Alternative Approaches Considered" or defer to implementation
- **Minor concerns**: Document as implementation notes

This catches architectural problems before any code is written.

## ADR Creation (If Required)

If TASK.md flagged "ADR Required":

1. **Create `/docs/adr/` directory** (if first ADR)
2. **Determine next number**: Count existing ADRs + 1
3. **Create ADR file** using MADR Light template:

```markdown
# ADR-{NUMBER}: {Short Title}

Date: YYYY-MM-DD
Status: proposed

## Context and Problem Statement
[What problem requires this decision?]

## Considered Options
* Option 1: [description]
* Option 2: [description]
* Option 3: [description]

## Decision Outcome
Chosen: [option] because [rationale: simplicity/user value/explicitness]

### Consequences
* Good: [benefits]
* Bad: [costs/downsides]
```

4. **Save as**: `docs/adr/{number}-{slug}.md`
5. **Reference in DESIGN.md**: "See ADR-{NUMBER} for decision rationale"
6. **Update `/docs/adr/README.md`** with entry for new ADR

## After Creating DESIGN.md

Present summary:
- Architecture selected and why
- Key modules and responsibilities
- Critical design decisions made
- Complexity hidden vs. exposed
- What's NOT in scope (saved for iteration)

**Next**: Run `/plan` to convert this architecture into atomic implementation tasks.

## Philosophy

**"Give me six hours to chop down a tree and I will spend the first four sharpening the axe."** - Abraham Lincoln

Architecture is sharpening the axe. The PRD told us which tree to chop. Now we're deciding exactly how to swing the axe for maximum efficiency and minimum wasted effort.

**Remember**: Bad architecture costs weeks in rework. Good architecture guides implementation and prevents design churn. Excellent architecture makes the "right" implementation obvious.

This is Version 2.0 of system design: not just deciding what to build, but exactly how to build it.
