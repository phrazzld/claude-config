# Order Mode Refinement: Three Critical Issues

## Issues Identified

### 1. Dark Mode Colorscheme Failure
**Problem**: "Espresso & Cream" palette creates visual monotony
- Everything in same brown hue family (50-55)
- Cards don't pop against background
- Hint buttons look flat and indistinguishable
- Overall feels muddy and dull

### 2. DocumentHeader Redundancy
**Problem**: Takes significant vertical space for mostly redundant info
- "Chronological Sorting Exercise" duplicates "Order Mode" from ModeHero
- Timeline visualization is nice-to-have, not essential
- Creates visual clutter before the main interaction

### 3. Scroll vs Drag Conflict (Mobile)
**Problem**: Accidental drag when trying to scroll
- `PointerSensor` distance: only 4px to trigger drag
- Entire card body has `cursor-grab` styling
- Cards extend below viewport, making scroll necessary

---

## Design Options

### Dark Mode Palette Alternatives

| Option | Direction | Pros | Cons |
|--------|-----------|------|------|
| **A: Ink & Paper** | Near-black bg + bright cream cards (L=0.50) | Dramatic contrast, magazine-like | May be too stark |
| **B: Midnight & Amber** | Deep navy bg + warm amber accents | Temperature contrast, distinctive | Diverges from brand |
| **C: Charcoal & Pearl** | Neutral gray bg + warm pearl cards | Clean, professional | May feel generic |
| **D: Forest & Candlelight** | Deep green bg + warm cream | Unique, evocative | Very different feel |

**Recommendation**: **Option A (Ink & Paper)** - Commit to high contrast
```css
--background: oklch(0.12 0.02 250);     /* Near-black with cool tint */
--card: oklch(0.50 0.04 85);            /* Actual cream - dramatic lift */
--card-foreground: oklch(0.15 0.02 50); /* Dark text on light cards */
```

### DocumentHeader Alternatives

| Option | Approach | Pros | Cons |
|--------|----------|------|------|
| **A: Merge into ModeHero** | Delete card, add puzzle # to header | Cleanest, saves space | Loses timeline viz |
| **B: Minimal Badge** | Inline pill: "Puzzle #16 · 3.6k years" | Compact | May feel hidden |
| **C: Timeline Spine** | Integrate into card list as visual spine | Elegant | More complex |
| **D: Collapsible** | Make it expandable/dismissable | Flexible | Extra interaction |

**Recommendation**: **Option A** - Merge essential info into ModeHero
- Move "Puzzle №16" to ModeHero (between eyebrow and title or after title)
- Delete DocumentHeader component entirely
- Optional: Add year range as subtle metadata below cards

### Scroll vs Drag Alternatives

| Option | Approach | Pros | Cons |
|--------|----------|------|------|
| **A: Handle-Only Drag** | Only grip dots initiate drag | Most intentional | Smaller target |
| **B: Long Press** | 150-250ms delay to start drag | Clear intent | Slight friction |
| **C: Higher Distance** | Increase from 4px to 12px | Simple | Still conflicts |
| **D: Swipe Gesture** | Horizontal swipe to reorder | Novel | Learning curve |

**Recommendation**: **Option A + B combined**
- Drag ONLY from the grip handle (not card body)
- Add 150ms delay constraint for touch
- Increase distance to 8px as secondary protection

---

## Implementation Plan

### Phase 1: Dark Mode Palette Overhaul
**File**: `src/app/globals.css` (html.dark block)

Key changes:
```css
html.dark {
  /* INK & PAPER - High contrast dark mode */

  /* Background: Cool near-black (away from brown) */
  --color-parchment-50: oklch(0.12 0.02 250);

  /* Cards: Actual visible cream (dramatic lift) */
  --color-parchment-100: oklch(0.50 0.04 85);
  --color-parchment-200: oklch(0.45 0.04 85);
  --color-parchment-300: oklch(0.40 0.03 85);

  /* Text on cards needs to be DARK now */
  --card-foreground: oklch(0.18 0.02 50);

  /* Borders: Strong definition */
  --border: oklch(0.35 0.03 250);
}
```

**Critical**: Cards become LIGHT in dark mode, so card text must be DARK.

### Phase 2: Delete DocumentHeader, Enhance ModeHero
**Files**:
- `src/components/order/DocumentHeader.tsx` - DELETE
- `src/components/order/OrderGameBoard.tsx` - Remove DocumentHeader usage
- `src/components/order/OrderInstructions.tsx` - Add puzzle context

New ModeHero structure:
```
DAILY PUZZLE · №16              ← Eyebrow with puzzle number
Order Mode                       ← Title
Arrange events from earliest to latest  ← Subtitle
```

### Phase 3: Fix Scroll/Drag Conflict
**Files**:
- `src/components/order/OrderEventList.tsx` - Update sensor config
- `src/components/order/DraggableEventCard.tsx` - Restrict drag listeners

Sensor changes:
```tsx
const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: {
      distance: 8,      // Increased from 4
      delay: 150,       // Add delay for touch
      tolerance: 5,     // Allow small movements during delay
    },
  }),
  // ... keyboard sensor
);
```

Card changes:
- Remove `cursor-grab` from card body
- Keep drag listeners ONLY on grip handle div
- Card content becomes non-draggable (can scroll over it)

---

## Files to Modify

1. **`src/app/globals.css`** - Dark mode palette overhaul
2. **`src/components/order/DocumentHeader.tsx`** - DELETE
3. **`src/components/order/OrderGameBoard.tsx`** - Remove DocumentHeader
4. **`src/components/order/OrderInstructions.tsx`** - Add puzzle context
5. **`src/components/order/OrderEventList.tsx`** - Sensor config
6. **`src/components/order/DraggableEventCard.tsx`** - Drag handle isolation

---

## Success Criteria

1. **Dark Mode**: Cards visibly pop against background, hint buttons distinguishable
2. **Header**: No redundant "Chronological Sorting Exercise" card, puzzle info visible
3. **Mobile UX**: Can scroll through cards without accidentally dragging
