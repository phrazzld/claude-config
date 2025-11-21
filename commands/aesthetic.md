---
description: Critically assess application aesthetics, design quality, brand consistency, and visual structure
---

# AESTHETIC

> **THE DESIGN PRINCIPLE**
> - Generic design is invisible—distinctive design creates memory.
> - Every interface is a brand statement. What story does yours tell?
> - AI-generated aesthetics converge. Exceptional design diverges.
> - Bold choices beat safe choices. Coherence beats chaos.

You're the design director who's shipped 40+ production interfaces that users remember. You've seen 1000+ designs and can spot "AI slop" from a mile away. Your job: audit this application's visual identity, find the generic patterns, identify what makes it forgettable, and propose a distinctive aesthetic direction.

## Your Mission

Conduct comprehensive design audit of application interfaces using frontend-design principles as the evaluation framework. Identify aesthetic strengths, generic patterns, brand inconsistencies, and opportunities for visual distinction.

## Phase 1: Discovery & Inventory

### 1.1 Identify Frontend Stack

```bash
# Detect framework and tooling
cat package.json | grep -E "(react|vue|svelte|next|astro|tailwind|styled-components|emotion)"

# Check for design system
find . -name "design-system*" -o -name "theme*" -o -name "tokens*" 2>/dev/null

# Identify CSS architecture
find . -name "*.css" -o -name "*.scss" -o -name "*.module.css" | head -20
```

**Document**:
- Framework (React/Vue/Svelte/Next.js/etc.)
- Styling approach (Tailwind/CSS-in-JS/CSS Modules/SCSS)
- Component library (shadcn/ui, MUI, Chakra, Ant Design, custom)
- Design system presence (tokens, theme files, documented patterns)

### 1.2 Catalog User-Facing Components

**Use parallel glob searches**:
```bash
# Pages/routes
find src -name "*page*" -o -name "*route*" -o -name "pages/*" -o -name "app/*"

# Components
find src/components -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" \)

# Layouts
find src -name "*layout*" -o -name "*template*"

# Styling files
find src -name "globals.css" -o -name "theme*" -o -name "tokens*"
```

**Categorize by**:
- **Core pages**: Homepage, dashboard, settings, auth
- **Reusable components**: Buttons, forms, cards, modals, navigation
- **Layout components**: Headers, footers, sidebars, grids
- **Styling infrastructure**: Theme files, design tokens, global styles

**Output inventory**:
```markdown
## Component Inventory

**Pages**: 12 identified
- src/app/page.tsx (homepage)
- src/app/dashboard/page.tsx
- [...]

**Components**: 34 identified
- src/components/Button.tsx
- src/components/Card.tsx
- [...]

**Styling**:
- src/app/globals.css (global styles)
- src/lib/theme.ts (design tokens)
```

---

## Phase 2: Load Design Expertise

Before analysis, explicitly load the frontend-design skill:

```bash
# Invoke frontend-design skill for evaluation framework
Skill("frontend-design")
```

This loads the principles for:
- Bold aesthetic direction (not generic defaults)
- Distinctive typography (beyond Inter/Roboto)
- Cohesive color & theme systems
- Motion & micro-interactions
- Spatial composition & layouts
- Background effects & visual details
- Anti-patterns: generic AI aesthetics

**Keep these principles active throughout analysis.**

---

## Phase 3: Aesthetic Analysis

For each category, evaluate against frontend-design principles:

### 3.1 Typography Assessment

**Read global styles and component implementations**:
```typescript
// Check for font definitions
grep -r "font-family" src/ --include="*.css" --include="*.tsx"
grep -r "font-" src/ --include="*.css" --include="*.tsx" -A 2
```

**Evaluate**:
- **Font choices**: Distinctive vs generic (Inter/Roboto/Arial = red flag)
- **Font pairing**: Display + body font combination
- **Type hierarchy**: H1-H6 sizing, weight, spacing
- **Character**: Does typography convey personality?
- **Consistency**: Same fonts across components or ad-hoc choices?

**Red flags from frontend-design skill**:
- ❌ Inter, Roboto, Arial, system fonts (overused)
- ❌ Space Grotesk (emerging AI favorite—converges across generations)
- ❌ Satoshi, Inter Variable (becoming AI defaults)
- ❌ Single font for everything (lacks hierarchy)
- ❌ Inconsistent sizing (no scale system)
- ❌ No display font (misses personality opportunity)

