---
name: design-tokens
description: "Apply design token patterns using Tailwind CSS 4 @theme directive: CSS variables, semantic naming, color systems, typography scales, spacing, dark mode. Use when designing UI systems, reviewing design consistency, or establishing brand guidelines. Integrates with frontend-design skill for aesthetic execution."
---

# Design Tokens

Modern design token patterns using Tailwind CSS 4's @theme directive for consistent, maintainable UI design systems.

## Philosophy

**Design tokens are the single source of truth for design decisions.** Rather than scattering magic numbers and colors throughout your codebase, centralize them as semantic variables that can be referenced everywhere.

**CSS-first in Tailwind 4**: No more JavaScript configuration. Define tokens directly in CSS using the `@theme` directive, making them available as Tailwind utilities and CSS variables.

**Semantic naming over descriptive**: `--color-primary` beats `--color-blue-500`. Semantic tokens communicate intent; descriptive tokens communicate implementation.

## Why Tailwind CSS 4 @theme

**Tailwind CSS 4 revolutionizes design token management:**
- **CSS-native**: Define tokens in CSS, not JavaScript config
- **Type-safe**: Auto-completion in editors
- **No build step overhead**: Faster development
- **CSS variable integration**: Use tokens anywhere (`var(--color-primary)`)
- **Dark mode built-in**: Theme-aware color switching

**Migration from Tailwind 3**: Delete `tailwind.config.js`, move to CSS `@theme` directive.

## Installation & Setup

```bash
# Install Tailwind CSS 4 (beta as of 2025)
pnpm add tailwindcss@next @tailwindcss/vite@next

# For Next.js projects
pnpm add tailwindcss@next @tailwindcss/postcss@next
```

## Basic @theme Structure

```css
/* app/globals.css or src/styles/theme.css */
@import "tailwindcss";

@theme {
  /* Brand hue - extract from your primary color's hue value */
  --brand-hue: 250;  /* Blue (change this to match your brand) */

  /* Color System */
  --color-primary: oklch(0.6 0.2 var(--brand-hue));
  --color-secondary: oklch(0.5 0.15 180);
  --color-accent: oklch(0.7 0.25 30);

  --color-success: oklch(0.6 0.18 140);
  --color-warning: oklch(0.7 0.2 80);
  --color-error: oklch(0.6 0.22 20);

  /* Brand-tinted neutrals (imperceptible tint creates cohesive feeling) */
  --color-background: oklch(0.995 0.005 var(--brand-hue));  /* Not pure white */
  --color-foreground: oklch(0.15 0.02 var(--brand-hue));    /* Not pure black */
  --color-muted: oklch(0.94 0.01 var(--brand-hue));
  --color-border: oklch(0.88 0.015 var(--brand-hue));

  /* Typography Scale */
  --font-size-xs: 0.75rem;      /* 12px */
  --font-size-sm: 0.875rem;     /* 14px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.125rem;     /* 18px */
  --font-size-xl: 1.25rem;      /* 20px */
  --font-size-2xl: 1.5rem;      /* 24px */
  --font-size-3xl: 1.875rem;    /* 30px */
  --font-size-4xl: 2.25rem;     /* 36px */
  --font-size-5xl: 3rem;        /* 48px */
  --font-size-6xl: 3.75rem;     /* 60px */

  /* Font Families */
  --font-sans: "Inter Variable", system-ui, sans-serif;
  --font-serif: "Merriweather", Georgia, serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;
  --font-display: "Clash Display", "Inter Variable", sans-serif;

  /* Spacing Scale */
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */
  --spacing-3xl: 4rem;     /* 64px */

  /* Border Radius */
  --radius-sm: 0.25rem;    /* 4px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-2xl: 1.5rem;    /* 24px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);

  /* Z-Index Layers */
  --z-base: 0;
  --z-dropdown: 1000;
  --z-sticky: 1100;
  --z-overlay: 1200;
  --z-modal: 1300;
  --z-popover: 1400;
  --z-tooltip: 1500;
}
```

