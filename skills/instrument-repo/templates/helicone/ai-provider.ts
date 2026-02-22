import { createAnthropic } from "@ai-sdk/anthropic";

const heliconeApiKey = process.env.HELICONE_API_KEY;

/**
 * Anthropic provider, optionally routed through Helicone for cost observability.
 * When HELICONE_API_KEY is set, requests go through the Helicone gateway
 * with product/environment tags. Falls back to direct Anthropic when unset.
 */
export const anthropic = heliconeApiKey
  ? createAnthropic({
      baseURL: "https://anthropic.helicone.ai/v1",
      headers: {
        "Helicone-Auth": `Bearer ${heliconeApiKey}`,
        "Helicone-Property-Product": "PRODUCT_NAME", // Replace with repo name
        "Helicone-Property-Environment": process.env.NODE_ENV ?? "development",
      },
    })
  : createAnthropic();
