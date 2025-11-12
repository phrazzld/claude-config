---
description: Triage production errors using Sentry/Vercel CLI, identify highest priority issue, launch debug agents, propose fix
---

Access production error monitoring, identify the most critical error, investigate with parallel debug agents, and propose a fix.

# TRIAGE

> **THE PRODUCTION PRINCIPLE**
> - Users don't care about technical debt. They care about broken features.
> - Every minute a production error persists costs trust, revenue, reputation.
> - Triage isn't optional—it's the immune system of your application.
> - Fix the bleed first, then find the cause, then prevent recurrence.

Production is on fire. 47 errors in the last hour. Users reporting issues. You're the ER surgeon who's triaged 200+ production incidents. Let's identify the highest-impact error, understand it completely, and fix it within 30 minutes. Every error resolved prevents 100+ users from hitting the same issue tomorrow.

## Your Mission

Access production monitoring systems (Sentry, Vercel), analyze recent errors, identify the single highest priority issue, launch parallel debug agents to investigate, and propose a fix for approval.

## The Triage Protocol

### Phase 1: Access Production Systems

**1.1 Sentry CLI - Primary Error Source**

```bash
# Check Sentry CLI availability
which sentry-cli || echo "Install: curl -sL https://sentry.io/get-cli/ | bash"

# List recent issues (last 24 hours, production environment)
sentry-cli issues list \
  --status unresolved \
  --environment production \
  --max-rows 50

# Get detailed issue data (event count, users affected, last seen)
sentry-cli api /projects/$SENTRY_ORG/$SENTRY_PROJECT/issues/ \
  -X GET \
  -d '{"statsPeriod": "24h", "environment": "production"}'

# Fetch full context for specific issue
sentry-cli api /issues/$ISSUE_ID/events/latest/ -X GET

# Get related deployment/release info
sentry-cli api /organizations/$SENTRY_ORG/releases/ -X GET
```

**Environment variables needed**:
```bash
# Load from .env.local or environment
SENTRY_AUTH_TOKEN    # From Vercel Integration or manual setup
SENTRY_ORG           # Organization slug
SENTRY_PROJECT       # Project slug
```

**1.2 Vercel CLI - Deployment & Log Correlation**

```bash
# Check recent production deployments
vercel ls --prod

# Get logs from production (last 1 hour)
vercel logs --prod --since 1h

# Check specific deployment logs (if error correlates to recent deploy)
vercel logs $DEPLOYMENT_URL --since 30m

# Get deployment metadata
vercel inspect $DEPLOYMENT_URL --prod
```

**1.3 Future: Grafana/OpenTelemetry (Prepare for)**

```bash
# When implemented, query traces and metrics
# grafana-cli traces query --from=-1h --filter="error=true"
# grpcurl -d '{"query": "error.type != nil"}' otlp-endpoint:4317 list

# For now: Note if OTel instrumentation exists in codebase
# Search for: @opentelemetry/*, instrumentation.ts, spectacle
```

**1.4 Application Logs (Pino/Winston - if consolidated)**

```bash
# If using structured logging, search for recent errors
# Example for Pino JSON logs:
# cat logs/production.log | grep '"level":50' | tail -20  # level 50 = error

# If using Vercel logs (temporary until Pino/Grafana consolidated):
# Already fetched in step 1.2
```

---

### Phase 2: Error Analysis & Prioritization

**2.1 Scoring Algorithm**

For each error, calculate priority score:

```
Priority Score = (
  Event Count Weight       × Event Count +
  User Impact Weight       × Unique Users Affected +
  Severity Weight          × Severity Multiplier +
  Recency Weight           × Recency Multiplier +
  Environment Weight       × Environment Multiplier
)

Weights (tunable):
- Event Count Weight: 1.0
- User Impact Weight: 5.0     # Users matter more than raw events
- Severity Weight: 3.0
- Recency Weight: 2.0
- Environment Weight: 4.0      # Production > preview > dev

Multipliers:
Severity:
  - fatal/critical: 10
  - error: 5
  - warning: 1
  - info: 0

Recency (first seen):
  - Last 1 hour: 10
  - Last 6 hours: 5
  - Last 24 hours: 2
  - Older: 1

Environment:
  - production: 10
  - preview: 2
  - development: 0.5
```

