# Prompt & Context Engineering

Modern AI engineering is **context engineering** - optimizing the entire configuration available to LLMs, not just prompt wording.

## Paradigm Shift: Context > Prompts

**Old thinking**: Find perfect prompt wording
**New thinking**: Optimize entire context configuration

## Prompt Caching (60-90% Cost Reduction)

**How it works**: Providers cache repeated context (system prompts, docs, code) for 5-15 minutes

**Implementation**:
```typescript
// Put static content first (cacheable)
const messages = [
  { role: 'system', content: longSystemPrompt }, // CACHED
  { role: 'system', content: codebaseContext },  // CACHED
  { role: 'user', content: userQuery }           // NOT CACHED
];
```

**Best practices**:
- Cache long static content (>1024 tokens)
- Place cacheable content early in prompt
- System instructions, reference docs, codebases are ideal
- Cache reduces cost by 90% and latency by 50-80%

## Structured Outputs (Eliminate JSON Parsing)

**Old way**:
```typescript
const prompt = "Return JSON with fields: name, age, email";
const response = await llm.complete(prompt);
const data = JSON.parse(response); // Can fail!
```

**New way** (Native JSON Schema):
```typescript
const response = await llm.complete(prompt, {
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "user_data",
      schema: {
        type: "object",
        properties: {
          name: { type: "string" },
          age: { type: "number" },
          email: { type: "string" }
        },
        required: ["name", "age", "email"]
      }
    }
  }
});
// Guaranteed valid JSON matching schema
```

**Benefits**: 100% schema compliance, no parsing errors, no retry logic needed

## System Prompts (Immutable Rules)

Use dedicated `system:` role for critical rules, constraints, policies:

```typescript
{
  role: 'system',
  content: `You are a code review assistant.

  Rules:
  - Never suggest changes without explanation
  - Focus on logic errors and security issues
  - Ignore style unless critical
  - Always provide examples for suggestions`
}
```

**Why**: System prompts can't be overridden by user messages

## Few-Shot vs Zero-Shot

**2025 Reality**: Modern models are highly capable zero-shot

**When to use few-shot**:
- Specific formatting requirements
- Tone/style matching
- Complex domain-specific tasks
- Edge cases and nuanced behaviors

**Optimal**: 1-3 examples (diminishing returns after)

**Meta few-shot** (advanced):
```typescript
const examples = [
  { input: "...", output: "...", note: "Perfect example" },
  { input: "...", output: "...", note: "❌ Common mistake: too verbose" }
];
```

## Chain-of-Thought (CoT)

**For regular models** (Claude, GPT, Gemini):
```
✅ "Think step by step"
✅ "Explain your reasoning"
✅ Numbered reasoning steps
```

**For reasoning models** (o1, o3, o4-mini):
```
❌ DON'T add "think step by step"
❌ DON'T add manual CoT prompts
✅ Keep prompts simple and direct
```

**Why**: Reasoning models handle CoT internally; adding it degrades performance

## Model-Specific Prompting

**Claude example** (likes XML structure):
```xml
<context>
  Background information here
</context>

<task>
  What you want done
</task>

<constraints>
  - Constraint 1
  - Constraint 2
</constraints>
```

**GPT example** (likes clear sections):
```
# Context
Background information

# Task
What you want done

# Requirements
1. Requirement 1
2. Requirement 2
```

## Prompt Engineering Checklist

- [ ] System prompt for immutable rules
- [ ] Static context placed early (for caching)
- [ ] Clear task description with success criteria
- [ ] Examples included (1-3 if needed for style/format)
- [ ] Output format specified (structured output when possible)
- [ ] Token limit set (prevent rambling)
- [ ] Temperature appropriate (0 for factual, 0.7-1.0 for creative)
