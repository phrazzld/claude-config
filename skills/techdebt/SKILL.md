# /techdebt

Find and kill duplicated code, stale TODOs, and complexity hotspots.

Run at end of every session to maintain codebase hygiene.

## Process

1. **Detect issues** using fast tools (rg, ast-grep, ts-unused-exports)
2. **Group by severity** (critical → moderate → low)
3. **Suggest refactors** using existing patterns in codebase

## Detection Commands

Run these in parallel where possible:

```bash
# 1. TODO/FIXME/HACK comments with age context
rg -n "TODO|FIXME|HACK|XXX" --type ts --type tsx --type js --type jsx 2>/dev/null | head -30

# 2. Unused exports (TypeScript only)
npx ts-unused-exports tsconfig.json 2>/dev/null | head -20

# 3. Long functions (>50 lines) - complexity hotspots
rg -l --type ts --type tsx . | head -20 | xargs -I{} sh -c 'awk "/^(export )?(async )?function|^const .* = (async )?\(/ {start=NR} /^}/ && start {if(NR-start>50) print FILENAME\":\"start\": \"NR-start\" lines\"; start=0}" {}'

# 4. Duplicated error handling patterns
ast-grep --pattern 'try { $$$A } catch (e) { console.error(e); throw e; }' --json 2>/dev/null | jq -r '.[] | "\(.file):\(.range.start.line)"' | head -10

# 5. Magic numbers (literals > 10 outside of obvious contexts)
rg -n '\b[0-9]{3,}\b' --type ts --type tsx -g '!*.test.*' -g '!*.spec.*' 2>/dev/null | grep -v "port\|1000\|width\|height\|timeout" | head -15

# 6. Empty catch blocks
ast-grep --pattern 'catch ($ERR) { }' --json 2>/dev/null | jq -r '.[] | "\(.file):\(.range.start.line): empty catch"' | head -10

# 7. Console.log in production code
rg -n 'console\.(log|debug)' --type ts --type tsx -g '!*.test.*' -g '!*.spec.*' 2>/dev/null | head -15
```

## Severity Classification

**Critical** (fix now):
- Empty catch blocks
- Hardcoded secrets or credentials
- Unused exports in public API
- Console.log in production paths

**Moderate** (fix this sprint):
- TODO/FIXME older than 30 days
- Functions > 100 lines
- Magic numbers in business logic
- Duplicated error handling

**Low** (track for later):
- HACK comments
- Minor code duplication
- Long parameter lists

## Output Format

```markdown
## Tech Debt Report - [date]

### Critical (fix now)
| Location | Issue | Suggested Fix |
|----------|-------|---------------|
| src/api.ts:42 | Empty catch | Add error logging |

### Moderate (fix this sprint)
| Location | Issue | Suggested Fix |
|----------|-------|---------------|
| src/utils.ts:15 | TODO from 60 days ago | Complete or delete |

### Low (track)
- 3x duplicated fetch wrapper pattern (consider shared util)
```

## Quick Mode

For fast feedback, run just these:

```bash
# Fast techdebt scan
rg -c "TODO|FIXME|console\.log" --type ts 2>/dev/null | sort -t: -k2 -nr | head -10
```

## Integration

After running, offer to:
1. Create GitHub issues for critical items
2. Add to existing tech debt tracking
3. Generate refactor plan for moderate items