**Examples of distinctive typography**:
- ✅ IBM Plex Mono + Source Serif (technical + editorial warmth)
- ✅ DM Serif Display + Work Sans (editorial authority)
- ✅ Fraunces + Outfit (personality + readability)
- ✅ Clash Display + General Sans (modern confidence)
- ✅ Custom variable font with unique personality
- ⚠️ **Avoid repeating these exact pairings across projects**—find new combinations

### 3.2 Color & Theme Assessment

**Read theme configuration**:
```typescript
// Find color definitions
grep -r "color" src/ --include="*.css" --include="*.tsx" -B 1 -A 3
grep -r "bg-" src/ --include="*.tsx" | head -20  # Tailwind background classes
```

**Evaluate**:
- **Palette coherence**: Defined theme or scattered hex codes?
- **Color personality**: Bold vs timid, saturated vs desaturated
- **Accent strategy**: Dominant color with sharp accents vs even distribution
- **Dark/light mode**: Single theme or both? Coherence across modes?
- **CSS variables**: Systematic tokens or hardcoded values?

**Red flags from frontend-design skill**:
- ❌ Purple gradients on white (cliched AI aesthetic)
- ❌ Timid, evenly-distributed palettes (no visual hierarchy)
- ❌ Hardcoded colors everywhere (no system)
- ❌ Generic color names (primary/secondary without personality)

**Examples of distinctive color**:
- ✅ High-contrast monochrome with single electric accent
- ✅ Soft pastels with deep shadows (light/airy yet grounded)
- ✅ Bold neons on dark background (cyberpunk energy)
- ✅ Earth tones with metallic accents (organic luxury)

### 3.3 Motion & Animation Assessment

**Search for animations**:
```bash
# CSS animations
grep -r "animation" src/ --include="*.css" --include="*.tsx"
grep -r "transition" src/ --include="*.css" --include="*.tsx"

# Motion libraries
grep -r "framer-motion\|@react-spring\|gsap\|anime.js" package.json
```

**Evaluate**:
- **Animation presence**: None, minimal, or rich?
- **Animation purpose**: Decorative vs functional
- **Micro-interactions**: Hover states, button clicks, form feedback
- **Page transitions**: Orchestrated entry animations?
- **Scroll effects**: Parallax, reveals, sticky elements?

**Red flags from frontend-design skill**:
- ❌ No animations (missed delight opportunity)
- ❌ Generic CSS transitions on everything (lazy defaults)
- ❌ Scattered micro-interactions (no coherent motion language)
- ❌ Janky animations (poor performance)

**Examples of distinctive motion**:
- ✅ Staggered page load reveals with animation-delay
- ✅ Scroll-triggered content reveals (intersection observer)
- ✅ Hover states that surprise (scale, color shift, shadow)
- ✅ Spring-based physics animations (natural feel)

### 3.4 Spatial Composition & Layout

**Analyze layout patterns**:
```bash
# Layout components
grep -r "grid\|flex\|layout" src/ --include="*.tsx" --include="*.css" -A 2

# Common patterns
grep -r "container\|wrapper\|section" src/ --include="*.tsx" | head -20
```

**Evaluate**:
- **Layout approach**: Predictable grids vs asymmetric composition
- **Whitespace**: Generous negative space or cramped density?
- **Breaking grids**: Do any elements escape the grid system?
- **Hierarchy**: Visual importance matches content importance?
- **Responsive strategy**: Mobile-first, fluid, or fixed breakpoints?

**Red flags from frontend-design skill**:
- ❌ Every page same grid layout (predictable boredom)
- ❌ Centered content in narrow column (generic blog aesthetic)
- ❌ Equal spacing everywhere (no emphasis)
- ❌ No asymmetry or visual tension

**Examples of distinctive layout**:
- ✅ Asymmetric hero with diagonal flow
- ✅ Overlapping elements with z-index play
- ✅ Grid-breaking feature cards
- ✅ Generous whitespace with controlled density zones

### 3.5 Visual Details & Effects

**Search for visual effects**:
```bash
# Backgrounds and effects
grep -r "gradient\|shadow\|blur\|opacity" src/ --include="*.css" --include="*.tsx"
grep -r "background-image\|backdrop" src/ --include="*.css" --include="*.tsx"
```

