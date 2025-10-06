Are you sure we should use the --no-verify flag?

# VERIFY

**Automation exists for a reason**. Pre-commit checks catch issues early and consistently. Bypassing them should be the exception, not the rule.

**If you must bypass checks, be explicit about why**. Document the specific reason and create TODO items to address the underlying issues you're working around.

Sometimes there's a very good reason to bypass checks. In these cases:
- Always document exactly why
- Always create at least one task in `@TODO.md` for fixing the issues
- Plan to commit changes that don't use --no-verify

Is this one of those cases? Or should you fix the issues the pre-commit checks are flagging before making this commit?
