# LLM Routing Strategies

## Overview

Routing strategies determine which model handles each request. Choose based on your priorities:

| Priority | Strategy | Trade-off |
|----------|----------|-----------|
| **Cost** | Cost-based routing | Quality may vary |
| **Quality** | Task-based routing | Higher cost |
| **Speed** | Latency-based routing | May miss better answers |
| **Reliability** | Fallback chains | Increased complexity |
| **Learning** | A/B testing | Requires analysis |

## Strategy Implementations

### 1. Cost-Based Routing

Route based on query complexity to optimize spend.

```typescript
interface CostTier {
  name: string;
  models: string[];
  costPer1MTokens: number;
}

const tiers: CostTier[] = [
  {
    name: "budget",
    models: ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
    costPer1MTokens: 0.15,
  },
  {
    name: "standard",
    models: ["anthropic/claude-3-5-haiku", "openai/gpt-4o"],
    costPer1MTokens: 2.5,
  },
  {
    name: "premium",
    models: ["anthropic/claude-3-5-sonnet", "openai/o1-preview"],
    costPer1MTokens: 15.0,
  },
];

function routeByCost(query: string): string {
  const complexity = estimateComplexity(query);

  if (complexity < 0.3) {
    return pickRandom(tiers[0].models);
  } else if (complexity < 0.7) {
    return pickRandom(tiers[1].models);
  } else {
    return pickRandom(tiers[2].models);
  }
}

function estimateComplexity(query: string): number {
  let score = 0;

  // Length factor
  score += Math.min(query.length / 1000, 0.3);

  // Code presence
  if (/```|function|class|import/.test(query)) score += 0.3;

  // Analysis keywords
  if (/analyze|explain|compare|why|how|implement/.test(query.toLowerCase())) {
    score += 0.2;
  }

  // Math/logic
  if (/\d+|calculate|equation|formula/.test(query)) score += 0.2;

  return Math.min(score, 1);
}
```

### 2. Task-Based Routing

Match models to their strengths.

```typescript
type TaskType = "coding" | "reasoning" | "creative" | "simple" | "vision";

const taskModels: Record<TaskType, string> = {
  coding: "anthropic/claude-3-5-sonnet",     // Best for code
  reasoning: "openai/o1-preview",             // Best for logic
  creative: "anthropic/claude-3-5-sonnet",    // Best for writing
  simple: "openai/gpt-4o-mini",               // Fast and cheap
  vision: "google/gemini-pro-1.5",            // Vision + text
};

