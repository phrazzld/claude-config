#!/usr/bin/env npx tsx
/**
 * List or fetch prompts from Langfuse.
 *
 * Usage:
 *   npx tsx scripts/list-prompts.ts --name scry-intent-extraction
 *   npx tsx scripts/list-prompts.ts --name scry-intent-extraction --label production
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

function parseArgs(): { name?: string; label?: string } {
  const args = process.argv.slice(2);
  const result: { name?: string; label?: string } = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--name" && args[i + 1]) {
      result.name = args[i + 1];
      i++;
    } else if (args[i] === "--label" && args[i + 1]) {
      result.label = args[i + 1];
      i++;
    }
  }

  return result;
}

async function main() {
  const { name, label } = parseArgs();
  const client = getClient();

  try {
    if (name) {
      // Fetch specific prompt
      const prompt = await client.getPrompt(name, undefined, { label });

      const result = {
        name: prompt.name,
        version: prompt.version,
        labels: (prompt as any).labels || [],
        config: (prompt as any).config || {},
        prompt: prompt.prompt || String(prompt),
      };

      console.log(JSON.stringify(result, null, 2));
    } else {
      // No list API in SDK - provide guidance
      console.log(JSON.stringify({
        message: "Specify a prompt name to fetch details",
        usage: "npx tsx scripts/list-prompts.ts --name <prompt-name>",
        examples: [
          "npx tsx scripts/list-prompts.ts --name scry-intent-extraction",
          "npx tsx scripts/list-prompts.ts --name scry-concept-synthesis --label production",
        ],
        hint: "View all prompts in the Langfuse dashboard",
      }, null, 2));
    }
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  } finally {
    await client.shutdownAsync();
  }
}

main();
