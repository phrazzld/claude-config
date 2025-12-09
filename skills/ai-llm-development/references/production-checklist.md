# Production Readiness

## Cost Optimization

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

**Result**: $100/month → $20/month typical optimization

## Error Handling

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

## Security

**Input Sanitization**:
```typescript
function sanitizeInput(userInput: string): string {
  return userInput
    .replace(/<\|im_start\|>|<\|im_end\|>/g, '')
    .replace(/\[SYSTEM\]|\[\/SYSTEM\]/gi, '')
    .trim();
}
```

**Output Validation**:
```typescript
function validateOutput(response: string): boolean {
  const piiPatterns = [/\b\d{3}-\d{2}-\d{4}\b/, /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i];
  return !piiPatterns.some(pattern => pattern.test(response));
}
```

**Rate Limiting**:
```typescript
const limiter = new RateLimiter({
  tokensPerInterval: 100,
  interval: 'hour'
});

await limiter.removeTokens(1);
```

## Observability

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

## Evaluation & Testing

### LLM-as-Judge

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

### Testing Strategy

1. **Create test dataset**: Representative samples covering edge cases
2. **Define success metrics**: Quantitative + qualitative
3. **Automated scoring**: LLM-as-judge for scale
4. **A/B test prompts**: Compare variations side-by-side
5. **Monitor production**: Sample real traffic

## Production Deployment Checklist

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
