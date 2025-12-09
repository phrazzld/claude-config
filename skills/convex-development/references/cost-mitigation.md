# Cost Mitigation & Bandwidth Optimization

**Bandwidth is often the largest and most unpredictable cost.** Costs driven by function execution time, storage, and database bandwidth.

## Golden Rule: "Index What You Query"

Queries without `.withIndex()` perform full table scans — the single largest contributor to excess bandwidth usage.

❌ **Anti-pattern: Full table scan**
```typescript
// Scans ENTIRE table, massive bandwidth waste
const tomsMessages = await ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("author"), "Tom"))
  .collect();
```

✅ **Best practice: Indexed query**
```typescript
defineTable({
  author: v.string(),
}).index("by_author", ["author"]);

const tomsMessages = await ctx.db
  .query("messages")
  .withIndex("by_author", (q) => q.eq("author", "Tom"))
  .collect();
```

## Never Fetch Unbounded Collections

A query returning 1,000+ documents consumes significant bandwidth and causes UI jank. Always use `.paginate()`.

❌ **Anti-pattern: Unbounded collect**
```typescript
const allMovies = await ctx.db.query("movies").collect();
const spielbergMovies = allMovies.filter(m => m.director === "Steven Spielberg");
```

✅ **Best practice: Pagination with index**
```typescript
import { paginationOptsValidator } from "convex/server";

export const listMessages = query({
  args: {
    channelId: v.id("channels"),
    paginationOpts: paginationOptsValidator,
  },
  handler: async (ctx, { channelId, paginationOpts }) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_channel", (q) => q.eq("channelId", channelId))
      .order("desc")
      .paginate(paginationOpts);
  },
});

// Client usage
const { results, status, loadMore } = usePaginatedQuery(
  api.messages.listMessages,
  { channelId }
);
```

## Separate Hot and Cold Data

When a document has frequently-updated fields (e.g., view counter) mixed with static fields (e.g., blog post body), the **entire document** is re-sent to subscribed clients on every update. Split into separate tables.

❌ **Anti-pattern: Mixed update frequency**
```typescript
defineTable({
  title: v.string(),
  body: v.string(),
  viewCount: v.number(), // Updates frequently, causes entire doc to resend
});
```

✅ **Best practice: Separated by update frequency**
```typescript
// Posts table (rarely changes)
defineTable({
  title: v.string(),
  body: v.string(),
});

// Post stats table (frequently updated)
defineTable({
  postId: v.id("posts"),
  viewCount: v.number(),
  lastViewed: v.number(),
}).index("by_post", ["postId"]);
```

## Batch Mutations

Instead of many small mutations from the client, create a single mutation accepting an array. Reduces network overhead and function execution costs.

❌ **Anti-pattern: Loop of mutations**
```typescript
// Client code
for (const item of items) {
  await api.items.create(item);
}
```

✅ **Best practice: Batch mutation**
```typescript
export const batchCreateItems = mutation({
  args: { items: v.array(v.object({ name: v.string(), ... })) },
  handler: async (ctx, { items }) => {
    for (const item of items) {
      await ctx.db.insert("items", item);
    }
  },
});
```

## Monitor Functions Log

Use the Functions Log in Convex Dashboard to identify slow queries. Add indexes for any query taking >50ms.

## Cost Optimization Checklist

- [ ] **Index what you query** - no full table scans
- [ ] **Paginate all unbounded queries**
- [ ] **Separate hot and cold data** - split frequently-updated fields
- [ ] **Batch mutations** - reduce network overhead
- [ ] **Monitor Functions Log** - identify slow queries
- [ ] **Consider embeddings placement** - separate table only when necessary