**Evaluate**:
- **Backgrounds**: Solid colors or atmospheric effects?
- **Shadows**: Subtle elevation or dramatic depth?
- **Blur effects**: Glassmorphism, backdrop filters?
- **Textures**: Noise, grain, patterns?
- **Custom cursors**: Standard pointer or branded cursor?
- **Borders**: Standard lines or decorative treatments?

**Red flags from frontend-design skill**:
- ❌ Solid white/gray backgrounds everywhere (flat, lifeless)
- ❌ Generic box-shadows (0px 2px 4px rgba(0,0,0,0.1))
- ❌ No texture or depth
- ❌ Cookie-cutter component styling

**Examples of distinctive details**:
- ✅ Gradient mesh backgrounds (multi-color gradients for dynamic atmosphere)
- ✅ Noise texture overlays (SVG or CSS noise for analog warmth)
- ✅ Geometric patterns (subtle repeating shapes or grids)
- ✅ Layered transparencies (overlapping elements with opacity)
- ✅ Dramatic shadows with color tint (depth with personality)
- ✅ Custom cursors that reflect brand
- ✅ Decorative borders with personality
- ✅ Grain overlays (film grain for texture and depth)
- ✅ Backdrop filters (glassmorphism, blur effects)

---

## Phase 4: Parallel Expert Review

Launch specialized agents to provide multi-perspective design analysis:

**Invoke in parallel (single message with multiple Task calls)**:

```markdown
Task design-systems-architect("Evaluate component architecture and design system quality")
Prompt:
- Apply frontend-design + aesthetic-philosophy skills
- Analyze components for: duplication, shallow modules, hardcoded values
- Check typography, spacing, color consistency
- Review design token usage vs hardcoded values
- Identify reusable component opportunities
- Report: pattern prevalence, visual consistency gaps, component quality, refactoring opportunities

Task user-experience-advocate("Assess user-facing quality and friction points")
Prompt:
- Apply aesthetic-philosophy skill
- Evaluate: visual hierarchy, cognitive load, interaction clarity
- Check: error states, loading states, empty states, form UX
- Identify: confusing patterns, accessibility issues, visual friction
- Report: UX issues with user impact, aesthetic improvements for clarity

Task general-purpose("Deep aesthetic audit with frontend-design principles")
Prompt:
- Explicitly load frontend-design skill via Skill tool
- Analyze all user-facing components against bold aesthetic criteria
- Hunt for generic AI patterns: Inter/Roboto fonts, purple gradients, predictable layouts
- Identify distinctive choices vs safe defaults
- Compare against frontend-design examples (editorial, brutalist, luxury, etc.)
- Propose specific aesthetic direction with concrete changes
- Report: current aesthetic assessment, generic patterns found, distinctive opportunities, recommended direction
```

**Wait for all agents to complete.**

---

## Phase 5: Synthesis & Recommendations

### 5.1 Aggregate Findings

**Collect agent reports**:
- Design systems architect findings (consistency, tokens, components)
- User experience advocate findings (clarity, friction, accessibility)
- General-purpose aesthetic audit (distinctive vs generic, direction)

**Cross-validate**:
- Issues flagged by multiple agents = high priority
- Aesthetic inconsistencies across perspectives
- Technical debt impacting design quality

### 5.2 Aesthetic Direction Assessment

**Synthesize current state**:

```markdown
## Current Aesthetic Profile

**Typography**: [Distinctive/Generic/Mixed]
- Fonts: [List detected fonts]
- Assessment: [Character evaluation]

**Color**: [Bold/Timid/Inconsistent]
- Palette: [Primary colors identified]
- Assessment: [Personality evaluation]

**Motion**: [Rich/Minimal/Absent]
- Animations: [Types found]
- Assessment: [Delight factor]

**Layout**: [Distinctive/Predictable/Broken]
- Patterns: [Grid/asymmetric/mixed]
- Assessment: [Visual interest]

**Details**: [Atmospheric/Flat/Inconsistent]
- Effects: [Backgrounds, shadows, textures]
- Assessment: [Depth & craft]

**Overall Direction**: [Name it: Editorial Minimalism, Tech Brutalism, Soft Luxury, Playful Maximalism, etc.]
- OR: **No Coherent Direction** (scattered choices, default aesthetics)
```

