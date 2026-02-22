"use client";

import { Suspense, useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";

import { posthogClient } from "@/lib/posthog";

function PostHogPageviewInner(): null {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const query = searchParams.toString();

  useEffect(() => {
    if (!pathname) return;
    if (!process.env.NEXT_PUBLIC_POSTHOG_KEY) return;

    let url = window.location.origin + pathname;
    if (query) url += `?${query}`;

    posthogClient.capture("$pageview", { $current_url: url });
  }, [pathname, query]);

  return null;
}

export function PostHogPageview() {
  return (
    <Suspense fallback={null}>
      <PostHogPageviewInner />
    </Suspense>
  );
}
