# Commitlint Configuration

Enforce conventional commit format.

## commitlint.config.js

```javascript
/**
 * Commitlint configuration
 *
 * Enforces conventional commits format:
 * type(scope): subject
 *
 * Examples:
 *   feat: add dark mode toggle
 *   fix(auth): resolve token refresh issue
 *   docs: update API documentation
 */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Allowed commit types
    'type-enum': [
      2, // Error level
      'always',
      [
        'feat',     // New feature (triggers MINOR release)
        'fix',      // Bug fix (triggers PATCH release)
        'docs',     // Documentation only
        'style',    // Formatting, white-space, etc.
        'refactor', // Code restructuring without behavior change
        'perf',     // Performance improvement (triggers PATCH)
        'test',     // Adding or updating tests
        'build',    // Build system or dependencies
        'ci',       // CI/CD configuration
        'chore',    // Maintenance tasks
        'revert',   // Reverting previous commit
      ],
    ],

    // Type must be lowercase
    'type-case': [2, 'always', 'lower-case'],

    // Type is required
    'type-empty': [2, 'never'],

    // Scope is optional but must be lowercase if provided
    'scope-case': [2, 'always', 'lower-case'],

    // Subject must be lowercase
    'subject-case': [2, 'always', 'lower-case'],

    // Subject is required
    'subject-empty': [2, 'never'],

    // No period at end of subject
    'subject-full-stop': [2, 'never', '.'],

    // Header (type + scope + subject) max 100 chars
    'header-max-length': [2, 'always', 100],

    // Body lines max 100 chars
    'body-max-line-length': [2, 'always', 100],

    // Footer lines max 100 chars
    'footer-max-line-length': [2, 'always', 100],
  },
};
```

## Installation

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

## Lefthook Integration

Add to `lefthook.yml`:

```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

Then install hooks:

```bash
pnpm lefthook install
```

## Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Examples

**Simple feature:**
```
feat: add user avatar upload
```

**Feature with scope:**
```
feat(dashboard): add usage analytics chart
```

**Bug fix with body:**
```
fix(auth): resolve session timeout issue

Users were being logged out after 5 minutes of inactivity
due to incorrect token refresh timing.
```

**Breaking change:**
```
feat(api): redesign authentication endpoints

BREAKING CHANGE: All /auth/* endpoints now require
API version header. See migration guide.
```

## Testing

```bash
# Test a commit message
echo "feat: add new feature" | pnpm commitlint

# Test the last commit
pnpm commitlint --from HEAD~1

# Verbose output
pnpm commitlint --edit --verbose
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `type-empty` | No type prefix | Add `feat:`, `fix:`, etc. |
| `type-enum` | Invalid type | Use allowed type |
| `subject-empty` | No subject | Add description after colon |
| `subject-case` | Wrong case | Use lowercase |
| `header-max-length` | Too long | Shorten subject |

## Tips

1. **Keep subjects short** — Save details for the body
2. **Use imperative mood** — "add feature" not "added feature"
3. **Reference issues** — Include issue numbers in body/footer
4. **Breaking changes** — Always use `BREAKING CHANGE:` footer
