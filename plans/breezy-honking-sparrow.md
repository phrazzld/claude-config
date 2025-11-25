# Fix: Projects Heading Dark Mode Visibility

## Root Cause

**Semantic/hardcoded color mismatch** between abstraction levels:

1. `projects-lab.tsx:18` uses hardcoded light-mode colors: `bg-zinc-100 text-zinc-900`
2. `section-header.tsx:29` uses semantic `text-foreground` (auto-switches via CSS variables)
3. In dark mode:
   - Section background stays `zinc-100` (light gray `#f4f4f5`)
   - `text-foreground` flips to off-white (`#f5f5f5`)
   - **Result: Off-white text on light gray = invisible**

## Section Theming Audit

| Section | Pattern | Status |
|---------|---------|--------|
| Hero | Semantic (`bg-background`, `text-foreground`) | ✓ Works |
| Services Schematic | Semantic (`bg-background`, `text-foreground`) | ✓ Works |
| Projects Lab | Hardcoded light-only (`bg-zinc-100`) | ✗ Broken |
| CTA Contact | Hardcoded dark-only (`bg-zinc-950`) | ⚠ Intentional |

**Dominant pattern**: Semantic tokens (2/4 sections)

## Strategic Fix (Ousterhout-Aligned)

**Migrate Projects Lab to semantic tokens** - Match the dominant pattern (Hero, Services).

This follows Ousterhout's principles:
- **Consistent abstraction level**: All sections use same theming approach
- **Information hiding**: Section doesn't need to know light/dark implementation
- **Single source of truth**: Theme logic lives in CSS variables, not scattered

## Changes

### `components/sections/projects-lab.tsx`

**Section container (line 18):**
```diff
- bg-zinc-100 py-24 text-zinc-900
+ bg-muted py-24 text-foreground
```

**Diagonal lines texture (lines 23-26):**
```diff
- backgroundImage: 'repeating-linear-gradient(45deg, #000 0, #000 1px, transparent 0, transparent 50%)',
+ backgroundImage: 'repeating-linear-gradient(45deg, currentColor 0, currentColor 1px, transparent 0, transparent 50%)',
```
Also change `opacity-[0.03]` to work in both modes.

**Product cards (line 43):**
```diff
- border border-zinc-200 bg-white
+ border border-border bg-card
```

**Status badge text (line 56):**
```diff
- text-zinc-400
+ text-muted-foreground
```

**Product name (line 62):**
```diff
- text-zinc-900
+ text-foreground
```

**Description (line 67):**
```diff
- text-zinc-500
+ text-muted-foreground
```

**Button styling (lines 78, 94):**
```diff
- border-zinc-200 bg-transparent text-zinc-600
- hover:border-zinc-900 hover:bg-zinc-900 hover:text-white
+ border-border bg-transparent text-muted-foreground
+ hover:border-foreground hover:bg-foreground hover:text-background
```

## Token Mapping Reference

| Hardcoded | Semantic Token |
|-----------|----------------|
| `bg-zinc-100` | `bg-muted` |
| `bg-white` | `bg-card` |
| `text-zinc-900` | `text-foreground` |
| `text-zinc-500/400/600` | `text-muted-foreground` |
| `border-zinc-200` | `border-border` |

## Out of Scope

**CTA Contact section** - Intentionally always-dark for emphasis. Different design pattern (forced contrast). Leave as-is unless user requests.

## Files to Modify

- `components/sections/projects-lab.tsx` - Convert all hardcoded colors to semantic tokens
