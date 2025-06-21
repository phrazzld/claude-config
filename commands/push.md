# PUSH

## 1. Final Checks
- Run linter. Fix all issues.
- Run build. Resolve all errors.
- Run full test suite. Address all failures.
- *(Proceed only if all pass)*

## 2. Push
- `git fetch origin` (or relevant remote).
- Verify local branch not behind remote. **Stop** if behind (manual sync needed).
- `git push origin HEAD` (or relevant branch).
- Report success or specific push errors. **Stop**.