**2.2 Select Highest Priority Error**

- Sort issues by priority score
- Select #1 highest priority
- If tied, prefer:
  1. Production over preview
  2. More users affected
  3. More recent first occurrence

**2.3 Extract Full Context**

For the highest priority error, gather:

```bash
# Sentry context
- Error message (exact text)
- Stack trace (full, with source maps)
- Breadcrumbs (user actions leading to error)
- Environment context (browser, OS, runtime version)
- Release/deployment SHA
- Tags (custom tags set in app)
- User context (PII-redacted: user ID, session ID, not email)

# Deployment correlation
- Which deployment introduced this error?
- Git commit SHA
- Deployment timestamp
- Previous deployment SHA (for comparison)

# Frequency data
- Event count (last 1h, 6h, 24h)
- Unique users affected
- First seen timestamp
- Last seen timestamp
- Trending up or down?

# Related issues
- Similar errors in same release
- Errors from same code path
- Errors with same root cause
```

---

### Phase 3: Report Critical Error

**Present comprehensive error report to user:**

```markdown
## 🚨 HIGHEST PRIORITY PRODUCTION ERROR

**Issue ID**: SENTRY-1234
**Severity**: [ERROR/FATAL/WARNING]
**Priority Score**: 247 (out of ~500 max)

---

### Summary

**Error**: [Exact error message]
**Location**: [File:line from stack trace top frame]
**Environment**: production
**First Seen**: 2025-11-12 14:23:15 UTC (2 hours ago)
**Last Seen**: 2025-11-12 16:45:32 UTC (3 minutes ago)

---

### Impact

- **Event Count**: 142 events (last 24h)
- **Users Affected**: 23 unique users
- **Trend**: ⬆️ Increasing (47 events in last hour alone)

---

### Stack Trace

```
Error: Cannot read property 'id' of undefined
  at getUserProfile (src/services/user.ts:45:12)
  at ProfilePage (src/app/profile/page.tsx:23:8)
  at renderComponent (node_modules/react-dom/...)
  ...
```

---

### Deployment Context

**Introduced By**: Deployment abc123 (git SHA: def456)
**Deployed**: 2025-11-12 14:15:00 UTC (2h 30m ago)
**Previous Deploy**: xyz789 (no errors from this code path)

**Recent Changes** (commits between xyz789...def456):
- feat: add user profile settings (def456)
- refactor: update user service API (bcd234)

---

### Breadcrumbs (User Actions Before Error)

1. Navigation: /dashboard → /profile
2. API Call: GET /api/user/settings (200 OK)
3. Click: "Edit Profile" button
4. **Error**: Cannot read property 'id' of undefined

---

### Related Issues

- Similar error in /api/user/preferences (12 events)
- Same root cause suspected (user object structure change)

---

### Environment Details

- Browser: Chrome 120 (83% of errors), Safari 17 (17%)
- OS: macOS (67%), Windows (33%)
- Runtime: Node 22.15 (serverless function)

---
```

---

### Phase 4: Launch Debug Agents (Parallel)

**4.1 Agent Selection Based on Error Type**

Determine which specialized agents to launch:

```
Error Type Decision Tree:

Is this a TypeError/ReferenceError?
├─ YES → Launch pattern-recognition-specialist (find null/undefined patterns)
│         Launch git-history-analyzer (recent type changes)
│
└─ NO → Is this a performance error (timeout, slow response)?
    ├─ YES → Launch performance-oracle (identify bottleneck)
    │         Launch git-history-analyzer (recent changes)
    │
    └─ NO → Is this a database/data error?
        ├─ YES → Launch data-integrity-guardian (check migrations, schema)
        │         Launch pattern-recognition-specialist (find similar queries)
        │
        └─ NO → Generic investigation
                Launch pattern-recognition-specialist (code analysis)
                Launch git-history-analyzer (recent changes)
```

