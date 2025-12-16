/**
 * OpenRouter Configuration Template
 * Copy and adapt for your project
 */

import { createOpenAI } from "@ai-sdk/openai";
import { generateText, streamText } from "ai";

// ============================================
// Configuration
// ============================================

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY!;

// Create OpenRouter client (OpenAI-compatible)
export const openrouter = createOpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: OPENROUTER_API_KEY,
  defaultHeaders: {
    "HTTP-Referer": process.env.APP_URL || "http://localhost:3000",
    "X-Title": process.env.APP_NAME || "My App",
  },
});

// ============================================
// Model Definitions
// ============================================

export const models = {
  // Premium (best quality)
  claudeSonnet: "anthropic/claude-3-5-sonnet",
  gpt4o: "openai/gpt-4o",
  o1Preview: "openai/o1-preview",
  geminiPro: "google/gemini-pro-1.5",

  // Balanced (quality/cost)
  claudeHaiku: "anthropic/claude-3-5-haiku",
  gpt4oMini: "openai/gpt-4o-mini",
  geminiFlash: "google/gemini-flash-1.5",

  // Budget
  llama3: "meta-llama/llama-3.1-70b-instruct",
  mistral: "mistralai/mistral-7b-instruct",

  // Auto (OpenRouter picks)
  auto: "openrouter/auto",
} as const;

export type ModelId = (typeof models)[keyof typeof models];

// ============================================
// Cost Routing
// ============================================

type Complexity = "simple" | "medium" | "complex";

const costTiers: Record<Complexity, ModelId[]> = {
  simple: [models.gpt4oMini, models.geminiFlash],
  medium: [models.claudeHaiku, models.gpt4oMini],
  complex: [models.claudeSonnet, models.gpt4o],
};

export function selectModelByCost(complexity: Complexity): ModelId {
  const tier = costTiers[complexity];
  return tier[Math.floor(Math.random() * tier.length)];
}

export function analyzeComplexity(query: string): Complexity {
  // Simple heuristics - customize for your use case
  const wordCount = query.split(" ").length;
  const hasCode = /```|function|class|const|let|var/.test(query);
  const hasAnalysis = /explain|analyze|compare|why|how/.test(query.toLowerCase());

  if (wordCount < 20 && !hasCode && !hasAnalysis) return "simple";
  if (hasCode || hasAnalysis || wordCount > 100) return "complex";
  return "medium";
}

// ============================================
// Fallback Chain
// ============================================

const fallbackChain: ModelId[] = [
  models.claudeSonnet,
  models.gpt4o,
  models.geminiPro,
];

export async function callWithFallback(
  prompt: string,
  options?: { maxRetries?: number }
): Promise<string> {
  const maxRetries = options?.maxRetries ?? fallbackChain.length;

  for (let i = 0; i < maxRetries; i++) {
    const model = fallbackChain[i];
    try {
      const { text } = await generateText({
        model: openrouter(model),
        prompt,
      });
      return text;
    } catch (error) {
      console.warn(`Model ${model} failed, trying next...`);
      if (i === maxRetries - 1) throw error;
    }
  }
  throw new Error("All models failed");
}

// ============================================
// A/B Testing
// ============================================

export function getModelForABTest(
  userId: string,
  testConfig: { modelA: ModelId; modelB: ModelId; splitRatio?: number }
): { model: ModelId; variant: "A" | "B" } {
  const { modelA, modelB, splitRatio = 0.5 } = testConfig;

  // Deterministic assignment based on user ID
  const hash = userId.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const normalized = (hash % 100) / 100;

  if (normalized < splitRatio) {
    return { model: modelA, variant: "A" };
  } else {
    return { model: modelB, variant: "B" };
  }
}

// ============================================
// Usage Examples
// ============================================

// Basic call
export async function basicCall(prompt: string): Promise<string> {
  const { text } = await generateText({
    model: openrouter(models.claudeSonnet),
    prompt,
  });
  return text;
}

// Streaming call
export async function streamingCall(prompt: string) {
  const { textStream } = await streamText({
    model: openrouter(models.claudeSonnet),
    prompt,
  });
  return textStream;
}

// Cost-optimized call
export async function costOptimizedCall(query: string): Promise<string> {
  const complexity = analyzeComplexity(query);
  const model = selectModelByCost(complexity);

  const { text } = await generateText({
    model: openrouter(model),
    prompt: query,
  });
  return text;
}

// Call with token limit
export async function limitedCall(
  prompt: string,
  maxTokens: number = 500
): Promise<string> {
  const { text } = await generateText({
    model: openrouter(models.claudeSonnet),
    prompt,
    maxTokens,
  });
  return text;
}

// ============================================
// Cost Tracking (for observability)
// ============================================

interface Usage {
  promptTokens: number;
  completionTokens: number;
}

// Pricing per 1M tokens (update as prices change)
const pricing: Record<string, { input: number; output: number }> = {
  [models.claudeSonnet]: { input: 3.0, output: 15.0 },
  [models.claudeHaiku]: { input: 0.25, output: 1.25 },
  [models.gpt4o]: { input: 2.5, output: 10.0 },
  [models.gpt4oMini]: { input: 0.15, output: 0.6 },
  [models.geminiPro]: { input: 1.25, output: 5.0 },
  [models.geminiFlash]: { input: 0.075, output: 0.3 },
};

export function calculateCost(model: ModelId, usage: Usage): number {
  const p = pricing[model] || { input: 1, output: 1 };
  return (
    (usage.promptTokens * p.input) / 1_000_000 +
    (usage.completionTokens * p.output) / 1_000_000
  );
}
