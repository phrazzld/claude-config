# RSS Feed Route

Next.js App Router route handler for RSS feed.

## app/changelog.xml/route.ts

```typescript
import { getReleases } from '@/lib/github-releases';

/**
 * RSS Feed for Changelog
 *
 * Serves an RSS 2.0 feed of releases.
 * Users can subscribe in their RSS readers.
 */
export async function GET() {
  try {
    const releases = await getReleases({ limit: 50 });

    const appName = process.env.NEXT_PUBLIC_APP_NAME || 'App';
    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://example.com';
    const description = process.env.NEXT_PUBLIC_APP_DESCRIPTION || 'Latest updates and improvements';

    const rss = generateRssFeed({
      title: `${appName} Changelog`,
      description,
      siteUrl,
      feedUrl: `${siteUrl}/changelog.xml`,
      releases,
    });

    return new Response(rss, {
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=300, s-maxage=300',
      },
    });
  } catch (error) {
    console.error('Error generating RSS feed:', error);

    return new Response(
      '<?xml version="1.0" encoding="UTF-8"?><error>Failed to generate feed</error>',
      {
        status: 500,
        headers: { 'Content-Type': 'application/xml' },
      }
    );
  }
}

interface FeedOptions {
  title: string;
  description: string;
  siteUrl: string;
  feedUrl: string;
  releases: Array<{
    tagName: string;
    name: string | null;
    body: string;
    publishedAt: string;
    htmlUrl: string;
  }>;
}

function generateRssFeed(options: FeedOptions): string {
  const { title, description, siteUrl, feedUrl, releases } = options;

  const items = releases
    .map((release) => {
      const itemTitle = release.name || release.tagName;
      const pubDate = new Date(release.publishedAt).toUTCString();

      return `    <item>
      <title>${escapeXml(itemTitle)}</title>
      <link>${escapeXml(release.htmlUrl)}</link>
      <guid isPermaLink="true">${escapeXml(release.htmlUrl)}</guid>
      <pubDate>${pubDate}</pubDate>
      <description><![CDATA[${release.body}]]></description>
    </item>`;
    })
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>${escapeXml(title)}</title>
    <link>${escapeXml(siteUrl)}/changelog</link>
    <description>${escapeXml(description)}</description>
    <language>en</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${escapeXml(feedUrl)}" rel="self" type="application/rss+xml"/>
${items}
  </channel>
</rss>`;
}

/**
 * Escape special XML characters
 */
function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
```

## Alternative: Atom Feed

If you prefer Atom format:

## app/changelog.xml/route.ts (Atom version)

```typescript
import { getReleases } from '@/lib/github-releases';

export async function GET() {
  const releases = await getReleases({ limit: 50 });

  const appName = process.env.NEXT_PUBLIC_APP_NAME || 'App';
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://example.com';

  const atom = `<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>${escapeXml(appName)} Changelog</title>
  <link href="${siteUrl}/changelog" rel="alternate"/>
  <link href="${siteUrl}/changelog.xml" rel="self"/>
  <id>${siteUrl}/changelog</id>
  <updated>${new Date().toISOString()}</updated>
${releases.map((release) => `  <entry>
    <title>${escapeXml(release.name || release.tagName)}</title>
    <link href="${release.htmlUrl}" rel="alternate"/>
    <id>${release.htmlUrl}</id>
    <published>${new Date(release.publishedAt).toISOString()}</published>
    <updated>${new Date(release.publishedAt).toISOString()}</updated>
    <content type="html"><![CDATA[${release.body}]]></content>
  </entry>`).join('\n')}
</feed>`;

  return new Response(atom, {
    headers: {
      'Content-Type': 'application/atom+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=300',
    },
  });
}

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
```

## Adding Feed Link to Head

In your layout or page, add the RSS feed link:

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  // ... other metadata
  alternates: {
    types: {
      'application/rss+xml': '/changelog.xml',
    },
  },
};
```

Or manually in the head:

```tsx
<link
  rel="alternate"
  type="application/rss+xml"
  title="Changelog RSS Feed"
  href="/changelog.xml"
/>
```

## Validation

Test your feed with:
- https://validator.w3.org/feed/
- Your favorite RSS reader (Feedly, NetNewsWire, etc.)

## Environment Variables

```bash
NEXT_PUBLIC_APP_NAME=MyApp
NEXT_PUBLIC_SITE_URL=https://myapp.com
NEXT_PUBLIC_APP_DESCRIPTION=Latest updates and improvements
```