## Dark Mode

Define dark mode variants using `@media (prefers-color-scheme: dark)`. **Keep brand hue in dark mode** - just invert lightness:

```css
@theme {
  --brand-hue: 250;

  /* Light mode (default) - brand-tinted */
  --color-background: oklch(0.995 0.005 var(--brand-hue));
  --color-foreground: oklch(0.15 0.02 var(--brand-hue));
  --color-muted: oklch(0.94 0.01 var(--brand-hue));
  --color-border: oklch(0.88 0.015 var(--brand-hue));

  @media (prefers-color-scheme: dark) {
    /* Dark mode - same hue, inverted lightness */
    --color-background: oklch(0.12 0.015 var(--brand-hue));
    --color-foreground: oklch(0.95 0.01 var(--brand-hue));
    --color-muted: oklch(0.22 0.02 var(--brand-hue));
    --color-border: oklch(0.28 0.025 var(--brand-hue));
  }
}
```

**Manual dark mode toggle** (class-based):

```css
@theme {
  --brand-hue: 250;
  --color-background: oklch(0.995 0.005 var(--brand-hue));
  --color-foreground: oklch(0.15 0.02 var(--brand-hue));
}

.dark {
  --color-background: oklch(0.12 0.015 var(--brand-hue));
  --color-foreground: oklch(0.95 0.01 var(--brand-hue));
}
```

```tsx
// Dark mode toggle component
'use client'

import { useEffect, useState } from 'react'

export function DarkModeToggle() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    const isDark = localStorage.getItem('theme') === 'dark'
    setIsDark(isDark)
    document.documentElement.classList.toggle('dark', isDark)
  }, [])

  const toggle = () => {
    const newIsDark = !isDark
    setIsDark(newIsDark)
    localStorage.setItem('theme', newIsDark ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', newIsDark)
  }

  return (
    <button onClick={toggle}>
      {isDark ? '☀️ Light' : '🌙 Dark'}
    </button>
  )
}
```

## Using Design Tokens

### In Tailwind Utilities

Design tokens automatically become Tailwind utilities:

```tsx
// Colors
<div className="bg-primary text-foreground">
<button className="bg-accent text-white">

// Typography
<h1 className="text-4xl font-display">
<p className="text-base font-sans">

// Spacing
<div className="p-md space-y-sm">
<section className="mb-xl">

// Border radius
<div className="rounded-lg">
<button className="rounded-full">

// Shadows
<div className="shadow-md">
<div className="shadow-lg hover:shadow-xl">
```

### In Custom CSS

Access tokens via CSS variables:

```css
.custom-component {
  background-color: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  font-family: var(--font-sans);
  transition: all var(--transition-base);
}

.custom-component:hover {
  background-color: var(--color-accent);
  box-shadow: var(--shadow-lg);
}
```

## Color System Design

### OKLCH Color Space (Recommended)

**Why OKLCH over RGB/HSL:**
- Perceptually uniform (consistent lightness across hues)
- Better for programmatic color generation
- Predictable color mixing
- Accessible contrast calculations

**Format**: `oklch(lightness chroma hue)`
- Lightness: 0 (black) to 1 (white)
- Chroma: 0 (gray) to ~0.4 (vivid)
- Hue: 0-360 degrees

```css
@theme {
  /* Primary color palette - Blue */
  --color-primary-50: oklch(0.95 0.02 250);
  --color-primary-100: oklch(0.9 0.05 250);
  --color-primary-200: oklch(0.8 0.1 250);
  --color-primary-300: oklch(0.7 0.15 250);
  --color-primary-400: oklch(0.65 0.18 250);
  --color-primary-500: oklch(0.6 0.2 250);    /* Base */
  --color-primary-600: oklch(0.5 0.2 250);
  --color-primary-700: oklch(0.4 0.18 250);
  --color-primary-800: oklch(0.3 0.15 250);
  --color-primary-900: oklch(0.2 0.1 250);

  /* Semantic aliases */
  --color-primary: var(--color-primary-500);
  --color-primary-hover: var(--color-primary-600);
  --color-primary-active: var(--color-primary-700);
}
```

