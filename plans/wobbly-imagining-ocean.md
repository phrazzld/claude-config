# Remove E2E Billing Tests from GitHub Workflow

## Problem
The e2e billing workflow (`.github/workflows/e2e-billing.yml`) exists in the `feat/freemium-pricing` branch and is running on all pull requests, even though billing functionality hasn't been implemented yet.

## Discovery
- Workflow file: `.github/workflows/e2e-billing.yml`
- Location: `feat/freemium-pricing` branch (commit c8db6eb)
- Not present in `master` branch
- Configured to trigger on all PRs via `on: pull_request:`
- Causes workflow runs across all pull requests

## Solution
Delete `.github/workflows/e2e-billing.yml` from the `feat/freemium-pricing` branch.

### Approach Options

**Option A: Delete on Current Branch (feature-health-check)**
- Won't solve the problem since the file doesn't exist here
- The workflow is triggered from other branches

**Option B: Delete from feat/freemium-pricing Branch** ✓ RECOMMENDED
- Switch to `feat/freemium-pricing` branch
- Delete `.github/workflows/e2e-billing.yml`
- Commit with message: "chore: remove e2e billing workflow until billing implementation"
- Push to origin

**Option C: Delete via Direct Branch Manipulation**
- Checkout feat/freemium-pricing branch
- Remove the file
- Force push if needed

## Implementation Steps (Option B)

1. Stash or commit any current changes on feature-health-check
2. Switch to feat/freemium-pricing: `git checkout feat/freemium-pricing`
3. Pull latest: `git pull origin feat/freemium-pricing`
4. Delete workflow: `rm .github/workflows/e2e-billing.yml`
5. Commit: `git commit -m "chore: remove e2e billing workflow until billing implementation"`
6. Push: `git push origin feat/freemium-pricing`
7. Return to original branch: `git checkout feature-health-check`

## Files to Modify
- `.github/workflows/e2e-billing.yml` (delete from feat/freemium-pricing branch)

## Verification
After deletion and push:
- Check GitHub Actions on any open PR
- Verify e2e-billing workflow no longer appears in workflow runs
- Confirm only expected workflows (test, claude-code-review, etc.) run

## Note for Later
When billing is actually implemented:
- Restore the workflow from git history: `git show c8db6eb:.github/workflows/e2e-billing.yml`
- Update paths in workflow trigger if needed
- Ensure all secrets are configured in GitHub repository settings