**4.2 Always Launch (for all errors)**

```
Task git-history-analyzer("Analyze git history around error introduction")
  Prompt:
  - Analyze commits between [previous-deploy-sha]...[current-deploy-sha]
  - Focus on files in stack trace: [affected files]
  - Identify changes that could cause: [error message]
  - Report: specific commit, code change, why it likely caused error
```

**4.3 Conditionally Launch (based on error type)**

**For null/undefined errors (TypeError, ReferenceError)**:
```
Task pattern-recognition-specialist("Find null safety patterns")
  Prompt:
  - Search codebase for similar patterns to: [error location]
  - Identify missing null checks, optional chaining opportunities
  - Find related code that handles same data structure correctly
  - Report: code smell, pattern violation, suggested fix
```

**For performance errors (timeouts, high latency)**:
```
Task performance-oracle("Identify performance bottleneck")
  Prompt:
  - Analyze code path: [stack trace]
  - Look for: N+1 queries, missing pagination, inefficient algorithms
  - Check recent changes to: database queries, API calls, loops
  - Report: bottleneck location, performance impact, optimization strategy
```

**For data/schema errors (validation, constraint violations)**:
```
Task data-integrity-guardian("Check data consistency")
  Prompt:
  - Analyze database migrations since: [previous deploy]
  - Check schema changes affecting: [affected tables/fields]
  - Verify data constraints, foreign keys, validations
  - Report: migration issue, data inconsistency, fix strategy
```

**For authentication/authorization errors**:
```
Task security-sentinel("Review auth implementation")
  Prompt:
  - Analyze authentication flow in: [affected route]
  - Check for: missing middleware, incorrect permissions, token issues
  - Review recent changes to: auth logic, middleware, guards
  - Report: auth gap, security implication, fix approach
```

**4.4 Specialized Code Review Agent**

```
Task general-purpose("Deep code review of affected files")
  Prompt:
  - Read files from stack trace: [file1, file2, file3]
  - Understand error context: [error message + breadcrumbs]
  - Identify root cause by examining code
  - Compare with recent git changes
  - Propose minimal fix
```

**4.5 Execute Parallel Agents**

Launch all selected agents in **single message** (parallel execution):

```
# Example for TypeError error:

Task git-history-analyzer("Analyze commits introducing error")
Task pattern-recognition-specialist("Find null safety patterns")
Task general-purpose("Review affected files for root cause")
```

---

### Phase 5: Synthesize & Propose Fix

**5.1 Aggregate Agent Findings**

Wait for all agents to complete, then synthesize:

```markdown
## Debug Agent Report

### Git History Analysis
[Summary from git-history-analyzer agent]
- Identified commit: def456
- Code change: Refactored getUserProfile() to use new API response
- Root cause: API now returns { data: { user: {...} } } instead of { user: {...} }

### Pattern Recognition
[Summary from pattern-recognition-specialist agent]
- Found 12 similar patterns in codebase handling API responses
- 8 of them properly check for nested structure
- 4 are vulnerable to same issue (potential future errors)

### Code Review
[Summary from general-purpose agent]
- Root cause confirmed in src/services/user.ts:45
- Missing null check after API response destructuring
- Fix: Add optional chaining or validate response structure
```

**5.2 Root Cause Analysis**

Synthesize agent findings into clear root cause:

```markdown
## Root Cause Analysis

**What**: TypeError - Cannot read property 'id' of undefined
**Where**: src/services/user.ts:45 (getUserProfile function)
**Why**: API response structure changed in commit def456, but consuming code wasn't updated
**When**: Triggered when users navigate to /profile after logging in

**Failure Mechanism**:
1. Backend API changed response format: `{ user: {...} }` → `{ data: { user: {...} } }`
2. Frontend code still expects `response.user` directly
3. Accessing `response.user.id` when `response.user` is undefined
4. No defensive checks or TypeScript type guards

**Why Didn't Tests Catch This?**
- API mocks in tests still used old response format
- No integration tests covering full user profile flow
- TypeScript types not updated (or not strict enough)
```