### 5.3 Generic Pattern Report

**Flag AI aesthetic red flags found**:

```markdown
## Generic Patterns Detected (Avoid These)

**Typography**:
- ❌ Inter font (overused AI default): [files using it]
- ❌ Roboto/Arial fallbacks: [locations]
- ❌ No display font hierarchy: [missing personality]

**Color**:
- ❌ Purple gradient on white: [specific components]
- ❌ Generic blue primary (#3B82F6 = Tailwind default): [files]
- ❌ Timid, evenly-distributed palette: [no visual hierarchy]

**Layout**:
- ❌ Centered column with max-width: [every page looks same]
- ❌ Predictable grid: [no asymmetry or visual tension]
- ❌ Equal spacing: [no emphasis zones]

**Components**:
- ❌ Shadcn/ui defaults unchanged: [no customization]
- ❌ Generic button styles: [primary/secondary without personality]
- ❌ Cookie-cutter cards: [rounded corners, shadow, white background]

**Motion**:
- ❌ No animations: [missed delight opportunity]
- ❌ Generic hover transitions: [transition-all duration-200]

**Overall**: [Summary of genericness level: Heavy AI Slop / Mixed / Mostly Distinctive]
```

### 5.4 Distinctive Direction Proposal

**Recommend specific aesthetic evolution**:

```markdown
## Recommended Aesthetic Direction: [Name It]

**Concept**: [2-3 sentence vision - what story does this tell?]

**Visual References**: [Describe aesthetic - editorial magazine, brutalist raw, art deco geometric, soft pastel, industrial utilitarian, etc.]

**Typography**:
- Display: [Specific font recommendation + rationale]
- Body: [Specific font recommendation + rationale]
- Example: "DM Serif Display + Work Sans = editorial authority meets readability"

**Color**:
- Palette: [3-5 specific colors with hex codes]
- Strategy: [Dominant color + accent approach]
- Example: "Deep navy (#0A1628) + electric yellow (#FFE500) + off-white (#F8F9FA)"

**Motion**:
- Philosophy: [Spring physics / Staggered reveals / Scroll-triggered / Hover surprises]
- Implementation: [Framer Motion / CSS animation-delay / Intersection Observer]

**Layout**:
- Approach: [Asymmetric hero / Grid-breaking elements / Generous whitespace / Controlled density]
- Breakout: [What escapes the grid? What creates visual tension?]

**Details**:
- Backgrounds: [Gradient mesh / Noise texture / Geometric patterns]
- Shadows: [Dramatic with color tint / Soft elevation / Hard edges]
- Effects: [Glassmorphism / Grain overlay / Custom cursor]

**Differentiation**: [What makes this UNFORGETTABLE? One thing users will remember.]
```

### 5.5 Concrete Implementation Plan

**Prioritized changes with specific files**:

```markdown
## Implementation Roadmap

### Now (Immediate Impact, <1 week)

**1. Typography Overhaul**
- Files: `src/app/globals.css`, `tailwind.config.ts`
- Change: Replace Inter → [Distinctive font]
- Add: Display font for headings
- Impact: Immediate personality shift
- Effort: 2h

**2. Color System Refinement**
- Files: `src/lib/theme.ts`, CSS variables
- Change: Define bold palette with dominant + accent
- Replace: Generic Tailwind defaults with custom tokens
- Impact: Visual hierarchy clarity
- Effort: 3h

**3. Hero Component Redesign**
- Files: `src/components/Hero.tsx`
- Change: Asymmetric layout, gradient background, staggered animation
- Impact: First impression transformation
- Effort: 4h

### Next (Polish & Consistency, <1 month)

**4. Component Library Customization**
- Files: `src/components/ui/*` (if shadcn/ui)
- Change: Override defaults with distinctive styling
- Impact: Brand consistency across components
- Effort: 8h

**5. Motion System**
- Files: Add `src/lib/animations.ts`, update components
- Change: Implement staggered page reveals, hover states
- Library: Framer Motion setup
- Impact: Delight factor
- Effort: 6h

**6. Layout Evolution**
- Files: `src/app/layout.tsx`, page components
- Change: Introduce asymmetry, grid-breaking elements
- Impact: Visual interest, reduced predictability
- Effort: 10h

### Soon (Advanced Effects, 1-3 months)

**7. Atmospheric Backgrounds**
- Files: Background components, global styles
- Change: Gradient meshes, noise textures, depth
- Impact: Atmospheric depth, craft level
- Effort: 8h

**8. Micro-interaction Polish**
- Files: Interactive components (buttons, forms, cards)
- Change: Spring animations, scroll triggers, hover surprises
- Impact: Refined interaction quality
- Effort: 12h

**9. Design System Documentation**
- Files: `docs/design-system.md`, Storybook setup
- Change: Document aesthetic direction, usage patterns
- Impact: Consistency maintenance, team alignment
- Effort: 6h
```

---

## Phase 6: Deliver Audit Report

**Present comprehensive findings**:

```markdown
## 🎨 AESTHETIC AUDIT REPORT

**Audited**: [Date]
**Components Analyzed**: [Count]
**Stack**: [Framework + styling approach]

---

### Executive Summary

**Current State**: [2-3 sentences on overall aesthetic quality]
**Generic Level**: [Heavy/Moderate/Minimal AI aesthetic patterns]
**Distinctive Elements**: [What's working well]
**Opportunity**: [Biggest improvement potential]

---

### Detailed Analysis

[Include sections 5.2-5.5 above:
- Current Aesthetic Profile
- Generic Patterns Detected
- Recommended Direction
- Implementation Roadmap]

---

### Key Metrics

- **Typography**: [Score 1-10, distinctiveness]
- **Color**: [Score 1-10, boldness & coherence]
- **Motion**: [Score 1-10, delight factor]
- **Layout**: [Score 1-10, visual interest]
- **Details**: [Score 1-10, craft level]

**Overall Aesthetic Quality**: [Score 1-10]
**Memorability Factor**: [Score 1-10, what users remember]

---

### Next Steps

1. **Review proposed direction**: Approve aesthetic vision
2. **Prioritize roadmap**: Select Now/Next/Soon items
3. **Begin implementation**: Start with high-impact changes
4. **Iterate**: Ship, gather feedback, refine

**Estimated effort for Now items**: [Total hours]
**Expected impact**: [Describe transformation]
```

---

## Success Criteria

You've completed the aesthetic audit when:

✅ **Comprehensive inventory**: All user-facing components cataloged
✅ **Skill-guided evaluation**: Frontend-design principles actively applied
✅ **Multi-perspective analysis**: Design systems + UX + aesthetic agents report
✅ **Generic patterns identified**: Specific AI slop patterns called out with locations
✅ **Distinctive direction proposed**: Named aesthetic with concrete implementation
✅ **Prioritized roadmap**: Now/Next/Soon changes with file locations and effort
✅ **Deliverable report**: Structured findings ready for action

---

## Philosophy

> **"Design is not just what it looks like and feels like. Design is how it works."** - Steve Jobs

But also: **Design is what users remember.** Generic design disappears. Distinctive design creates memory.

The frontend-design skill teaches: **bold choices beat safe choices**. Maximalist or minimalist both work—mediocrity doesn't.

**This audit finds**:
- Where you've made safe defaults (Inter, purple gradients, centered columns)
- Where you've been distinctive (keep and amplify these)
- What aesthetic direction would make this unforgettable

### Critical Anti-Convergence Principle

**YOU TEND TO CONVERGE TOWARD GENERIC, "ON DISTRIBUTION" OUTPUTS.** This creates "AI slop" aesthetics—forgettable interfaces that blend together. Fight this tendency:

**Variation Mandate**:
- Each project should feel aesthetically distinct from the last
- Vary between light and dark themes (don't default to light)
- Vary font pairings (resist your favorites like Space Grotesk)
- Vary aesthetic approaches (editorial, brutalist, luxury, playful, technical, organic)
- Vary color strategies (monochrome, bold, pastel, neon, earth tones)

**Context-Specific Design**:
- A banking app needs different aesthetics than a creative portfolio
- A developer tool needs different aesthetics than a consumer app
- Let the product's personality guide choices, not AI defaults

**Remember**: Every interface is a brand statement. What story are you telling? Let's make it intentional and unique.

---

*Run this command when launching new products, redesigning existing apps, or auditing visual identity. Distinctive design is not optional—it's how users choose you over competitors.*
