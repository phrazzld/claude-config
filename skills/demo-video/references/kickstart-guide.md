# Remotion Kickstart Guide

## Repo: jhartquist/claude-remotion-kickstart
- Use it when you want a ready-to-render demo scaffold fast.
- It includes sane defaults for fonts, layout, and rendering scripts.

## Pre-built Components You Can Reuse
- Title cards and section dividers.
- Caption overlays designed for narration sync.
- Screen frames / device shells for product UI.
- Simple chart and metric callouts.

## Transcript Synchronization
- Keep voiceover lines in a transcript file.
- Store timing in `timestamps.json` with `start`, `end`, `text`.
- Drive captions by mapping timestamps to frames using fps.
- Align scene boundaries to narration segments to reduce drift.

## Quick Start Commands
- Scaffold: `npx degit jhartquist/claude-remotion-kickstart demo-video`
- Install: `cd demo-video && pnpm install` (or `npm install`)
- Preview: `pnpm remotion preview`
- List comps: `pnpm remotion compositions`
- Render: `pnpm remotion render Demo out.mp4`
