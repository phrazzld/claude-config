---
description: Iteratively improve visual design through screenshot-critique-implement loop until quality threshold met
---

Iteratively polish visual design through automated critique and implementation cycles.

# POLISH

Transform your application's visual design through iterative improvement: screenshot routes with Playwright, critique through master designer perspectives, implement changes programmatically, repeat until design reaches quality bar set by Rams, Hara, Norman, and Vignelli.

**What makes this different:** Adaptive approach based on project maturity. Early-stage projects get bold transformations. Sophisticated design systems get respectful refinements.

## Intent

- Capture current visual state via Playwright screenshots
- Assess design system maturity (0-10 score: greenfield vs sophisticated)
- Auto-detect mobile optimization needs
- Critique design through 3-4 parallel perspectives + web-grounded research
- Implement improvements programmatically (typography, color, layout, motion, components)
- Iterate until master designers approve (quality threshold based on mode)
- Generate before/after journey report with iteration history

## Quality Levels

**Standard:** 85/100 threshold, 5 iterations max (default)
**Stripe-Level:** 92/100 threshold, 6 iterations max (invoke with "polish to Stripe-level" or "make it stunning")

When Stripe-level requested:
- Extend max iterations to 6
- Add mobile-specific screenshot phase (if mobile detected)
- Require Humanist agent "delight score" >= 30/35
- Ask "Would this make someone gasp?" at each iteration

## Key Optimization

**Adaptive approach prevents over-engineering:**
- Detects design maturity (0-10 score based on tokens, typography, colors, components, spacing)
- Greenfield (< 4): Bold changes, establish foundation, transformative improvements
- Sophisticated (>= 4): Respect investments, refine within system, preserve what works
- Prevents destroying good design systems while fixing poor ones

**Parallel critique for speed:**
Run 3 design agents + Gemini research concurrently (2-3 minutes vs 8-10 sequential).

---

## Your Approach

### 1. Setup & Discovery

**Ensure Playwright MCP available:**
Check if Playwright MCP configured. If missing, auto-install:
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

**Detect framework and stack:**
- Read package.json (Next.js, Vite, Astro, SvelteKit, Gatsby?)
- Identify styling approach (Tailwind, CSS-in-JS, CSS modules, plain CSS?)
- Find dev server configuration and default port

**Manage dev server:**
- Check if already running (curl health check on common ports)
- If running: Use existing session (note PID for awareness)
- If not: Start in background, wait for ready, store PID for cleanup
- On completion: Kill only if we started it

**Discover routes:**
- If `$1` provided: Use it as single route to polish (e.g., `/polish /dashboard`)
- Otherwise discover all routes:
  - **Next.js**: Scan `app/` for `page.tsx` (App Router) or `pages/` (Pages Router)
  - **Vite/React**: Parse router config, extract route paths
  - **Static sites**: Crawl from homepage, follow internal links
  - **Fallback**: Start at `/`, use Playwright to extract all `<a href>` links
- Prioritize: Homepage → Core flows → Error pages → Rest

**Auto-detect mobile optimization:**
```bash
# Check for responsive design signals
grep -r "max-width\|@media\|breakpoint\|sm:\|md:\|lg:" src/ --include="*.css" --include="*.tsx"
# Check for viewport meta
grep -r "viewport" src/ --include="*.html" --include="*.tsx"
# Check for mobile-specific packages
grep -E "react-native|capacitor|@use-gesture|swiper" package.json
```

If any signals found:
- Set `MOBILE_DETECTED=true`
- Include The-Mobile-Advocate agent in parallel critique
- Capture mobile viewport screenshots (375px width) alongside desktop
- Score mobile separately from desktop

### 2. Assess Design Maturity

