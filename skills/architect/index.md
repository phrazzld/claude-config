
## Data Flow Validation

Before finalizing architecture for UI features, verify:

1. **Optional fields actually populated** - If UI depends on `model.optionalField`, confirm the backend code path actually sets it
2. **Query returns expected shape** - Trace from UI → query → mutation → database to ensure data flows correctly  
3. **Fallback behavior is appropriate** - If optional data may be missing, ensure fallback UX is helpful (not "coming soon" indefinitely)

Red flag: UI code that accesses optional schema fields without verifying the write path populates them.
