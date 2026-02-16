---
name: brand-assets
description: |
  Generate branded visual assets (OG cards, social images, blog headers)
  from brand.yaml. Replaces manual image creation with template-driven rendering.
argument-hint: "<template> --title \"...\" [options]"
effort: medium
---

# /brand-assets

Generate branded visual assets from templates.

## What This Does

Renders 1200x630 PNG images using brand tokens from `brand.yaml`. Templates consume the brand palette, typography, and identity for consistent visuals.

## Available Templates

| Template | Use Case |
|----------|----------|
| `og-blog` | Blog post OG cards |
| `og-product` | Product announcement cards |
| `og-changelog` | Version release cards |
| `og-default` | Generic fallback OG card |
| `social-announce` | Social media announcements |
| `social-quote` | Quote cards for social |
| `blog-header` | Blog post hero images |
| `launch-hero` | Product launch hero images |

## Process

1. Ensure `brand.yaml` exists in project root (run `/brand-compile` first if needed)
2. Determine which assets are needed from context:
   - Blog post → `og-blog` + `blog-header`
   - Product launch → `launch-hero` + `social-announce` + `og-product`
   - Changelog → `og-changelog`
   - General → `og-default`
3. Render each asset:
   ```bash
   node ~/Development/brand-kit/dist/src/cli.js render og-blog \
     --title "Post Title" \
     --author "Author Name" \
     --date "2026-02-12" \
     --out ./public/og-blog.png
   ```
4. For bulk generation:
   ```bash
   node ~/Development/brand-kit/dist/src/cli.js render-all --out ./public/brand-assets
   ```

## Template Options

All templates accept:
- `--title "..."` (required)
- `--subtitle "..."`
- `--author "..."`
- `--date "..."`
- `--version "..."`
- `--out file.png` (required)

## Context-Aware Generation

When invoked without arguments, infer what's needed:
- If recent `git log` shows a version tag → render `og-changelog`
- If a blog post draft exists → render `og-blog` + `blog-header`
- If `product-hunt-kit.md` exists → render `launch-hero` + `social-announce`
- Otherwise → render `og-default`

## Related Skills

- `/brand-compile` — Compile brand.yaml to tokens (prerequisite)
- `/og-card` — Legacy card generation (superseded)
- `/og-hero-image` — AI-generated hero images (complementary)
- `/launch-assets` — Full launch asset orchestration