**Calculate maturity score (0-10):**
```
Design Maturity Signals:
- Design token infrastructure? (check for @theme directive, design-tokens/, theme.ts) [+2]
- Typography system with custom fonts? (not Inter/Roboto/system-ui) [+2]
- OKLCH colors + semantic tokens? (not just blue-500, purple-600) [+2]
- Component library integration? (shadcn/ui, Radix, Ark, etc.) [+2]
- Consistent spacing/grid system? (8px grid, systematic spacing scale) [+2]

Score 0-3: Greenfield (overhaul mode - bold changes acceptable)
Score 4-7: Established (tweak mode - respect existing patterns)
Score 8-10: Production-grade (refinement mode - preserve investments)
```

**Set adaptive thresholds based on maturity:**
- Low maturity: Suggest transformative changes (new fonts, color systems, layout restructuring)
- High maturity: Focus on refinements (token value adjustments, consistency fixes, polish)

### 3. The Polish Loop

**Iterate until quality threshold met (max 5 iterations):**

**A. Capture Visual State**

For each route (parallel screenshot capture):
- Navigate with Playwright `browser_navigate`
- Take full-page screenshot (PNG, high quality): `browser_take_screenshot`
- Take accessibility snapshot (semantic structure): `browser_snapshot`
- Store in `.polish-sessions/${TIMESTAMP}/iteration-${N}/screenshots/`

**B. Invoke Design Council (Parallel)**

Launch 3 agents concurrently using Task tool (single message, 3 calls):

**The-Essentialist** (Rick Rubin + Dieter Rams):
```
Channel Rick Rubin and Dieter Rams. Question: "What can be removed?"

Analyze screenshots from iteration ${N}. Current maturity: ${SCORE}/10.

Hunt for:
- Visual noise preventing content from singing
- Decoration serving no function
- Default choices that should be decisions
- "More" where "less" would be better

Scoring (30 points total):
- Typography simplicity and hierarchy (0-10)
- Visual clarity and focus (0-10)
- Removal opportunities identified (0-10)

If maturity < 4: Be bold with simplification suggestions
If maturity >= 4: Respect existing system, suggest refinements

Return specific changes with file:line locations.
```

**The-Humanist** (Don Norman + Steve Jobs):
```
Channel Don Norman and Steve Jobs. Question: "How does it feel to be human here?"

Analyze screenshots from iteration ${N}. Current maturity: ${SCORE}/10.

Assess three levels:
1. Visceral: First impression, gut reaction (0-10 points)
2. Behavioral: Interaction pleasure, friction vs delight (0-15 points)
3. Reflective: Meaning, story told about user (0-10 points)

**The Gasp Question (required for Stripe-level mode):**
> "Would users literally gasp at how polished/beautiful/satisfying this is?
> If not, what specific changes would make them gasp?"

If maturity < 4: Suggest transformative UX improvements
If maturity >= 4: Focus on micro-interactions and polish

Return emotional gaps + delight opportunities + gasp-worthy suggestions + file changes.
```

**The-Architect** (Massimo Vignelli + Systems):
```
Channel Massimo Vignelli. Question: "Is there intellectual elegance through structure?"

Analyze screenshots from iteration ${N}. Current maturity: ${SCORE}/10.

Check:
- Grid discipline and intentional breaks (0-15 points)
- Typography scale consistency (0-10 points)
- Component architecture depth (0-10 points)

Brand-Tinted Neutrals Check:
- Does interface use pure grays (chroma = 0) for neutrals?
- Is there a brand color that could tint the entire neutral palette?
- If brand color exists but neutrals are pure gray: suggest tinting
  background, foreground, surfaces, borders with brand hue at very
  low chroma (0.01-0.02) for imperceptible but present brand feeling

Advanced Techniques Check:
- Could backgrounds benefit from WebGL/Three.js (particle systems, gradient meshes)?
- Would GSAP/Lottie animations improve storytelling?
- Are there opportunities for CSS art (clip-paths, pure CSS illustrations)?
- Would Iconify provide better icon options than current library?
- Does design need custom assets? Suggest Midjourney/Nano Banana Pro generation.

Apply Ousterhout: Are UI components deep modules (simple interface, rich functionality)?

If maturity < 4: Propose design system foundation
If maturity >= 4: Identify system violations and inconsistencies

Return system issues + token opportunities + advanced technique suggestions + file changes.
```

