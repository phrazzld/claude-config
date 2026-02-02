# Heartbeat Hearthstone Design Audit

Audit Heartbeat components for Hearthstone design system compliance.

## Trigger
- `heartbeat:audit-design` or `/heartbeat:audit-design`
- When asked to check Heartbeat design compliance
- When asked to audit Heartbeat styling

## Scope
- Only applies to `/Users/phaedrus/Development/heartbeat` project
- Checks React components, CSS, and TypeScript files

## Hearthstone Design System Rules

### Colors (MUST use CSS variables)

**Light Mode:**
| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | `#f5efe5` | Main background |
| `--color-bg-secondary` | `#f0e8dc` | Secondary surfaces |
| `--color-bg-elevated` | `#faf6f0` | Cards, elevated surfaces |
| `--color-text-primary` | `#2a2018` | Primary text |
| `--color-text-secondary` | `#5c4a3a` | Secondary text |
| `--color-accent-primary` | `#a0522d` | Buttons, links |
| `--color-status-up` | `#d4891a` | Healthy status |
| `--color-status-degraded` | `#c1762e` | Warning status |
| `--color-status-down` | `#8b7359` | Error status |

**Dark Mode:**
| Token | Value | Usage |
|-------|-------|-------|
| `--color-bg-primary` | `#1f1815` | Main background |
| `--color-text-primary` | `#faf6f0` | Primary text |
| `--color-accent-primary` | `#ff9500` | Ember glow |
| `--color-status-up` | `#ffb366` | Healthy status |

### Typography

**Allowed fonts:**
- Display: `Lora` (serif)
- Body: `Nunito` (rounded sans)
- Mono: `IBM Plex Mono`

**Banned fonts (from other systems):**
- Inter, Roboto, Space Grotesk
- Noto Serif JP, Manrope

### Animations

**Use these (Hearthstone):**
- `animate-hs-ember-pulse` - Status indicator up
- `animate-hs-ember-flicker` - Status indicator degraded
- `animate-hs-float-up` - Ember particles
- `animate-hs-fade-in` - Enter animations
- `animate-hs-fade-in-up` - Enter with motion

**Remove these (Kyoto Moss):**
- `animate-km-breathe` → `animate-hs-ember-pulse`
- `animate-km-breathe-subtle` → `animate-hs-ember-flicker`
- `animate-km-fade-in` → `animate-hs-fade-in`
- `animate-zen-*` → `animate-hs-*`

### Border Radii (softer)
- `--radius-sm`: 6px (was 4px)
- `--radius-md`: 8px
- `--radius-lg`: 12px
- `--radius-xl`: 16px

## Quick Audit Commands

```bash
# Find banned fonts
grep -rn "Inter\|Roboto\|Space Grotesk\|Noto Serif\|Manrope" --include="*.tsx" --include="*.ts" /Users/phaedrus/Development/heartbeat

# Find old animations
grep -rn "animate-km-\|animate-zen-" --include="*.tsx" --include="*.ts" --include="*.css" /Users/phaedrus/Development/heartbeat

# Find hardcoded colors (excluding CSS files)
grep -rn "#[0-9a-fA-F]\{6\}" --include="*.tsx" --include="*.ts" /Users/phaedrus/Development/heartbeat | grep -v "var(--"

# Find rgba/rgb colors
grep -rn "rgb(" --include="*.tsx" --include="*.ts" /Users/phaedrus/Development/heartbeat
```

## Workflow

1. Run quick audit commands above
2. Review each finding
3. For hardcoded colors: Replace with `var(--color-*)` tokens
4. For banned fonts: Replace with Lora/Nunito/IBM Plex Mono
5. For old animations: Replace with `animate-hs-*` classes
6. Verify with `pnpm type-check && pnpm lint`

## Components to Check

Priority components for visual consistency:
1. `components/ui/StatusIndicator.tsx` - Status dot animations
2. `app/page.tsx` - Landing page hero
3. `components/landing/StatusDisplayVariants.tsx` - Bento grid card
4. `components/DashboardMonitorCard.tsx` - Monitor cards
5. `app/globals.css` - Token definitions

## Success Criteria

- [ ] No banned fonts in codebase
- [ ] No old animation classes
- [ ] No hardcoded colors in components
- [ ] EmberParticles on landing page hero
- [ ] StatusIndicator uses `animate-hs-ember-pulse`
- [ ] `pnpm type-check` passes
- [ ] `pnpm lint` passes
