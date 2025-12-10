#!/usr/bin/env npx tsx
/**
 * Fetch recent traces from Langfuse with optional filters.
 *
 * Usage:
 *   npx tsx scripts/fetch-traces.ts --limit 10
 *   npx tsx scripts/fetch-traces.ts --name "quiz-generation" --limit 5
 *   npx tsx scripts/fetch-traces.ts --user-id "user_abc" --limit 10
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

function parseArgs(): { limit: number; name?: string; userId?: string; tags?: string[] } {
  const args = process.argv.slice(2);
  const result: { limit: number; name?: string; userId?: string; tags?: string[] } = { limit: 10 };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--limit" && args[i + 1]) {
      result.limit = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === "--name" && args[i + 1]) {
      result.name = args[i + 1];
      i++;
    } else if (args[i] === "--user-id" && args[i + 1]) {
      result.userId = args[i + 1];
      i++;
    } else if (args[i] === "--tags" && args[i + 1]) {
      result.tags = args[i + 1].split(",");
      i++;
    }
  }

  return result;
}

interface FormattedTrace {
  id: string;
  name: string | null;
  userId: string | null;
  sessionId: string | null;
  input: unknown;
  output: unknown;
  metadata: unknown;
  tags: string[];
  latencyMs: number | null;
  createdAt: string | null;
}

function formatTrace(trace: any): FormattedTrace {
  return {
    id: trace.id,
    name: trace.name,
    userId: trace.userId,
    sessionId: trace.sessionId,
    input: trace.input,
    output: trace.output,
    metadata: trace.metadata,
    tags: trace.tags || [],
    latencyMs: trace.latency ? Math.round(trace.latency * 1000) : null,
    createdAt: trace.timestamp || null,
  };
}

async function main() {
  const { limit, name, userId, tags } = parseArgs();
  const client = getClient();

  try {
    const response = await client.fetchTraces({
      limit,
      name,
      userId,
      tags,
    });

    const traces = response.data.map(formatTrace);
    console.log(JSON.stringify(traces, null, 2));
  } catch (error) {
    console.error("Error fetching traces:", error);
    process.exit(1);
  } finally {
    await client.shutdownAsync();
  }
}

main();