**The-Mobile-Advocate** (invoke when MOBILE_DETECTED=true):
```
Channel Steve Jobs' iPhone unveil obsession. Question: "Does mobile make people gasp?"

Analyze mobile viewport screenshots (375px) from iteration ${N}.

Hunt for:
- Touch targets that frustrate fat fingers (< 44px)
- Gestures that should exist but don't (swipe, pull-to-refresh)
- Scroll behaviors that feel mechanical vs natural
- Missing haptic feedback opportunities
- Typography too small for outdoor viewing
- Bottom nav vs hamburger (prefer bottom for key actions)
- Pull-to-refresh physics quality
- Desktop layout squeezed vs mobile-native composition

Scoring (0-35 points):
- Touch interaction delight (0-15)
- Mobile-specific layout quality (0-10)
- Gesture and haptic opportunities (0-10)

Reference: See frontend-design skill `references/mobile-excellence.md`

Return mobile-specific changes with file:line locations.
```

**C. Web-Grounded Research (Gemini CLI)**

After 3 agents return, invoke Gemini for anti-convergence check:
```bash
gemini "Design critic analysis for ${FRAMEWORK} app (maturity ${MATURITY}/10).

Analyze these screenshots and provide:

1. Anti-Convergence Check (2025):
   - Detect oversaturated AI patterns (Inter font, purple gradients, centered max-w layouts)
   - Identify generic design defaults
   - Suggest distinctive alternatives backed by real examples

2. Current Best Practices:
   - What are leading ${PRODUCT_TYPE} apps doing differently?
   - Typography trends avoiding AI convergence
   - Color approaches that stand out
   - Motion patterns showing craft

3. Actionable Recommendations:
   - Specific font suggestions (avoid Inter/Roboto/Space Grotesk)
   - Palette alternatives with reasoning
   - Layout innovations beyond centered columns
   - Motion opportunities

Score (0-30 points) + specific improvements with file paths."
```

If Gemini unavailable: Continue with 3 local agents only (adjust threshold to 75/100).

**D. Calculate Quality Score**

```
# Standard mode (no mobile)
Total Score = Essentialist + Humanist + Architect + Gemini
           = (0-30)      + (0-35)    + (0-35)     + (0-30)
           = 0-100 points

# With mobile detected
Total Score = Essentialist + Humanist + Architect + Mobile-Advocate + Gemini
           = (0-30)      + (0-35)    + (0-35)     + (0-35)           + (0-30)
           = 0-135 points (normalized to 100)

Quality Thresholds:
- Standard: 85/100
- Stripe-Level: 92/100
```

**Additional checks (all must pass):**
- Master consensus: Each agent scores >= 80% of their max
- Anti-convergence: Gemini confirms no generic AI patterns
- Cross-route consistency: All route scores within 10 points of each other
- **Stripe-level only**: Humanist delight score >= 30/35
- **If mobile detected**: Mobile-Advocate score >= 25/35

**E. Quality Decision Point**

**If score >= 85 AND all checks pass:**
- Log success + final scores
- Generate final report (see section 4)
- Exit loop ✓

**If score < 85 OR checks fail:**
- Aggregate all agent recommendations
- Prioritize by impact (highest point-gain potential)
- Proceed to implementation

**F. Implement Changes**

**Identify files to modify based on agent recommendations:**

Typography changes → `globals.css`, `tailwind.config.ts`, font imports
Color changes → `theme.ts`, `tailwind.config.ts`, design token files
Layout changes → Page components, layout files
Motion changes → `globals.css`, component animations
Component simplification → Shallow modules identified by Architect

**Apply changes programmatically using Edit tool:**
- Make precise file modifications based on agent guidance
- Validate syntax (TypeScript/CSS linting)
- Check dev server still runs (no crashes)
- Take verification screenshot to confirm change applied

**Rollback on failure:**
If build breaks after changes:
- `git reset --hard HEAD` (rollback to last iteration)
- Log failed change to `.polish-sessions/${TIMESTAMP}/failed-changes.log`
- Try alternative approach from agent suggestions
- If 3 consecutive failures: Stop iteration, report blocking issue

