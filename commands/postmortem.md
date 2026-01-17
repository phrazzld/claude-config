---
description: Create blameless postmortem for a recent bug
argument-hint: [commit or branch]
---

Create a blameless postmortem for the given commit (or most recent fix commit if not specified): **$ARGUMENTS**

Include:
- What broke, who was affected
- Timeline: introduced → discovered → fixed
- 5 Whys root cause analysis
- Mitigation: tests to add, monitoring to improve

Keep it blameless. Focus on systems, not people.

Use git history to understand what happened:
- `git show <commit>` to see the fix
- `git log -p <file>` or `git blame` to find when the bug was introduced
- Look for linked issues in commit messages
