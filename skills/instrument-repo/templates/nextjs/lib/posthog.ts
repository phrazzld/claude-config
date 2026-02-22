import posthog from "posthog-js";

export function initPostHog(): void {
  if (typeof window === "undefined") return;

  const apiKey = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  if (!apiKey) return;

  posthog.init(apiKey, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || "/ingest",
    ui_host: "https://us.posthog.com",
    capture_pageview: false,
    respect_dnt: true,
  });
}

export function trackEvent(
  name: string,
  properties?: Record<string, unknown>
): void {
  if (typeof window === "undefined") return;
  posthog.capture(name, properties);
}

export function identify(
  userId: string,
  traits?: Record<string, unknown>
): void {
  if (typeof window === "undefined") return;
  posthog.identify(userId, traits);
}

export function reset(): void {
  if (typeof window === "undefined") return;
  posthog.reset();
}

export { posthog as posthogClient };