**G. Commit Iteration**

Create git checkpoint:
```bash
git add [modified files]
git commit -m "polish(iteration ${N}): [summary of changes]

Iteration ${N}/5 - Score: ${SCORE}/100 (${DELTA:+${DELTA} improvement})

Changes applied:
- [Change 1]
- [Change 2]
- [Change 3]

Agent scores:
- Essentialist: ${ESSENTIALIST_SCORE}/30
- Humanist: ${HUMANIST_SCORE}/35
- Architect: ${ARCHITECT_SCORE}/35
- Gemini: ${GEMINI_SCORE}/30

Screenshots: .polish-sessions/${TIMESTAMP}/iteration-${N}/"
```

**H. Stall Detection**

If score improvement < 5 points from previous iteration:
- Log: "Design improvements plateauing (${CURRENT_SCORE} vs ${PREV_SCORE})"
- Ask user: "Continue refining or stop here? (Current score: ${SCORE}/100)"
- If stop: Generate report, exit gracefully

**I. Loop Control**

```
Max iterations:
- Standard mode: 5
- Stripe-level mode: 6
```

If iterations < max AND threshold not met AND no stall:
- Increment iteration counter
- Return to step A (Capture Visual State)

If max iterations reached or user stops:
- Generate final report
- Exit with current best score

### 4. Generate Final Report

**Create comprehensive journey summary:**

```markdown
# Polish Session Report
**Date:** ${TIMESTAMP}
**Framework:** ${FRAMEWORK}
**Design Maturity:** ${INITIAL_MATURITY}/10 → ${FINAL_MATURITY}/10

## Summary
Iterations completed: ${N}
Initial score: ${INITIAL_SCORE}/100
Final score: ${FINAL_SCORE}/100
Improvement: +${DELTA} points
Duration: ${MINUTES} minutes

## Journey

### Iteration 1 (Score: ${SCORE_1}/100)
**Changes:**
- [List changes applied]

**Agent Feedback:**
- Essentialist: "${FEEDBACK}" (${SCORE}/30)
- Humanist: "${FEEDBACK}" (${SCORE}/35)
- Architect: "${FEEDBACK}" (${SCORE}/35)
- Gemini: "${FEEDBACK}" (${SCORE}/30)

[Screenshot comparison: before/after]

### Iteration 2 (Score: ${SCORE_2}/100, +${DELTA})
[Same structure...]

## Final Assessment

**Quality Breakdown:**
- Typography: ${SCORE}/20
- Color: ${SCORE}/20
- Motion: ${SCORE}/15
- Composition: ${SCORE}/20
- Craft: ${SCORE}/15
- Consistency: ${SCORE}/10

**Total: ${FINAL_SCORE}/100** ${THRESHOLD_MET ? "✓ Threshold met" : "◯ Stopped at max iterations"}

## Files Modified
- [List all changed files with descriptions]

## Recommendations for Next Session
[Remaining opportunities for improvement]
```

Save to: `.polish-sessions/${TIMESTAMP}/final-report.md`

---

## Playwright MCP Integration

**Check installation:**
```bash
claude mcp ls | grep -i playwright
```

**If missing, auto-install:**
```bash
echo "🎨 Installing Playwright MCP for screenshot capture..."
claude mcp add playwright npx @playwright/mcp@latest

# Verify
claude mcp ls | grep -i playwright && echo "✓ Playwright MCP ready"
```

**If auto-install fails:**
```
Playwright MCP installation required but failed.

Manual installation:
  claude mcp add playwright npx @playwright/mcp@latest

Then re-run: /polish
```

---

## Usage Examples

**Basic usage (all routes):**
```bash
/polish
# Discovers all routes, runs full polish loop until threshold met
```

**Focus on specific route:**
```bash
/polish /dashboard
# Only analyzes and improves the dashboard route
```

**Custom iteration count:**
Before running, tell Claude:
```bash
"Please only do 3 iterations max"
/polish
```

