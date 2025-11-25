# PR Cleanup Plan - GitHub Accounts

## Investigation Summary

### phrazzld Account
- **Total PRs:** 294
- **Dependabot:** 278 (94.6%)
- **Manual:** 13 (4.4%)
- **GitHub Actions:** 3 (1.0%)
- **Critical Finding:** 180 PRs (61%) are over 2 years old
- **Archived Repos:** 81 repos with ~200+ PRs (can close immediately)
- **Active Repos:** 29 repos with ~50-60 PRs (need review)

### misty-step Account
- **Total PRs:** 116 across 10 repositories
- **Dependabot:** 103 (89%)
- **Manual:** 13 (11%)
- **Hotspot:** brainrot repo (60 PRs - 58 dependabot, 2 manual)
- **Recent Activity:** chrondle (15 PRs with Jules AI work), gitpulse (5 fresh PRs)

### Combined Totals
- **410 total PRs** across both accounts
- **381 dependabot PRs** (93%)
- **26 manual PRs** requiring code review
- **Potential 85-90% reduction** through systematic cleanup

## Recommended Approach

### Phase 1: Bulk Closures (phrazzld - Immediate Win)
**Target:** ~200 PRs in archived repositories
**Time:** 1-2 hours using bulk operations
**Strategy:**
- Close all PRs in 81 archived repos (kitchen-table-magic, mcginnis, brainstorm-press-client, shop, mug, etc.)
- These repos are no longer maintained - all PRs obsolete
- Use `gh pr close` with scripting for efficiency

### Phase 2: Ancient Dependabot Cleanup (Both Accounts)
**Target:** ~80 PRs (2+ years old in stale repos)
**Time:** 1-2 hours
**Strategy:**
- Close very old dependabot PRs in repos without recent activity
- Examples: BlueWallet, directory.btcpayserver.org PRs from 2023
- These require major version jumps anyway - better to close than merge

### Phase 3: Quick Wins - GitHub Actions (misty-step Priority)
**Target:** 13 PRs (actions/checkout, actions/setup-node, etc.)
**Time:** 30 minutes
**Strategy:**
- Auto-merge all GitHub Actions version bumps
- Zero risk - no code changes, just workflow updates
- Repos: chrondle, scry, volume, gitpulse

### Phase 4: Simple Dependency Updates (Both Accounts)
**Target:** ~60 PRs (single-file, minor/patch versions)
**Time:** 2-3 hours
**Strategy:**
- Focus on PRs with 1 file, <100 changes, passing CI
- Examples:
  - gitpulse: All 5 PRs (Sentry, zod, convex updates)
  - misty-step repo: 2 PRs (Sentry, Next.js)
  - brainrot: Individual package updates
- Review, test if needed, merge

### Phase 5: Grouped Updates (Medium Complexity)
**Target:** ~15 PRs (multi-package grouped updates)
**Time:** 3-4 hours
**Strategy:**
- PRs that update multiple dependencies at once
- Examples:
  - brainrot #292: 31 dependency updates
  - chrondle #52: 188 minor & patch updates
  - volume #42: 26 dev dependencies
- Require more thorough testing but still low risk

### Phase 6: Major Version Updates (Higher Risk)
**Target:** ~40 PRs (breaking changes likely)
**Time:** 6-8 hours
**Strategy:**
- Updates crossing major version boundaries (openai 5→6, Next.js 15→16, Tailwind 3→4)
- Requires code review, testing, potential code changes
- Prioritize by:
  1. Testing tools (safe to update)
  2. Framework updates (test thoroughly)
  3. Build tools (check for config changes)
  4. API clients (verify breaking changes)

### Phase 7: Manual PR Review
**Target:** 26 manual PRs (13 per account)
**Time:** Variable (10+ hours)
**Strategy:**
- Code review for feature work, refactors, infrastructure changes
- **phrazzld priorities:**
  - timeismoney #129: TypeScript migration (recent)
  - gitpulse-legacy #119: Large refactor (draft)
  - superwire #9: AI news platform revival
- **misty-step priorities:**
  - chrondle #58, #57, #56: Recent Jules AI work
  - sploot #18: Freemium billing (11k additions)
  - brainrot #200: Genesis translation (293k additions - MASSIVE)

### Phase 8: Prevent Future Deluge
**Target:** Configure dependabot grouping
**Time:** 30 minutes
**Strategy:**
- Update `.github/dependabot.yml` in active repos
- Group updates by type (dependencies, dev-dependencies, actions)
- Switch to weekly grouped updates instead of individual PRs
- Reduce future PR volume by 80-90%

## Execution Strategy (Parallel Approach)

Based on user preferences:
- ✅ Bulk-close all archived repo PRs
- ✅ Auto-merge minor/patch updates when CI passes
- ✅ Configure dependabot grouping to prevent future deluge
- ✅ Work both accounts in parallel for maximum efficiency

### Session 1: Massive Bulk Operations (2-3 hours)
**Target: 280+ PRs → ~130 PRs**

**Parallel Track A (phrazzld):**
1. Bulk close all PRs in 81 archived repos (~200 PRs)
   - Script using `gh pr list` + `gh pr close` for each archived repo
   - Add closing comment: "Closing - repository archived"
2. Close ancient (2+ year) dependabot PRs in stale repos (~80 PRs)

