Analyze project codebase and generate project-specific Skills for component library, API conventions, state management, styling, and database schemas.

# SKILL-BOOTSTRAP

Automatically detect project stack and generate applicable project-specific Skills that encode your codebase's patterns and conventions.

## Mission

Extract project knowledge from code and generate Skills that help Claude:
- Suggest correct components with proper props
- Follow existing API patterns when adding endpoints
- Use established state management conventions
- Apply consistent styling approaches
- Work with your database schema correctly

## Phase 1: Stack Detection

Run multi-signal detection to identify project technologies and structure.

### 1. Analyze package.json

```bash
# Read package.json
Read package.json

# Detect:
- Framework: React, Next.js, Vue, Svelte
- Backend: Convex, Prisma, Drizzle, Express, Fastify
- Styling: Tailwind, styled-components, emotion, @stitches
- State: zustand, redux, jotai, nanostores
- Monorepo: Check "workspaces" field
- Package manager: "packageManager" field
```

### 2. Analyze File Structure

```bash
# Detect framework
Glob for: app/layout.tsx (Next.js App Router)
Glob for: pages/_app.tsx (Next.js Pages Router)
Glob for: src/routes/ (SvelteKit)

# Detect components
Glob for: components/**/*.tsx
Glob for: ui/**/*.tsx
Glob for: lib/components/**/*.tsx

# Detect API
Glob for: api/**/*.ts
Glob for: app/api/**/route.ts
Glob for: pages/api/**/*.ts
Glob for: server/**/*.ts

# Detect database
Glob for: convex/schema.ts
Glob for: prisma/schema.prisma
Glob for: drizzle.config.ts
```

### 3. Count Language Files

```bash
# Count file types
Glob **/*.tsx | count
Glob **/*.ts | count
Glob **/*.jsx | count
Glob **/*.js | count
Glob **/*.go | count
Glob **/*.rs | count
```

### 4. Summarize Detection

Output detection summary:
```
✅ Stack Detected:
  Framework: Next.js 15 (App Router)
  Language: TypeScript (142 files)
  Backend: Convex
  Styling: Tailwind CSS + shadcn/ui
  State: Convex (server) + React hooks (client)
  Package Manager: pnpm
  Monorepo: Yes (apps/web, packages/db, packages/sdk)
```

## Phase 2: Skill Generation Decision

Based on detection, determine which Skills to generate:

### Decision Tree

**Component Library Skill:**
- IF: (React OR Next.js OR Vue OR Svelte detected)
- AND: (components/ OR ui/ OR lib/components/ exists)
- THEN: Generate component-library Skill

**API Conventions Skill:**
- IF: (api/ OR app/api/ OR pages/api/ OR server/ exists)
- THEN: Generate api-conventions Skill

**State Management Skill:**
- IF: (zustand OR redux OR jotai OR Convex detected)
- THEN: Generate state-management Skill

**Styling Conventions Skill:**
- IF: (tailwind OR styled-components OR emotion detected)
- THEN: Generate styling-conventions Skill

**Database Schema Skill:**
- IF: (Convex OR Prisma OR Drizzle detected)
- THEN: Generate database-schema Skill

Output generation plan:
```
📋 Will Generate 4 Skills:
  ✓ component-library (23 components found)
  ✓ api-conventions (Convex functions)
  ✓ styling-conventions (Tailwind + design tokens)
  ✓ database-schema (Convex schema with 8 tables)
```

## Phase 3: Generate Skills

For each applicable Skill, run extraction and generation.

### Component Library Skill

**Extract Components:**
```bash
# Find component exports
ast-grep --lang tsx -p 'export function $COMP($$$) { $$$ }' components/

# Find prop interfaces
Grep -r 'interface.*Props' components/ --output-mode=content

# Analyze common patterns
Grep -r 'children' components/
Grep -r 'className' components/
```

**Generate Skill:**
Create `.claude/skills/component-library/SKILL.md`:
```markdown
---
name: component-library
description: "Component library for [ProjectName]. Use when building UI, choosing components, or checking prop APIs."
---

# Component Library - [ProjectName]

## Quick Reference

| Component | Props | Purpose |
|-----------|-------|---------|
[Table from analysis]

## Component Patterns
[Extracted patterns: children, className forwarding, variants]

## Detailed APIs
[Component-by-component breakdown]
```

---

### API Conventions Skill

**Extract API Patterns:**
```bash
# Next.js App Router
Glob app/api/**/route.ts

# Convex functions
Glob convex/**/*.ts
Grep 'export const' convex/ --output-mode=content

# Auth patterns
Grep -r 'auth\|Auth' api/ --output-mode=content -C 3
```

**Generate Skill:**
Create `.claude/skills/api-conventions/SKILL.md`:
```markdown
---
name: api-conventions
description: "API patterns for [ProjectName]. Use when creating endpoints, handling auth, or implementing error handling."
---

# API Conventions - [ProjectName]

## Stack
Framework: [Detected framework]
Auth: [Detected auth approach]

## Endpoint Patterns
[Extracted route structure]

## Authentication
[Extracted auth middleware patterns]

## Error Handling
[Extracted error response formats]
```

---

### State Management Skill

