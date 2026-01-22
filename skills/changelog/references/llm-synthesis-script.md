# LLM Release Notes Synthesis Script

Script that transforms technical changelog into user-friendly release notes using Gemini 3 Flash.

## scripts/synthesize-release-notes.mjs

```javascript
#!/usr/bin/env node
/**
 * Release Notes Synthesizer
 *
 * Transforms technical changelog into user-friendly release notes
 * using Gemini 3 Flash.
 *
 * Environment variables:
 * - GITHUB_TOKEN: GitHub API token (required)
 * - GEMINI_API_KEY: Gemini API key (required)
 * - RELEASE_VERSION: Version being released (optional, fetches latest if not set)
 * - RELEASE_NOTES: Raw release notes (optional, fetches from GitHub if not set)
 *
 * Configuration:
 * - .release-notes-config.yml in repo root
 */

import { readFileSync, existsSync } from 'fs';
import { load as loadYaml } from 'js-yaml';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GITHUB_REPOSITORY = process.env.GITHUB_REPOSITORY;

if (!GITHUB_TOKEN || !GEMINI_API_KEY) {
  console.error('Missing required environment variables: GITHUB_TOKEN, GEMINI_API_KEY');
  process.exit(1);
}

// Load app-specific configuration
function loadConfig() {
  const configPaths = [
    '.release-notes-config.yml',
    '.release-notes-config.yaml',
    '.release-notes.yml',
  ];

  for (const path of configPaths) {
    if (existsSync(path)) {
      const content = readFileSync(path, 'utf8');
      return loadYaml(content);
    }
  }

  // Default configuration
  return {
    app_name: 'the app',
    personality: 'professional and friendly',
    audience: 'users',
    tone_examples: [],
    avoid: ['technical jargon', 'commit hashes', 'internal code names'],
    categories: {
      feat: 'New Features',
      fix: 'Improvements',
      perf: 'Performance',
      chore: 'Behind the Scenes',
      refactor: 'Behind the Scenes',
      docs: 'Documentation',
      test: 'Quality',
    },
  };
}

// Get latest release from GitHub
async function getLatestRelease() {
  const res = await fetch(
    `https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/latest`,
    {
      headers: {
        Accept: 'application/vnd.github.v3+json',
        Authorization: `Bearer ${GITHUB_TOKEN}`,
      },
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch release: ${res.status}`);
  }

  return res.json();
}

// Call Gemini API
async function synthesizeWithGemini(technicalNotes, config) {
  const prompt = buildPrompt(technicalNotes, config);

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${GEMINI_API_KEY}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 2048,
        },
      }),
    }
  );

  if (!res.ok) {
    const error = await res.text();
    throw new Error(`Gemini API error: ${error}`);
  }

  const data = await res.json();
  return data.candidates[0].content.parts[0].text;
}

// Build the synthesis prompt
function buildPrompt(technicalNotes, config) {
  return `You are writing release notes for ${config.app_name}.

Your audience is: ${config.audience}
Your tone should be: ${config.personality}

${config.tone_examples?.length ? `Example phrases that match the desired tone:
${config.tone_examples.map(e => `- "${e}"`).join('\n')}` : ''}

AVOID:
${config.avoid.map(a => `- ${a}`).join('\n')}

TECHNICAL CHANGELOG:
${technicalNotes}

INSTRUCTIONS:
1. Transform each technical change into user-friendly language
2. Focus on user benefits, not technical details
3. Group related changes if they serve the same user goal
4. EVERY change must be included - even maintenance/chore commits should become "Behind-the-scenes improvements for reliability and performance"
5. Use active voice and present tense
6. Keep each item to 1-2 sentences max
7. Format with markdown (headers, bullet points)

REQUIRED OUTPUT FORMAT:
## What's New

[For feat: commits - user-facing features]

## Improvements

[For fix: and perf: commits - things that work better]

## Behind the Scenes

[For chore:, refactor:, build:, ci:, test: commits - grouped as general reliability improvements]

If a section would be empty, omit it entirely.
Do NOT include version numbers, dates, or commit hashes.
Do NOT use technical terms like API, SDK, webhook, endpoint, etc.
Write as if explaining to a friend who uses the product but isn't technical.`;
}

