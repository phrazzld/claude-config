# Skill-Bootstrap Command Test Plan

## Overview

This document outlines the test plan for validating the `/skill-bootstrap` command on real projects.

## Test Project: Noesis

**Location:** ~/Development/noesis
**Stack:** Next.js 15 (App Router) + Convex + TypeScript + Tailwind + pnpm monorepo

### Expected Detection Results

#### Phase 1: Stack Detection

**package.json Analysis:**
- Framework: Next.js (detected from dependencies)
- Language: TypeScript (from dependencies + file count)
- Backend: Convex (from dependencies)
- Styling: Tailwind CSS (from dependencies)
- Package Manager: pnpm (from packageManager field)
- Monorepo: Yes (workspaces: ["apps/*", "packages/*"])

**File Structure:**
- Next.js App Router: ✓ (apps/web/app/layout.tsx exists)
- Components: ✓ (apps/web/components/ exists)
- Convex Backend: ✓ (apps/web/convex/ exists with schema.ts)
- Tailwind Config: ✓ (apps/web/tailwind.config.ts exists)

**Language Files:**
- TypeScript: 142+ files (.ts, .tsx)
- JavaScript: Minimal (.js files)

**Expected Summary:**
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

#### Phase 2: Skill Generation Decision

**Expected Skills to Generate:**

1. ✅ **component-library** - React components detected in apps/web/components/
2. ✅ **api-conventions** - Convex functions detected in apps/web/convex/
3. ✅ **styling-conventions** - Tailwind detected in dependencies and config
4. ✅ **database-schema** - Convex schema detected at apps/web/convex/schema.ts

**Expected Decision Output:**
```
📋 Will Generate 4 Skills:
  ✓ component-library (3+ components found)
  ✓ api-conventions (Convex functions)
  ✓ styling-conventions (Tailwind + design tokens)
  ✓ database-schema (Convex schema with 8 tables)
```

#### Phase 3: Generation Validation

**Component Library Skill:**
- Should find: `IngestionBanner`, `AuthStatusIndicator`, `AuthLoadingBoundary`
- Should extract: Props interfaces, composition patterns (children usage)
- Should document: Common patterns (Convex queries, loading states)

**API Conventions Skill:**
- Should find: Convex query/mutation patterns
- Should extract: Auth patterns (Clerk tokenIdentifier)
- Should document: Error handling, data fetching patterns

**Styling Conventions Skill:**
- Should extract: Design tokens from tailwind.config.ts
- Should find: Common utilities (bg-blue-50, border-blue-200, rounded-lg)
- Should document: Color palette (blue for primary, gray scale)

**Database Schema Skill:**
- Should extract: Tables (users, repos, events, ingestionJobs)
- Should document: Indexes (by_clerkId, by_ghId, by_ghLogin)
- Should show: Relationships (users → repos, users → events)

#### Phase 4: Summary Validation

**Expected Output:**
```
✅ Generated 4 Project-Specific Skills

Skills created in .claude/skills/:
  - component-library/ (3 components documented)
  - api-conventions/ (Convex patterns + auth)
  - styling-conventions/ (Tailwind tokens + patterns)
  - database-schema/ (8 tables + indexes + queries)

Next steps:
  1. Review generated Skills: ls -la .claude/skills/
  2. Edit Skills to add project-specific notes or examples
  3. Skills will auto-activate when relevant keywords detected
  4. Run /skill-update to refresh Skills as code evolves
```

**Files Created:**
- `.claude/skills/component-library/SKILL.md`
- `.claude/skills/api-conventions/SKILL.md`
- `.claude/skills/styling-conventions/SKILL.md`
- `.claude/skills/database-schema/SKILL.md`

## Validation Criteria

### ✅ Must Have

1. **Detection Accuracy**
   - All technologies correctly identified
   - Monorepo structure recognized
   - File counts approximately accurate

2. **Skill Generation**
   - All 4 expected Skills created
   - Each Skill has valid YAML frontmatter
   - Each Skill has required sections

3. **Content Quality**
   - Component names match actual files
   - Schema tables match convex/schema.ts
   - Styling tokens match tailwind.config.ts
   - API patterns reflect actual Convex usage

4. **No Errors**
   - Command completes without crashes
   - All phases execute successfully
   - Graceful handling of edge cases

### 📋 Should Have

1. **Useful Content**
   - Quick reference sections are scannable
   - Examples come from actual codebase
   - Patterns are accurately described

2. **Proper Formatting**
   - Markdown renders correctly
   - Code blocks have correct syntax
   - Tables are properly formatted

3. **Monorepo Handling**
   - Detects apps/web as primary workspace
   - Doesn't analyze node_modules
   - Focuses on source code only

## Edge Cases to Test

### Monorepo Scenarios

**Current:** Noesis has apps/ and packages/
- Should analyze apps/web (main Next.js app)
- Should skip packages/ unless they contain components/UI
- Should handle workspace detection correctly

### Missing Dependencies

**Test:** What if Convex not in dependencies but convex/ exists?
- Should still detect via file structure
- Should note "Limited detection" in summary

### Existing Skills

**Test:** What if .claude/skills/ already exists?
- Should warn user
- Should offer to backup
- Should default to skip (preserve edits)

## Manual Testing Steps

1. **Navigate to Noesis:**
   ```bash
   cd ~/Development/noesis
   ```

2. **Run Command:**
   ```
   /skill-bootstrap
   ```

3. **Verify Phase 1:**
   - Check detection summary matches expected
   - Verify all technologies identified

4. **Verify Phase 2:**
   - Check decision output lists 4 Skills
   - Verify reasoning is correct

5. **Verify Phase 3:**
   - Check each Skill file created
   - Read content for accuracy
   - Validate YAML frontmatter

6. **Verify Phase 4:**
   - Check summary is clear
   - Verify file paths correct
   - Confirm next steps helpful

7. **Validate Content:**
   - Compare component names to actual files
   - Check schema matches convex/schema.ts
   - Verify Tailwind tokens from config
   - Confirm Convex patterns accurate

## Success Criteria

✅ **Command Complete** when:
- All 4 Skills generated without errors
- Detection accurately identifies stack
- Content matches actual codebase
- Skills have proper YAML frontmatter
- Summary provides clear next steps
- No crashes or unexpected behavior
- Monorepo handled appropriately

## Notes

- **Test Environment:** macOS with pnpm, Node 22+
- **Prerequisites:** Project has package.json and standard structure
- **Execution Context:** Run from project root directory
- **Expected Duration:** 30-60 seconds for analysis and generation

## Future Test Projects

After Noesis validation, test on:
1. **Simple React app** (no monorepo, basic structure)
2. **Next.js Pages Router** (different from App Router)
3. **Non-TypeScript project** (JavaScript only)
4. **Prisma project** (different ORM)
5. **Go + React** (mixed backend)
