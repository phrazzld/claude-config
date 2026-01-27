# Remotion Patterns

## Basic Composition Structure
- A composition is a React component rendered over frames.
- Define it in `Root.tsx` via `<Composition ... component={Demo} />`.
- Use `useCurrentFrame()` + `useVideoConfig()` to drive animation.
- Convert seconds to frames with `Math.round(seconds * fps)`.

## Timeline and Sequence Patterns
- Model each scene as a `Sequence` with explicit duration.
- Keep durations in constants so edits are cheap.
- Prefer scene components like `TitleScene`, `FeatureScene`, `EndCard`.
- Avoid temporal decomposition in callers; centralize in one timeline.

## Screen Capture Integration
- Treat captures as assets: `.png`, `.mp4`, or image sequences.
- Use `<Img />` for stills and `<OffthreadVideo />` for recordings.
- Normalize resolution up front; animation math gets simpler.
- Consider pre-trimming with ffmpeg so Remotion stays declarative.

## Voiceover Sync with timestamps.json
- Store narration timing in `timestamps.json`:
- Each entry should include `start`, `end`, and `text`.
- Map timestamps to frames, then render captions conditionally.
- Keep caption logic pure: `frame >= startF && frame <= endF`.

## Common Compositions
- Title slides: big type, short duration, light motion.
- Code blocks: monospace, stable layout, highlight deltas only.
- Captions: bottom safe-area, high contrast, max two lines.
- Feature walkthroughs: zoom + pan on the product, not the UI chrome.

## Export Settings by Platform
- YouTube / web: 1920x1080, 30fps, H.264.
- Shorts / reels: 1080x1920, 30fps, H.264.
- Product teaser: 1440x810, 30fps, H.264, higher bitrate.
- Example: `npx remotion render Demo out.mp4 --codec=h264 --crf=18`
