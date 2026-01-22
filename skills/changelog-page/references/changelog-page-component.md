# Changelog Page Component

Next.js App Router page component for displaying releases.

## app/changelog/page.tsx

```tsx
import { Metadata } from 'next';
import { Suspense } from 'react';
import {
  getReleases,
  groupReleasesByMinor,
  sortMinorVersions,
  formatReleaseDate,
} from '@/lib/github-releases';
import { parseMarkdown } from '@/lib/markdown';

export const metadata: Metadata = {
  title: 'Changelog',
  description: 'Latest updates and improvements',
  alternates: {
    types: {
      'application/rss+xml': '/changelog.xml',
    },
  },
};

// Revalidate every 5 minutes
export const revalidate = 300;

async function ReleasesList() {
  const releases = await getReleases();
  const grouped = groupReleasesByMinor(releases);
  const sortedVersions = sortMinorVersions(Object.keys(grouped));

  if (releases.length === 0) {
    return (
      <p className="text-muted-foreground">
        No releases yet. Check back soon!
      </p>
    );
  }

  return (
    <div className="space-y-16">
      {sortedVersions.map((minorVersion) => (
        <section key={minorVersion} id={minorVersion}>
          {/* Sticky minor version header */}
          <h2 className="text-xl font-semibold mb-6 sticky top-0 bg-background/95 backdrop-blur py-2 -mx-4 px-4 border-b">
            {minorVersion}
          </h2>

          <div className="space-y-10">
            {grouped[minorVersion].map((release) => (
              <article
                key={release.id}
                className="relative pl-6 border-l-2 border-border hover:border-primary transition-colors"
              >
                {/* Version indicator dot */}
                <div className="absolute -left-[5px] top-0 w-2 h-2 rounded-full bg-border" />

                <header className="mb-3">
                  <div className="flex items-baseline gap-3 flex-wrap">
                    <h3 className="font-medium text-lg">
                      {release.name || release.tagName}
                    </h3>
                    <span className="text-xs font-mono text-muted-foreground">
                      {release.tagName}
                    </span>
                  </div>
                  <time
                    dateTime={release.publishedAt}
                    className="text-sm text-muted-foreground"
                  >
                    {formatReleaseDate(release.publishedAt)}
                  </time>
                </header>

                {/* Release notes content */}
                <div
                  className="prose prose-sm dark:prose-invert max-w-none
                    prose-headings:text-base prose-headings:font-medium prose-headings:mt-4 prose-headings:mb-2
                    prose-p:my-2 prose-ul:my-2 prose-li:my-0"
                  dangerouslySetInnerHTML={{
                    __html: parseMarkdown(release.body),
                  }}
                />

                {/* Link to GitHub release */}
                <a
                  href={release.htmlUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block mt-4 text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  View on GitHub →
                </a>
              </article>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      {[1, 2, 3].map((i) => (
        <div key={i} className="space-y-3">
          <div className="h-6 w-20 bg-muted rounded" />
          <div className="pl-6 space-y-2">
            <div className="h-5 w-48 bg-muted rounded" />
            <div className="h-4 w-32 bg-muted rounded" />
            <div className="h-20 w-full bg-muted rounded" />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ChangelogPage() {
  const appName = process.env.NEXT_PUBLIC_APP_NAME || 'this app';

  return (
    <main className="max-w-3xl mx-auto py-12 px-4 sm:px-6">
      {/* Header */}
      <header className="mb-12">
        <h1 className="text-3xl font-bold tracking-tight mb-3">
          Changelog
        </h1>
        <p className="text-muted-foreground text-lg">
          Latest updates and improvements to {appName}.
        </p>
        <div className="mt-4 flex items-center gap-4 text-sm">
          <a
            href="/changelog.xml"
            className="text-primary hover:underline inline-flex items-center gap-1"
          >
            <RssIcon className="w-4 h-4" />
            RSS Feed
          </a>
        </div>
      </header>

      {/* Releases list */}
      <Suspense fallback={<LoadingSkeleton />}>
        <ReleasesList />
      </Suspense>
    </main>
  );
}

// Simple RSS icon component
function RssIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="M4 11a9 9 0 0 1 9 9" />
      <path d="M4 4a16 16 0 0 1 16 16" />
      <circle cx="5" cy="19" r="1" />
    </svg>
  );
}
```

## lib/markdown.ts

Simple markdown parser (or use a library like `marked` or `remark`):

```typescript
/**
 * Parse markdown to HTML
 *
 * For a simple changelog, basic parsing is sufficient.
 * For complex markdown, consider using 'marked' or 'remark'.
 */
export function parseMarkdown(markdown: string): string {
  if (!markdown) return '';

  let html = markdown
    // Escape HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Headers
    .replace(/^### (.*$)/gim, '<h4>$1</h4>')
    .replace(/^## (.*$)/gim, '<h3>$1</h3>')
    .replace(/^# (.*$)/gim, '<h2>$1</h2>')
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Code
    .replace(/`(.*?)`/g, '<code>$1</code>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    // Unordered lists
    .replace(/^\s*[-*]\s+(.*)$/gim, '<li>$1</li>')
    // Wrap consecutive <li> in <ul>
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // Paragraphs (double newlines)
    .replace(/\n\n/g, '</p><p>')
    // Single newlines to <br> within paragraphs
    .replace(/\n/g, '<br>');

  // Wrap in paragraph if not starting with block element
  if (!html.startsWith('<h') && !html.startsWith('<ul') && !html.startsWith('<p')) {
    html = `<p>${html}</p>`;
  }

  return html;
}
```

## Alternative: Using a Markdown Library

For more robust parsing:

```bash
pnpm add marked
```

```typescript
// lib/markdown.ts
import { marked } from 'marked';

// Configure marked
marked.setOptions({
  gfm: true,
  breaks: true,
});

export function parseMarkdown(markdown: string): string {
  if (!markdown) return '';
  return marked.parse(markdown) as string;
}
```

## Styling Notes

The component uses Tailwind CSS classes. Key considerations:

1. **Prose classes** - Uses `@tailwindcss/typography` for markdown content
2. **Dark mode** - Supports `dark:` variants
3. **Sticky headers** - Minor version headers stick during scroll
4. **Timeline style** - Left border creates visual timeline

### Required Tailwind Plugin

```bash
pnpm add -D @tailwindcss/typography
```

```javascript
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
```

## Customization Points

- **Colors**: Use your design system's color tokens
- **Typography**: Adjust prose styles to match app
- **Spacing**: Modify padding/margins as needed
- **Animations**: Add or remove transitions
