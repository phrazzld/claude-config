#!/usr/bin/env npx tsx
/**
 * Get metrics summary from recent Langfuse traces.
 *
 * Usage:
 *   npx tsx scripts/get-metrics.ts --limit 50
 *   npx tsx scripts/get-metrics.ts --name "quiz-generation" --limit 100
 */

import { Langfuse } from "langfuse";

function getClient(): Langfuse {
  const secretKey = process.env.LANGFUSE_SECRET_KEY;
  const publicKey = process.env.LANGFUSE_PUBLIC_KEY;
  const baseUrl = process.env.LANGFUSE_HOST || "https://cloud.langfuse.com";

  if (!secretKey || !publicKey) {
    console.error("Error: LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY must be set");
    process.exit(1);
  }

  return new Langfuse({ secretKey, publicKey, baseUrl });
}

function parseArgs(): { limit: number; name?: string } {
  const args = process.argv.slice(2);
  const result: { limit: number; name?: string } = { limit: 50 };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === "--name" && args[i + 1]) {
      result.name = args[i + 1];
      i++;
    }
  }

  return result;
}

async function main() {
  const { limit, name } = parseArgs();
  const client = getClient();

  try {
    // Fetch traces
    const traces = await client.fetchTraces({ limit, name });

    // Aggregate metrics
    const totalTraces = traces.data.length;
    const latencies: number[] = [];
    let totalTokens = 0;
    const byName: Record<string, number> = {};
    let errorCount = 0;

    for (const trace of traces.data) {
      const traceName = trace.name || "unnamed";
      byName[traceName] = (byName[traceName] || 0) + 1;

      if (trace.latency) {
        latencies.push(trace.latency * 1000); // Convert to ms
      }

      // Check for errors
      if (trace.metadata && typeof trace.metadata === "object" && "error" in trace.metadata) {
        errorCount++;
      }
    }

    // Fetch observations for token counts (limit to first 20 for performance)
    const tracesToAnalyze = traces.data.slice(0, 20);
    for (const trace of tracesToAnalyze) {
      try {
        const observations = await client.fetchObservations({ traceId: trace.id });
        for (const obs of observations.data) {
          if (obs.usage?.totalTokens) {
            totalTokens += obs.usage.totalTokens;
          }
        }
      } catch {
        // Skip if observation fetch fails
      }
    }

    const result = {
      totalTraces,
      successCount: totalTraces - errorCount,
      errorCount,
      avgLatencyMs: latencies.length > 0
        ? Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length)
        : null,
      minLatencyMs: latencies.length > 0 ? Math.round(Math.min(...latencies)) : null,
      maxLatencyMs: latencies.length > 0 ? Math.round(Math.max(...latencies)) : null,
      totalTokens,
      tokenNote: totalTokens > 0 ? `Token count from first ${tracesToAnalyze.length} traces` : "No token data",
      byName,
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("Error fetching metrics:", error);
    process.exit(1);
  } finally {
    await client.shutdownAsync();
  }
}

main();
