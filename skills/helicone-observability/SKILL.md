---
name: helicone-observability
description: |
  LLM cost observability via Helicone gateway. Integration patterns for AI SDK,
  custom property tagging for multi-product segmentation, per-user cost attribution.
argument-hint: "[action: 'integrate' | 'audit' | 'tag']"
effort: low
---

# /helicone-observability

Route LLM API calls through Helicone for cost tracking, latency monitoring, and per-user attribution across all products.

## Architecture

```
App → Helicone Gateway (proxy) → LLM Provider (Anthropic, OpenAI, etc.)
                ↓
    Helicone Dashboard (cost, latency, properties)
```

Helicone is a transparent proxy. One URL + header change per provider. No SDK lock-in.

## Multi-Product Strategy

Helicone has ONE dashboard per account. Segmentation is via custom properties, not separate projects.

**Mandatory properties for every LLM call:**

| Header | Purpose | Example |
|--------|---------|---------|
| `Helicone-Property-Product` | Which product/repo | `moneta`, `adminifi`, `vox` |
| `Helicone-Property-Environment` | Deploy stage | `production`, `staging`, `development` |
| `Helicone-Property-Feature` | What triggered the call | `chat`, `upload`, `classification` |
| `Helicone-User-Id` | Per-user cost attribution | User ID from auth |

**Optional properties (add as needed):**

| Header | Purpose |
|--------|---------|
| `Helicone-Session-Id` | Group multi-turn conversations |
| `Helicone-Session-Path` | Hierarchical session path |
| `Helicone-Property-Model` | Override for model routing analysis |
| `Helicone-Property-TaxYear` | Domain-specific segmentation |

## Integration: Vercel AI SDK + Anthropic

### Install

No extra packages needed. Helicone works via `baseURL` + headers on `@ai-sdk/anthropic`.

### Provider Setup

```typescript
// lib/ai-provider.ts
import { createAnthropic } from "@ai-sdk/anthropic";

// Helicone-proxied Anthropic provider
export const anthropic = createAnthropic({
  baseURL: "https://anthropic.helicone.ai/v1",
  headers: {
    "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    // Static properties set once at provider level
    "Helicone-Property-Product": "your-product-name",
    "Helicone-Property-Environment": process.env.NODE_ENV ?? "development",
  },
});
```

### Per-Request Properties

Dynamic properties (userId, feature, session) go in the `headers` option of `streamText`/`generateText`:

```typescript
import { streamText } from "ai";
import { anthropic } from "@/lib/ai-provider";

const result = streamText({
  model: anthropic("claude-sonnet-4-6"),
  system: "...",
  messages,
  headers: {
    "Helicone-User-Id": userId,
    "Helicone-Property-Feature": "chat",
    "Helicone-Session-Id": conversationId,
    "Helicone-Session-Path": "/chat",
  },
});
```

### Other Providers

```typescript
// OpenAI
import { createOpenAI } from "@ai-sdk/openai";
const openai = createOpenAI({
  baseURL: "https://oai.helicone.ai/v1",
  headers: {
    "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    "Helicone-Property-Product": "your-product-name",
  },
});

// Google Gemini
import { createGoogleGenerativeAI } from "@ai-sdk/google";
const google = createGoogleGenerativeAI({
  baseURL: "https://gateway.helicone.ai/v1beta",
  headers: {
    "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    "Helicone-Target-URL": "https://generativelanguage.googleapis.com",
    "Helicone-Property-Product": "your-product-name",
  },
});
```

## Caching

Enable for deterministic prompts (system prompt caching, repeated queries):

```typescript
const anthropic = createAnthropic({
  baseURL: "https://anthropic.helicone.ai/v1",
  headers: {
    "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    "Helicone-Cache-Enabled": "true",
    // Default 7 days. Max 365 days.
    "Cache-Control": "max-age=604800",
  },
});
```

Per-user cache isolation:
```typescript
headers: {
  "Helicone-Cache-Seed": userId,  // Separate cache per user
}
```

## Environment Variables

```bash
# .env.example / .env.local
HELICONE_API_KEY=sk-helicone-...
```

API key location: `~/.secrets` (line: `export HELICONE_API_KEY=...`)

Generate new keys: https://helicone.ai → Developer → API Keys

## Pricing Awareness

| Tier | Requests/mo | Retention | Cost |
|------|-------------|-----------|------|
| Free | 10,000 | 1 month | $0 |
| Growth | Unlimited | 3 months | $20/seat/mo |
| Self-host | Unlimited | Unlimited | Infra cost |

Free tier is sufficient for beta/early launch of most indie products.

## Audit Checklist

When adding Helicone to a project, verify:

- [ ] `HELICONE_API_KEY` in `.env.local` and deployment env vars
- [ ] Provider `baseURL` points to Helicone gateway
- [ ] `Helicone-Auth` header on every provider
- [ ] `Helicone-Property-Product` set (identifies this product in shared dashboard)
- [ ] `Helicone-Property-Environment` set (prevents dev/prod mixing)
- [ ] `Helicone-User-Id` passed on every user-facing request
- [ ] `Helicone-Property-Feature` distinguishes call types
- [ ] Requests visible in Helicone dashboard after deploy
- [ ] Cost per user queryable in dashboard

## Dashboard Queries

Filter the Helicone dashboard by:

- **Product**: `Property: Product = moneta` → see only Moneta costs
- **User**: `User Id = user_123` → per-user cost breakdown
- **Feature**: `Property: Feature = chat` → chat vs upload vs classification costs
- **Environment**: `Property: Environment = production` → exclude dev noise

## Anti-Patterns

- Setting only `Helicone-Auth` without custom properties (everything is unsegmented noise)
- Using `Helicone-Property-*` in client-side code (leaks API key)
- Forgetting `Helicone-Property-Product` (can't distinguish products in shared account)
- Enabling cache for non-deterministic chat completions (stale responses)
- Hardcoding API keys instead of using env vars

## References

- [Vercel AI SDK integration](https://docs.helicone.ai/getting-started/integration-method/vercelai)
- [Custom properties](https://docs.helicone.ai/features/advanced-usage/custom-properties)
- [User metrics](https://docs.helicone.ai/features/advanced-usage/user-metrics)
- [Caching](https://docs.helicone.ai/features/advanced-usage/caching)
- [AI SDK observability docs](https://ai-sdk.dev/providers/observability/helicone)
