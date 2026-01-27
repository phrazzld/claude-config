# ElevenLabs Voices (Quick Reference)

## Popular Starter Voices
- `adam`: clear, professional, neutral demo narration (default)
- `rachel`: warm, friendly female; onboarding, product tours
- `josh`: deep male; trailers, gravitas, brand moments
- `bella`: bright female; energetic promos, social clips
- `antoni`: confident male; explainers, sales demos

## Choosing a Voice
- Demos + tutorials: `adam`, `rachel`
- Bold intros + teasers: `josh`, `antoni`
- Short marketing beats: `bella`
- When in doubt: start with `adam`, then A/B with `rachel`

## Finding Voice IDs via API
Run this to list voices and IDs:

```bash
curl -s https://api.elevenlabs.io/v1/voices \
  -H "xi-api-key: $ELEVENLABS_API_KEY" | jq '.voices[] | {name, voice_id}'
```

Use either the `voice_id` or a known name in `--voice`.

## Custom Voices
- ElevenLabs supports custom voice cloning and uploads.
- Create in the ElevenLabs dashboard, then use returned `voice_id`.
