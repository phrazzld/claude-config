# GitHub Releases Client

TypeScript client for fetching releases from GitHub API.

## lib/github-releases.ts

```typescript
/**
 * GitHub Releases API Client
 *
 * Fetches releases from GitHub and provides utilities for
 * grouping and formatting.
 */

export interface Release {
  id: number;
  tagName: string;
  name: string | null;
  body: string;
  publishedAt: string;
  htmlUrl: string;
  prerelease: boolean;
  draft: boolean;
}

export interface GroupedReleases {
  [minorVersion: string]: Release[];
}

// Environment validation
function getGitHubRepo(): string {
  const repo = process.env.GITHUB_REPO;
  if (!repo) {
    throw new Error('GITHUB_REPO environment variable is required');
  }
  return repo;
}

/**
 * Fetch releases from GitHub API
 *
 * @param options.includePrereleases - Include prerelease versions (default: false)
 * @param options.includeDrafts - Include draft releases (default: false)
 * @param options.limit - Maximum number of releases to fetch (default: 100)
 */
export async function getReleases(options?: {
  includePrereleases?: boolean;
  includeDrafts?: boolean;
  limit?: number;
}): Promise<Release[]> {
  const { includePrereleases = false, includeDrafts = false, limit = 100 } = options ?? {};

  const res = await fetch(
    `https://api.github.com/repos/${getGitHubRepo()}/releases?per_page=${limit}`,
    {
      headers: {
        Accept: 'application/vnd.github.v3+json',
        // Optional: add token for higher rate limits (60/hr unauthenticated, 5000/hr authenticated)
        ...(process.env.GITHUB_TOKEN && {
          Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
        }),
      },
      // Next.js cache configuration
      next: { revalidate: 300 }, // Revalidate every 5 minutes
    }
  );

  if (!res.ok) {
    if (res.status === 404) {
      throw new Error(`Repository not found: ${getGitHubRepo()}`);
    }
    if (res.status === 403) {
      throw new Error('GitHub API rate limit exceeded');
    }
    throw new Error(`GitHub API error: ${res.status}`);
  }

  const data = await res.json();

  // Transform and filter
  const releases: Release[] = data
    .map((release: any) => ({
      id: release.id,
      tagName: release.tag_name,
      name: release.name,
      body: release.body || '',
      publishedAt: release.published_at,
      htmlUrl: release.html_url,
      prerelease: release.prerelease,
      draft: release.draft,
    }))
    .filter((release: Release) => {
      if (!includePrereleases && release.prerelease) return false;
      if (!includeDrafts && release.draft) return false;
      return true;
    });

  return releases;
}

/**
 * Group releases by minor version
 *
 * v1.2.3 -> v1.2
 * v2.0.0 -> v2.0
 */
export function groupReleasesByMinor(releases: Release[]): GroupedReleases {
  return releases.reduce((acc, release) => {
    // Extract minor version: v1.2.3 -> v1.2, 1.2.3 -> v1.2
    const match = release.tagName.match(/^v?(\d+\.\d+)/);
    const minorVersion = match ? `v${match[1]}` : 'other';

    if (!acc[minorVersion]) {
      acc[minorVersion] = [];
    }
    acc[minorVersion].push(release);

    return acc;
  }, {} as GroupedReleases);
}

/**
 * Get a single release by tag
 */
export async function getReleaseByTag(tag: string): Promise<Release | null> {
  const res = await fetch(
    `https://api.github.com/repos/${getGitHubRepo()}/releases/tags/${tag}`,
    {
      headers: {
        Accept: 'application/vnd.github.v3+json',
        ...(process.env.GITHUB_TOKEN && {
          Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
        }),
      },
      next: { revalidate: 300 },
    }
  );

  if (!res.ok) {
    if (res.status === 404) return null;
    throw new Error(`GitHub API error: ${res.status}`);
  }

  const data = await res.json();

  return {
    id: data.id,
    tagName: data.tag_name,
    name: data.name,
    body: data.body || '',
    publishedAt: data.published_at,
    htmlUrl: data.html_url,
    prerelease: data.prerelease,
    draft: data.draft,
  };
}

/**
 * Format a date for display
 */
export function formatReleaseDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Sort minor versions in descending order
 *
 * ['v1.0', 'v2.1', 'v1.2'] -> ['v2.1', 'v1.2', 'v1.0']
 */
export function sortMinorVersions(versions: string[]): string[] {
  return versions.sort((a, b) => {
    // Handle 'other' category
    if (a === 'other') return 1;
    if (b === 'other') return -1;

    // Compare semantically
    return b.localeCompare(a, undefined, { numeric: true });
  });
}
```

## Usage Example

```typescript
import {
  getReleases,
  groupReleasesByMinor,
  sortMinorVersions,
  formatReleaseDate,
} from '@/lib/github-releases';

// In a Server Component
export default async function ChangelogPage() {
  const releases = await getReleases();
  const grouped = groupReleasesByMinor(releases);
  const sortedVersions = sortMinorVersions(Object.keys(grouped));

  return (
    <div>
      {sortedVersions.map((version) => (
        <section key={version}>
          <h2>{version}</h2>
          {grouped[version].map((release) => (
            <article key={release.id}>
              <h3>{release.name || release.tagName}</h3>
              <time>{formatReleaseDate(release.publishedAt)}</time>
              <div>{release.body}</div>
            </article>
          ))}
        </section>
      ))}
    </div>
  );
}
```

## Environment Variables

```bash
# Required
GITHUB_REPO=owner/repo  # e.g., "acme/myapp"

# Optional (for higher rate limits)
GITHUB_TOKEN=ghp_xxx
```

## Rate Limits

- **Unauthenticated:** 60 requests/hour
- **Authenticated:** 5,000 requests/hour

For public changelog pages with caching (5 min revalidation), unauthenticated is usually sufficient. Add `GITHUB_TOKEN` if you see rate limit errors.
