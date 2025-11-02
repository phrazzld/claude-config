---
name: ai-llm-development
description: Apply modern AI/LLM development best practices: staying current on models, prompt/context engineering, architecture patterns, stack decisions, evaluation, and production deployment. Use when building AI features, selecting models, writing prompts, reviewing LLM code, or discussing AI architecture.
---

# AI/LLM Development

## Core Principle

**The landscape changes monthly. Learn HOW to find current solutions, not memorize specific models.**

AI development requires balancing:
- **Currency** - Models deprecate in 6-12 months; stay current through tools, not memory
- **Simplicity** - Start with single LLM calls before building multi-agent systems
- **Empiricism** - Test with YOUR data; leaderboards guide, tests prove
- **Cost Awareness** - $100/month difference between naive and optimized implementations

Modern AI engineering is **context engineering** - optimizing the entire configuration available to LLMs, not just prompt wording.

---

## 1. Staying Current on Models (Critical Skill)

### The Failure Mode

**Problem**: Training cutoffs cause agents to recommend deprecated models (GPT-4, Gemini 2.0) months after they're obsolete.

**Solution**: Learn how to find current best models, don't memorize them.

### How to Find Current Models

**Primary Leaderboards** (bookmark these):
- **LMSYS Chatbot Arena** (lmarena.ai) - Human preference rankings, updated continuously
- **Artificial Analysis** (artificialanalysis.ai) - Intelligence, speed, price tracking for 100+ models
- **LiveBench** (livebench.ai) - Contamination-free monthly benchmarks
- **Hugging Face Open LLM Leaderboard** - Best open-source models

**Search Strategy**:
```
✅ GOOD: "AI model leaderboard 2025 coding"
✅ GOOD: "SOTA reasoning models November 2025"
❌ BAD:  "best AI models" (no date context)
❌ BAD:  "GPT-4 vs Claude" (likely outdated)
```

**Always**:
- Include current year in searches
- Check article/benchmark publication dates
- Verify model release dates
- Cross-reference 2-3 sources

### Model Selection Framework

```
1. Define task → Identify relevant benchmark
   (Coding: SWE-bench | Reasoning: GPQA | General: Arena Elo)

2. Check leaderboards → Find top 3-5 models

3. Consider constraints:
   - Budget: tokens/$ ratio
   - Speed: latency requirements
   - Context: window size needed

4. Test empirically → Use OpenRouter to test multiple models

5. Monitor & iterate → Models improve monthly
```

### Red Flags for Outdated Info

- Articles >3 months old without update dates
- Generic claims: "GPT-4 is best for X"
- No model version numbers (dates/build codes)
- Comparisons missing recent releases
- Benchmark scores without test dates

### Use OpenRouter for Flexibility

**Why**: Single API for 400+ models across all providers
- Easy A/B testing between models
- Automatic fallbacks if model unavailable
- Unified cost tracking
- No vendor lock-in

```typescript
// Test multiple models easily
const models = [
  "anthropic/claude-sonnet-4.5",
  "openai/gpt-5",
  "google/gemini-2.5-pro"
];

for (const model of models) {
  const response = await openrouter.chat({
    model,
    messages: yourTestCases
  });
  // Evaluate quality, cost, speed
}
```

**Key Features**:
- `openrouter/auto` - Automatic best model selection
- Fallback chains for reliability
- Real-time pricing data
- `/models` API endpoint for current model list

---

## 2. Prompt & Context Engineering

### Paradigm Shift: Context > Prompts

**Old thinking**: Find perfect prompt wording
**New thinking**: Optimize entire context configuration

### Prompt Caching (60-90% Cost Reduction)

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

### Structured Outputs (Eliminate JSON Parsing)

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

### System Prompts (Immutable Rules)

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

**Why**: System prompts can't be overridden by user messages (unlike putting rules in user context)

### Few-Shot vs Zero-Shot

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

### Chain-of-Thought (CoT)

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

### Model-Specific Patterns

Different models have different strengths:

| Model Family | Best For | Prompting Style |
|-------------|----------|-----------------|
| **Claude** | Deep reasoning, coding | Rich context + XML tags + critique. Tends toward verbose code. |
| **GPT-4/5** | Structured output, consistency | Clear sections + few-shot examples. Concise and reliable. |
| **Gemini** | Multimodal, research | Research parameters + citations. Add "Be concise" to shorten. |
| **Reasoning (o-series)** | Complex logic, math | Simple, direct instructions. No manual CoT. |

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

