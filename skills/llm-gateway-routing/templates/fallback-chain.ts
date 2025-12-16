/**
 * LLM Fallback Chain Implementation
 * Robust error handling with automatic failover
 */

// ============================================
// Types
// ============================================

interface Message {
  role: "system" | "user" | "assistant";
  content: string;
}

interface LLMResponse {
  content: string;
  model: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  latencyMs: number;
}

interface FallbackConfig {
  models: string[];
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
}

// ============================================
// Default Configuration
// ============================================

const defaultConfig: FallbackConfig = {
  models: [
    "anthropic/claude-3-5-sonnet",
    "openai/gpt-4o",
    "google/gemini-pro-1.5",
  ],
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 10000,
};

// ============================================
// Error Classification
// ============================================

type ErrorType = "retryable" | "rate_limit" | "fatal";

function classifyError(error: any): ErrorType {
  const status = error.status || error.statusCode;

  // Rate limited
  if (status === 429) return "rate_limit";

  // Server errors - retryable
  if (status >= 500) return "retryable";

  // Network errors - retryable
  if (error.code === "ECONNRESET" || error.code === "ETIMEDOUT") {
    return "retryable";
  }

  // Client errors - fatal
  if (status >= 400 && status < 500) return "fatal";

  // Unknown - assume retryable
  return "retryable";
}

// ============================================
// Delay Calculation
// ============================================

function getDelay(attempt: number, config: FallbackConfig): number {
  // Exponential backoff with jitter
  const exponential = Math.min(
    config.baseDelayMs * Math.pow(2, attempt),
    config.maxDelayMs
  );
  const jitter = Math.random() * 0.2 * exponential; // 20% jitter
  return exponential + jitter;
}

async function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ============================================
// LLM Client (Abstract)
// ============================================

interface LLMClient {
  chat(model: string, messages: Message[]): Promise<LLMResponse>;
}

// Example implementation for OpenRouter
class OpenRouterClient implements LLMClient {
  private apiKey: string;
  private baseUrl = "https://openrouter.ai/api/v1";

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async chat(model: string, messages: Message[]): Promise<LLMResponse> {
    const startTime = Date.now();

    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        messages,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw { status: response.status, ...error };
    }

    const data = await response.json();
    const latencyMs = Date.now() - startTime;

    return {
      content: data.choices[0].message.content,
      model: data.model,
      usage: {
        promptTokens: data.usage.prompt_tokens,
        completionTokens: data.usage.completion_tokens,
        totalTokens: data.usage.total_tokens,
      },
      latencyMs,
    };
  }
}

// ============================================
// Fallback Chain
// ============================================

export class FallbackChain {
  private client: LLMClient;
  private config: FallbackConfig;

  constructor(client: LLMClient, config: Partial<FallbackConfig> = {}) {
    this.client = client;
    this.config = { ...defaultConfig, ...config };
  }

  async call(messages: Message[]): Promise<LLMResponse> {
    const errors: Array<{ model: string; error: any }> = [];

    for (const model of this.config.models) {
      for (let attempt = 0; attempt < this.config.maxRetries; attempt++) {
        try {
          console.log(`Trying ${model} (attempt ${attempt + 1})`);
          return await this.client.chat(model, messages);
        } catch (error: any) {
          const errorType = classifyError(error);
          errors.push({ model, error });

          console.warn(`${model} failed:`, {
            attempt: attempt + 1,
            errorType,
            status: error.status,
            message: error.message,
          });

          if (errorType === "fatal") {
            // Don't retry fatal errors, move to next model
            break;
          }

          if (errorType === "rate_limit") {
            // Respect rate limit headers
            const retryAfter = error.headers?.["retry-after"] || 60;
            console.log(`Rate limited, waiting ${retryAfter}s`);
            await sleep(retryAfter * 1000);
          } else {
            // Exponential backoff for retryable errors
            const delay = getDelay(attempt, this.config);
            console.log(`Retrying in ${delay}ms`);
            await sleep(delay);
          }
        }
      }
      console.log(`${model} exhausted, trying next model`);
    }

    // All models failed
    throw new Error(
      `All models failed. Errors: ${JSON.stringify(errors, null, 2)}`
    );
  }
}

// ============================================
// Convenience Functions
// ============================================

let defaultChain: FallbackChain | null = null;

export function initFallbackChain(apiKey: string, config?: Partial<FallbackConfig>) {
  const client = new OpenRouterClient(apiKey);
  defaultChain = new FallbackChain(client, config);
  return defaultChain;
}

export async function callWithFallback(messages: Message[]): Promise<LLMResponse> {
  if (!defaultChain) {
    throw new Error("FallbackChain not initialized. Call initFallbackChain first.");
  }
  return defaultChain.call(messages);
}

// ============================================
// Usage Example
// ============================================

/*
// Initialize once at app startup
initFallbackChain(process.env.OPENROUTER_API_KEY!, {
  models: [
    "anthropic/claude-3-5-sonnet",
    "openai/gpt-4o",
    "google/gemini-pro-1.5",
  ],
  maxRetries: 3,
});

// Use anywhere in your app
const response = await callWithFallback([
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "Hello!" },
]);

console.log(response.content);
console.log(`Used model: ${response.model}`);
console.log(`Latency: ${response.latencyMs}ms`);
console.log(`Tokens: ${response.usage.totalTokens}`);
*/
