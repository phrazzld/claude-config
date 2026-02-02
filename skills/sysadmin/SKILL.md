# sysadmin

System health diagnostics and maintenance for macOS.

user-invocable: true

---

## Purpose

Quick system health check and maintenance tasks. Identifies resource hogs, disk usage, and potential issues.

**Critical constraint:** NEVER kill or terminate Claude Code processes. Warn only.

## Execution

Run these diagnostics in sequence:

### 1. System Overview
```bash
system_profiler SPHardwareDataType | grep -E "(Model|Chip|Memory|Cores)"
```

### 2. Resource Usage
```bash
# Top CPU consumers (macOS BSD ps)
ps aux -r | head -15

# Top memory consumers
ps aux -m | head -15
```

### 3. Claude Code Check
```bash
# Find Claude-related processes
ps aux | grep -i "claude\|anthropic" | grep -v grep
```

**If Claude Code appears in top resource consumers:**
- Report memory/CPU usage prominently
- Suggest: "Consider restarting Claude Code session if memory exceeds 4GB"
- Suggest: "Long sessions accumulate context - `/clear` can help"
- **DO NOT suggest killing processes**

### 4. Disk Usage
```bash
# Overall disk usage
df -h / | tail -1

# Large directories in home
du -sh ~/Library/Caches ~/Library/Application\ Support ~/.Trash 2>/dev/null | sort -hr

# Docker if present
docker system df 2>/dev/null || echo "Docker not running"
```

### 5. Memory Pressure
```bash
# Memory stats
vm_stat | head -10

# Swap usage
sysctl vm.swapusage
```

### 6. Network Connections
```bash
# Active connections count by state
netstat -an | grep -E "ESTABLISHED|LISTEN" | wc -l
```

### 7. Homebrew Health (if time permits)
```bash
brew doctor 2>&1 | head -20
```

## Output Format

```
## System Health Report

**Machine:** [model] | **Chip:** [chip] | **RAM:** [total]

### Resource Usage
| Process | CPU% | MEM% | Notes |
|---------|------|------|-------|
...

### Claude Code Status
[Warning block if high usage, otherwise "Normal"]

### Disk
- Root: X% used (Y available)
- Caches: X GB
- Docker: X GB reclaimable

### Recommendations
1. [Actionable items only]
```

## Maintenance Actions (on request)

Only run these if user explicitly asks:

```bash
# Clear caches (safe)
rm -rf ~/Library/Caches/* 2>/dev/null

# Empty trash
rm -rf ~/.Trash/* 2>/dev/null

# Docker cleanup
docker system prune -f

# Homebrew cleanup
brew cleanup --prune=7
```

Never run maintenance automatically. Always confirm first.