---

## 3. Opinionated Stack Defaults

### For TypeScript/Next.js Projects

**SDK**: Vercel AI SDK
- Streaming by default
- React hooks integration
- OpenAI-compatible (works with any provider)
- Built-in prompt caching support

**Model Provider**: OpenRouter
- Single API, 400+ models
- Test multiple providers easily
- No vendor lock-in
- Automatic fallbacks

**Vector Storage**: Postgres with pgvector
- Default choice for 95% of use cases
- Use Neon (serverless) or Supabase (full backend)
- Handles millions of vectors efficiently
- ACID transactions + vectors together
- $20-50/month typical cost

**Alternative vector storage**: Convex
- If already using for full-stack app
- Built-in vector indexes
- Real-time reactivity
- <1M vectors sweet spot

**Observability**: Langfuse (self-hosted) or simple logging
- Open-source, comprehensive
- Native Vercel AI SDK support
- OpenTelemetry-based

### When to Deviate

**Use dedicated vector DB** ONLY if:
- >50M vectors regularly queried
- Need <10ms p99 latency at scale
- 80%+ of workload is vector search
- Budget allows $500-5000+/month

**Then consider**: Qdrant (performance), Weaviate (hybrid search), Milvus (enterprise scale)

### Anti-Recommendations

❌ **LangChain** - Over-engineered, steep learning curve, bloated for most use cases
❌ **Helicone** - Poor reliability experiences reported
❌ **Pinecone by default** - Expensive ($70-200+/month) when Postgres handles most needs
❌ **Building multi-agent systems first** - Start simple, add complexity only when needed

---

## 4. Architecture Patterns

### Complexity Ladder (Start at Bottom)

```
1. Single LLM Call
   ↓ (only if single call insufficient)
2. Sequential LLM Calls (workflow)
   ↓ (only if static workflow insufficient)
3. LLM with Tools (function calling)
   ↓ (only if pre-defined tools insufficient)
4. Agentic System (LLM controls flow)
   ↓ (only if single agent insufficient)
5. Multi-Agent System

⚠️ 80% of use cases stop at level 1-2
```

**Rule**: Add complexity only when simpler approach fails

### RAG Pattern (Retrieval-Augmented Generation)

**Modern RAG Pipeline**:
```
1. Index: Store documents in Postgres with pgvector
2. Query: Convert user question to embedding
3. Search: Hybrid search (vector + keyword/BM25)
4. Re-rank: Cross-encoder for precision (optional but recommended)
5. Generate: LLM with retrieved context
```

**Postgres pgvector implementation**:
```sql
-- Create table with vector column
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536)
);

-- Create vector index
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Hybrid search
SELECT id, content,
  (embedding <=> query_embedding) as vector_distance,
  ts_rank(to_tsvector(content), query) as keyword_rank
FROM documents
WHERE to_tsvector(content) @@ query
ORDER BY (vector_distance * 0.7 + (1 - keyword_rank) * 0.3)
LIMIT 10;
```

**Key insight**: Hybrid search (vector + keyword) outperforms pure vector similarity by 15-25%

### Tool Use / Function Calling

**Pattern**: LLM selects and calls functions dynamically

```typescript
const tools = [
  {
    name: "search_docs",
    description: "Search documentation for information",
    parameters: {
      query: { type: "string", description: "Search query" }
    }
  },
  {
    name: "create_ticket",
    description: "Create support ticket",
    parameters: {
      title: { type: "string" },
      priority: { type: "string", enum: ["low", "medium", "high"] }
    }
  }
];

const response = await llm.chat({
  messages,
  tools,
  tool_choice: "auto" // Let model decide
});

if (response.tool_calls) {
  for (const call of response.tool_calls) {
    const result = await executeTool(call.name, call.arguments);
    // Continue conversation with result
  }
}
```

**Best practices**:
- Clear, unambiguous tool descriptions
- Strict parameter validation
- Parallel tool calls when possible (3.7x speedup)
- Timeout and error handling for each tool

### Caching Strategy (Multi-Layer)

