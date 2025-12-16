# OpenRouter Complete Guide

## Account Setup

1. **Sign up**: https://openrouter.ai
2. **Get API key**: Dashboard → API Keys → Create Key
3. **Free credits**: $1 free on signup

## API Reference

### Endpoint

```
POST https://openrouter.ai/api/v1/chat/completions
```

### Headers

```http
Authorization: Bearer sk-or-v1-...
Content-Type: application/json
HTTP-Referer: https://your-app.com  # Optional, for tracking
X-Title: Your App Name  # Optional, shows in dashboard
```

### Request Body

```json
{
  "model": "anthropic/claude-3-5-sonnet",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 500,
  "stream": false
}
```

### Response

```json
{
  "id": "gen-...",
  "model": "anthropic/claude-3-5-sonnet",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 10,
    "total_tokens": 25
  }
}
```

## Model Selection

### List Available Models

```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### Popular Models (2025)

```typescript
const models = {
  // Premium (best quality)
  premium: [
    "anthropic/claude-3-5-sonnet",      // Best overall
    "openai/gpt-4o",                     // Strong all-around
    "openai/o1-preview",                 // Best reasoning
    "google/gemini-pro-1.5",             // Long context
  ],

  // Balanced (quality/cost)
  balanced: [
    "anthropic/claude-3-5-haiku",        // Fast Claude
    "openai/gpt-4o-mini",                // Fast GPT-4
    "google/gemini-flash-1.5",           // Fast Gemini
  ],

  // Budget (cheap)
  budget: [
    "meta-llama/llama-3.1-8b-instruct",  // Open source
    "mistralai/mistral-7b-instruct",     // Fast and cheap
  ],

  // Specialized
  coding: "anthropic/claude-3-5-sonnet",
  vision: "google/gemini-pro-1.5",
  longContext: "anthropic/claude-3-5-sonnet",  // 200K tokens
};
```

### Auto Model

```typescript
// OpenRouter picks the best model for your query
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  body: JSON.stringify({
    model: "openrouter/auto",  // Auto-select
    messages: [...],
  }),
});
```

## Advanced Features

### Streaming

```typescript
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  body: JSON.stringify({
    model: "anthropic/claude-3-5-sonnet",
    messages: [...],
    stream: true,  // Enable streaming
  }),
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = new TextDecoder().decode(value);
  // Parse SSE: data: {...}
  console.log(chunk);
}
```

### Tool/Function Calling

```typescript
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  body: JSON.stringify({
    model: "anthropic/claude-3-5-sonnet",
    messages: [...],
    tools: [
      {
        type: "function",
        function: {
          name: "get_weather",
          description: "Get weather for a location",
          parameters: {
            type: "object",
            properties: {
              location: { type: "string" },
            },
            required: ["location"],
          },
        },
      },
    ],
  }),
});
```

### JSON Mode

```typescript
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  body: JSON.stringify({
    model: "openai/gpt-4o",
    messages: [...],
    response_format: { type: "json_object" },
  }),
});
```

### Vision (Multimodal)

```typescript
const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  body: JSON.stringify({
    model: "google/gemini-pro-1.5",  // Vision-capable
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "What's in this image?" },
          {
            type: "image_url",
            image_url: { url: "data:image/png;base64,..." },
          },
        ],
      },
    ],
  }),
});
```

## Cost Management

### Check Pricing

```bash
# Get model pricing
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | jq '.data[] | {id, pricing}'
```

### Cost Calculation

```typescript
function calculateCost(model: string, usage: Usage): number {
  const pricing: Record<string, { input: number; output: number }> = {
    "anthropic/claude-3-5-sonnet": { input: 3.0, output: 15.0 },
    "openai/gpt-4o": { input: 2.5, output: 10.0 },
    "openai/gpt-4o-mini": { input: 0.15, output: 0.6 },
    "google/gemini-flash-1.5": { input: 0.075, output: 0.3 },
  };

  const p = pricing[model] || { input: 1, output: 1 };
  return (
    (usage.prompt_tokens * p.input) / 1_000_000 +
    (usage.completion_tokens * p.output) / 1_000_000
  );
}
```

### Set Budget Limits

```typescript
// Track spending
let monthlySpend = 0;
const monthlyBudget = 100; // $100

async function callWithBudget(params: ChatParams) {
  if (monthlySpend >= monthlyBudget) {
    throw new Error("Monthly budget exceeded");
  }

  const response = await openrouter.chat(params);
  const cost = calculateCost(params.model, response.usage);
  monthlySpend += cost;

  return response;
}
```

## Error Handling

### Common Errors

```typescript
try {
  const response = await openrouter.chat({ model, messages });
} catch (error) {
  if (error.status === 429) {
    // Rate limited - wait and retry
    await sleep(error.headers["retry-after"] * 1000);
  } else if (error.status === 402) {
    // Payment required - add credits
    console.error("Out of credits");
  } else if (error.status === 503) {
    // Model unavailable - use fallback
    return callFallback(messages);
  }
}
```

### Retry Logic

```typescript
async function callWithRetry(params: ChatParams, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await openrouter.chat(params);
    } catch (error) {
      if (error.status === 429) {
        await sleep(Math.pow(2, i) * 1000);
      } else if (error.status >= 500) {
        await sleep(1000);
      } else {
        throw error;
      }
    }
  }
  throw new Error("Max retries exceeded");
}
```

## SDK Integration

### Vercel AI SDK

```typescript
import { createOpenAI } from "@ai-sdk/openai";
import { generateText, streamText } from "ai";

const openrouter = createOpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

// Non-streaming
const { text } = await generateText({
  model: openrouter("anthropic/claude-3-5-sonnet"),
  prompt: "Explain recursion",
});

// Streaming
const { textStream } = await streamText({
  model: openrouter("anthropic/claude-3-5-sonnet"),
  prompt: "Write a poem",
});
for await (const chunk of textStream) {
  process.stdout.write(chunk);
}
```

### LangChain

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  modelName: "anthropic/claude-3-5-sonnet",
  openAIApiKey: process.env.OPENROUTER_API_KEY,
  configuration: {
    baseURL: "https://openrouter.ai/api/v1",
  },
});
```

### OpenAI SDK (Direct)

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

const completion = await client.chat.completions.create({
  model: "anthropic/claude-3-5-sonnet",
  messages: [{ role: "user", content: "Hello!" }],
});
```

## Best Practices

1. **Set HTTP-Referer header** - Helps with abuse prevention
2. **Use X-Title header** - Shows in dashboard for tracking
3. **Pin model versions** - Avoid unexpected changes
4. **Set max_tokens** - Prevent runaway costs
5. **Implement fallbacks** - Handle provider outages
6. **Track costs** - Log usage for monitoring
