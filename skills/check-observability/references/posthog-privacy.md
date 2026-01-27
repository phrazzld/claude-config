# PostHog Privacy Checklist

When implementing PostHog, ensure these privacy protections are in place.

## Required Configuration

```typescript
posthog.init(POSTHOG_KEY, {
  api_host: '/ingest', // Use proxy to avoid ad blockers
  person_profiles: 'identified_only',

  // PRIVACY: Required masking
  mask_all_text: true, // Prevent autocapture text leakage

  // PRIVACY: Session recording masking
  session_recording: {
    maskAllInputs: true, // Mask all input values
  },

  // Pageview handling
  capture_pageview: false, // Manual for SPA
  capture_pageleave: true,

  // Autocapture (restricted)
  autocapture: {
    dom_event_allowlist: ['click', 'submit'],
    element_allowlist: ['button', 'a', 'input', 'form'],
  },
});
```

## User Identification

When integrating with Clerk (or other auth):

```typescript
// CORRECT: ID only, no PII
if (user) {
  posthog.identify(user.id);
} else {
  posthog.reset();
}

// WRONG: Sending PII
posthog.identify(user.id, {
  email: user.email,     // ❌ PII
  name: user.fullName,   // ❌ PII
});
```

**Rule:** Only send `user.id` for identification. No email, name, or other PII.

## Privacy Settings Rationale

| Setting | Purpose |
|---------|---------|
| `mask_all_text: true` | Prevents autocapture from sending button/link text that might contain PII |
| `maskAllInputs: true` | Session replays show `***` instead of actual input values |
| `person_profiles: 'identified_only'` | Don't create person profiles for anonymous users |

## Common Mistakes

1. **Sending PII to identify()** - Only use opaque IDs
2. **Missing mask_all_text** - Text content can leak via autocapture
3. **Missing maskAllInputs** - Session replays expose form data
4. **Using direct PostHog host** - Use `/ingest` proxy for ad blocker bypass

## Verification

After setup, verify in PostHog dashboard:
1. Events show masked text (`***`) not actual content
2. Session replays show masked inputs
3. Person profiles only show user ID, not email/name