**5.3 Propose Fix**

Present concrete fix with code changes:

```markdown
## Proposed Fix

**Strategy**: Update code to handle new API response structure + add defensive checks

**Files to Change**:
1. src/services/user.ts:45 - Update response handling
2. src/types/api.ts - Update TypeScript types
3. tests/services/user.test.ts - Update mocks

**Code Changes**:

### File 1: src/services/user.ts

```typescript
// BEFORE (broken):
export async function getUserProfile(userId: string) {
  const response = await fetch(`/api/user/${userId}`);
  const data = await response.json();
  return data.user; // ❌ Assumes user is at top level
}

// AFTER (fixed):
export async function getUserProfile(userId: string) {
  const response = await fetch(`/api/user/${userId}`);
  const json = await response.json();

  // ✅ Handle new nested structure + defensive checks
  if (!json.data || !json.data.user) {
    throw new Error('Invalid user response structure');
  }

  return json.data.user;
}
```

### File 2: src/types/api.ts

```typescript
// Update type definition to match new API
export interface UserProfileResponse {
  data: {
    user: User;
  };
}
```

### File 3: tests/services/user.test.ts

```typescript
// Update mocks to match new structure
const mockResponse = {
  data: {
    user: { id: '123', name: 'Test User' }
  }
};
```

**Testing Plan**:
1. Add test case for missing `data` field (error handling)
2. Add test case for missing `user` field (error handling)
3. Verify existing tests pass with updated mocks
4. Manual test: Navigate to /profile after deploy

**Rollout Strategy**:
- Create fix in new branch: `fix/user-profile-undefined-error`
- Deploy to preview environment first
- Test with `/test-error` route + manual QA
- Deploy to production via fast-follow release

**Prevent Recurrence**:
- Add integration test covering full profile flow
- Enable TypeScript strict mode (strictNullChecks)
- Add API contract testing (validate response structure)
- Document API response format changes in CHANGELOG
```

**5.4 Ask for Approval**

```markdown
---

## Next Steps

**Option 1**: Approve fix and implement immediately
**Option 2**: Request modifications to proposed fix
**Option 3**: Investigate further before fixing

Which option would you like to proceed with?
```

---

## CLI Commands Reference

### Sentry CLI Quick Reference

```bash
# Authentication (one-time setup)
export SENTRY_AUTH_TOKEN="sntrys_..."  # From .env.local or Vercel env

# List recent issues
sentry-cli issues list --status unresolved --environment production

# Get issue details
sentry-cli api /issues/$ISSUE_ID/ -X GET

# Get latest event for issue
sentry-cli api /issues/$ISSUE_ID/events/latest/ -X GET

# List releases
sentry-cli releases list

# Get release details (commits, deploys)
sentry-cli api /organizations/$SENTRY_ORG/releases/$RELEASE_VERSION/ -X GET

# Mark issue as resolved
sentry-cli api /issues/$ISSUE_ID/ -X PUT -d '{"status": "resolved"}'

# Installation (if missing)
curl -sL https://sentry.io/get-cli/ | bash
```

### Vercel CLI Quick Reference

```bash
# Authentication (one-time)
vercel login

# List recent deployments
vercel ls --prod

# Get deployment logs
vercel logs --prod --since 1h
vercel logs $DEPLOYMENT_URL --since 30m

# Get deployment metadata
vercel inspect $DEPLOYMENT_URL --prod

# Get environment variables
vercel env ls

# Rollback to previous deployment (emergency)
vercel rollback $PREVIOUS_DEPLOYMENT_URL --prod
```

### Git History Analysis

```bash
# Compare deployments
git log $PREVIOUS_SHA..$CURRENT_SHA --oneline

# See what changed in specific file
git log -p $PREVIOUS_SHA..$CURRENT_SHA -- src/services/user.ts

# Find when line was changed
git log -L 45,45:src/services/user.ts

# Search commits for keyword
git log --all --grep="user profile" --since="24 hours ago"
```

