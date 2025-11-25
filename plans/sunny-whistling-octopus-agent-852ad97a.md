# Gemini CLI Integration for /aesthetic Command

**Mission:** Enhance the aesthetic command with web-grounded design research while preserving its philosophical framework and anti-convergence principles.

**Philosophy:** Gemini researches, Claude synthesizes and guides. Web grounding prevents AI convergence by surfacing real-world inspiration.

---

## Strategic Overview

### Integration Philosophy

The aesthetic command excels at **philosophical guidance and synthesis**. Gemini CLI adds **current real-world grounding** to prevent generic AI aesthetics.

**Division of Labor:**
- **Gemini**: Research current design trends, find real-world exemplars, analyze visual artifacts, discover anti-convergence examples
- **Claude**: Synthesize findings, apply design philosophy, orchestrate workflow, guide implementation

**Core Principle:** Lightweight enhancement - don't overload the command. Gemini provides inspiration and grounding; Claude maintains the creative council's vision.

---

## Integration Points (3 Selected)

After analyzing all 5 potential integration points, I recommend **3 strategic integrations** that provide maximum value without overwhelming the workflow:

### 1. **Phase 2: Anti-Convergence Research** (MANDATORY)
### 2. **Phase 3: Visual Artifact Analysis** (OPTIONAL - if user provides screenshots)
### 3. **Phase 5: Real-World Exemplar Grounding** (OPTIONAL - for elevation roadmap)

**Rejected integrations:**
- Contextual masters selection - the existing table is comprehensive and decisive
- Multi-perspective design inspiration - would dilute the specialized Task agents' focus

---

## INTEGRATION 1: Anti-Convergence Research (Phase 2)

**Location:** Phase 2: Summoning the Council - after loading frontend-design skill

**Purpose:** Ground the aesthetic review in current design trends to identify what's becoming "default territory" and surface distinctive alternatives.

**Execution:** MANDATORY (always run)

### Implementation

**Insert after line 127 (after Skill invocation):**

```markdown
### 2.2 Research Current Design Landscape

Before analyzing the application, ground yourself in the 2025 design landscape:

**What to Research:**
```bash
gemini "What design patterns and aesthetics are becoming oversaturated in web applications in 2025?
Specifically identify:
1. Font families appearing everywhere (the new 'Inter' or 'Space Grotesk')
2. Color palette trends that feel generic
3. Layout patterns everyone is copying
4. Animation/motion trends that lack originality
5. Background/texture treatments becoming cliché

Then provide 3-5 examples of memorable, distinctive designs that break these patterns.
Focus on intentional choices that show human craft vs AI defaults."
```

**Document the findings:**
```markdown
## Design Landscape (2025)

**Default Territory (Avoid):**
- [List current oversaturated patterns from Gemini]

**Distinctive Alternatives (Inspire):**
- [List memorable examples that break conventions]
```

**Use this research throughout the review** - when you identify defaults in the application, cross-reference against current trends. When proposing alternatives, draw from distinctive examples.

**Caveat:** Trends inform but don't dictate. The goal is awareness of convergence zones, not copying what's "in."
```

### Gemini Prompt Specification

**Exact invocation:**
```bash
gemini "What design patterns and aesthetics are becoming oversaturated in web applications in 2025?

Specifically identify:
1. Font families appearing everywhere (the new 'Inter' or 'Space Grotesk')
2. Color palette trends that feel generic (purple gradients, etc.)
3. Layout patterns everyone is copying (centered containers, card grids)
4. Animation/motion trends that lack originality
5. Background/texture treatments becoming cliché (gradient meshes, etc.)

Then provide 3-5 examples of memorable, distinctive web designs that break these patterns.
Focus on:
- Intentional choices that show human craft vs AI defaults
- Designs that would be immediately recognizable
- Approaches that match different aesthetic directions (minimalist, maximalist, editorial, etc.)

Return concrete examples with URLs if possible."
```

### What Gemini Returns