1. **Prompt caching**: System instructions, reference docs (60-90% cost reduction)
2. **Response caching**: Repeated/similar queries → stored answers (latency + cost)
3. **Embedding caching**: Cache computed embeddings for reuse (RAG workflows)

```typescript
// Response caching example
const cacheKey = hashPrompt(messages);
const cached = await cache.get(cacheKey);
if (cached && isFresh(cached)) return cached;

const response = await llm.complete(messages);
await cache.set(cacheKey, response, ttl: '15m');
return response;
```

---

## 5. Evaluation & Testing

### LLM-as-Judge (Standard Approach)

**Why**: Scalable evaluation of subjective qualities (85-90% agreement with humans)

**Implementation**:
```typescript
const judgePrompt = `
Evaluate the response on these criteria:
1. Accuracy - Is information factually correct?
2. Relevance - Does it answer the question?
3. Completeness - Are all aspects addressed?
4. Clarity - Is it easy to understand?

Rate each 1-10 and provide brief justification.

Question: ${question}
Response: ${response}
`;

const judgment = await llm.complete(judgePrompt, {
  response_format: { type: "json_schema", schema: ratingSchema }
});
```

**Best practices**:
- Clear rubrics for each criterion
- Use structured outputs for consistent scoring
- Multiple judge models for consensus (when stakes high)
- Calibrate against human baselines periodically

### What to Measure

**Quality**:
- Factual accuracy
- Relevance to query
- Completeness of answer
- Safety/toxicity scores

**Performance**:
- Latency (p50, p95, p99)
- Time to first token (TTFT)
- Tokens per second
- Request throughput

**Cost**:
- Tokens per request (input + output)
- Cost per request
- Cost per user
- Monthly burn rate

**Reliability**:
- Error rate
- Timeout rate
- Retry counts
- Cache hit rate

### Testing Strategy

1. **Create test dataset**: Representative samples covering edge cases
2. **Define success metrics**: Quantitative (accuracy) + qualitative (human review)
3. **Automated scoring**: LLM-as-judge for scale
4. **A/B test prompts**: Compare variations side-by-side
5. **Monitor production**: Sample real traffic for continuous evaluation

**Example test suite**:
```typescript
const tests = [
  { input: "...", expected: "...", tags: ["basic", "happy-path"] },
  { input: "...", expected: "...", tags: ["edge-case", "ambiguous"] },
  { input: "...", expected: "...", tags: ["safety", "adversarial"] }
];

for (const test of tests) {
  const response = await llm.complete(test.input);
  const score = await judge(response, test.expected);
  recordMetric(test.tags, score);
}
```

---

## 6. Production Readiness

### Cost Optimization

**Model Routing** (small → large):
```typescript
async function routeToModel(query: string) {
  const complexity = analyzeComplexity(query);

  if (complexity === 'simple') {
    return "gpt-4o-mini"; // $0.15 per 1M tokens
  } else if (complexity === 'medium') {
    return "gemini-2.5-flash"; // $0.17 per 1M tokens
  } else {
    return "claude-sonnet-4.5"; // $3 per 1M tokens
  }
}
```

**Token Limits**:
```typescript
const config = {
  max_tokens: 500, // Don't let model ramble
  temperature: 0.7,
  top_p: 0.9
};
```

**Prompt Caching**: Enable for all static context (see section 2)

**Result**: $100/month → $20/month typical optimization

### Error Handling

**Retry with Exponential Backoff**:
```typescript
async function callWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429) { // Rate limit
        await sleep(Math.pow(2, i) * 1000);
      } else if (error.status >= 500) { // Server error
        await sleep(1000);
      } else {
        throw error; // Don't retry client errors
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

**Fallback Models**:
```typescript
const fallbackChain = [
  "anthropic/claude-sonnet-4.5",
  "openai/gpt-5",
  "google/gemini-2.5-pro"
];