**Override maturity mode:**
Before running:
```bash
"Be bold with changes, treat this as greenfield"
/polish
```

**Export remaining items:**
After completion:
```bash
"Add the remaining polish suggestions to TODO.md"
# Creates backlog items from unimplemented recommendations
```

---

## Common Issues

**Playwright MCP not found:**
- Auto-installs on first run
- Manual: `claude mcp add playwright npx @playwright/mcp@latest`

**Dev server won't start:**
- Check package.json scripts
- Try: npm run dev / pnpm dev / yarn dev
- If still fails: Start manually, then re-run `/polish`

**Port already in use:**
- Command detects and uses existing server
- If conflict with different app: Stop it or set `PORT=3001` env before running

**Route discovery returns 0 routes:**
- Provide manual route: `/polish /`
- Or specify: "Focus on these routes: /, /about, /pricing" before running

**Screenshot fails on specific route:**
- Logs error, skips route, continues with others
- Check browser console for errors on that route

**Agent returns unexpected response:**
- Retries once automatically
- Falls back to previous iteration score if retry fails
- Logs warning but continues

**Changes break build:**
- Auto-rollback via `git reset --hard HEAD`
- Logs failed change
- Attempts alternative approach
- After 3 failures: Stops and reports

**Gemini CLI unavailable:**
- Gracefully degrades to 3 local agents only
- Adjusts threshold to 75/100 (from 85/100)
- Logs: "Gemini unavailable, using local agents only"

---

## Your Output

**After each iteration:**
```
🎨 Iteration 2/5 Complete

Score: 78/100 (+16 from iteration 1)
├─ Essentialist:  26/30 ✓ Approves
├─ Humanist:      29/35 ✓ Approves
├─ Architect:     31/35 ✓ Approves
└─ Gemini:        28/30 ✓ Approves (anti-convergence passing)

Changes Applied:
✓ Replaced Inter with Cabinet Grotesk
✓ Introduced OKLCH color palette
✓ Implemented spring-based motion language
✓ Refined spacing to 8px grid system

7 points from threshold (85). Continue? [Press Enter to continue, Ctrl+C to stop]
```

**On completion:**
```
✨ Design Polish Complete!

Final Score: 87/100 (+25 from start)
Iterations: 3/5
Duration: 18 minutes

All master designers approve! Design has reached quality bar.

📊 Full Report: .polish-sessions/2025-01-27-14-30-22/final-report.md
🎨 Screenshots: .polish-sessions/2025-01-27-14-30-22/iteration-3/screenshots/
🌳 Git History: 3 commits on branch polish/2025-01-27-14-30-22

Next Steps:
- Review changes: git diff polish-start-2025-01-27-14-30-22
- Merge to main: git checkout main && git merge polish/2025-01-27-14-30-22
- Or continue polishing specific route: /polish /pricing
```

---

## Philosophy

> "Design is not just what it looks like and feels like. Design is how it works." — *Steve Jobs*

**The Loop is the Learning:**
Each iteration teaches the system what good design means for *this specific project*. By iteration 3-5, the agents understand your domain, your users, your brand soul.

**Adaptive, Not Prescriptive:**
Greenfield projects need boldness to establish foundation. Mature systems need respect for existing investments. The maturity score ensures we build where nothing exists, and refine where foundations are solid.

**Quality Over Quantity:**
Better to stop at 2 iterations with 87/100 than force 5 iterations chasing 95/100. The threshold (85) represents "ready to ship" quality—not perfection, but intention.

**Master Consensus Matters:**
When Essentialist, Humanist, Architect, and Gemini all approve, trust them. They embody centuries of design wisdom: Rams' functionalism, Hara's emptiness, Norman's emotion, Vignelli's systems thinking.

---

## Related Commands

- `/aesthetic` - Strategic design analysis (one-time roadmap generation with 3 options)
- `/groom` - Multi-perspective codebase audit (includes design-systems-architect agent)
- `/execute` - Execute tasks from TODO.md (can tackle exported polish backlog items)
