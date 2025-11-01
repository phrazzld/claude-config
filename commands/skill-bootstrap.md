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

## Command Implementation Notes

This is a **design document** for the `/skill-bootstrap` command. Implementation tasks:

1. **Detection logic** (this document) ✅
2. **Skill generation templates** (component, API, state, styling, database)
3. **Core command logic** (orchestration, error handling, user feedback)
4. **Testing** (validate on sample projects: React, Next.js, monorepo)

---

**Philosophy:** Skills encode project knowledge that would otherwise exist only in developers' heads or scattered across docs. Bootstrap automates extracting this knowledge from the codebase itself.
