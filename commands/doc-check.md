---
description: Audit codebase for stale or missing documentation
---

# DOC-CHECK

Audit documentation freshness across the codebase. Find stale READMEs and directories missing documentation.

## Usage

- `/doc-check` - Audit entire codebase from current directory
- `/doc-check src/` - Audit specific directory

## Audit Process

### 1. Find All Documentation

```bash
# Find all README and DOCS files
find . -name "README.md" -o -name "DOCS.md" -o -name "README.rst" | grep -v node_modules | grep -v .git
```

### 2. Check Staleness

For each documentation file found:

```bash
# Get doc modification time
stat -f "%m %N" [doc_path]  # macOS
# or
stat -c "%Y %n" [doc_path]  # Linux

# Get newest file in same directory (excluding the doc itself)
find [dir] -maxdepth 1 -type f ! -name "README*" ! -name "DOCS*" -exec stat -f "%m %N" {} \; | sort -rn | head -1
```

Compare timestamps. If any source file is newer than the doc, mark as stale.

### 3. Find Missing Documentation

```bash
# Find directories with code but no README
find . -type d ! -path "*/node_modules/*" ! -path "*/.git/*" | while read dir; do
  if [ -n "$(find "$dir" -maxdepth 1 -name "*.ts" -o -name "*.js" -o -name "*.py" 2>/dev/null)" ]; then
    if [ ! -f "$dir/README.md" ] && [ ! -f "$dir/DOCS.md" ]; then
      echo "$dir"
    fi
  fi
done
```

### 4. Generate Report

Output a structured report:

```markdown
## Documentation Staleness Report

**Scanned**: [timestamp]
**Path**: [scanned path]

### Critical (30+ days stale)

| Directory | Doc | Doc Age | Newest File | File Age |
|-----------|-----|---------|-------------|----------|
| src/auth | README.md | 45d | login.ts | 2d |

### Warning (7-30 days stale)

| Directory | Doc | Doc Age | Newest File | File Age |
|-----------|-----|---------|-------------|----------|
| src/api | README.md | 12d | routes.ts | 1d |

### Healthy (up to date)

- src/components/README.md (2d old, newest file 3d old)
- docs/ARCHITECTURE.md (5d old, newest file 5d old)

### Missing Documentation

Directories with code but no README:

| Directory | Files | Suggested Action |
|-----------|-------|------------------|
| src/utils | 8 | Create README explaining utilities |
| src/hooks | 3 | Create README for React hooks |

### Summary

- Total docs found: [N]
- Critical (30+ days stale): [N]
- Warning (7-30 days stale): [N]
- Healthy: [N]
- Missing docs: [N] directories
```

## Thresholds

- **Critical**: Doc is 30+ days older than newest source file
- **Warning**: Doc is 7-30 days older than newest source file
- **Healthy**: Doc is within 7 days of newest source file

## After Audit

If stale docs found, offer to update them:

```
Found [N] stale documentation files.

Options:
1. Update most critical first (src/auth/README.md)
2. Update all stale docs
3. Show detailed report only

Which would you like?
```

When updating docs, analyze the changed files to understand what documentation needs updating, then make targeted edits to reflect current state.
