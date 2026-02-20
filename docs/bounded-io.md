# Bounded I/O Protocol

Purpose: avoid hangs from unbounded shell output.

## Rules

1. Check size first.
   - `wc -l <file>`
   - `du -h <path>`
2. Read in windows, not full dumps.
   - `safe-read.sh <file> 1 120`
   - `sed -n '1,120p' <file>`
3. Cap logs and API output.
   - `tail -n 200 <log>`
   - `gh run list --limit 5`
4. Cap runtime.
   - `timeout 15s <cmd>` or `gtimeout 15s <cmd>`
5. Abort quickly.
   - No useful signal after 20s: stop, narrow, rerun.

## Safe Patterns

```bash
wc -l path/to/file
rg -n "target" path/to/file
safe-read.sh path/to/file 1 120

gh run list --limit 5
gh run view <run-id> --log-failed | tail -n 200
```

## Anti-Patterns

- `cat` on unknown-size files
- Raw unbounded `--paginate` output
- Parallel unknown-size output commands