### Semantic Color System

```css
@theme {
  /* Brand hue - single source of truth */
  --brand-hue: 250;  /* Extract from your primary color */

  /* Base palette */
  --color-brand-blue: oklch(0.6 0.2 250);
  --color-brand-purple: oklch(0.65 0.25 290);
  --color-brand-green: oklch(0.7 0.2 140);

  /* Semantic mappings */
  --color-primary: var(--color-brand-blue);
  --color-secondary: var(--color-brand-purple);
  --color-accent: var(--color-brand-green);

  /* State colors (keep distinct hues for clarity) */
  --color-success: oklch(0.65 0.18 140);  /* Green */
  --color-warning: oklch(0.7 0.2 80);     /* Yellow */
  --color-error: oklch(0.6 0.22 20);      /* Red */
  --color-info: oklch(0.65 0.2 230);      /* Blue */

  /* Surface colors - brand-tinted (chroma 0.005-0.02) */
  --color-background: oklch(0.995 0.005 var(--brand-hue));
  --color-foreground: oklch(0.15 0.02 var(--brand-hue));
  --color-surface: oklch(0.98 0.008 var(--brand-hue));
  --color-surface-hover: oklch(0.96 0.01 var(--brand-hue));

  /* Border colors - brand-tinted */
  --color-border: oklch(0.88 0.015 var(--brand-hue));
  --color-border-hover: oklch(0.8 0.02 var(--brand-hue));
  --color-border-focus: var(--color-primary);

  /* Text colors - brand-tinted */
  --color-text-primary: var(--color-foreground);
  --color-text-secondary: oklch(0.45 0.015 var(--brand-hue));
  --color-text-muted: oklch(0.55 0.01 var(--brand-hue));
  --color-text-disabled: oklch(0.65 0.008 var(--brand-hue));
}
```

**Why brand-tinted neutrals?** Pure grays (`oklch(x 0 0)`) feel generic. Adding imperceptible brand tint (chroma 0.005-0.02) creates cohesive "feeling" without visible color. Especially effective when semantic colors (red/green/blue) dominate.

## Typography System

### Type Scale

**Modular scale** (1.200 ratio recommended for web):

```css
@theme {
  /* Type scale using modular scale (1.200 ratio) */
  --font-size-xs: 0.694rem;     /* 11.11px */
  --font-size-sm: 0.833rem;     /* 13.33px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.2rem;       /* 19.20px */
  --font-size-xl: 1.44rem;      /* 23.04px */
  --font-size-2xl: 1.728rem;    /* 27.65px */
  --font-size-3xl: 2.074rem;    /* 33.18px */
  --font-size-4xl: 2.488rem;    /* 39.81px */
  --font-size-5xl: 2.986rem;    /* 47.78px */
  --font-size-6xl: 3.583rem;    /* 57.33px */
  --font-size-7xl: 4.300rem;    /* 68.80px */

  /* Line heights */
  --line-height-tight: 1.2;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Letter spacing */
  --letter-spacing-tight: -0.02em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.02em;
  --letter-spacing-wider: 0.05em;
}
```

### Font Pairings

**Avoid generic fonts (Inter, Roboto, Arial)**—choose distinctive, memorable fonts that align with brand personality (per frontend-design skill).

```css
@theme {
  /* Example: Editorial style */
  --font-display: "Clash Display", "Inter Variable", sans-serif;
  --font-sans: "Inter Variable", system-ui, sans-serif;
  --font-serif: "Merriweather", Georgia, serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;

  /* Font weights */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
}
```

**Font loading:**

