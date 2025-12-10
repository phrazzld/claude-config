#!/usr/bin/env npx tsx
/**
 * Fetch a single trace with full details including observations (spans/generations).
 *
 * Usage:
 *   npx tsx scripts/fetch-trace.ts <trace-id>
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

interface FormattedObservation {
  id: string;
  type: string;
  name: string | null;
  startTime: string | null;
  endTime: string | null;
  input: unknown;
  output: unknown;
  metadata: unknown;
  level: string | null;
  statusMessage: string | null;
  model?: string;
  modelParameters?: unknown;
  usage?: {
    promptTokens: number | null;
    completionTokens: number | null;
    totalTokens: number | null;
  };
  latencyMs?: number | null;
}

function formatObservation(obs: any): FormattedObservation {
  const result: FormattedObservation = {
    id: obs.id,
    type: obs.type,
    name: obs.name,
    startTime: obs.startTime || null,
    endTime: obs.endTime || null,
    input: obs.input,
    output: obs.output,
    metadata: obs.metadata,
    level: obs.level || null,
    statusMessage: obs.statusMessage || null,
  };

  if (obs.type === "GENERATION") {
    result.model = obs.model;
    result.modelParameters = obs.modelParameters;
    result.usage = {
      promptTokens: obs.usage?.promptTokens || null,
      completionTokens: obs.usage?.completionTokens || null,
      totalTokens: obs.usage?.totalTokens || null,
    };
    result.latencyMs = obs.latency ? Math.round(obs.latency * 1000) : null;
  }

  return result;
}

async function main() {
  const traceId = process.argv[2];

  if (!traceId) {
    console.error("Usage: npx tsx scripts/fetch-trace.ts <trace-id>");
    process.exit(1);
  }

  const client = getClient();

  try {
    // Fetch trace
    const trace = await client.fetchTrace(traceId);

    // Fetch observations for this trace
    const observations = await client.fetchObservations({ traceId });

    const result = {
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
      observations: observations.data.map(formatObservation),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("Error fetching trace:", error);
    process.exit(1);
  } finally {
    await client.shutdownAsync();
  }
}

main();
