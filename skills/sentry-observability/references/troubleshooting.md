# Sentry Troubleshooting

Common issues and their solutions.

## Quick Diagnosis

Run the verification script first:

```bash
~/.claude/skills/sentry-observability/scripts/verify_setup.sh
```

## Common Issues

### Minified Stack Traces

**Symptom:** Stack traces show minified/obfuscated code instead of original source

**Cause:** Source maps not uploading to Sentry

**Fix:**
1. Install Vercel Integration (recommended)
   ```
   https://vercel.com/integrations/sentry
   ```
2. Or ensure SENTRY_AUTH_TOKEN is set for manual upload

**Verify:**
```bash
# Check for recent releases with source maps
sentry-cli releases list
```

### Errors Not Appearing in Dashboard

**Symptom:** Errors occur but don't show up in Sentry

**Causes & Fixes:**

1. **DSN not set**
   ```bash
   # Check DSN in environment
   echo $NEXT_PUBLIC_SENTRY_DSN
   echo $SENTRY_DSN
   ```

2. **DSN mismatch between environments**
   - Verify DSN is same in .env.local AND Vercel deployment

3. **Error being filtered**
   - Check `ignoreErrors` configuration
   - Check `beforeSend` returning null

4. **Network issues**
   - Check browser console for Sentry errors
   - Verify DSN endpoint is accessible

### "Release not found" Errors

**Symptom:** Sentry shows "Release not found" for source maps

**Cause:** Manual token setup with mismatched release IDs

**Fix:** Switch to Vercel Integration (auto-matches release IDs)

### High Quota Usage

**Symptom:** Approaching or exceeding free tier limits

**Causes & Fixes:**

1. **High sample rates**
   ```bash
   # Lower sample rates
   SENTRY_TRACES_SAMPLE_RATE=0.1
   NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0
   ```

2. **Noisy errors**
   - Add to `ignoreErrors` configuration
   - Or resolve the underlying issues

3. **Session Replay overhead**
   - Disable routine recording
   - Keep only error recording

### Session Replay Not Working

**Symptom:** No replay available for errors

**Causes & Fixes:**

1. **Sample rate is 0**
   ```bash
   NEXT_PUBLIC_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0
   ```

2. **Replay integration not added**
   ```typescript
   integrations: [
     Sentry.replayIntegration(),
   ],
   ```

3. **Client-side only errors**
   - Ensure error occurs in browser, not just server

### Email Alerts Not Working

**Symptom:** Errors occur but no email notifications

**Causes & Fixes:**

1. **No alert rules configured**
   ```bash
   # Create alert rule
   ~/.claude/skills/sentry-observability/scripts/create_alert.sh \
     --name "New Errors" --type issue
   ```

2. **Email notifications disabled**
   - Check Sentry Settings > Notifications

3. **Alert conditions not met**
   - Review alert rule conditions in dashboard

### Preview Deployments Not Tracked

**Symptom:** Preview deployments don't send errors to Sentry

**Cause:** Missing environment variables for preview

**Fix:** Vercel Integration sets these automatically. For manual setup:
- Ensure all SENTRY_* vars are set for "Preview" environment in Vercel

### Server-Side Errors Missing

**Symptom:** Client errors appear but server errors don't

**Causes & Fixes:**

1. **Missing server DSN**
   ```bash
   # Ensure both DSNs are set
   NEXT_PUBLIC_SENTRY_DSN=...  # Client
   SENTRY_DSN=...              # Server
   ```

2. **Server config not loaded**
   - Verify `sentry.server.config.ts` exists
   - Check it's imported in instrumentation

### Slow Page Load

**Symptom:** Pages load slowly after adding Sentry

**Causes & Fixes:**

1. **High trace sample rate**
   ```bash
   SENTRY_TRACES_SAMPLE_RATE=0.1  # Lower from 1.0
   ```

2. **Replay capturing too much**
   - Reduce session sample rate
   - Disable routine recording

## Troubleshooting Table

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Minified stack traces | Source maps not uploading | Install Vercel Integration |
| Errors not appearing | DSN mismatch | Verify DSN in all environments |
| "release not found" | Manual token setup | Switch to Vercel Integration |
| High quota usage | Excessive sampling | Lower sample rates |
| Session Replay not working | Sample rate = 0 | Set ERROR_SAMPLE_RATE=1.0 |
| Email alerts not working | Alert not configured | Run create_alert.sh |
| Preview not tracked | Missing env vars | Use Vercel Integration |

## Getting Help

1. Check Sentry status: https://status.sentry.io/
2. Sentry documentation: https://docs.sentry.io/platforms/javascript/guides/nextjs/
3. Run verification: `verify_setup.sh`