```tsx
// app/layout.tsx (Next.js with next/font)
import { Inter, Merriweather, JetBrains_Mono } from 'next/font/google'
import localFont from 'next/font/local'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
const merriweather = Merriweather({
  weight: ['300', '400', '700'],
  subsets: ['latin'],
  variable: '--font-serif'
})
const jetbrains = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' })
const clashDisplay = localFont({
  src: './fonts/ClashDisplay-Variable.woff2',
  variable: '--font-display',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${merriweather.variable} ${jetbrains.variable} ${clashDisplay.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

## Spacing System

**8-point grid** (industry standard):

```css
@theme {
  /* Spacing scale (8px base unit) */
  --spacing-0: 0;
  --spacing-0\.5: 0.125rem;   /* 2px */
  --spacing-1: 0.25rem;       /* 4px */
  --spacing-2: 0.5rem;        /* 8px */
  --spacing-3: 0.75rem;       /* 12px */
  --spacing-4: 1rem;          /* 16px */
  --spacing-5: 1.25rem;       /* 20px */
  --spacing-6: 1.5rem;        /* 24px */
  --spacing-8: 2rem;          /* 32px */
  --spacing-10: 2.5rem;       /* 40px */
  --spacing-12: 3rem;         /* 48px */
  --spacing-16: 4rem;         /* 64px */
  --spacing-20: 5rem;         /* 80px */
  --spacing-24: 6rem;         /* 96px */
  --spacing-32: 8rem;         /* 128px */

  /* Semantic spacing */
  --spacing-xs: var(--spacing-1);
  --spacing-sm: var(--spacing-2);
  --spacing-md: var(--spacing-4);
  --spacing-lg: var(--spacing-6);
  --spacing-xl: var(--spacing-8);
  --spacing-2xl: var(--spacing-12);
  --spacing-3xl: var(--spacing-16);
}
```

## Responsive Breakpoints

```css
@theme {
  /* Breakpoints */
  --screen-sm: 640px;
  --screen-md: 768px;
  --screen-lg: 1024px;
  --screen-xl: 1280px;
  --screen-2xl: 1536px;
}
```

**Usage with media queries:**

```css
.container {
  padding: var(--spacing-md);

  @media (min-width: theme(--screen-md)) {
    padding: var(--spacing-lg);
  }

  @media (min-width: theme(--screen-xl)) {
    padding: var(--spacing-2xl);
  }
}
```

## Component Tokens

Define component-specific tokens for consistency:

```css
@theme {
  /* Button tokens */
  --button-height-sm: 2rem;
  --button-height-md: 2.5rem;
  --button-height-lg: 3rem;
  --button-padding-x: var(--spacing-4);
  --button-border-radius: var(--radius-md);

  /* Input tokens */
  --input-height: 2.5rem;
  --input-padding-x: var(--spacing-3);
  --input-border-width: 1px;
  --input-border-radius: var(--radius-md);
  --input-border-color: var(--color-border);
  --input-focus-border-color: var(--color-primary);
  --input-focus-ring-width: 2px;
  --input-focus-ring-color: oklch(from var(--color-primary) l c h / 0.2);

  /* Card tokens */
  --card-padding: var(--spacing-6);
  --card-border-radius: var(--radius-lg);
  --card-border-color: var(--color-border);
  --card-shadow: var(--shadow-sm);
  --card-shadow-hover: var(--shadow-md);
}
```

## Animation Tokens

```css
@theme {
  /* Durations */
  --duration-instant: 0ms;
  --duration-fast: 150ms;
  --duration-base: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;

  /* Easing functions */
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

  /* Combined transitions */
  --transition-fast: var(--duration-fast) var(--ease-out);
  --transition-base: var(--duration-base) var(--ease-in-out);
  --transition-slow: var(--duration-slow) var(--ease-in-out);
}
```

### WebGL & Shader Integration

When using Three.js or GLSL shaders, export tokens in formats shaders can consume:

```css
@theme {
  /* Shader-compatible color format (RGB normalized 0-1) */
  /* Use these for uniforms in GLSL */
  --color-primary-rgb: 0.376 0.510 0.965;  /* oklch(0.6 0.2 250) → RGB */
  --color-accent-rgb: 0.878 0.420 0.420;

  /* Animation timing for GSAP/Lottie sync */
  --duration-stagger: 50ms;      /* Delay between staggered elements */
  --duration-reveal: 600ms;      /* Page reveal animations */
  --duration-scroll: 1000ms;     /* Scroll-triggered sequences */

  /* Spring physics (for Framer Motion / GSAP) */
  --spring-stiffness: 300;
  --spring-damping: 30;
  --spring-mass: 1;
}
```

**Accessing tokens in JavaScript for Three.js:**
```tsx
const styles = getComputedStyle(document.documentElement)
const primaryRGB = styles.getPropertyValue('--color-primary-rgb')
  .split(' ')
  .map(Number) // [0.376, 0.510, 0.965]