**Expected output structure:**
```markdown
## Oversaturated Patterns (2025)

**Typography:**
- [Specific fonts becoming defaults]
- [Trending but overused pairings]

**Color:**
- [Palette trends losing distinctiveness]
- [Cliché color approaches]

**Layout:**
- [Predictable composition patterns]
- [Overused grid systems]

**Motion:**
- [Generic animation patterns]

**Details:**
- [Background/texture trends]

## Distinctive Alternatives

**Example 1: [Name/URL]**
- Aesthetic: [Editorial/Brutalist/etc.]
- Key distinction: [What makes it memorable]
- Approach: [Specific techniques]

[...more examples...]
```

### How Claude Uses This

**During Phase 3 (Analysis):**
- Cross-reference detected patterns against Gemini's oversaturated list
- Flag when application uses "default territory" patterns
- Cite specific oversaturation when calling out defaults

**During Phase 5 (Vision):**
- Draw from distinctive alternatives when proposing intentional moves
- Reference real-world examples in elevation roadmap
- Use memorable designs as inspiration for Option B/C directions

### Value Proposition

**Why this matters:**
- **Prevents stale anti-convergence lists**: The hardcoded lists (Inter, Space Grotesk, purple gradients) will age - Gemini keeps them current
- **Real-world grounding**: Gemini's web search finds what's actually proliferating in 2025, not what Claude thinks from training data
- **Inspires distinctive alternatives**: Real examples are more actionable than generic advice
- **Strengthens credibility**: "This pattern is trending in 2025" > "This pattern is generic"

**Unique to Gemini:** Only web grounding can identify current trends post-Jan 2025.

---

## INTEGRATION 2: Visual Artifact Analysis (Phase 3 - Optional)

**Location:** Phase 3: The Studio Session - new subsection after 3.1

**Purpose:** If user provides screenshots or UI mockups, leverage Gemini's multimodal analysis to identify visual patterns, color extraction, and typographic choices.

**Execution:** CONDITIONAL (only if user provides images)

### Implementation

**Insert after section 3.1 (Typography):**

```markdown
### 3.0 Visual Artifact Analysis (If Provided)

If the user has provided screenshots or UI mockups, analyze them multimodally:

**Check for image files:**
```bash
# Look for provided screenshots
ls screenshots/ designs/ mockups/ *.png *.jpg 2>/dev/null || echo "No visual artifacts provided"
```

**If images exist, delegate to Gemini:**
```bash
gemini "Analyze this UI screenshot and identify:

1. Typography:
   - Font families (if detectable)
   - Scale and hierarchy
   - Line height and spacing

2. Color Palette:
   - Dominant colors (hex values if possible)
   - Accent colors
   - Background treatment

3. Layout & Composition:
   - Grid system or layout approach
   - Whitespace treatment
   - Visual hierarchy

4. Visual Details:
   - Shadows and depth
   - Border treatments
   - Background textures/gradients
   - Motion hints (if animation present)

5. Overall Aesthetic:
   - Closest design philosophy (Rams/Vignelli/Norman/etc.)
   - Distinctive vs. generic assessment
   - What makes it memorable (or not)

Be specific and technical." < screenshot.png
```

**Document findings:**
```markdown
## Visual Analysis (From Screenshots)