for (const model of fallbackChain) {
  try {
    return await llm.complete({ model, messages });
  } catch (error) {
    console.log(`${model} failed, trying next...`);
  }
}
```

**Circuit Breaker** (fail fast when provider down):
```typescript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.state = 'closed'; // closed, open, half-open
  }

  async call(fn) {
    if (this.state === 'open') {
      throw new Error('Circuit breaker open');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'open';
      setTimeout(() => this.state = 'half-open', this.timeout);
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }
}
```

### Security

**Input Sanitization**:
```typescript
function sanitizeInput(userInput: string): string {
  // Remove system-breaking patterns
  return userInput
    .replace(/<\|im_start\|>|<\|im_end\|>/g, '')
    .replace(/\[SYSTEM\]|\[\/SYSTEM\]/gi, '')
    .trim();
}
```

**Output Validation**:
```typescript
function validateOutput(response: string): boolean {
  // Check for PII leakage
  const piiPatterns = [/\b\d{3}-\d{2}-\d{4}\b/, /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i];
  return !piiPatterns.some(pattern => pattern.test(response));
}
```

**Rate Limiting**:
```typescript
// Per user rate limits
const limiter = new RateLimiter({
  tokensPerInterval: 100,
  interval: 'hour'
});

await limiter.removeTokens(1);
```

### Observability

**Minimal setup** (OpenTelemetry + logging):
```typescript
import { trace } from '@opentelemetry/api';

async function tracedLLMCall(messages) {
  const span = trace.getTracer('llm').startSpan('llm.complete');

  const startTime = Date.now();
  try {
    const response = await llm.complete(messages);

    span.setAttributes({
      'llm.model': response.model,
      'llm.input_tokens': response.usage.prompt_tokens,
      'llm.output_tokens': response.usage.completion_tokens,
      'llm.latency_ms': Date.now() - startTime,
      'llm.cost_usd': calculateCost(response.usage)
    });

    return response;
  } finally {
    span.end();
  }
}
```

**What to log**:
```typescript
{
  timestamp: new Date().toISOString(),
  model: "claude-sonnet-4.5",
  prompt_tokens: 150,
  completion_tokens: 200,
  total_tokens: 350,
  cost_usd: 0.00105,
  latency_ms: 1234,
  user_id: "user_123",
  success: true,
  error: null
}
```

**Alerts to set**:
- Cost spike: >2x daily average
- Error rate: >5% of requests
- Latency: p95 >5 seconds
- Token usage: Approaching rate limits

### Performance

**Streaming** (better perceived speed):
```typescript
const stream = await llm.stream(messages);

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
  // Send to client immediately
}
```

**Batch Processing** (when latency allows):
```typescript
// Process multiple requests together
const results = await Promise.all(
  requests.map(req => llm.complete(req.messages))
);
```

**Parallel Tool Calls**:
```typescript
// Execute independent tools simultaneously
if (response.tool_calls.length > 1) {
  const results = await Promise.all(
    response.tool_calls.map(call =>
      executeTool(call.name, call.arguments)
    )
  );
}
```

---

## Quick Reference

### Model Selection Decision Tree

```
1. What's the task?
   Coding → Check SWE-bench leaderboard → Test top 3
   Reasoning → Check GPQA leaderboard → Test top 3
   General → Check Arena Elo → Test top 3

2. What's the budget?
   <$50/mo → Gemini Flash, GPT-4o Mini
   $50-500/mo → Mix of mid-tier + premium
   >$500/mo → Premium models + specialized routing

3. What's the speed requirement?
   <200ms → Check Artificial Analysis latency rankings
   <1s → Most models acceptable
   >1s → Batch processing acceptable

4. Test empirically with OpenRouter → Choose best for YOUR use case
```

### Prompt Engineering Checklist

- [ ] System prompt for immutable rules
- [ ] Static context placed early (for caching)
- [ ] Clear task description with success criteria
- [ ] Examples included (1-3 if needed for style/format)
- [ ] Output format specified (structured output when possible)
- [ ] Token limit set (prevent rambling)
- [ ] Temperature appropriate (0 for factual, 0.7-1.0 for creative)

### Vector Storage Decision Tree

```
How many vectors?
├─ <1M → Postgres pgvector (Neon) or Convex
├─ 1-10M → Postgres pgvector (Supabase/Neon)
├─ 10-50M → Postgres pgvectorscale extension
└─ >50M + <10ms latency → Dedicated (Qdrant, Weaviate, Milvus)

