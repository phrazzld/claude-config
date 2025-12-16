# Promptfoo Complete Guide

## Installation

```bash
# No global install needed - use npx
npx promptfoo@latest init

# Or install globally
npm install -g promptfoo

# Or add to project
pnpm add -D promptfoo
```

## Configuration Deep Dive

### Prompts

```yaml
# Inline prompts
prompts:
  - "Answer: {{question}}"
  - "You are a helpful assistant. Answer: {{question}}"

# File prompts
prompts:
  - file://prompts/system.txt
  - file://prompts/v2.txt

# Function prompts (dynamic)
prompts:
  - file://prompts/dynamic.js  # Export function(vars) { return prompt }
```

### Providers

```yaml
providers:
  # OpenAI
  - openai:gpt-4o-mini
  - openai:gpt-4o
  - id: openai:gpt-4o
    config:
      temperature: 0.7
      max_tokens: 500

  # Anthropic
  - anthropic:claude-3-5-sonnet-latest
  - anthropic:claude-3-5-haiku-latest

  # OpenRouter (recommended for multi-model)
  - openrouter:anthropic/claude-3-5-sonnet
  - openrouter:openai/gpt-4o
  - openrouter:google/gemini-pro-1.5

  # Custom endpoint
  - id: custom-model
    config:
      url: http://localhost:8000/v1/chat/completions
      headers:
        Authorization: "Bearer ${API_KEY}"
```

### Test Structure

```yaml
tests:
  # Basic test
  - vars:
      question: "What is 2+2?"
    assert:
      - type: equals
        value: "4"

  # Named test
  - description: "Math question"
    vars:
      question: "What is 2+2?"
    assert:
      - type: contains
        value: "4"

  # Multiple assertions
  - vars:
      question: "Explain Python"
    assert:
      - type: contains
        value: "programming"
      - type: not-contains
        value: "snake"
      - type: llm-rubric
        value: "Technical explanation"
      - type: cost
        threshold: 0.01

  # Load from file
  - file://tests/golden.yaml
```

### Variables from CSV/JSON

```yaml
tests:
  - file://tests/cases.csv
  # CSV format:
  # question,expected
  # "What is 2+2?","4"
  # "What is 3+3?","6"

  - file://tests/cases.json
  # JSON format:
  # [{"vars": {"question": "..."}, "assert": [...]}]
```

## Assertion Types Reference

### String Assertions

| Type | Description | Example |
|------|-------------|---------|
| `contains` | Output contains string | `value: "Paris"` |
| `not-contains` | Output doesn't contain | `value: "error"` |
| `equals` | Exact match | `value: "yes"` |
| `starts-with` | Prefix match | `value: "Hello"` |
| `ends-with` | Suffix match | `value: "."` |
| `regex` | Regular expression | `value: "\\d{4}"` |
| `icontains` | Case-insensitive contains | `value: "paris"` |

### JSON Assertions

| Type | Description | Example |
|------|-------------|---------|
| `is-json` | Valid JSON | (no value needed) |
| `is-valid-json-schema` | Matches schema | `value: {type: object}` |
| `json-contains` | JSON has key/value | `value: {key: "value"}` |

### Semantic Assertions

| Type | Description | Example |
|------|-------------|---------|
| `similar` | Embedding similarity | `value: "expected", threshold: 0.8` |
| `llm-rubric` | LLM-as-judge | `value: "criteria to evaluate"` |
| `factuality` | Fact-check against ref | `value: "reference facts"` |
| `model-graded-closedqa` | Closed QA eval | (built-in rubric) |

### Performance Assertions

| Type | Description | Example |
|------|-------------|---------|
| `cost` | USD cost limit | `threshold: 0.05` |
| `latency` | Response time (ms) | `threshold: 2000` |

### Safety Assertions

| Type | Description | Example |
|------|-------------|---------|
| `moderation` | OpenAI moderation | `value: "violence"` |
| `not-similar` | Reject similar outputs | `value: "harmful text"` |

### Custom Assertions

```yaml
assert:
  # JavaScript assertion
  - type: javascript
    value: |
      return output.length < 500 && output.includes('Python');

  # Python assertion
  - type: python
    value: |
      return len(output) < 500 and 'Python' in output
```

## CLI Commands

```bash
# Initialize config
npx promptfoo@latest init

# Run evaluation
npx promptfoo@latest eval
npx promptfoo@latest eval -c custom-config.yaml
npx promptfoo@latest eval -o results.json

# View results
npx promptfoo@latest view
npx promptfoo@latest view -y results.json

# Compare runs
npx promptfoo@latest diff results1.json results2.json

# Cache management
npx promptfoo@latest cache clear

# Red team
npx promptfoo@latest redteam init
npx promptfoo@latest redteam run
npx promptfoo@latest redteam report --output report.html
```

## Environment Variables

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...

# Promptfoo config
PROMPTFOO_CACHE_TYPE=disk  # or redis, memory
PROMPTFOO_CACHE_PATH=~/.promptfoo/cache
PROMPTFOO_DISABLE_TELEMETRY=1
```

## Advanced Patterns

### Prompt Versioning

```yaml
# Compare v1 vs v2
prompts:
  - id: v1
    raw: file://prompts/v1.txt
  - id: v2
    raw: file://prompts/v2.txt

# Label in output
defaultTest:
  options:
    prefix: "{{prompt.id}}"
```

### Provider Fallbacks

```yaml
providers:
  - id: primary
    config:
      url: https://api.openai.com/v1/chat/completions
    fallback:
      - id: backup
        config:
          url: https://openrouter.ai/api/v1/chat/completions
```

### Caching for Cost Savings

```yaml
evaluateOptions:
  cache: true
  cacheType: disk  # Persist across runs
```

### Parallel Execution

```yaml
evaluateOptions:
  maxConcurrency: 10  # Run 10 tests in parallel
```

### Transform Output

```yaml
# Pre-process output before assertions
defaultTest:
  transform: |
    output.toLowerCase().trim()
```

## Debugging

```bash
# Verbose output
npx promptfoo@latest eval --verbose

# Debug specific test
npx promptfoo@latest eval --filter "test description"

# Show prompts being sent
npx promptfoo@latest eval --debug

# Output raw responses
npx promptfoo@latest eval -o results.json --include-raw
```
