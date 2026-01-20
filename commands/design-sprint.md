---
description: Full design cycle: audit → catalog → pick → theme → build
argument-hint: "[route-or-url]"
---

# DESIGN-SPRINT

> Explore before you implement.

Full UI/UX design cycle from audit to implementation.

## Argument

- `route-or-url` — Optional. What to design. If omitted, asks user.

## Workflow

### 1. Audit Current State

```
/design-audit
```

Understand what exists:
- Token inventory
- Consistency issues
- Design debt
- RAMS accessibility score

### 2. Generate Options

```
/design-catalog $1
```

Create 5-8 visual proposals:
- Research trends (Gemini)
- Build working previews
- Validate each against ui-skills + RAMS
- Present catalog to user

### 3. User Selection

Wait for user to browse catalog and select direction.

If user wants hybrids, generate them and re-validate.

### 4. Implement Theme

```
/design-theme "[selected direction]"
```

Build the design system:
- Define tokens in CSS `@theme`
- Update components
- Validate accessibility

### 5. Build

```
/build
```

Implement the selected design.

### 6. Clean Up

```bash
# Remove catalog if user approves
rm -rf .design-catalog
pkill -f "python -m http.server 8888"
```

## Philosophy

Design is different from other development:
- **Visual exploration matters** — Show options before committing
- **Trends change** — Research prevents "AI slop"
- **Iteration is expected** — Multiple rounds are normal

## Output

Design system implemented. Report: audit findings, proposals generated, selection made, tokens defined, components updated.