Already using Convex? → Use Convex vector search
Already using Postgres? → Add pgvector extension
Need ACID + vectors? → Postgres (only option)
```

### Production Deployment Checklist

**Before Launch**:
- [ ] Prompt caching enabled for static content
- [ ] Structured outputs for critical responses
- [ ] Error handling: retries, fallbacks, circuit breaker
- [ ] Rate limiting per user
- [ ] Input sanitization and output validation
- [ ] Cost tracking and alerts configured
- [ ] Logging/observability in place
- [ ] Test dataset with success metrics defined
- [ ] A/B testing infrastructure ready

**Post-Launch**:
- [ ] Monitor latency (p50, p95, p99)
- [ ] Track cost per user/request
- [ ] Sample evaluation on production traffic
- [ ] Alert thresholds configured (cost, errors, latency)
- [ ] Iteration plan based on metrics

---

## Common Failure Modes (Avoid These)

### ❌ Outdated Model Selection
**Problem**: Recommending GPT-4 when GPT-5 has been out for 3 months
**Fix**: Always search for current leaderboards; include year in queries

### ❌ Premature Optimization
**Problem**: Building multi-agent systems for simple CRUD operations
**Fix**: Start with single LLM call; add complexity only when proven necessary

### ❌ Ignoring Caching
**Problem**: Paying 10x more than necessary
**Fix**: Enable prompt caching for all static context (60-90% cost reduction)

### ❌ Manual JSON Parsing
**Problem**: Retry loops and error handling for malformed JSON
**Fix**: Use native structured outputs with JSON Schema

### ❌ No Evaluation Strategy
**Problem**: Can't tell if changes improve or degrade quality
**Fix**: Create test dataset on day one; use LLM-as-judge for scale

### ❌ Using Dedicated Vector DB by Default
**Problem**: Paying $200/month when $20/month Postgres handles your 2M vectors fine
**Fix**: Start with Postgres pgvector; migrate only when proven necessary

### ❌ Over-Engineering Prompts
**Problem**: 500-word mega-prompts that confuse the model
**Fix**: Modern models are capable; keep prompts concise and structured

### ❌ Same Prompt Across All Models
**Problem**: Suboptimal results because Claude likes XML but gets GPT-style sections
**Fix**: Adapt prompting style to model family strengths

### ❌ No Monitoring Until Problems
**Problem**: Discover cost overruns or quality issues weeks late
**Fix**: Log tokens, cost, latency from first production request

### ❌ Treating LLMs as Deterministic
**Problem**: Assuming same input always produces same output
**Fix**: Use temperature=0 for consistency; test with multiple runs; validate outputs

---

## Philosophy

### AI Augments, Doesn't Replace

Design systems where AI enhances human capabilities:
- Keep humans in the loop for critical decisions
- Make AI suggestions easy to accept/reject/modify
- Provide clear explanations, not just answers
- Build trust through transparency

### Currency Over Perfection

In a field that evolves monthly:
- Learn how to find current solutions
- Build systems that adapt to new models
- Use OpenRouter to avoid vendor lock-in
- Monitor, measure, iterate continuously

### Simplicity Fights Complexity

Complexity is the enemy:
- Single LLM call before multi-agent systems
- Postgres before dedicated vector DB
- Direct API calls before heavy frameworks
- Add abstraction only when proven necessary

### Evaluate Rigorously

Intuition fails at scale:
- Create test datasets on day one
- Use LLM-as-judge for scalable evaluation
- A/B test prompt variations
- Monitor production metrics continuously
- Let data guide decisions

### Cost Consciousness

Small optimizations compound:
- Prompt caching: 60-90% reduction
- Model routing: 5-10x cost difference between tiers
- Token limits: Prevent runaway costs
- Track spending per user/feature

The difference between $1000/month and $100/month is often just smart caching and model routing.

### Embrace Empiricism

Leaderboards guide, but YOUR data decides:
- Benchmark scores don't match your use case perfectly
- Test top 3-5 models with your actual prompts
- Measure what matters (quality, cost, speed)
- Choose based on evidence, not hype

---

## When to Use This Skill

- Selecting which AI model to use for a task
- Writing or improving prompts
- Designing AI feature architecture
- Choosing vector storage solution
- Evaluating LLM output quality
- Optimizing AI feature costs
- Reviewing AI-related code
- Planning production deployment
- Debugging AI feature issues
- Discussing AI development strategy

This skill represents 2025 best practices. The field evolves rapidly—when in doubt, search for current leaderboards and benchmarks. The techniques here (context engineering, caching, structured outputs, empirical testing) remain valuable even as specific models change.
