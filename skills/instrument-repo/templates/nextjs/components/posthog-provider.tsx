"use client";

import type { ReactNode } from "react";
import { useEffect, useState } from "react";

import { PostHogProvider as BaseProvider } from "posthog-js/react";

import { initPostHog, posthogClient } from "@/lib/posthog";
import { PostHogPageview } from "@/components/posthog-pageview";

interface Props {
  children: ReactNode;
}

export function PostHogProvider({ children }: Props): ReactNode {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    initPostHog();
    queueMicrotask(() => setReady(true));
  }, []);

  return (
    <BaseProvider client={posthogClient}>
      {ready && <PostHogPageview />}
      {children}
    </BaseProvider>
  );
}
