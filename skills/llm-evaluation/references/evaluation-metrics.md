# Evaluation Metrics Deep Dive

## Categories of Evaluation

### 1. Functional Evaluation

**Purpose**: Does the output work as expected?

| Metric | Use Case | Example |
|--------|----------|---------|
| Exact Match | Classification, yes/no | `equals: "yes"` |
| Contains | Key information present | `contains: "Paris"` |
| JSON Valid | Structured output | `is-json` |
| Schema Match | API responses | `is-valid-json-schema` |
| Regex | Format validation | `regex: "\\d{4}-\\d{2}-\\d{2}"` |

**When to use**: Unit testing prompts, validation checks, format enforcement.

### 2. Semantic Evaluation

**Purpose**: Is the output meaningful and correct?

| Metric | Use Case | Example |
|--------|----------|---------|
| Similarity | Semantic match | `similar: "expected", threshold: 0.8` |
| LLM-as-Judge | Quality assessment | `llm-rubric: "clear and helpful"` |
| Factuality | Fact checking | `factuality: "reference facts"` |
| Relevance | RAG retrieval | `llm-rubric: "relevant to query"` |

**When to use**: Quality assessment, content validation, RAG evaluation.

### 3. Performance Evaluation

**Purpose**: Is the system efficient?

| Metric | Use Case | Example |
|--------|----------|---------|
| Latency | Response time | `latency: 2000` (ms) |
| Cost | Token budget | `cost: 0.05` (USD) |
| Token Count | Output length | Custom assertion |

**When to use**: Production monitoring, budget enforcement, SLA compliance.

### 4. Safety Evaluation

**Purpose**: Is the output safe and appropriate?

| Metric | Use Case | Example |
|--------|----------|---------|
| Moderation | Content safety | `moderation: "violence"` |
| PII Detection | Privacy | `not-contains: "{{email}}"` |
| Jailbreak | Security | Red team plugins |
| Injection | Security | Red team plugins |

**When to use**: Production apps, user-facing systems, compliance.

## LLM-as-Judge Patterns

### Basic Rubric

```yaml
assert:
  - type: llm-rubric
    value: |
      Rate the response on:
      1. Accuracy (factually correct)
      2. Clarity (easy to understand)
      3. Completeness (covers all aspects)

      Fail if any criterion scores below 3/5.
```

### Specific Criteria

```yaml
assert:
  - type: llm-rubric
    value: "Response is concise (under 50 words)"
  - type: llm-rubric
    value: "Response includes a code example"
  - type: llm-rubric
    value: "Response cites sources or references"
```

### Comparative Evaluation

```yaml
# Compare two outputs
assert:
  - type: llm-rubric
    value: |
      Compare these two responses and determine which is better:
      Response A: {{output_a}}
      Response B: {{output_b}}

      Return "A" or "B" based on clarity and accuracy.
```

### Domain-Specific

```yaml
# Medical
assert:
  - type: llm-rubric
    value: "Response does not provide medical diagnoses or treatment advice"

# Legal
assert:
  - type: llm-rubric
    value: "Response includes appropriate legal disclaimers"

# Financial
assert:
  - type: llm-rubric
    value: "Response does not promise specific investment returns"
```

## RAG Evaluation Metrics

### Retrieval Quality

```yaml
tests:
  - vars:
      query: "Python list comprehension"
      retrieved_docs: ["doc1", "doc2"]
    assert:
      - type: llm-rubric
        value: "Retrieved documents are relevant to the query"
```

### Answer Quality

```yaml
assert:
  # Faithfulness: Answer is supported by context
  - type: llm-rubric
    value: "Answer is directly supported by the provided context"

  # Answer relevancy: Answer addresses the question
  - type: llm-rubric
    value: "Answer directly addresses the user's question"

  # Context utilization: Uses provided context
  - type: llm-rubric
    value: "Answer incorporates information from the context"
```

### Hallucination Detection

```yaml
assert:
  - type: factuality
    value: "{{context}}"  # Reference for fact checking

  - type: not-contains
    value: "I think"  # Uncertainty hedging

  - type: llm-rubric
    value: "No information is added beyond what's in the context"
```

## Custom Metrics

### JavaScript

```yaml
assert:
  - type: javascript
    value: |
      // Check output length
      const wordCount = output.split(' ').length;
      return wordCount >= 50 && wordCount <= 200;
```

### Python

```yaml
assert:
  - type: python
    value: |
      import re
      # Check for proper sentence structure
      sentences = re.split(r'[.!?]', output)
      return len(sentences) >= 3
```

### External API

```yaml
assert:
  - type: webhook
    value: https://my-validator.com/check
    # POST request with {output, context, vars}
```

## Scoring Patterns

### Pass/Fail (Default)

```yaml
assert:
  - type: contains
    value: "Paris"
  # Pass if contains, fail otherwise
```

### Threshold-Based

```yaml
assert:
  - type: similar
    value: "The capital of France is Paris"
    threshold: 0.8  # 80% similarity required
```

### Weighted Scoring

```yaml
assert:
  - type: llm-rubric
    value: "Rate accuracy 1-10"
    weight: 2  # Double importance

  - type: llm-rubric
    value: "Rate clarity 1-10"
    weight: 1
```

### Multi-Dimensional

```yaml
assert:
  - type: llm-rubric
    value: |
      Score on multiple dimensions:
      - Accuracy: 1-5
      - Completeness: 1-5
      - Clarity: 1-5

      Return JSON: {"accuracy": X, "completeness": Y, "clarity": Z}
```

## Benchmark Integration

### Standard Benchmarks

```yaml
# MMLU-style
tests:
  - file://benchmarks/mmlu-subset.yaml

# HumanEval-style
tests:
  - file://benchmarks/coding-problems.yaml
```

### Custom Benchmarks

```yaml
# Create domain-specific benchmark
tests:
  # Easy
  - vars:
      difficulty: easy
      question: "What is 2+2?"
    assert:
      - type: contains
        value: "4"

  # Medium
  - vars:
      difficulty: medium
      question: "Explain recursion"
    assert:
      - type: llm-rubric
        value: "Explains base case and recursive case"

  # Hard
  - vars:
      difficulty: hard
      question: "Implement a balanced BST"
    assert:
      - type: llm-rubric
        value: "Correct implementation with O(log n) operations"
```

## Metrics Dashboard

### What to Track

1. **Pass Rate**: % of tests passing over time
2. **Regression Rate**: % of previously passing tests now failing
3. **Cost per Test**: Average token cost
4. **Latency Distribution**: p50, p95, p99
5. **Failure Categories**: What types of assertions fail most

### Alerting Thresholds

```yaml
# Suggested alert thresholds
alerts:
  pass_rate_drop: 5%  # Alert if pass rate drops 5%
  cost_spike: 2x      # Alert if cost doubles
  latency_p95: 5000   # Alert if p95 > 5s
  security_failure: any  # Alert on any security test failure
```
