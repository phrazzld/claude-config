---
description: Bundled quality gate (tests + lint + typecheck)
---

# CHECK-QUALITY

Run all quality gates and report issues.

## What This Does

1. **Run tests** — `pnpm test` or equivalent
2. **Run linter** — `pnpm lint`
3. **Run typecheck** — `pnpm typecheck` or `tsc --noEmit`
4. **Report** — Summarize failures with suggested fixes

## Execution

```bash
# Detect package manager and scripts
if [ -f pnpm-lock.yaml ]; then
  PM="pnpm"
elif [ -f yarn.lock ]; then
  PM="yarn"
else
  PM="npm"
fi

# Run quality gates
echo "=== Tests ==="
$PM test 2>&1 | tail -20

echo "=== Lint ==="
$PM lint 2>&1 | tail -20

echo "=== Typecheck ==="
$PM typecheck 2>&1 || tsc --noEmit 2>&1 | tail -20
```

## Output

For each gate:
- **PASS** — Gate passed
- **FAIL** — Errors with suggested fixes

If all pass: "All quality gates passed."
