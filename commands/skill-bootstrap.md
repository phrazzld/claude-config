Analyze project codebase and generate project-specific Skills for component library, API conventions, state management, styling, and database schemas.

# SKILL-BOOTSTRAP

Automatically detect project stack and generate applicable project-specific Skills.

## Overview

Project-specific Skills encode knowledge from your actual codebase: component APIs, API patterns, state conventions, styling systems, and database schemas. This command analyzes your project and generates Skills tailored to your stack.

**Generated Skills help Claude:**
- Suggest correct components with proper props
- Follow existing API patterns when adding endpoints
- Use established state management conventions
- Apply consistent styling approaches
- Work with your database schema correctly

## Detection Algorithm

### Multi-Signal Stack Detection

**1. Package.json Analysis**
- Dependencies: React, Next.js, Vue, Svelte, Convex, Tailwind, shadcn/ui, Zustand, Redux, Prisma, Drizzle
- DevDependencies: Vite, Turbo, TypeScript, ESLint, Prettier
- Workspaces: Detect monorepo structure (apps/*, packages/*)
- PackageManager: pnpm, npm, yarn, bun

**2. File Structure Analysis**
- Framework: app/ (Next.js App Router), pages/ (Next.js Pages Router), src/ (standard)
- Components: components/, ui/, lib/components/, packages/ui/
- API: api/, app/api/, pages/api/, server/, apps/api/
- Database: convex/, prisma/, drizzle/
- Config: next.config.js, vite.config.ts, turbo.json, tsconfig.json

**3. Language File Counting**
- TypeScript: .ts, .tsx files
- JavaScript: .js, .jsx files
- Other: .go, .rs, .py, .vue, .svelte

**4. Framework-Specific Indicators**
- Next.js App Router: app/layout.tsx, app/page.tsx
- Next.js Pages Router: pages/_app.tsx, pages/index.tsx
- Convex: convex/ directory, convex.json
- Turbo monorepo: turbo.json, workspaces in package.json

## Skill Generation Decision Tree

### Component Library Skill
**Trigger:** (React OR Next.js OR Vue OR Svelte) AND (components/ OR ui/ OR lib/components/)

**Extracts:**
- Component names and file locations
- Prop interfaces (TypeScript types)
- Common composition patterns (children, render props, slots)
- Component categories (layout, UI, forms, data display)

**Tools:** ast-grep for component exports, Grep for "export.*function", Read for prop types

**Output:** `.claude/skills/component-library/SKILL.md`

---

### API Conventions Skill
**Trigger:** api/ OR app/api/ OR pages/api/ OR server/ exists

**Extracts:**
- Endpoint patterns (RESTful, RPC, GraphQL)
- Authentication middleware (JWT, session, API key)
- Error response formats
- Request/response types
- Route naming conventions

**Tools:** Glob for API routes, ast-grep for handler patterns, Grep for error handling

**Output:** `.claude/skills/api-conventions/SKILL.md`

---

### State Management Skill
**Trigger:** zustand OR redux OR jotai OR nanostores in package.json

**Extracts:**
- Store structure and naming
- Action/reducer patterns
- Selector conventions
- Async state handling
- State persistence patterns

**Tools:** ast-grep for store definitions, Grep for hooks, Read for store files

**Output:** `.claude/skills/state-management/SKILL.md`

---

### Styling Conventions Skill
**Trigger:** tailwind OR styled-components OR emotion OR @stitches in package.json

**Extracts:**
- Utility patterns (Tailwind classes)
- Design tokens (colors, spacing, typography)
- Component styling conventions
- Responsive patterns
- Theme configuration

**Tools:** Read tailwind.config.js, Grep for className patterns, Read theme files

**Output:** `.claude/skills/styling-conventions/SKILL.md`

---

### Database Schema Skill
**Trigger:** Convex OR Prisma OR Drizzle detected

**Extracts:**
- Table/collection schemas
- Relationships and indexes
- Query patterns
- Validation rules
- Data access conventions

**Tools:** Read schema files (schema.ts, schema.prisma, convex/schema.ts)

**Output:** `.claude/skills/database-schema/SKILL.md`

## Input/Output Flow

### 1. Discovery Phase
```
Read package.json → Detect dependencies and workspaces
Glob **/*.{ts,tsx,js,jsx} → Count language files
Glob **/app/ **/pages/ **/components/ → Detect structure
Read next.config.js / vite.config.ts → Confirm framework
```

### 2. Analysis Phase
```
FOR EACH applicable Skill type:
  Run specific extraction logic
  Analyze patterns and conventions
  Generate Skill content
```

### 3. Generation Phase
```
Create .claude/skills/ directory (if not exists)
Write each Skill to .claude/skills/[skill-name]/SKILL.md
Add YAML frontmatter (name, description)
Generate activation keywords for each Skill
```

### 4. Summary Phase
```
Output:
✅ Generated 3 project-specific Skills:
  - component-library (23 components detected)
  - api-conventions (12 endpoints analyzed)
  - styling-conventions (Tailwind + shadcn/ui)

Next steps:
- Review generated Skills in .claude/skills/
- Edit Skills to add project-specific notes
- Skills will auto-activate in relevant contexts
```

## Edge Cases

**No package.json:**
- Graceful degradation: Detect via file extensions only
- Count .tsx/.ts → Likely TypeScript project
- Count .jsx/.js → Likely JavaScript project
- Generate generic Skills based on file structure

**Monorepo:**
- Detect via package.json workspaces field
- Analyze apps/* and packages/* separately
- Generate Skills for each workspace if significantly different
- OR generate unified Skills if patterns are consistent

**Mixed Stack:**
- Generate Skills for all detected technologies
- Example: Next.js frontend + Go backend → Generate component, API, and Go-specific Skills
- Clearly label which Skills apply to which part of stack

**No Applicable Skills:**
- Simple project with no detectable patterns
- Output: "No project-specific Skills generated. User-level Skills are available."
- Suggest running command again after adding more code

**Existing Skills:**
- Warn: ".claude/skills/ directory already exists"
- Options: Overwrite, merge, or skip
- Default: Skip (preserve manual edits)

## Skill Format Template

Each generated Skill follows this structure:

```markdown
---
name: [skill-name]
description: "[What this Skill helps with]. Use when [triggering contexts]."
---

# [Skill Title]

[Brief overview of what this Skill covers]

## Quick Reference

[Most useful patterns/components/conventions in scannable format]

## Patterns and Conventions

[Detailed analysis of detected patterns]

## Examples

[Code examples from actual project]

## Common Operations

[How-to guides for common tasks using these patterns]
```

## Skill Generation Templates

Each Skill type has a specific extraction and formatting approach. Templates define what to extract, which tools to use, and how to structure the output.

### Template 1: Component Library Skill

**Extraction Logic:**
- **Component Discovery:** Glob `**/*.{tsx,jsx}` in components/, ui/, lib/components/
- **Export Detection:** ast-grep `export function $NAME($PROPS)` or `export const $NAME`
- **Prop Types:** ast-grep `interface $NAMEProps` or analyze function parameters
- **Composition Patterns:** Grep for `children`, `render`, `as` props

**Analysis Tools:**
```bash
# Find all component exports
ast-grep --lang tsx -p 'export function $COMP($PROPS) { $$$ }'

# Find prop interfaces
grep -r 'interface.*Props' components/

# Analyze usage patterns
grep -r 'import.*from.*components' --include="*.tsx"
```

**Output Format:**
```markdown
---
name: component-library
description: "Component library reference for [ProjectName]. Use when building UI, choosing components, or checking prop APIs."
---

# Component Library - [ProjectName]

## Quick Reference

| Component | Props | Purpose |
|-----------|-------|---------|
| Button | variant, size, onClick, disabled | Primary CTA and actions |
| Card | title, children, footer | Content containers |
| Modal | isOpen, onClose, title, children | Overlays and dialogs |

## Component Patterns

### Composition via Children
Components accept `children` for flexible content:
- Layout components (Card, Container, Stack)
- Wrapper components (Modal, Drawer, Tooltip)

### Prop Forwarding
Components spread ...props to underlying elements for flexibility.

### Variant System
Most components use `variant` prop for visual styles:
- primary, secondary, ghost, danger

## Detailed Component APIs

### Button
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  disabled?: boolean
  children: React.ReactNode
}
```

Usage: Primary actions, form submissions, navigation

[Additional components...]

## Common Patterns from Codebase

[Extracted from actual usage - top 5 patterns]
```

---

### Template 2: API Conventions Skill

**Extraction Logic:**
- **Route Discovery:** Glob `**/api/**/*.{ts,tsx}` or `**/app/api/**/route.ts`
- **Handler Patterns:** ast-grep `export async function GET|POST|PUT|DELETE`
- **Auth Middleware:** Grep for authentication patterns (JWT, session, API key)
- **Error Responses:** Analyze error handler functions and return types

**Analysis Tools:**
```bash
# Find API routes (Next.js App Router)
find . -name "route.ts" -path "*/app/api/*"

# Find handler functions
ast-grep --lang typescript -p 'export async function $METHOD(request) { $$$ }'

# Find error patterns
grep -r 'throw new.*Error\|return.*error' app/api/
```

**Output Format:**
```markdown
---
name: api-conventions
description: "API conventions for [ProjectName]. Use when creating endpoints, handling errors, or implementing authentication."
---

# API Conventions - [ProjectName]

## Quick Reference

**Framework:** [Next.js App Router / Pages API / Express / etc]
**Auth:** [JWT / Session / API Key / OAuth]
**Error Format:** `{ message: string, code?: string }`

## Endpoint Patterns

### Route Structure
```
/api/[resource]/route.ts → GET, POST
/api/[resource]/[id]/route.ts → GET, PUT, DELETE
```

### Handler Signature
```typescript
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  // Handler logic
}
```

## Authentication

**Pattern:** [Describe auth approach]
```typescript
// Example from codebase
const user = await authenticateRequest(request)
if (!user) {
  return Response.json({ message: 'Unauthorized' }, { status: 401 })
}
```

## Error Handling

**Conventions:**
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid auth)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

