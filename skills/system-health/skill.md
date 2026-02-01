# System Health Check

Quick system health diagnosis with remediation suggestions.

## Invocation
- `/health` - Full system health check
- User asks about disk space, memory, swap, or system performance

## Checks Performed

### 1. Disk Space
```bash
df -h /System/Volumes/Data | tail -1 | awk '{print "Disk: " $3 " used, " $4 " free (" $5 ")"}'
```
- **Green:** < 80% capacity
- **Yellow:** 80-90% capacity
- **Red:** > 90% capacity

### 2. Swap Usage
```bash
sysctl vm.swapusage
```
- **Green:** < 5GB used
- **Yellow:** 5-15GB used
- **Red:** > 15GB used

### 3. Stuck Processes
```bash
ps aux | awk '$3 > 50 {print}' | head -10
```
Look for processes with high CPU (>50%) for extended periods.

### 4. Homebrew Health
```bash
brew doctor 2>&1 | head -10
```

### 5. Docker (if running)
```bash
docker system df 2>/dev/null
```

## Remediation Commands

### Quick Cache Clean
```bash
brew cleanup --prune=all && go clean -cache && pnpm store prune && pip cache purge
```

### Kill Stuck Processes
```bash
pkill -f "convex typecheck"
pkill -f "lefthook run"
```

### Aggressive Cleanup (manual trash empty required)
```bash
/usr/bin/trash ~/Library/Caches/ms-playwright
/usr/bin/trash ~/Library/Developer/Xcode/DerivedData
xcrun simctl delete unavailable
```

## Thresholds

| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| Disk | < 80% | 80-90% | > 90% |
| Swap | < 5GB | 5-15GB | > 15GB |
| CPU stuck | None | 1-2 procs | 3+ procs |

## Output Format

Present a summary table:
```
=== SYSTEM HEALTH ===
💾 Disk: XXGi free (YY%) [STATUS]
🔄 Swap: X.XGB / Y.YGB [STATUS]
⚡ CPU: N stuck processes [STATUS]
🍺 Homebrew: [STATUS]

Recommendations:
- [If any issues, list specific commands]
```
