# Postmortem: [Brief Title]

**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Duration:** [Time from detection to resolution]
**Author:** [Names]

## Incident Summary

[2-3 sentences: What broke, who was affected, what was the impact]

- **Sentry Issue:** PROJ-XXX
- **Users Affected:** N
- **Events:** N

## Timeline

| Time | Event |
|------|-------|
| | Incident introduced |
| | Incident detected |
| | Investigation started |
| | Root cause identified |
| | Fix deployed |
| | Incident resolved |

## Root Cause

[Clear technical explanation of what went wrong]

## 5 Whys Analysis

1. **Why did [symptom] happen?** → Because [immediate cause]
2. **Why was [immediate cause] possible?** → Because [deeper cause]
3. **Why wasn't [deeper cause] prevented?** → Because [process gap]
4. **Why did [process gap] exist?** → Because [systemic issue]
5. **Why wasn't [systemic issue] addressed?** → Because [root cause]

## Contributing Factors

- [ ] Time pressure / rushed deployment
- [ ] Missing or inadequate tests
- [ ] Unclear requirements or documentation
- [ ] Complex code / technical debt
- [ ] Missing code review
- [ ] Insufficient monitoring
- [ ] Configuration management issues
- [ ] Other: [describe]

## Fixes Applied

| Fix | Commit | Lines Changed | Necessary? |
|-----|--------|---------------|------------|
| [Description] | `abc123` | +X/-Y | Yes/No |

## Mitigation Plan

### Preventive Measures

| Action | Owner | Status |
|--------|-------|--------|
| [Action item] | [Name] | Pending/In Progress/Done |

### Detection Improvements

| Action | Owner | Status |
|--------|-------|--------|
| [Action item] | [Name] | Pending/In Progress/Done |

### Process Changes

| Action | Owner | Status |
|--------|-------|--------|
| [Action item] | [Name] | Pending/In Progress/Done |

## Lessons Learned

### 1. [Key Lesson Title]

[Explanation and how to apply it going forward]

### 2. [Key Lesson Title]

[Explanation and how to apply it going forward]

## Related Documents

- [Sentry Issue](https://sentry.io/...)
- [Fix PR](https://github.com/...)
- [Link to relevant ADRs, docs, or issues]

## Appendix

```bash
# Commands used during investigation
# ...
```