function detectTaskType(query: string): TaskType {
  // Code patterns
  if (/```|function|class|import|def |const |let |var /.test(query)) {
    return "coding";
  }

  // Reasoning patterns
  if (/prove|calculate|solve|logic|math|step by step/.test(query.toLowerCase())) {
    return "reasoning";
  }

  // Creative patterns
  if (/write|story|poem|creative|imagine|describe/.test(query.toLowerCase())) {
    return "creative";
  }

  // Vision (check for image in messages)
  // Note: Handled separately in message processing

  // Default to simple
  return "simple";
}

function routeByTask(query: string): string {
  const taskType = detectTaskType(query);
  return taskModels[taskType];
}
```

### 3. Latency-Based Routing

Route to fastest responding model.

```typescript
interface ModelStats {
  model: string;
  samples: number[];
  avgLatency: number;
  p95Latency: number;
}

const stats: Map<string, ModelStats> = new Map();

function updateStats(model: string, latencyMs: number) {
  let modelStats = stats.get(model);

  if (!modelStats) {
    modelStats = { model, samples: [], avgLatency: 0, p95Latency: 0 };
    stats.set(model, modelStats);
  }

  // Keep last 100 samples
  modelStats.samples.push(latencyMs);
  if (modelStats.samples.length > 100) {
    modelStats.samples.shift();
  }

  // Calculate stats
  const sorted = [...modelStats.samples].sort((a, b) => a - b);
  modelStats.avgLatency = sorted.reduce((a, b) => a + b, 0) / sorted.length;
  modelStats.p95Latency = sorted[Math.floor(sorted.length * 0.95)] || latencyMs;
}

function routeByLatency(models: string[]): string {
  // Filter models we have data for
  const withStats = models.filter((m) => stats.has(m));

  if (withStats.length === 0) {
    // No data yet, pick random
    return models[Math.floor(Math.random() * models.length)];
  }

  // Sort by p95 latency
  const sorted = withStats
    .map((m) => ({ model: m, stats: stats.get(m)! }))
    .sort((a, b) => a.stats.p95Latency - b.stats.p95Latency);

  return sorted[0].model;
}
```

### 4. Quality-Based Routing (LLM-as-Judge)

Use a judge model to route based on expected quality.

```typescript
async function routeByQuality(query: string, models: string[]): Promise<string> {
  // Use fast model to analyze query and pick best model
  const judgeResponse = await llm.chat({
    model: "openai/gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `You are a model router. Given a query, select the best model from the list.
        Consider:
        - Claude: Best for nuanced writing, code, long context
        - GPT-4o: Best for structured output, consistency
        - O1: Best for complex reasoning, math
        - Gemini: Best for multimodal, research

        Return only the model name.`,
      },
      {
        role: "user",
        content: `Query: ${query}\n\nAvailable models: ${models.join(", ")}`,
      },
    ],
    max_tokens: 50,
  });

  const selectedModel = judgeResponse.content.trim();
  return models.includes(selectedModel) ? selectedModel : models[0];
}
```

### 5. Hybrid Routing

Combine multiple strategies.

```typescript
interface RoutingConfig {
  maxCost?: number;           // Max cost per request
  maxLatency?: number;        // Max acceptable latency (ms)
  taskType?: TaskType;        // Force task type
  preferredProvider?: string; // Prefer specific provider
}

function hybridRoute(query: string, config: RoutingConfig = {}): string {
  const allModels = getAllModels();

  // Filter by cost
  let candidates = allModels;
  if (config.maxCost) {
    candidates = candidates.filter((m) => getCostPer1K(m) <= config.maxCost!);
  }

  // Filter by latency
  if (config.maxLatency) {
    candidates = candidates.filter((m) => {
      const s = stats.get(m);
      return !s || s.p95Latency <= config.maxLatency!;
    });
  }

  // Filter by provider
  if (config.preferredProvider) {
    const providerModels = candidates.filter((m) =>
      m.startsWith(config.preferredProvider!)
    );
    if (providerModels.length > 0) {
      candidates = providerModels;
    }
  }

  // Select based on task
  const taskType = config.taskType || detectTaskType(query);
  const taskModel = taskModels[taskType];

  if (candidates.includes(taskModel)) {
    return taskModel;
  }

  // Fallback: best available by latency
  return routeByLatency(candidates);
}
```

### 6. A/B Testing Router

Test different models with users.

```typescript
interface Experiment {
  id: string;
  variants: {
    name: string;
    model: string;
    weight: number;
  }[];
  startDate: Date;
  endDate?: Date;
}

const experiments: Map<string, Experiment> = new Map([
  [
    "claude-vs-gpt",
    {
      id: "claude-vs-gpt",
      variants: [
        { name: "claude", model: "anthropic/claude-3-5-sonnet", weight: 0.5 },
        { name: "gpt", model: "openai/gpt-4o", weight: 0.5 },
      ],
      startDate: new Date(),
    },
  ],
]);

interface ABResult {
  model: string;
  experiment: string;
  variant: string;
}

function routeAB(userId: string, experimentId: string): ABResult {
  const experiment = experiments.get(experimentId);
  if (!experiment) {
    return {
      model: "anthropic/claude-3-5-sonnet",
      experiment: "default",
      variant: "default",
    };
  }

  // Deterministic assignment based on user ID
  const hash = hashString(userId + experiment.id);
  const normalized = hash / 0xffffffff;

  let cumulative = 0;
  for (const variant of experiment.variants) {
    cumulative += variant.weight;
    if (normalized < cumulative) {
      return {
        model: variant.model,
        experiment: experiment.id,
        variant: variant.name,
      };
    }
  }

  // Fallback to first variant
  return {
    model: experiment.variants[0].model,
    experiment: experiment.id,
    variant: experiment.variants[0].name,
  };
}

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}
```

## Best Practices

### 1. Start Simple

```typescript
// Start with task-based routing
const model = routeByTask(query);

// Add cost optimization when you have volume
const model = routeByCost(query);

// Add latency optimization when you have data
const model = routeByLatency(candidates);
```

### 2. Log Everything

```typescript
async function trackedRoute(query: string): Promise<Response> {
  const model = selectModel(query);
  const startTime = Date.now();

  const response = await llm.chat({ model, query });

  await log({
    model,
    query: query.substring(0, 100),
    latencyMs: Date.now() - startTime,
    tokens: response.usage.totalTokens,
    cost: calculateCost(model, response.usage),
    routingStrategy: "cost-based",
  });

  return response;
}
```

### 3. Monitor and Adjust

```typescript
// Weekly review metrics
interface RoutingMetrics {
  totalRequests: number;
  avgCost: number;
  avgLatency: number;
  qualityScore: number; // From user feedback or LLM-as-judge
  modelDistribution: Record<string, number>;
}

// Adjust thresholds based on metrics
if (metrics.avgCost > budget) {
  // Shift more traffic to cheaper models
  costThreshold *= 0.8;
}

if (metrics.avgLatency > sla) {
  // Prioritize faster models
  enableLatencyRouting = true;
}
```

### 4. Have Fallbacks

```typescript
async function robustRoute(query: string): Promise<Response> {
  const primaryModel = selectModel(query);
  const fallbackChain = [primaryModel, ...getFallbacks(primaryModel)];

  for (const model of fallbackChain) {
    try {
      return await llm.chat({ model, query });
    } catch (error) {
      console.warn(`${model} failed, trying next`);
    }
  }

  throw new Error("All models failed");
}
```
