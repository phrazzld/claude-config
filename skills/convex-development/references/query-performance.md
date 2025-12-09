# Query & Performance Patterns

## Compound Indexes for Multi-Field Queries

Order matters. Match the order of your `eq` filters for maximum efficiency.

✅ **Best practice: Ordered compound index**
```typescript
defineTable({
  status: v.string(),
  priority: v.string(),
  dueDate: v.number(),
})
  .index("by_status_and_priority", ["status", "priority"])
  .index("by_status_and_due", ["status", "dueDate"]);

// Query matches index order
const tasks = await ctx.db
  .query("tasks")
  .withIndex("by_status_and_priority", (q) =>
    q.eq("status", "active").eq("priority", "high")
  )
  .collect();
```

## Indexes Define Sort Order

An index also defines sort order. To sort by `dueDate`, you need an index on that field.

```typescript
defineTable({
  channelId: v.id("channels"),
  _creationTime: v.number(),
})
  .index("by_channel", ["channelId"])                    // Sorted by _creationTime (default)
  .index("by_channel_reverse", ["channelId", "_creationTime"]); // Explicit sort field

// Ordered query
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .order("desc")
  .take(50);
```

## Staged Index Builds

When adding an index to a very large table, backfill can be slow. Deploy index in "staged" state, wait for backfill in dashboard, then deploy "enabled" state to avoid blocking.

## Query Segmentation for Better Caching

Separate queries by update frequency to optimize reactivity.

❌ **Anti-pattern: One query touches all data**
```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, { userId }) => {
    const user = await ctx.db.get(userId);
    const preferences = await ctx.db.query("preferences")...collect();
    const notifications = await ctx.db.query("notifications")...collect();
    return { user, preferences, notifications }; // Entire result invalidates if ANY part changes
  },
});
```

✅ **Best practice: Separate queries**
```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  handler: (ctx, { userId }) => ctx.db.get(userId),
});

export const getUserPreferences = query({
  args: { userId: v.id("users") },
  handler: async (ctx, { userId }) => {
    return await ctx.db.query("preferences")
      .withIndex("by_userId", (q) => q.eq("userId", userId))
      .first();
  },
});

export const getUnreadNotifications = query({
  args: { userId: v.id("users") },
  handler: async (ctx, { userId }) => {
    return await ctx.db.query("notifications")
      .withIndex("by_userId_unread", (q) => q.eq("userId", userId).eq("unread", true))
      .collect();
  },
});
```

## Use `.unique()` vs `.first()` Appropriately

**`.unique()`**: Enforces exactly one result (throws if multiple)
**`.first()`**: Returns first result or null

```typescript
// ✅ Use .unique() when expecting exactly one
const user = await ctx.db
  .query("users")
  .withIndex("by_email", (q) => q.eq("email", email))
  .unique(); // Throws if multiple

// ✅ Use .first() when getting most recent
const latestMessage = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .order("desc")
  .first();
```

## Minimize `ctx.runQuery/runMutation` Calls from Actions

Each call is a separate transaction; risk of inconsistency between calls.

❌ **Anti-pattern: Multiple sequential transactions**
```typescript
export const processOrder = action({
  handler: async (ctx, { orderId }) => {
    const order = await ctx.runQuery(api.orders.get, { orderId });
    const user = await ctx.runQuery(api.users.get, { userId: order.userId });
    // ❌ Order might have changed between these calls!
    await ctx.runMutation(api.orders.update, { orderId, status: "processing" });
  },
});
```

✅ **Best practice: Single transaction**
```typescript
export const processOrder = action({
  handler: async (ctx, { orderId }) => {
    const { order, user } = await ctx.runQuery(
      internal.orders.getOrderWithUser,
      { orderId }
    );
    await ctx.runMutation(internal.orders.update, { orderId, status: "processing" });
  },
});

export const getOrderWithUser = internalQuery({
  handler: async (ctx, { orderId }) => {
    const order = await ctx.db.get(orderId);
    if (!order) throw new Error("Order not found");
    const user = await ctx.db.get(order.userId);
    return { order, user };
  },
});
```

## Index Design Best Practices

**Create indexes for all query patterns**:
```typescript
defineTable({
  channelId: v.id("channels"),
  userId: v.id("users"),
  content: v.string(),
  _creationTime: v.number(),
})
  .index("by_channel", ["channelId"])                          // For: list all messages in channel
  .index("by_user", ["userId"])                                // For: list user's messages
  .index("by_channel_and_user", ["channelId", "userId"]);      // For: user's messages in channel
```

**Avoid redundant indexes**: `by_foo` and `by_foo_and_bar` are usually redundant (keep compound index).

**Name indexes clearly**: `by_userId_createdAt` not `idx1`.

## Performance Review Checklist

- [ ] Indexes exist for all query patterns
- [ ] Compound indexes match filter order
- [ ] No unbounded `.collect()` calls
- [ ] Pagination used for large result sets
- [ ] Query segmentation for cache optimization
- [ ] Hot/cold data separated
- [ ] Minimal `ctx.runQuery/runMutation` from actions
- [ ] Use `.withIndex()` not `.filter()` on queries
- [ ] Proper `.unique()` vs `.first()` usage
- [ ] Embeddings placement optimized for usage pattern
