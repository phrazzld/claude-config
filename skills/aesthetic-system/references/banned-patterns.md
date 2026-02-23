# Banned Patterns

Explicit "never use" elements to avoid AI slop and generic aesthetics.

## Banned Elements

### Typography

**BANNED fonts:**
- Inter
- Roboto
- Arial
- system-ui
- Open Sans
- Space Grotesk (AI favorite)
- Satoshi (overused)

**BANNED patterns:**
- Oversized H1s that scream — control hierarchy with weight and color, not massive scale
- Serif fonts in dashboard/software UIs — use high-end sans-serif pairings (Geist + Geist Mono, Satoshi + JetBrains Mono)

**Why:** These are defaults that signal "no decision was made."

**Instead:** Choose fonts with character that match the brand soul.

### Layout Patterns

**BANNED:**
- Hero badges/pills above headlines ("New", "AI-Powered", "Introducing", "Beta")
- Predictable hero → CTA → features → testimonials → footer
- `max-w-7xl mx-auto` centered everything
- Generic grid cards with even spacing
- Hamburger menu hiding everything on mobile
- 3-column equal-card feature rows (use 2-column zig-zag, asymmetric grid, or horizontal scroll)
- Complex flexbox percentage math (`w-[calc(33%-1rem)]`) — use CSS Grid instead

**Why:** These patterns are templates, not designs.

**Instead:** Start from content and meaning, not from patterns.

### Color

**BANNED:**
- Purple/blue gradients on white backgrounds
- Tailwind default colors without customization (blue-500, etc.)
- Pure grays (no brand tinting)
- Generic semantic names without personality

**Why:** These are the statistical average of all AI outputs.

**Instead:** Commit to a color voice. Tint your neutrals with brand hue.

### Visual Elements

**BANNED:**
- Generic geometric shapes
- Abstract blobs
- Excessive uniform rounded corners everywhere
- Gradients that "glow" without purpose
- Stock illustration styles
- Neon/outer `box-shadow` glows (use inner borders or subtle tinted shadows)
- Pure black `#000000` (use off-black, Zinc-950, or charcoal)
- Oversaturated accents (saturation > 80%)
- Excessive gradient-fill text on large headers
- Custom mouse cursors (outdated, hurts performance/accessibility)

**Why:** Decoration without meaning is noise.

**Instead:** Every visual element should serve a purpose or tell a story.

### Alert/Callout Patterns

**BANNED:**
- Left border accent with rounded corners (e.g., `border-left: 3px solid color; border-radius: 8px`)
- The "rounded card with colored left stripe" pattern for alerts, warnings, info boxes

**Why:** This is one of the most overused AI patterns. It's lazy, generic, and signals "no thought was applied." Every AI chatbot and generated codebase uses this exact pattern.

**Instead:** Consider:
- Full-width colored background with subtle tint
- Icon-led alerts with the icon providing the semantic color
- Top border or bottom border instead of left
- No border at all — use background color alone
- Outlined/stroke style cards
- Inset box shadows for depth
- Completely custom alert paradigms (toast, banner, inline text)

### Motion

**BANNED:**
- `transition-all duration-200` everywhere
- Instant state changes with no acknowledgment
- Decorative animations that distract from content
- Scattered micro-interactions without coherence

**Why:** Motion should be orchestrated, not sprinkled.

**Instead:** One well-choreographed page load beats 20 random hover effects.

### Content & Data

**BANNED:**
- Generic placeholder names ("John Doe", "Jane Smith", "Acme Corp") — use realistic, creative names
- Generic SVG "egg" or Lucide user icons for avatars — use photo placeholders or distinctive styling
- Predictable fake numbers (99.99%, exactly 50%, `1234567`) — use organic messy data (47.2%, +1 (312) 847-1928)
- Startup slop names ("Acme", "Nexus", "SmartFlow") — invent premium contextual brand names
- AI copywriting filler ("Elevate", "Seamless", "Unleash", "Next-Gen") — use concrete verbs

**Why:** Fake-looking placeholder data breaks immersion and signals a lazy prototype, not a designed product.

### External Resources & Components

**BANNED:**
- Unsplash image URLs (frequently return 404) — use `https://picsum.photos/seed/{string}/800/600` or SVG UI Avatars
- `shadcn/ui` in generic default state — always customize radii, colors, and shadows to match project aesthetic

**Why:** Broken images and unmodified shadcn are the fastest ways to signal "AI-generated slop."

## Self-Review Checklist

Before delivering any design, scan for violations:

```
[ ] No hero badges above headlines?
[ ] No banned fonts (Inter, Roboto, Arial, Space Grotesk)?
[ ] No purple/blue gradient on white?
[ ] No Tailwind defaults without customization?
[ ] No generic geometric shapes/blobs?
[ ] No left-border-accent alerts with rounded corners?
[ ] Layout starts from content, not template?
[ ] Mobile has real navigation, not buried hamburger?
[ ] Motion is orchestrated, not scattered?
[ ] No neon/outer box-shadow glows?
[ ] No pure black (#000000)?
[ ] No 3-column equal card layouts?
[ ] No generic placeholder names/avatars/numbers?
[ ] No Unsplash image URLs?
[ ] shadcn customized to project aesthetic (not default)?
[ ] Full-height sections use min-h-[100dvh] not h-screen?
```

## The "Discard First 10" Rule

When generating proposals or improvements:

> Mentally discard your first 10 ideas. These are usually the statistical average—the patterns most frequently seen in training data. The 11th idea is where originality begins.

Practically: Before committing to any design choice, ask:
- "Is this what everyone would do?"
- "What's a distinctive alternative?"
- "Would this be memorable?"

## Pattern Detection

Watch for these red flags in your output:

| Red Flag | What It Signals |
|----------|-----------------|
| `font-sans` without override | No typography decision |
| `bg-white` + purple accent | AI default palette |
| Centered cards in 3-column grid | Template thinking |
| "Introducing" badge | Startup cliche |
| Hamburger menu everywhere | Laziness |
| `border-left` + `border-radius` on alerts | Peak AI slop |

When you catch yourself reaching for these, stop and choose something intentional.
