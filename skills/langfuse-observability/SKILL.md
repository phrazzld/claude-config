---
name: langfuse-observability
description: |
  Query Langfuse traces, prompts, and LLM metrics. Use when:
  - Analyzing LLM generation traces (errors, latency, tokens)
  - Reviewing prompt performance and versions
  - Debugging failed generations
  - Comparing model outputs across runs
  Keywords: langfuse, traces, observability, LLM metrics, prompt management, generations
---

# Langfuse Observability

Query traces, prompts, and metrics from Langfuse. Requires env vars:
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_HOST` (e.g., `https://us.cloud.langfuse.com`)

## Quick Start

All commands run from the skill directory:
```bash
cd ~/.claude/skills/langfuse-observability
```

### List Recent Traces
```bash
# Last 10 traces
npx tsx scripts/fetch-traces.ts --limit 10

# Filter by name pattern
npx tsx scripts/fetch-traces.ts --name "quiz-generation" --limit 5

# Filter by user
npx tsx scripts/fetch-traces.ts --user-id "user_abc123" --limit 10
```

### Get Single Trace Details
```bash
# Full trace with spans and generations
npx tsx scripts/fetch-trace.ts <trace-id>
```

### Get Prompt
```bash
# Fetch specific prompt
npx tsx scripts/list-prompts.ts --name scry-intent-extraction

# With label
npx tsx scripts/list-prompts.ts --name scry-intent-extraction --label production
```

### Get Metrics Summary
```bash
# Summary for recent traces
npx tsx scripts/get-metrics.ts --limit 50

# Filter by trace name
npx tsx scripts/get-metrics.ts --name "quiz-generation" --limit 100
```

## Output Formats

All scripts output JSON to stdout for easy parsing.

### Trace List Output
```json
[
  {
    "id": "trace-abc123",
    "name": "quiz-generation",
    "userId": "user_xyz",
    "input": {"prompt": "..."},
    "output": {"concepts": [...]},
    "latencyMs": 3200,
    "createdAt": "2025-12-09T..."
  }
]
```

### Single Trace Output
Includes full nested structure: trace → observations (spans + generations) with token usage.

### Metrics Output
```json
{
  "totalTraces": 50,
  "successCount": 48,
  "errorCount": 2,
  "avgLatencyMs": 2850,
  "totalTokens": 125000,
  "byName": {"quiz-generation": 30, "phrasing-generation": 20}
}
```

## Common Workflows

### Debug Failed Generation
```bash
cd ~/.claude/skills/langfuse-observability

# 1. Find recent traces
npx tsx scripts/fetch-traces.ts --limit 10

# 2. Get details of specific trace
npx tsx scripts/fetch-trace.ts <trace-id>
```

### Monitor Token Usage
```bash
# Get metrics for cost analysis
npx tsx scripts/get-metrics.ts --limit 100
```

### Check Prompt Configuration
```bash
npx tsx scripts/list-prompts.ts --name scry-concept-synthesis --label production
```