```

## Integration with frontend-design Skill

**Design tokens provide the foundation; frontend-design provides the aesthetic direction.**

```css
/* Design tokens define the system */
@theme {
  --color-primary: oklch(0.6 0.2 250);
  --font-display: "Clash Display", sans-serif;
  --spacing-base: 1rem;
}

/* frontend-design skill guides implementation */
/* - Bold aesthetic choices */
/* - Distinctive typography and color palettes */
/* - High-impact animations and visual details */
/* - Context-aware, production-ready code */
```

When implementing UI:
1. **Load design-tokens skill** for the system
2. **Load frontend-design skill** for aesthetic execution
3. **Result**: Consistent system + distinctive design

## Best Practices

### Do ✅

- **Use semantic names**: `--color-primary` not `--color-blue-500`
- **Define once, use everywhere**: Single source of truth
- **Support dark mode**: Plan from the start
- **Use OKLCH colors**: Better than RGB/HSL
- **Tint neutrals with brand hue**: `oklch(0.95 0.01 brandHue)` not `oklch(0.95 0 0)`
- **Follow 8-point grid**: For spacing consistency
- **Create component tokens**: Card, button, input-specific values
- **Document your system**: Include usage examples
- **Reference frontend-design**: Let that skill guide aesthetics

### Don't ❌

- **Don't hardcode values**: Always use tokens
- **Don't use descriptive names**: Semantic intent over implementation
- **Don't skip dark mode**: Users expect it (2025)
- **Don't use pure grays**: Tint neutrals with brand hue (chroma 0.005-0.02)
- **Don't use generic fonts**: Avoid Inter/Roboto/Arial (per frontend-design)
- **Don't create too many tokens**: Start minimal, expand as needed
- **Don't ignore accessibility**: Ensure adequate contrast ratios
- **Don't forget mobile**: Test tokens at all breakpoints

## Philosophy

**"Design tokens are contracts between design and development."**

When design changes (new brand colors, updated spacing), you update tokens—not hundreds of scattered values across components.

**Systematic consistency enables creative expression.** The design token system provides guardrails; the frontend-design skill provides the artistry within those guardrails.

**Start with semantic meaning, not visual appearance.** `--color-primary` adapts to brand changes; `--color-blue-500` does not.

---

When agents design UI systems, they should:
- Use Tailwind 4 @theme directive (not tailwind.config.js)
- Define semantic color tokens (primary, secondary, accent, not blue-500)
- Use OKLCH color space for perceptual uniformity
- **Tint all neutrals with brand hue** (chroma 0.005-0.02, not pure gray)
- Follow 8-point spacing grid
- Create modular type scale (1.200 ratio recommended)
- Support dark mode from the start (same brand hue, inverted lightness)
- Avoid generic fonts (per frontend-design skill)
- Define component-specific tokens for consistency
- Document the design system with usage examples
- Reference frontend-design skill for aesthetic guidance