**Error Response Format:**
```typescript
{
  message: string  // Human-readable error
  code?: string    // Machine-readable error code
  details?: any    // Additional context (dev only)
}
```

## Request/Response Types

[Extract common types from codebase]

## Examples from Codebase

[Real endpoint examples with patterns]
```

---

### Template 3: State Management Skill

**Extraction Logic:**
- **Store Detection:** Grep for Zustand `create(`, Redux `createSlice`, Jotai `atom(`
- **Hook Patterns:** ast-grep for custom hooks (useConvex, useSWR, useQuery)
- **Async Patterns:** Analyze how async state is handled (loading, error, data)
- **Selectors:** Find selector patterns in stores

**Analysis Tools:**
```bash
# Find Zustand stores
grep -r 'create<.*>(' --include="*.ts"

# Find Convex queries
grep -r 'useQuery(api\.' --include="*.tsx"

# Find custom hooks
ast-grep --lang typescript -p 'export function use$HOOK() { $$$ }'
```

**Output Format:**
```markdown
---
name: state-management
description: "State management patterns for [ProjectName]. Use when managing state, creating stores, or fetching data."
---

# State Management - [ProjectName]

## Stack

**Server State:** [Convex / TanStack Query / SWR]
**Client State:** [Zustand / Redux / Context / None]
**Form State:** [React Hook Form / Formik / Native]

## Convex Query Patterns (Server State)

### Basic Query
```typescript
const data = useQuery(api.namespace.functionName, { param: value })

// data is undefined while loading
// data is result when loaded
// Automatically reactive - updates on server changes
```

### Conditional Query
```typescript
const data = useQuery(
  isReady ? api.namespace.func : "skip",
  isReady ? { param: value } : "skip"
)
```

## Client State Patterns

[If using Zustand]
```typescript
const useStore = create<State>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}))

// Usage
const count = useStore((state) => state.count)
const increment = useStore((state) => state.increment)
```

## Common Patterns from Codebase

[Extract top 5 state patterns used]
```

---

### Template 4: Styling Conventions Skill

**Extraction Logic:**
- **Config Analysis:** Read tailwind.config.js/ts for theme tokens
- **Utility Patterns:** Grep `className=` and analyze frequency of utilities
- **Component Classes:** Find common class combinations
- **Design Tokens:** Extract colors, spacing, typography from config

**Analysis Tools:**
```bash
# Read Tailwind config
cat tailwind.config.js

# Find most common utilities
grep -roh 'className="[^"]*"' --include="*.tsx" | sort | uniq -c | sort -rn | head -20

# Find color usage
grep -r 'bg-\|text-\|border-' --include="*.tsx" | cut -d: -f2 | sort | uniq -c | sort -rn
```

**Output Format:**
```markdown
---
name: styling-conventions
description: "Styling conventions and design system for [ProjectName]. Use when styling components or implementing designs."
---

# Styling Conventions - [ProjectName]

## Tech Stack

**CSS Framework:** [Tailwind CSS / Styled Components / CSS Modules]
**Component Library:** [shadcn/ui / Radix / Headless UI / None]

## Design Tokens

### Colors
```
Primary: blue-600, blue-50 (bg), blue-200 (border)
Success: green-600, green-50 (bg)
Danger: red-600, red-50 (bg)
Gray scale: gray-50, gray-100, ..., gray-900
```

### Spacing
```
Compact: gap-2 (8px), p-2
Standard: gap-4 (16px), p-4
Loose: gap-6 (24px), p-6
```

### Typography
```
Headings: text-2xl font-bold, text-xl font-semibold
Body: text-base (16px), text-sm (14px)
Captions: text-xs (12px)
```

## Common Patterns

### Card Container
```tsx
className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm"
```

### Primary Button
```tsx
className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
```

### Status Indicators
```tsx
// Success
className="bg-green-50 text-green-700 border border-green-200"

// Error
className="bg-red-50 text-red-700 border border-red-200"
```

## Responsive Patterns

[Extract common responsive utilities: sm:, md:, lg:]

## Component Styling Conventions

[Patterns from actual components]
```

---

### Template 5: Database Schema Skill

**Extraction Logic:**
- **Schema Reading:** Read schema.prisma, schema.ts (Convex), drizzle.config.ts
- **Table Analysis:** ast-grep for table definitions
- **Index Detection:** Find .index() calls (Convex) or @@index (Prisma)
- **Relationships:** Analyze foreign keys, references

**Analysis Tools:**
```bash
# Read Convex schema
cat convex/schema.ts

# Find table definitions
ast-grep --lang typescript -p 'defineTable({ $$$ })'

# Find indexes
grep -r '\.index(' convex/
```

**Output Format:**
```markdown
---
name: database-schema
description: "Database schema for [ProjectName]. Use when querying data, creating tables, or understanding relationships."
---

# Database Schema - [ProjectName]

## Database

**Type:** [Convex / Postgres + Prisma / SQLite + Drizzle]
**ORM:** [Convex SDK / Prisma / Drizzle]

## Quick Reference

### Tables
- **users** - User profiles (auth + GitHub data)
- **repos** - Repository metadata
- **events** - GitHub activity events
- **ingestionJobs** - Background job tracking

## Schema Details

### users
```typescript
{
  _id: Id<"users">
  clerkId?: string          // Clerk auth ID
  ghId: number              // GitHub user ID
  ghLogin: string           // GitHub username
  name?: string
  email?: string
  avatarUrl?: string
  createdAt: number
  updatedAt: number
}

Indexes:
- by_clerkId (unique lookup)
- by_ghId (GitHub user lookup)
- by_ghLogin (username search)
```

### repos
```typescript
{
  _id: Id<"repos">
  ghId: number
  name: string
  fullName: string          // "owner/repo"
  description?: string
  language?: string
  stars: number
  forks: number
  userId: Id<"users">       // Owner
  createdAt: number
}

Indexes:
- by_userId (user's repos)
- by_fullName (repo lookup)
- by_ghId (GitHub repo ID)
```

## Relationships

```
users (1) ──< (N) repos
users (1) ──< (N) events
users (1) ──< (N) ingestionJobs
repos (1) ──< (N) events
```

## Common Query Patterns

### Find user by Clerk ID
```typescript
const user = await ctx.db
  .query("users")
  .withIndex("by_clerkId", (q) => q.eq("clerkId", clerkId))
  .unique()
```

### Get user's repos
```typescript
const repos = await ctx.db
  .query("repos")
  .withIndex("by_userId", (q) => q.eq("userId", userId))
  .collect()
```

[Additional common patterns from codebase]
```

---

## Template Usage in Command

When `/skill-bootstrap` runs:

1. **Detect applicable Skills** using decision tree
2. **For each applicable Skill:**
   - Run extraction logic with specified tools
   - Analyze extracted data
   - Generate Skill file using template structure
   - Write to `.claude/skills/[skill-name]/SKILL.md`
3. **Output summary** of generated Skills

**Key Principle:** Templates are guidelines, not rigid structures. Generated Skills should adapt to what's actually found in the codebase.

---

## Command Implementation Notes

This is a **design document** for the `/skill-bootstrap` command. Implementation tasks:

1. **Detection logic** ✅
2. **Skill generation templates** ✅
3. **Core command logic** (orchestration, error handling, user feedback)
4. **Testing** (validate on sample projects: React, Next.js, monorepo)

---

**Philosophy:** Skills encode project knowledge that would otherwise exist only in developers' heads or scattered across docs. Bootstrap automates extracting this knowledge from the codebase itself.