---

## Anti-Patterns to Avoid

### ❌ Fixing Symptoms, Not Root Cause

```typescript
// BAD: Wrapping in try-catch without understanding why
try {
  const user = data.user.id; // Still broken, just silent
} catch {
  return null; // Error hidden, users still affected
}
```

**Fix**: Understand why `data.user` is undefined, then fix the source

### ❌ Guessing Instead of Measuring

```bash
# BAD: Making assumptions without data
"I think the database is slow"  # Without checking traces/logs
```

**Fix**: Use Sentry breadcrumbs, Vercel logs, traces to confirm hypothesis

### ❌ Fixing Multiple Issues at Once

```bash
# BAD: Combining unrelated fixes
git commit -m "fix user profile error + refactor auth + update deps"
```

**Fix**: One error, one fix, one commit. Atomic changes enable safe rollback.

### ❌ Deploying Untested Fixes to Production

```bash
# BAD: Skipping preview deployment
git push origin main  # Directly to prod
```

**Fix**: Deploy to preview, test with real production config, then promote

### ❌ Ignoring Related Issues

```markdown
Found 4 similar errors in other endpoints, but only fixed one
```

**Fix**: After fixing high-priority error, create follow-up tasks for related issues

---

## Decision Trees

### Should I Rollback or Fix Forward?

```
Is the error affecting > 50% of users?
├─ YES → ROLLBACK immediately
│         vercel rollback $PREVIOUS_DEPLOYMENT_URL --prod
│         Then investigate root cause
│
└─ NO → Can you fix within 30 minutes?
    ├─ YES → FIX FORWARD (faster recovery)
    │         Implement fix, deploy to preview, test, promote
    │
    └─ NO → Is this a data corruption issue?
        ├─ YES → ROLLBACK + data recovery
        └─ NO → FIX FORWARD with feature flag (disable broken feature)
```

### Which Debug Agents to Launch?

```
Check error type first:

TypeError/ReferenceError (null/undefined)
  → pattern-recognition-specialist
  → git-history-analyzer
  → general-purpose

Performance (timeout, slow)
  → performance-oracle
  → git-history-analyzer
  → general-purpose

Database/Schema (validation, constraint)
  → data-integrity-guardian
  → git-history-analyzer
  → general-purpose

Auth/Permission
  → security-sentinel
  → git-history-analyzer
  → general-purpose

Unknown/Complex
  → pattern-recognition-specialist
  → git-history-analyzer
  → general-purpose
```

---

## Triage Philosophy

**Speed Matters**: Every minute delayed = users experiencing broken functionality

**Data Over Intuition**: Use Sentry metrics, Vercel logs, git history—not guesses

**Fix The Bleed First**: Highest priority error first. Don't get distracted by interesting-but-low-impact issues.

**Parallel Investigation**: Launch multiple debug agents concurrently. Synthesis happens after all data gathered.

**Atomic Fixes**: One error, one root cause, one minimal fix. No "while we're here" refactoring.

**Prevention Mindset**: Every fix should include "how do we prevent this class of errors?"

**Trust The Tools**: Sentry knows user impact. Vercel knows deployment timing. Git knows what changed. Combine all three.

---

## Success Criteria

After running `/triage`, you should have:

✅ Identified single highest-priority production error (data-driven)
✅ Full context gathered (stack trace, breadcrumbs, deployment, users affected)
✅ Parallel debug agents launched and findings synthesized
✅ Root cause analysis documented (what, where, why, when)
✅ Concrete fix proposed with code changes
✅ Testing plan and rollout strategy defined
✅ Prevention measures identified

**Time Target**: 15-30 minutes from `/triage` start to fix proposal

---

*Run this command when production alerts fire, error budgets exceeded, or users report broken functionality. Triage isn't optional—it's the first line of defense for production reliability.*