**Parallel Track B (misty-step):**
1. Auto-merge all GitHub Actions PRs with passing CI (~13 PRs)
   - chrondle, scry, volume, gitpulse
   - Use `gh pr merge --auto --squash`
2. Auto-merge gitpulse simple updates with passing CI (~5 PRs)

### Session 2: Automated Dependency Merges (2-3 hours)
**Target: 130 PRs → ~55 PRs**

**Criteria for Auto-merge:**
- Single file changes
- Minor/patch version updates only
- CI status: passing
- No major version bumps
- Use `gh pr checks` to verify CI status

**Parallel Track A (phrazzld - ~30 PRs):**
- Active repos: vanity, scry-splash, hyperbolic-time-chamber, etc.
- Individual package updates (js-yaml, glob, vite, crypto)

**Parallel Track B (misty-step - ~45 PRs):**
- brainrot: Single-package updates (glob, js-yaml, @types/node, etc.)
- scry: Sentry, minor/patch group
- chrondle: Simple Sentry update
- volume: Sentry update
- sploot: Sentry update
- misty-step repo: Sentry, Next.js updates

### Session 3: Grouped Updates Review (3-4 hours)
**Target: 55 PRs → ~40 PRs**

**Manual review required but still low risk:**
- brainrot #292: 31 dependencies (1929 additions)
- brainrot #266: 29 minor/patch (1961 additions)
- chrondle #52: 188 updates (1892 additions)
- volume #42: 26 dev deps (1711 additions)

**Process:**
1. Review changelog/diff for breaking changes
2. Check CI status
3. Local test if changes affect critical paths
4. Merge with squash

### Session 4: Major Version Updates (6-8 hours)
**Target: 40 PRs → ~26 PRs**

**High-impact breaking changes - prioritize by safety:**

**Round 1: Testing Tools (safest)**
- jsdom, happy-dom, playwright updates
- Low risk - only affects test environment

**Round 2: Build Tools**
- Tailwind 3→4 (multiple PRs in brainrot)
- esbuild, prettier-plugin updates
- Check for config migration needs

**Round 3: Framework Updates**
- Next.js 15→16 (brainrot #281)
- eslint-config-next updates
- Test thoroughly - affects entire app

**Round 4: Libraries**
- openai 5→6 (API changes likely)
- inquirer 12→13
- glob 11→12
- Research breaking changes first

### Session 5: Manual PR Review (Variable - 10+ hours)
**Target: 26 manual PRs**

**High Priority (Review First):**
- chrondle #58: Health endpoint (recent, 1 day old)
- sploot #21, #20: Health checks (recent)
- chrondle #56: Event truncation fix (recent)

**Medium Priority (Active Development):**
- timeismoney #129: TypeScript migration
- chrondle #57: Unified share (9k additions)
- chrondle #41: Wager system design

**Large/Complex (Schedule Dedicated Time):**
- sploot #18: Freemium billing (11k additions)
- brainrot #200: Genesis translation (293k additions)
- gitpulse-legacy #119: Refactor (2.6k deletions)
- chrondle #30: UI/UX overhaul (3.6k additions)

**Older/Stale (Consider Closing):**
- PRs >60 days old without activity
- May need rebasing or re-implementation

### Session 6: Prevent Future Deluge (30-60 minutes)
**Configure dependabot grouping in active repos:**

**Repos to configure:**
- misty-step: brainrot, chrondle, scry, gitpulse, sploot, volume, misty-step
- phrazzld: vanity, scry-splash, hyperbolic-time-chamber, timeismoney, plus any other active repos

**Dependabot config template:**
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    groups:
      production-dependencies:
        patterns:
          - "*"
        exclude-patterns:
          - "@types/*"
      development-dependencies:
        dependency-type: "development"
        patterns:
          - "*"
      github-actions:
        patterns:
          - "actions/*"
          - "github/*"
```

## Expected Timeline

**Week 1 (Sessions 1-2):**
- Bulk closures + auto-merges
- **410 PRs → ~55 PRs (87% reduction)**

**Week 2 (Sessions 3-4):**
- Grouped updates + major versions
- **55 PRs → ~26 PRs (additional 29 PRs)**

**Week 3+ (Sessions 5-6):**
- Manual reviews by priority
- Configure dependabot grouping
- **26 PRs → 0-5 PRs (only active work)**

## Tools & Scripts

**Bulk Operations:**
```bash
# List PRs in archived repos
gh repo list phrazzld --archived --limit 100 --json name | \
  jq -r '.[].name' | \
  xargs -I {} gh pr list --repo phrazzld/{} --state open

# Close PRs with comment
gh pr close <number> --repo <repo> --comment "Closing - repository archived"
```

**Auto-merge with CI check:**
```bash
# Check CI status first
gh pr checks <number> --repo <repo>

# Auto-merge if passing
gh pr merge <number> --repo <repo> --auto --squash
```

**Dependabot config:**
- Create/update `.github/dependabot.yml` in each active repo
- Use template above, adjust for repo needs

## Success Metrics

- **Start:** 410 total PRs
- **After Week 1:** ~55 PRs (87% reduction)
- **After Week 2:** ~26 PRs (93% reduction)
- **Final:** 0-5 PRs (98%+ reduction)
- **Ongoing:** 5-10 PRs/week (vs 50+ currently)