// Update GitHub release with synthesized notes
async function updateRelease(releaseId, synthesizedNotes, originalNotes) {
  // Preserve original notes in a collapsible section
  const body = `${synthesizedNotes}

<details>
<summary>Technical Details</summary>

${originalNotes}

</details>`;

  const res = await fetch(
    `https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/${releaseId}`,
    {
      method: 'PATCH',
      headers: {
        Accept: 'application/vnd.github.v3+json',
        Authorization: `Bearer ${GITHUB_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ body }),
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to update release: ${res.status}`);
  }

  return res.json();
}

// Main execution
async function main() {
  console.log('🚀 Synthesizing release notes...');

  const config = loadConfig();
  console.log(`📝 Config loaded for: ${config.app_name}`);

  // Get release info
  let release;
  if (process.env.RELEASE_VERSION && process.env.RELEASE_NOTES) {
    release = {
      id: null, // Will need to fetch
      tag_name: process.env.RELEASE_VERSION,
      body: process.env.RELEASE_NOTES,
    };
  } else {
    release = await getLatestRelease();
  }

  console.log(`📦 Processing release: ${release.tag_name}`);

  // Synthesize notes
  const synthesized = await synthesizeWithGemini(release.body, config);
  console.log('✨ Notes synthesized');

  // Update release if we have the ID
  if (release.id) {
    await updateRelease(release.id, synthesized, release.body);
    console.log('✅ Release updated');
  } else {
    // Need to fetch release ID first
    const latestRelease = await getLatestRelease();
    await updateRelease(latestRelease.id, synthesized, release.body);
    console.log('✅ Release updated');
  }

  // Output for debugging
  console.log('\n--- Synthesized Notes ---\n');
  console.log(synthesized);
}

main().catch((error) => {
  console.error('❌ Error:', error.message);
  process.exit(1);
});
```

## .release-notes-config.yml

```yaml
# App-specific configuration for release notes synthesis

# Name as it should appear in notes
app_name: "MyApp"

# Tone/personality for the writing
personality: "professional, friendly, confident"

# Who reads these notes?
audience: "small business owners and entrepreneurs"

# Example phrases that capture the desired tone
tone_examples:
  - "We made it faster to find what you need"
  - "Your dashboard now shows more detail at a glance"
  - "Getting started is now even simpler"

# Words/phrases to avoid
avoid:
  - Technical jargon (API, SDK, webhook, endpoint)
  - Git references (commit, merge, branch)
  - Internal code names
  - Version numbers in descriptions
  - Passive voice

# How to categorize different commit types
categories:
  feat: "New Features"
  fix: "Improvements"
  perf: "Performance"
  chore: "Behind the Scenes"
  refactor: "Behind the Scenes"
  docs: "Documentation"
  test: "Quality"
  build: "Behind the Scenes"
  ci: "Behind the Scenes"
```

## Dependencies

```bash
pnpm add -D js-yaml
```

## Testing Locally

```bash
# Set environment variables
export GITHUB_TOKEN=ghp_xxx
export GEMINI_API_KEY=xxx
export GITHUB_REPOSITORY=owner/repo

# Run synthesis
node scripts/synthesize-release-notes.mjs

# Or dry run (just print, don't update)
DRY_RUN=true node scripts/synthesize-release-notes.mjs
```

## Example Transformation

**Input (technical changelog):**
```
## [1.2.0] - 2026-01-20

### Features
* feat: add subscription pause endpoint (#123)
* feat(dashboard): implement usage charts

### Bug Fixes
* fix: resolve race condition in webhook handler
* fix(auth): correct token refresh timing

### Maintenance
* chore: upgrade Stripe SDK to v17
* refactor: simplify payment processing logic
* test: add integration tests for checkout
```

**Output (synthesized):**
```
## What's New

- **Pause your subscription anytime** — Need a break? You can now pause your subscription directly from your account settings.
- **See your usage at a glance** — Your dashboard now includes charts showing how you've been using the app over time.

## Improvements

- **More reliable payment processing** — Fixed an issue that occasionally caused payment confirmations to be delayed.
- **Smoother sign-in experience** — Resolved a timing issue that sometimes required signing in twice.

## Behind the Scenes

We've made improvements to our infrastructure for better reliability and performance.
```
