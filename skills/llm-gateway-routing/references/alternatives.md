# LLM Gateway Alternatives

## Quick Comparison

| Gateway | Best For | Hosting | Key Feature |
|---------|----------|---------|-------------|
| **OpenRouter** | Fast multi-model | Managed | 400+ models, easy |
| **LiteLLM** | Self-hosted control | Self | Load balancing, caching |
| **Helicone** | Observability + routing | Managed/Self | Built-in analytics |
| **Portkey** | Enterprise | Managed | Guardrails, compliance |
| **Martian** | Cost optimization | Managed | Smart routing |

## Detailed Comparison

### OpenRouter

**Best for**: Quick setup, multi-model access, prototyping

**Pros**:
- 400+ models from all providers
- No infrastructure needed
- $1 free credits
- A/B testing built-in
- Unified billing

**Cons**:
- Data routes through their servers
- Small markup on token costs
- No caching
- Limited customization

**Pricing**: Pay-per-token (small markup on base prices)

**Setup**: Sign up → Get API key → Use OpenAI-compatible API

### LiteLLM

**Best for**: Self-hosted, full control, complex routing

**Pros**:
- Self-hosted (full data control)
- Built-in caching (Redis, local)
- Load balancing
- Rate limiting
- Cost tracking
- Free (open source)

**Cons**:
- Requires infrastructure
- More complex setup
- You manage updates

**Pricing**: Free (you pay only provider API costs)

**Setup**: pip install → Configure YAML → Run proxy

### Helicone

**Best for**: Observability-first teams

**Pros**:
- One-line integration (just change base URL)
- Excellent observability dashboard
- Cost tracking
- Caching
- Rate limiting
- Self-host option

**Cons**:
- Proxy-based (adds latency)
- Less routing features than LiteLLM
- Pricing scales with usage

**Pricing**: Free tier (10K requests/month), then paid

**Setup**: Change baseURL → Use same API

```typescript
// Before
const client = new OpenAI({ apiKey: "..." });

// After
const client = new OpenAI({
  apiKey: "...",
  baseURL: "https://oai.helicone.ai/v1",
  defaultHeaders: {
    "Helicone-Auth": `Bearer ${HELICONE_API_KEY}`,
  },
});
```

### Portkey

**Best for**: Enterprise, compliance, guardrails

**Pros**:
- Enterprise features
- AI guardrails (content filtering)
- Compliance (SOC 2, HIPAA)
- Virtual keys (rotate without code changes)
- Semantic caching
- Fallback chains

**Cons**:
- Enterprise pricing
- More complex than needed for small teams
- Vendor lock-in potential

**Pricing**: Contact sales

**Setup**: SDK integration + Portkey dashboard

### Martian

**Best for**: Cost optimization at scale

**Pros**:
- AI-powered routing (picks cheapest model that works)
- Automatic quality scoring
- Cost savings 30-50%
- Simple integration

**Cons**:
- Newer platform
- Less proven than alternatives
- Limited provider coverage

**Pricing**: Percentage of savings

**Setup**: API key + SDK integration

## Feature Matrix

| Feature | OpenRouter | LiteLLM | Helicone | Portkey |
|---------|------------|---------|----------|---------|
| Multi-provider | ✅ 400+ | ✅ 100+ | ⚠️ Limited | ✅ 200+ |
| Self-host | ❌ | ✅ | ✅ | ❌ |
| Caching | ❌ | ✅ | ✅ | ✅ |
| Rate limiting | ❌ | ✅ | ✅ | ✅ |
| Load balancing | ❌ | ✅ | ⚠️ | ✅ |
| Observability | ⚠️ | ⚠️ | ✅ | ✅ |
| Guardrails | ❌ | ❌ | ❌ | ✅ |
| A/B testing | ✅ | ⚠️ DIY | ⚠️ | ✅ |
| Free tier | ✅ $1 | ✅ | ✅ 10K/mo | ❌ |

## Decision Guide

### Startup / Side Project
**Recommendation**: OpenRouter

- Quick setup (minutes)
- Free credits to start
- No infrastructure
- Easy model switching

### Scaling Startup
**Recommendation**: OpenRouter → LiteLLM

- Start with OpenRouter for speed
- Move to LiteLLM when:
  - Need caching
  - Cost optimization critical
  - Privacy requirements arise

### Enterprise
**Recommendation**: Portkey or LiteLLM (self-hosted)

- Portkey for managed + guardrails
- LiteLLM for full control + compliance

### Observability-First
**Recommendation**: Helicone + (OpenRouter or LiteLLM)

- Use Helicone proxy for observability
- Pair with OpenRouter or LiteLLM for routing

## Migration Paths

### OpenRouter → LiteLLM

```yaml
# LiteLLM config to replicate OpenRouter setup
model_list:
  - model_name: claude
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: ${ANTHROPIC_API_KEY}

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: ${OPENAI_API_KEY}

router_settings:
  fallbacks:
    claude: [gpt-4o]
```

### Add Observability to Any Gateway

```typescript
// Wrap any gateway with Langfuse
import { Langfuse } from "langfuse";

const langfuse = new Langfuse({
  publicKey: "...",
  secretKey: "...",
});

async function trackedCall(model: string, messages: Message[]) {
  const trace = langfuse.trace({ name: "llm-call" });
  const generation = trace.generation({
    name: "chat",
    model,
    input: messages,
  });

  const response = await gateway.chat({ model, messages });

  generation.end({
    output: response.choices[0].message,
    usage: response.usage,
  });

  return response;
}
```

## Cost Comparison (Rough)

| Gateway | 1M tokens (Claude) | 10M tokens | 100M tokens |
|---------|-------------------|------------|-------------|
| Direct API | $3.00 | $30 | $300 |
| OpenRouter | $3.30 (~10% markup) | $33 | $330 |
| LiteLLM | $3.00 + infra | $30 + infra | $300 + infra |
| Helicone | $3.00 + $0.50 | $30 + $5 | $300 + ~$50 |
| Portkey | Contact sales | Contact sales | Contact sales |

*Note: Infra costs for self-hosted can be $20-100/month for small scale.*
