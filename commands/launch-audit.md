---
description: Audit a project's launch readiness and create GitHub Issues to close gaps
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, Task, AskUserQuestion
---

# LAUNCH AUDIT

> ⚠️ **PERSISTENCE REMINDER**: Create GitHub issues as you identify gaps, don't batch at the end. Save audit findings to project notes in real-time.

> Ship it or it doesn't exist. — Pieter Levels

Audit this project against the **launch-ready checklist**. Identify gaps. Create GitHub Issues to close them. Give a score.

## The Launch-Ready Checklist

A project is launch-ready when it can:
1. **Attract** - Landing page explains value, converts visitors
2. **Deliver** - Core flow gives value in <2 minutes
3. **Monetize** - Stripe integrated, at least one paid path
4. **Measure** - Analytics show who visits, what they do
5. **Grow** - At least one traffic channel is ready

**Score: X/5** — Count of requirements met.

## Process

### Phase 1: Gather Context

```bash
# Get repo info
gh repo view --json name,description,url,homepageUrl

# Check for existing issues
gh issue list --state open --json number,title,labels --jq '.[] | "#\(.number): \(.title)"'

# Check Vercel deployment
vercel ls --prod 2>/dev/null | head -5

# Look for Stripe integration
grep -r "stripe" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" -l 2>/dev/null | head -10

# Look for analytics
grep -r "analytics\|gtag\|posthog\|plausible\|mixpanel" --include="*.ts" --include="*.tsx" --include="*.js" -l 2>/dev/null | head -10
```

Also examine:
- README for project description
- Landing page / marketing pages
- Pricing page or monetization code
- Core user flows

### Phase 2: Interview (Brief)

Ask the founder to confirm context:

1. **What's the core value prop?** (one sentence)
2. **Who's the target user?**
3. **What's the monetization plan?** (subscription, one-time, freemium, etc.)
4. **Any specific concerns or focus areas?**

### Phase 3: Audit Each Dimension

#### 1. ATTRACT — Landing Page

Check for:
- [ ] Clear headline stating value prop
- [ ] Compelling subheadline or description
- [ ] Primary CTA (sign up, try it, etc.)
- [ ] Social proof (testimonials, logos, numbers)
- [ ] Mobile responsive
- [ ] Fast load time
- [ ] SEO basics (title, meta description, OG tags)

**Score**: Ready / Needs Work / Missing

#### 2. DELIVER — Core Flow

Check for:
- [ ] User can get to value in <5 clicks
- [ ] Core flow is obvious (no confusion about what to do)
- [ ] Flow completes without errors
- [ ] Value is delivered (not just promised)
- [ ] Works on mobile (if applicable)

**Score**: Ready / Needs Work / Missing

#### 3. MONETIZE — Stripe Integration

Check for:
- [ ] Stripe SDK installed and configured
- [ ] At least one product/price created
- [ ] Checkout flow works
- [ ] Webhook handling (subscription events)
- [ ] User can see their subscription status
- [ ] Pricing page exists

**Score**: Ready / Needs Work / Missing

#### 4. MEASURE — Analytics

Check for:
- [ ] Analytics provider installed (Plausible, PostHog, GA, etc.)
- [ ] Page views tracked
- [ ] Key events tracked (signup, conversion, core actions)
- [ ] User identification (if applicable)
- [ ] Dashboard accessible

**Score**: Ready / Needs Work / Missing

#### 5. GROW — Traffic Channel

Check for at least ONE ready channel:
- [ ] Product Hunt launch prepared (assets, copy, date)
- [ ] Twitter/X presence and announcement ready
- [ ] Paid ads configured (Google, Meta, etc.)
- [ ] SEO content published
- [ ] Email list with subscribers
- [ ] Other distribution channel

**Score**: Ready / Needs Work / Missing

### Phase 4: Create Issues

For each gap identified, create a GitHub Issue:

```bash
gh issue create \
  --title "[Launch] Concise description of gap" \
  --body "## Gap
[What's missing]

## Why It Matters
[Impact on launch readiness]

## Acceptance Criteria
- [ ] Specific thing to do
- [ ] Another thing

## Notes
[Any context or suggestions]" \
  --label "launch,type/feature,horizon/now"
```

**Labels to use:**
- `launch` — marks as launch-readiness work
- `launch/attract` | `launch/deliver` | `launch/monetize` | `launch/measure` | `launch/grow` — dimension
- `horizon/now` | `horizon/next` — urgency
- `effort/s` | `effort/m` | `effort/l` — size

Create the `launch` label if it doesn't exist:
```bash
gh label create launch --color "0E8A16" --description "Launch readiness work" 2>/dev/null || true
gh label create launch/attract --color "1D76DB" --description "Landing page & conversion" 2>/dev/null || true
gh label create launch/deliver --color "1D76DB" --description "Core value delivery" 2>/dev/null || true
gh label create launch/monetize --color "1D76DB" --description "Stripe & payments" 2>/dev/null || true
gh label create launch/measure --color "1D76DB" --description "Analytics & tracking" 2>/dev/null || true
gh label create launch/grow --color "1D76DB" --description "Traffic & distribution" 2>/dev/null || true
```

### Phase 5: Summary Report

Output a summary:

```markdown
# Launch Audit: [Project Name]

**Date**: [Today]
**Score**: X/5

## Scorecard

| Dimension | Status | Issues Created |
|-----------|--------|----------------|
| Attract (Landing) | ✅/⚠️/❌ | #123, #124 |
| Deliver (Core Flow) | ✅/⚠️/❌ | #125 |
| Monetize (Stripe) | ✅/⚠️/❌ | #126, #127 |
| Measure (Analytics) | ✅/⚠️/❌ | #128 |
| Grow (Traffic) | ✅/⚠️/❌ | #129 |

## Critical Gaps

1. [Most important gap]
2. [Second most important]
3. [Third]

## Recommended Sequence

1. [What to do first]
2. [What to do second]
3. [What to do third]

## Notes

[Any other observations]
```

## Quality Bar

- Every issue is specific and actionable
- Issues are properly sized (break down XL items)
- No duplicates of existing open issues
- Critical gaps get `horizon/now`
- Summary gives clear next steps

---

*Audit complete. Now close the gaps and ship.*
