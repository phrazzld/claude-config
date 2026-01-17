---
name: algorithmic-art
description: "Generative art creation with p5.js. Invoke for: algorithmic art, computational aesthetics, seeded randomness, particle systems, flow fields, noise functions, interactive visualizations, emergent behavior, procedural generation."
---

# Algorithmic Art Creation Guide

> Algorithmic expression. Emergent behavior. Computational beauty. Seeded variation.

Create generative art using p5.js with philosophical grounding and computational expertise.

## The Process

Two stages:

1. **Algorithmic Philosophy** — A markdown document articulating your computational aesthetics. What patterns emerge? What forces govern? What beauty lives in the system?

2. **Interactive p5.js Code** — A self-contained HTML artifact expressing that philosophy through code.

## Philosophical Framework

Before writing code, write your philosophy. 4-6 substantial paragraphs that:

- Describe the computational essence of your vision
- Articulate what "beauty" means in this system
- Define the forces, rules, and emergent behaviors
- Guide implementation without over-constraining it

The philosophy manifests through:
- Noise functions and flow fields
- Particle dynamics and swarm behavior
- Field interactions and force systems
- Temporal evolution and accumulation

Each piece should reflect **deep computational expertise** — not random noise dressed up, but a meticulously crafted algorithm expressing a coherent aesthetic vision.

## Technical Implementation

### Critical Requirements

1. **Seeded Randomness** — Always use `randomSeed()` and `noiseSeed()` for reproducibility. Same seed = same output.

2. **Self-Contained Artifacts** — Single HTML file with everything inline (except p5.js CDN).

3. **Build from Template** — Start from `templates/viewer.html`. Don't reinvent the UI.

4. **Anthropic Branding** — Poppins/Lora fonts, light theme, specific color palette.

### Template Structure

**Fixed Elements** (preserve unchanged):
- Header and sidebar layout
- Seed navigation (display, prev/next, random, jump)
- Action buttons (regenerate, reset, download)
- Overall CSS structure

**Variable Elements** (customize per artwork):
- Complete p5.js algorithm in `<script>`
- Parameter definitions matching your system
- UI controls for your parameters
- Color sections (include only if needed)

### Parameter Design

Parameters should emerge from the question: **"What qualities of this system can be adjusted?"**

Not: pick from preset patterns
But: what knobs reveal different facets of this algorithm?

Examples:
- Particle count, speed, lifetime
- Noise scale, octaves, persistence
- Force strength, falloff, interaction radius
- Color palette, opacity, blend mode

Each parameter should meaningfully change the output while preserving the system's essential character.

## Templates

### `templates/viewer.html`
The starting point for every artwork. Contains:
- Complete UI structure with Anthropic styling
- Seed management system
- Placeholder algorithm ready to replace
- Parameter controls to customize

### `templates/generator_template.js`
Best practices for p5.js generative art:
- Parameter organization
- Seeded randomness patterns
- Performance strategies
- Utility functions

## Workflow

1. **Conceive** — What computational system interests you?
2. **Philosophize** — Write the algorithmic philosophy document
3. **Template** — Copy `viewer.html` as starting point
4. **Implement** — Replace placeholder with your algorithm
5. **Parameterize** — Define meaningful controls
6. **Iterate** — Test across seeds, refine the system

## The Goal

Beauty lives in algorithmic process. Each seed variation reveals different facets of the underlying system. The art isn't a single image — it's the infinite possibility space defined by your algorithm.

A successful piece:
- Produces compelling output across many seeds
- Has parameters that meaningfully transform the output
- Reflects a coherent aesthetic philosophy
- Demonstrates computational craft and expertise