**Extract State Patterns:**
```bash
# Zustand stores
Grep -r 'create<' --include="*.ts" --output-mode=content

# Convex queries
Grep -r 'useQuery(api\.' --include="*.tsx" --output-mode=content
Grep -r 'useMutation(api\.' --include="*.tsx" --output-mode=content

# Custom hooks
ast-grep --lang typescript -p 'export function use$HOOK() { $$$ }'
```

**Generate Skill:**
Create `.claude/skills/state-management/SKILL.md`:
```markdown
---
name: state-management
description: "State management for [ProjectName]. Use when managing state, creating stores, or fetching data."
---

# State Management - [ProjectName]

## Stack
Server State: [Detected - Convex/TanStack/SWR]
Client State: [Detected - Zustand/Redux/Context]

## Query Patterns
[Extracted query patterns with examples]

## Store Patterns
[Extracted store patterns if applicable]
```

---

### Styling Conventions Skill

**Extract Styling Patterns:**
```bash
# Read Tailwind config
Read tailwind.config.js OR tailwind.config.ts

# Find common utilities
Grep -roh 'className="[^"]*"' --include="*.tsx" | head -50

# Analyze color usage
Grep -r 'bg-\|text-\|border-' --include="*.tsx" --output-mode=files_with_matches
```

**Generate Skill:**
Create `.claude/skills/styling-conventions/SKILL.md`:
```markdown
---
name: styling-conventions
description: "Styling conventions for [ProjectName]. Use when styling components or implementing designs."
---

# Styling Conventions - [ProjectName]

## Stack
Framework: [Tailwind/Styled/CSS Modules]
Component Library: [shadcn/Radix/None]

## Design Tokens
[Extracted from config: colors, spacing, typography]

## Common Patterns
[Most frequent className combinations]

## Component Patterns
[Extracted patterns: cards, buttons, status indicators]
```

---

### Database Schema Skill

**Extract Schema:**
```bash
# Convex
Read convex/schema.ts

# Prisma
Read prisma/schema.prisma

# Extract table definitions
ast-grep --lang typescript -p 'defineTable({ $$$ })'

# Extract indexes
Grep -r '\.index(' convex/
Grep -r '@@index' prisma/
```

**Generate Skill:**
Create `.claude/skills/database-schema/SKILL.md`:
```markdown
---
name: database-schema
description: "Database schema for [ProjectName]. Use when querying data, creating tables, or understanding relationships."
---

# Database Schema - [ProjectName]

## Database
Type: [Convex/Postgres/SQLite]
ORM: [Convex/Prisma/Drizzle]

## Tables
[Quick reference list]

## Schema Details
[Table-by-table breakdown with fields and indexes]

## Relationships
[Relationship diagram]

## Query Patterns
[Common query patterns from codebase]
```

---

## Phase 4: Summary and Next Steps

Output final summary:
```
✅ Generated 4 Project-Specific Skills

Skills created in .claude/skills/:
  - component-library/ (23 components documented)
  - api-conventions/ (Convex patterns + auth)
  - styling-conventions/ (Tailwind tokens + patterns)
  - database-schema/ (8 tables + indexes + queries)

Next steps:
  1. Review generated Skills: ls -la .claude/skills/
  2. Edit Skills to add project-specific notes or examples
  3. Skills will auto-activate when relevant keywords detected
  4. Run /skill-update to refresh Skills as code evolves

Skills help Claude understand your codebase patterns and conventions.
```

## Error Handling

**No package.json:**
- Continue with file-based detection only
- Generate Skills based on file structure
- Note in summary: "Limited detection (no package.json)"

**No applicable Skills:**
- Output: "No project-specific Skills generated. Stack not detected or too simple."
- Suggest: "Add more code or run in correct directory"

**Existing .claude/skills/:**
- Warn: "Project Skills already exist in .claude/skills/"
- Options: "Overwrite? (y/N): "
- Default: Skip (preserve manual edits)
- If overwrite: Back up existing to .claude/skills.backup/

**Monorepo detected:**
- Ask: "Monorepo detected. Generate Skills for:"
  - "1. All workspaces (unified)"
  - "2. Current workspace only"
  - "3. Each workspace separately"
- Default: Current workspace only

**Partial generation:**
- If one Skill fails, continue with others
- Note failed Skills in summary
- Provide error details for debugging

## Implementation Notes

This command orchestrates:
1. **Detection** - Multi-signal stack detection
2. **Decision** - Which Skills to generate
3. **Extraction** - Use ast-grep, Grep, Read, Glob to analyze code
4. **Generation** - Create Skill files with YAML frontmatter
5. **Summary** - Report what was created

**Tools used:**
- Read: package.json, config files, schema files
- Glob: File discovery and counting
- Grep: Pattern extraction and analysis
- ast-grep: Code structure analysis
- Write: Generate Skill markdown files

**Design principles:**
- Graceful degradation (work with missing signals)
- Partial success (generate what's detectable)
- Preserve user edits (don't overwrite by default)
- Clear feedback (show what's happening)

---

**Philosophy:** Skills encode project knowledge that would otherwise exist only in developers' heads or scattered across docs. Bootstrap automates extracting this knowledge from the codebase itself.