**Typography Detected:**
- [Gemini's findings]

**Color Palette Extracted:**
- [Specific hex values and usage]

**Layout Observations:**
- [Grid/composition notes]

**Aesthetic Assessment:**
- [Overall vibe and distinctiveness]
```

**Use this analysis** to inform the rest of Phase 3 - you now have concrete data about the current implementation rather than guessing from code.
```

### Gemini Prompt Specification

**Exact invocation:**
```bash
gemini "Analyze this UI screenshot/mockup in detail:

**Typography Analysis:**
- Identify font families (if detectable - compare to common web fonts)
- Measure scale progression and hierarchy
- Assess line height, letter spacing, and typographic rhythm
- Note any distinctive or generic choices

**Color Palette Extraction:**
- List dominant colors with hex approximations
- Identify accent and signal colors
- Describe background treatment (solid/gradient/texture)
- Assess color personality (bold/timid/systematic/scattered)

**Layout & Composition:**
- Identify grid system or layout approach
- Measure whitespace/density
- Note asymmetry or unusual composition
- Assess visual tension and hierarchy

**Visual Details:**
- Describe shadow treatment (subtle/dramatic/none)
- Note border styles and decorative elements
- Identify any textures or patterns
- Look for custom UI elements

**Motion Hints:**
- Any evidence of animation or transitions?
- Hover states or interactive states visible?

**Overall Aesthetic:**
- Closest design philosophy (Rams/Hara/Vignelli/Norman/etc.)
- Rate distinctiveness (1-10, where 10 = unforgettable)
- Identify the one memorable element
- Flag any 'AI default' aesthetics

Be technical and specific. Include measurements if possible." < [IMAGE_PATH]
```

### What Gemini Returns

**Expected output structure:**
```markdown
## Visual Analysis

**Typography:**
- Primary font: [Name or "Sans-serif, likely Inter/Roboto"]
- Heading scale: [Measurements]
- Body text: [Size/line-height]
- Distinctiveness: [Assessment]

**Color Palette:**
- Background: #FFFFFF
- Primary: #3B82F6 (Tailwind blue-500)
- Accent: #8B5CF6 (Purple)
- Text: #1F2937
- Assessment: [Generic/Distinctive]

**Layout:**
- Centered container, max-width ~1200px
- 3-column grid with 24px gaps
- Whitespace: [Generous/Cramped/Balanced]

**Details:**
- Shadows: Subtle drop shadows (0 4px 6px rgba(0,0,0,0.1))
- Borders: 1px solid gray
- Backgrounds: Solid white
- Custom elements: None detected

**Aesthetic:**
- Philosophy: Functional minimalism (Rams-adjacent)
- Distinctiveness: 3/10 - uses common patterns
- Memorable element: None - follows conventions
- Default territory: Yes - Tailwind defaults unchanged

**Motion:**
- No animation detected
- Standard hover states likely
```

### How Claude Uses This

**During Typography Review (3.1):**
- Instead of grepping for font-family, reference Gemini's detection
- Compare detected fonts against anti-convergence lists
- Cite specific measurements from visual analysis

**During Color Review (3.2):**
- Use extracted hex values for precise analysis
- Reference specific Tailwind defaults if detected
- Compare palette against current trends

**During Composition Review (3.4):**
- Reference measured whitespace and grid systems
- Cite specific layout patterns detected
- Use measurements to inform recommendations

### Value Proposition

**Why this matters:**
- **Precise analysis**: Extracting colors from screenshots is faster than grepping CSS
- **Visual truth**: Screenshots show the reality vs. what code might suggest
- **Multimodal strength**: Gemini excels at visual analysis
- **Saves time**: One analysis replaces multiple grep operations

**Unique to Gemini:** Claude cannot analyze images with the same visual intelligence. Multimodal analysis is Gemini's strength.

### Fallback Handling

**If no images provided:**
```markdown
### 3.0 Visual Artifact Analysis
*No screenshots provided - proceeding with code analysis.*
```

**If Gemini CLI unavailable:**
```markdown
### 3.0 Visual Artifact Analysis
*Gemini CLI not available for multimodal analysis - proceeding with code analysis.*
```

---

## INTEGRATION 3: Real-World Exemplar Grounding (Phase 5 - Optional)

**Location:** Phase 5: The Vision - section 5.3 Elevation Roadmap

**Purpose:** Ground the elevation roadmap options in real-world examples to make recommendations concrete and actionable.

**Execution:** OPTIONAL (run for unfamiliar project types or when user requests)

### Implementation

**Insert before section 5.3 (Elevation Roadmap):**

```markdown
### 5.2b Real-World Exemplar Research (Optional)

To ground the elevation roadmap in reality, research current exemplars:

**When to run this:**
- Unfamiliar product category (first time reviewing this type of app)
- User explicitly requests real-world inspiration
- Proposed directions feel abstract without examples

**Research query:**
```bash
# Customize based on assessed project soul
gemini "Find 3-5 exemplary web applications or sites that demonstrate [AESTHETIC_DIRECTION] in [PRODUCT_CATEGORY]:

For example, if direction is 'editorial/magazine' for a blogging platform:
Find sites with exceptional editorial design - bold typography, asymmetric layouts, strong visual hierarchy.

For each example:
1. Name and URL
2. Key aesthetic moves (typography, color, layout)
3. One distinctive choice worth stealing
4. How it avoids generic defaults

Focus on 2025 examples that show intentional craft."
```

**Document findings to inform roadmap:**
```markdown
## Real-World Exemplars

**Example 1: [Name]**
- URL: [link]
- Aesthetic moves: [specific]
- Distinctive choice: [what to steal]

[...more examples...]
```

**Use these examples** when writing Option B and Option C in the Elevation Roadmap - reference specific techniques from real sites.
```

### Gemini Prompt Specification

**Exact invocation (customized per project):**
```bash
gemini "Find 3-5 exemplary web applications or sites that demonstrate [AESTHETIC_DIRECTION] aesthetics for [PRODUCT_TYPE]:

**Aesthetic Direction:** [e.g., 'brutalist minimalism', 'editorial richness', 'playful maximalism', 'luxury refinement']

**Product Type:** [e.g., 'developer tools', 'creative portfolio', 'SaaS dashboard', 'e-commerce']

**What to identify:**
1. Site name and URL (must be current/accessible in 2025)
2. Key aesthetic moves:
   - Typography choices and hierarchy
   - Color palette and treatment
   - Layout/composition approach
   - Motion and interaction patterns
   - Visual details (shadows, textures, etc.)
3. One distinctive choice worth stealing (specific technique)
4. How it avoids generic AI/default territory

**Requirements:**
- Must be production sites (not design portfolios or concept work)
- Should show 2025-current design thinking
- Prioritize sites that feel immediately recognizable
- Include mix of well-known and hidden gems

Return concrete, actionable examples."
```

### What Gemini Returns

**Expected output structure:**
```markdown
## Real-World Exemplars

**1. Linear (linear.app) - Precision Minimalism**
- **Typography:** Custom geometric sans with tight tracking, bold hierarchy
- **Color:** Monochrome with electric purple accent, gradient overlays
- **Layout:** Edge-to-edge compositions, asymmetric content blocks
- **Motion:** Smooth spring physics, orchestrated page reveals
- **Distinctive choice:** Gradient cursor trail on hover
- **Avoids defaults:** Custom font, no centered containers, unexpected motion

**2. [Example 2]**
[Similar structure]

**3. [Example 3]**
[Similar structure]
```

### How Claude Uses This

**During Elevation Roadmap (5.3):**

**Option A (Rams)** - Already well-defined, no examples needed

**Option B** - Ground in exemplar:
```markdown
### Option B: The Editorial (Inspired by [Example Name])
*Confident typography meets asymmetric composition.*

**Vibe:** Magazine editorial meets digital product
**Typography:** Bold display + refined serif body (like [Example] uses [Font])
**Color:** [Palette inspired by Example]
**Layout:** [Specific technique from Example]
**Differentiation:** "The [memorable element from Example]"

**Real-world reference:** [Example URL] demonstrates this aesthetic in production.
```

**Option C** - Ground in different exemplar:
```markdown
### Option C: The [Direction] (Inspired by [Example Name])
[Similar structure referencing different example]
```

### Value Proposition

**Why this matters:**
- **Concrete inspiration**: "Like Linear's gradient cursor" > "Add motion delight"
- **Validation**: Real production sites prove the approach works
- **Actionable**: Specific techniques to steal
- **Credibility**: Grounded recommendations feel less theoretical

**Unique to Gemini:** Web search finds current exemplars that Claude can't access from training data.

### When to Skip

**Skip this integration if:**
- Roadmap options are already clear (Rams is always Option A)
- Product category is familiar (developer tools, blogs, etc.)
- User doesn't request external inspiration
- Time is constrained

**This is the most optional integration** - use judgment.

---

## Integration Summary Table

| Integration | Phase | Mandatory | Execution | Value | Gemini Strength |
|-------------|-------|-----------|-----------|-------|-----------------|
| Anti-Convergence Research | Phase 2 | ✅ Yes | Always run | Prevents stale defaults, current trends | Web grounding |
| Visual Artifact Analysis | Phase 3 | ❌ No | If images provided | Precise color/typography extraction | Multimodal |
| Real-World Exemplar Grounding | Phase 5 | ❌ No | If unfamiliar/requested | Concrete inspiration | Web search |

---

## Workflow Integration

### Updated Aesthetic Command Flow

**Phase 1: Understanding the Canvas** (Unchanged)
- Detect framework, components, styling

**Phase 2: Summoning the Council**
- Load frontend-design skill
- ✅ **NEW: Run Anti-Convergence Research** (Gemini)
- Document current default territory + distinctive alternatives

**Phase 3: The Studio Session**
- ✅ **NEW: Visual Artifact Analysis** (Gemini - if images provided)
- Typography analysis (informed by visual analysis if available)
- Color analysis (using extracted palette if available)
- Motion, composition, emptiness, details

**Phase 4: Perspectives** (Unchanged)
- Launch 3 Task agents in parallel
- The-Essentialist, The-Humanist, The-Architect

**Phase 5: The Vision**
- Soul assessment
- From Default to Intentional (informed by Phase 2 research)
- ✅ **NEW: Real-World Exemplar Research** (Gemini - optional)
- Elevation Roadmap (grounded in exemplars if researched)
- Implementation Priorities

**Phase 6: The Closing Encouragement** (Unchanged)
- Hero Experiment
- Closing wisdom

---

## Error Handling & Fallbacks

### If Gemini CLI Unavailable

**Check availability:**
```bash
which gemini >/dev/null 2>&1 || echo "Gemini CLI not installed"
```

**Fallback strategy:**

**For Anti-Convergence Research (Phase 2):**
- Use hardcoded lists from frontend-design skill
- Add note: "*Using established anti-convergence patterns - install Gemini CLI for current 2025 trends*"

**For Visual Artifact Analysis (Phase 3):**
- Skip multimodal analysis
- Proceed with code-based grep analysis
- Add note: "*Code-based analysis only - provide Gemini CLI for visual extraction*"

**For Real-World Exemplar Grounding (Phase 5):**
- Skip external research
- Use internal knowledge for Option B/C
- Roadmap remains actionable but less concrete

### If Gemini Returns Poor Results

**Quality thresholds:**
- Anti-Convergence Research: Must return 3+ current oversaturated patterns
- Visual Analysis: Must extract colors or typography
- Exemplar Research: Must return 2+ real URLs

**If below threshold:**
- Document partial results
- Supplement with internal knowledge
- Note limitation to user

### Rate Limiting

**Gemini free tier:** 60 req/min, 1000 req/day

**For aesthetic command:**
- Maximum 3 Gemini calls per run
- Total time: ~2-5 minutes of Gemini research
- Well within limits for daily use

**If rate limited:**
- Skip optional integrations (Visual, Exemplar)
- Proceed with code analysis only

---

## Preserving Philosophical Framework

### Anti-Convergence Principles (Maintained)

**Gemini enhances anti-convergence by:**
- Identifying what's becoming "default territory" in real-time
- Surfacing distinctive alternatives from real world
- Grounding recommendations in current examples

**Critical:** Gemini provides inspiration, not prescription. The Council (Claude) synthesizes.

### Design Master Wisdom (Maintained)

**The Creative Council remains Claude's domain:**
- Rams, Hara, Norman (core lenses)
- Contextual masters selection
- Philosophical framing and quotations

**Gemini never replaces the Council** - it informs them with current data.

### The Variation Mandate (Enhanced)

**Gemini strengthens variation by:**
- Showing diverse real-world approaches
- Identifying what NOT to converge toward
- Inspiring context-specific choices

**Each project still gets unique personality** - Gemini prevents copying last project's favorites.

---

## Implementation Checklist

**Preparation:**
- [ ] Verify Gemini CLI installed (`which gemini`)
- [ ] Test basic Gemini invocation
- [ ] Confirm web grounding works (check Google Search attribution)

**Phase 2 Integration:**
- [ ] Add section 2.2 "Research Current Design Landscape"
- [ ] Insert Gemini anti-convergence prompt
- [ ] Add documentation template for findings
- [ ] Test with sample run

**Phase 3 Integration:**
- [ ] Add section 3.0 "Visual Artifact Analysis"
- [ ] Add conditional check for image files
- [ ] Insert Gemini multimodal prompt
- [ ] Add fallback for no images
- [ ] Test with sample screenshot

**Phase 5 Integration:**
- [ ] Add section 5.2b "Real-World Exemplar Research"
- [ ] Insert Gemini exemplar prompt template
- [ ] Add customization notes
- [ ] Add "when to skip" guidance
- [ ] Test with sample project type

**Error Handling:**
- [ ] Add Gemini availability check
- [ ] Add fallback messaging
- [ ] Test with Gemini unavailable
- [ ] Verify graceful degradation

**Documentation:**
- [ ] Update aesthetic.md with integration notes
- [ ] Add Gemini CLI requirement to README (optional)
- [ ] Document fallback behavior

---

## Success Criteria

**Integration succeeds when:**

✅ **Anti-convergence is current** - Identifies 2025 trends, not 2024 assumptions
✅ **Visual analysis is precise** - Extracts exact colors and measurements
✅ **Roadmap is concrete** - References real production examples
✅ **Philosophy is preserved** - Council wisdom guides synthesis
✅ **Command stays lightweight** - 3 integrations max, all purposeful
✅ **Fallbacks work gracefully** - Command succeeds without Gemini
✅ **User sees value** - "This research grounded my aesthetic direction"

---

## Example Run Flow

**User invokes:** `/aesthetic`

**Phase 1:** Claude analyzes codebase structure
- Detects Next.js + Tailwind + TypeScript
- Inventories 47 components, 12 pages

**Phase 2:** Claude loads frontend-design skill
- ✅ **Gemini researches** current design trends (2 min)
- Returns: "Gradient meshes saturating, monochrome + neon is distinctive"
- Claude documents findings

**Phase 3:** User provided screenshot
- ✅ **Gemini analyzes** visual artifact (1 min)
- Returns: "Uses Tailwind blue-500, Inter font, centered layout"
- Claude uses extracted data for typography/color analysis

**Phase 4:** Claude launches Task agents
- The-Essentialist, The-Humanist, The-Architect run in parallel
- Each returns specialized perspective

**Phase 5:** Claude synthesizes vision
- Soul assessment: "Sterile clinic → Confident studio"
- ✅ **Gemini researches** exemplars for "editorial" direction (2 min)
- Returns: "Stripe Press, Linear, ReadCV as examples"
- Claude creates 3 grounded roadmap options:
  - Option A: Rams (no research needed)
  - Option B: Editorial (inspired by Stripe Press techniques)
  - Option C: Precision (inspired by Linear's motion)

**Phase 6:** Claude delivers hero experiment
- Specific, actionable, inspired by research

**Total Gemini time:** ~5 minutes
**Total value:** Current trends + precise analysis + concrete inspiration

---

## Critical Files for Implementation

### /Users/phaedrus/.claude/commands/aesthetic.md
**Reason:** Primary file to modify - insert 3 integration points

**Modifications needed:**
- Line ~127: Insert Phase 2.2 (Anti-Convergence Research)
- Line ~152: Insert Phase 3.0 (Visual Artifact Analysis)  
- Line ~393: Insert Phase 5.2b (Real-World Exemplar Research)
- Add error handling sections
- Add Gemini availability checks

### /Users/phaedrus/.claude/skills/frontend-design/SKILL.md
**Reason:** Contains anti-convergence lists - reference point for Gemini research

**Modifications needed:**
- None (reference only)
- Gemini research supplements these lists, doesn't replace

### /Users/phaedrus/.claude/skills/gemini-cli-integration/SKILL.md
**Reason:** Documents Gemini capabilities - pattern reference

**Modifications needed:**
- None (reference only)
- Add aesthetic command as example use case in documentation

### /Users/phaedrus/.claude/commands/research.md
**Reason:** Research command pattern - invocation reference

**Modifications needed:**
- None (reference only)
- Aesthetic uses similar Gemini delegation pattern

