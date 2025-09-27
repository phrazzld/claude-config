Are you sure we should use the --no-verify flag?

## Tenet Reminder: Automation & Explicitness
**Automation** - Pre-commit checks exist for a reason. They catch issues early and consistently. Bypassing them should be the exception, not the rule. **Explicitness** - If you must bypass checks, be explicit about why. Document the specific reason and create TODO items to address the underlying issues.

Sometimes there is a very good reason to bypass checks. In these cases you should always document exactly why, and you should always create at least one task -- if not multiple tasks -- in `@TODO.md` for fixing the issues you're facing and committing changes that don't use the --no-verify flag.

Is this one of those cases? Or should you fix the issues the pre-commit checks are flagging before making this commit?
