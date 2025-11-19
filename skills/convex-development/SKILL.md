---
name: convex-development
description: Apply Convex database best practices including cost mitigation, bandwidth optimization, embeddings/vector search patterns, security, query optimization, schema migrations, and architectural patterns. Use when building Convex backends, optimizing performance, handling embeddings, reviewing Convex code, or discussing cost-effective Convex architecture.
---

# Convex Development

Best practices for building robust, secure, performant, cost-effective Convex backends. Updated November 2025 with latest patterns for bandwidth optimization and embeddings management.

## Core Principle

**Deep modules via the `convex/model/` pattern.**

Most logic should be plain TypeScript functions; query/mutation/action wrappers should be thin.

```
convex/
  _generated/
  model/              # Core business logic (testable, reusable)
    users.ts
    teams.ts
  users.ts            # Public API (thin wrappers)
  teams.ts
  schema.ts
```

**Benefits**:
- Easier testing (pure functions)
- Better code reuse
- Simpler refactoring
- Clear separation of concerns
- Type-safe helpers callable from any function

**Example**:
```typescript
// convex/model/users.ts - Business logic
import { QueryCtx } from "../_generated/server";

export async function getCurrentUser(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) throw new Error("Unauthenticated");

  return await ctx.db
    .query("users")
    .withIndex("by_token", (q) => q.eq("tokenIdentifier", identity.tokenIdentifier))
    .unique();
}

// convex/users.ts - Public API (thin wrapper)
import { query } from "./_generated/server";
import * as Users from "./model/users";

export const getCurrentUser = query({
  args: {},
  handler: (ctx) => Users.getCurrentUser(ctx),
});
```

---

## 1. Cost Mitigation & Bandwidth Optimization

**Bandwidth is often the largest and most unpredictable cost.** Costs driven by function execution time, storage, and database bandwidth.

### Golden Rule: "Index What You Query"

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

### Never Fetch Unbounded Collections

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

### Separate Hot and Cold Data

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

### Batch Mutations

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

### Monitor Functions Log

Use the Functions Log in Convex Dashboard to identify slow queries. Add indexes for any query taking >50ms.

---

## 2. Embeddings & Vector Search

Vector search is a core Convex feature. How you store embeddings critically impacts performance and cost.

### Default Pattern: Co-location (Same Table)

For most applications, store embedding vector **in the same table** as source data. Simplest and most effective.

✅ **Best practice: Co-located embeddings**
```typescript
// convex/schema.ts
defineTable({
  text: v.string(),
  embedding: v.array(v.float64()), // OpenAI embeddings are 1536 dims
})
.vectorIndex("by_embedding", {
  vectorField: "embedding",
  dimensions: 1536,
  filterFields: [], // Add fields here to filter during vector search
});
```

### Advanced Pattern: Separate Embeddings Table

**Only use separate table when:**
- Multiple embeddings per document (e.g., different models or chunked text)
- Source document is extremely large (keep main table lean)
- Embeddings generated by decoupled process

This pattern requires "joins" (two `ctx.db.get()` calls) or denormalization, adding complexity.

❌ **Avoid unless necessary: Separate tables**
```typescript
// Main documents table
defineTable({
  title: v.string(),
  content: v.string(),
});

// Separate embeddings table
defineTable({
  documentId: v.id("documents"),
  embedding: v.array(v.float64()),
})
.index("by_document", ["documentId"])
.vectorIndex("by_embedding", {
  vectorField: "embedding",
  dimensions: 1536,
});
```

### Vector Search Must Use Actions

Vector searches **must** be performed inside `actions` using `ctx.vectorSearch`.

✅ **Best practice: Vector search in action**
```typescript
// convex/similarItems.ts
import { action } from "./_generated/server";
import { api, internal } from "./_generated/api";

export const findSimilar = action({
  args: { id: v.id("documents") },
  handler: async (ctx, args) => {
    const doc = await ctx.runQuery(api.documents.get, { id: args.id });
    if (!doc || !doc.embedding) {
      throw new Error("Document or embedding not found");
    }

    const results = await ctx.vectorSearch("documents", "by_embedding", {
      vector: doc.embedding,
      limit: 10,
    });
    return results;
  },
});
```

### Batch Embeddings API Calls

Fetch multiple embeddings at once to reduce overhead.

❌ **Anti-pattern: Sequential API calls**
```typescript
for (const doc of docs) {
  const embedding = await openai.embeddings.create({
    input: doc.text,
    model: "text-embedding-ada-002",
  });
  await ctx.db.patch(doc._id, { embedding: embedding.data[0].embedding });
}
```

✅ **Best practice: Batch embeddings**
```typescript
// Batch all texts together
const embeddings = await openai.embeddings.create({
  input: docs.map(d => d.text),
  model: "text-embedding-ada-002",
});

// Update all documents
for (let i = 0; i < docs.length; i++) {
  await ctx.db.patch(docs[i]._id, {
    embedding: embeddings.data[i].embedding
  });
}
```

### Model Consistency

Different embedding models produce incompatible arrays. **Commit to a single model** (e.g., `text-embedding-ada-002`) rather than experimenting across providers.

### When to Separate Embeddings (Critical Decision)

**Keep embeddings WITH source data when:**
- ✅ One embedding per document
- ✅ Source document is small-to-medium size (<10KB)
- ✅ Embeddings generated inline with document creation
- ✅ Embeddings are always needed with the document

**Separate embeddings ONLY when:**
- ⚠️ Multiple embeddings per document (chunks, different models)
- ⚠️ Source document is very large (>100KB)
- ⚠️ Embeddings generated asynchronously/decoupled
- ⚠️ **Bandwidth optimization**: Embeddings 1536 floats (~6KB each) — if frequently fetching documents WITHOUT needing embeddings, separation reduces bandwidth

---

## 3. Query & Performance Patterns

### Compound Indexes for Multi-Field Queries

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

### Indexes Define Sort Order

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

### Staged Index Builds

When adding an index to a very large table, backfill can be slow. Deploy index in "staged" state, wait for backfill in dashboard, then deploy "enabled" state to avoid blocking.

### Query Segmentation for Better Caching

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

### Use `.unique()` vs `.first()` Appropriately

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

### Minimize `ctx.runQuery/runMutation` Calls from Actions

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

### Index Design Best Practices

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

---

## 4. Security & Access Control

### Critical Rule: Trust `ctx.auth`, Never User Input

Authentication data from users is spoofable. Always use `ctx.auth.getUserIdentity()`.

❌ **Anti-pattern: Spoofable auth**
```typescript
export const deleteMessage = mutation({
  args: { messageId: v.id("messages"), userEmail: v.string() },
  handler: async (ctx, { messageId, userEmail }) => {
    const message = await ctx.db.get(messageId);
    if (message.authorEmail === userEmail) { // ❌ Email can be faked!
      await ctx.db.delete(messageId);
    }
  },
});
```

✅ **Best practice: Use `ctx.auth`**
```typescript
export const deleteMessage = mutation({
  args: { messageId: v.id("messages") },
  handler: async (ctx, { messageId }) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthenticated");

    const message = await ctx.db.get(messageId);
    if (!message) throw new Error("Message not found");
    if (message.authorTokenIdentifier !== identity.tokenIdentifier) {
      throw new Error("Unauthorized");
    }

    await ctx.db.delete(messageId);
  },
});
```

### Row-Level Security (RLS) Pattern

Most common pattern: users can only access their own data. Add `userId` field, create index.

✅ **Best practice: RLS with userId**
```typescript
// Schema
defineTable({
  userId: v.string(),
  content: v.string(),
}).index("by_user", ["userId"]);

// Query
export const getMyDocuments = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return [];

    return await ctx.db
      .query("documents")
      .withIndex("by_user", (q) => q.eq("userId", identity.subject))
      .collect();
  },
});
```

### Centralize Authorization with convex-helpers

Use `convex-helpers` package for reusable RLS/RBAC patterns.

✅ **Best practice: Custom functions for auth middleware**
```typescript
// convex/functions.ts
import { customMutation } from "convex-helpers/server/customFunctions";
import { mutation } from "./_generated/server";

// Authenticated mutation builder
export const userMutation = customMutation(mutation, {
  args: {},
  input: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthenticated");

    const user = await ctx.db
      .query("users")
      .withIndex("by_token", (q) => q.eq("tokenIdentifier", identity.tokenIdentifier))
      .unique();

    if (!user) throw new Error("User not found");

    return { ctx: { user }, args: {} };
  },
});

// Usage: ctx.user is now type-safe and guaranteed to exist
export const createNote = userMutation({
  args: { content: v.string() },
  handler: async (ctx, { content }) => {
    await ctx.db.insert("notes", {
      content,
      authorId: ctx.user._id, // ✅ Type-safe!
    });
  },
});
```

### Parametrized Custom Functions (RBAC)

```typescript
// convex/functions.ts
type Role = "admin" | "user" | "anonymous";

export const teamMutation = customMutation(mutation, {
  args: { teamId: v.id("teams") },
  input: async (ctx, args, opts: { role: Role }) => {
    const user = await getCurrentUser(ctx);
    await ensureUserHasRoleOnTeam(ctx, user, args.teamId, opts.role);
    return { ctx: { user, teamId: args.teamId }, args: {} };
  },
});

// Usage: role is enforced at definition time
export const suspendUser = teamMutation({
  role: "admin", // ✅ Type error if missing!
  args: { targetUserId: v.id("users") },
  handler: async (ctx, { targetUserId }) => {
    // Only admins can reach here
    await ctx.db.patch(membershipId, { status: "suspended" });
  },
});
```

### Argument Validators for All Public Functions

Public functions are exposed to the internet. Validate all arguments.

❌ **No validation - vulnerable**
```typescript
export const updateMessage = mutation({
  handler: async (ctx, { id, update }) => {
    await ctx.db.patch(id, update); // Can update ANY document, ANY field!
  },
});
```

✅ **Strict validation**
```typescript
import { v } from "convex/values";

export const updateMessage = mutation({
  args: {
    id: v.id("messages"),
    update: v.object({
      body: v.optional(v.string()),
      author: v.optional(v.string()),
    }),
  },
  handler: async (ctx, { id, update }) => {
    await ctx.db.patch(id, update);
  },
});
```

### Only Schedule and `ctx.run*` Internal Functions

Public functions are exposed to attackers. Use `internal.*` for scheduling and `ctx.run*` calls.

❌ **Scheduling public function**
```typescript
import { crons } from "./_generated/server";
import { api } from "./_generated/api";

crons.daily(
  "send reminder",
  { hourUTC: 17, minuteUTC: 30 },
  api.messages.sendMessage, // ❌ Public function - anyone can call!
  { author: "System", body: "Daily reminder" }
);
```

✅ **Schedule internal function**
```typescript
import { internal } from "./_generated/api";

export const sendMessage = mutation({
  args: { body: v.string() },
  handler: async (ctx, { body }) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");
    await sendMessageHelper(ctx, { body, author: identity.name ?? "Anonymous" });
  },
});

export const sendInternalMessage = internalMutation({
  args: { body: v.string(), author: v.string() },
  handler: async (ctx, { body, author }) => {
    await sendMessageHelper(ctx, { body, author });
  },
});

crons.daily(
  "send reminder",
  { hourUTC: 17, minuteUTC: 30 },
  internal.messages.sendInternalMessage, // ✅ Internal function
  { author: "System", body: "Daily reminder" }
);
```

---

## 5. Schema Design & Migrations

### Convex Auto-Migrates (No Manual Migrations)

Schema changes are immediate in dev, require push in prod. No SQL migration files needed.

### The "Expand and Contract" Pattern

**Use for any breaking schema change** (renaming, type changes, removing fields).

**Four Phases**: Expand → Migrate → Contract → Cleanup

**Example: Renaming `name` to `fullName`**

**Phase 1: Expand** — Add new field as optional, dual write
```typescript
// schema.ts - Step 1
defineTable({
  name: v.string(),
  fullName: v.optional(v.string()), // NEW - optional
});

// mutation.ts - Step 1
export const createUser = internalMutation({
  args: { name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("users", {
      name: args.name,
      fullName: args.name, // Write to both
    });
  },
});
```

**Phase 2: Migrate** — Backfill existing records
```typescript
// convex/migrations.ts
export const backfillFullNames = internalAction({
  handler: async (ctx) => {
    const users = await ctx.runQuery(internal.users.listAll);
    for (const user of users) {
      if (!user.fullName) {
        await ctx.runMutation(internal.users.patch, {
          userId: user._id,
          fullName: user.name,
        });
      }
    }
  },
});

// For large datasets, use Convex Migration Component
```

**Phase 3: Contract** — Switch reads to new field, stop writing to old field
```typescript
// Read from fullName only
export const getUser = query({
  handler: async (ctx, { userId }) => {
    const user = await ctx.db.get(userId);
    return { name: user.fullName }; // Read from new field
  },
});

// Stop dual-writing (remove name from inserts)
```

**Phase 4: Cleanup** — Remove old field from schema
```typescript
// schema.ts - Final
defineTable({
  fullName: v.string(), // Only new field remains
});

// May need migration to unset old field if Convex blocks removal
```

### Migration Best Practices

✅ **Safe patterns**:
- Add optional fields first
- Backfill via internal actions
- Test in dev/preview before prod
- Use `v.optional()` for backward compatibility
- Use Convex Migration Component for large datasets (>10k docs)

❌ **Dangerous patterns**:
- Removing fields before code updated
- Changing field types without migration
- Breaking changes without deprecation period
- Testing migrations directly in production
- No rollback strategy

### Staged Rollout for Large Tables

When backfilling large tables (>100k documents), use staged approach:

1. Deploy schema with optional field
2. Run backfill migration in background (may take hours)
3. Monitor completion in dashboard
4. Deploy code changes to read from new field
5. Remove old field after grace period

---

## 6. Architectural Patterns

### File Organization

```
convex/
  _generated/
  model/              # Business logic (reusable, testable)
    users.ts
    teams.ts
    messages.ts
  users.ts            # Public API (thin wrappers)
  teams.ts
  messages.ts
  schema.ts           # Database schema
  http.ts             # HTTP endpoints
  crons.ts            # Scheduled functions
  auth.ts             # Authentication config
```

### Transactional State Machines

Model entity status explicitly. Use mutations to perform atomic state transitions.

✅ **Best practice: State machine pattern**
```typescript
// Schema
defineTable({
  orderId: v.string(),
  status: v.union(
    v.literal("pending"),
    v.literal("processing"),
    v.literal("shipped"),
    v.literal("delivered"),
    v.literal("cancelled")
  ),
});

// Mutation with state validation
export const shipOrder = mutation({
  args: { orderId: v.id("orders") },
  handler: async (ctx, { orderId }) => {
    const order = await ctx.db.get(orderId);
    if (!order) throw new Error("Order not found");

    // Validate state transition
    if (order.status !== "processing") {
      throw new Error(`Cannot ship order in ${order.status} state`);
    }

    await ctx.db.patch(orderId, { status: "shipped" });
  },
});
```

### CQRS-like Separation

Use `queries` for real-time reactive reads. Use `httpAction` for write-heavy, non-reactive endpoints (webhooks).

✅ **Best practice: Separate read/write paths**
```typescript
// Query: Real-time reactive reads
export const getMessages = query({
  handler: async (ctx) => {
    return await ctx.db.query("messages").collect();
  },
});

// httpAction: Webhook (no reactivity needed)
export const receiveWebhook = httpAction(async (ctx, request) => {
  const payload = await request.json();
  await ctx.runMutation(internal.webhooks.processPayload, { payload });
  return new Response("OK", { status: 200 });
});
```

### Optimistic Updates with Server-Generated IDs

Generate temporary client-side ID for optimistic update, then patch with real server ID.

✅ **Best practice: Optimistic with ID reconciliation**
```typescript
// Client code (React)
const optimisticId = useOptimistic();

const handleCreate = async () => {
  // Optimistic update
  setMessages([...messages, { _id: optimisticId, text: "New message", pending: true }]);

  // Server call
  const realId = await createMessage({ text: "New message" });

  // Replace optimistic with real
  setMessages(messages.map(m => m._id === optimisticId ? { ...m, _id: realId, pending: false } : m));
};
```

### Function Type Selection

**When to use**:
- **Query**: Read-only, reactive, cached (UI updates automatically)
- **Mutation**: Write data, atomic transactions
- **Action**: External API calls, non-deterministic operations (time, random, fetch), vector search
- **Internal**: Scheduled functions, `ctx.run*` calls, administrative tasks

**Example**:
```typescript
// Query: Read data reactively
export const listMessages = query({...});

// Mutation: Write to database
export const createMessage = mutation({...});

// Action: Call external API or vector search
export const sendEmail = action({...});
export const searchSimilar = action({...});

// Internal: Scheduled or admin tasks
export const cleanupOldData = internalMutation({...});
```

### Transaction Boundaries

Mutations are atomic. All database operations succeed or all fail.

```typescript
export const transferCredits = mutation({
  handler: async (ctx, { fromUserId, toUserId, amount }) => {
    // Atomic: both updates succeed or both fail
    await ctx.db.patch(fromUserId, { credits: (user.credits - amount) });
    await ctx.db.patch(toUserId, { credits: (user.credits + amount) });
  },
});
```

### Naming Conventions

❌ **Avoid generic names**:
- `Manager`, `Util`, `Helper` → Vague, non-specific
- `Service`, `Handler`, `Processor` → Sometimes justified, often lazy

✅ **Use intention-revealing names**:
- `listMessages` not `getData`
- `createTeam` not `doStuff`
- `sendWelcomeEmail` not `helper`
- `getTeamBySlug` not `find`

---

## 7. Anti-Patterns Scanner

Quick checks when reviewing Convex code:

### Performance Anti-Patterns

❌ **Unbounded `.collect()` calls**
- Use pagination for large result sets
- Use `.take(n)` for bounded results

❌ **Using `.filter()` on database queries**
- Use `.withIndex()` for efficient filtering

❌ **Missing indexes for common queries**
- Create indexes for all query patterns
- Check index usage in dashboard

❌ **Query mixing update frequencies**
- Separate queries by update frequency for better caching

❌ **Not awaiting promises**
- Enable `no-floating-promises` ESLint rule
- Unwaited promises cause silent failures

### Modern Anti-Patterns (2025)

❌ **Ignoring Reactivity**
- Fetching data in `useEffect` with one-off action call instead of `useQuery`
- Forfeits Convex's greatest strength: real-time updates

❌ **Fat Client Logic**
- Putting authorization logic, complex calculations, or multi-step workflows on client
- **All business logic belongs in mutations and actions**

❌ **Storing Large Files/Blobs in Documents**
- Do not store user-uploaded images, videos, or large JSON blobs in documents
- Bloats documents, consumes massive bandwidth
- **Use Convex File Storage instead**

❌ **Prop-Drilling `db` or `ctx`**
- Never pass `db` or `ctx` objects from one function to another
- Use `ctx.runQuery` or `ctx.runMutation` instead
- Preserves dependency tracking and caching

❌ **Calling Convex functions from Convex functions**
- Extract to helper functions in `convex/model/`
- Direct function calls instead of `api.*` calls within Convex

### Security Anti-Patterns

❌ **User-provided data for auth**
- Always use `ctx.auth.getUserIdentity()`

❌ **No argument validators**
- All public functions need validators

❌ **Exposing internal functions publicly**
- Use `internal.*` for admin/scheduled functions

❌ **Hardcoded environment values**
- Use environment variables via dashboard

### Migration Anti-Patterns

❌ **Breaking schema changes without migration**
- Always additive changes first (optional fields)

❌ **No backfill strategy**
- Plan how to migrate existing data

❌ **Testing migrations directly in production**
- Use dev/preview environments

### Architecture Anti-Patterns

❌ **Poor naming (Manager/Util/Helper)**
- Use intention-revealing names

❌ **Business logic in query/mutation handlers**
- Extract to `convex/model/` helpers

❌ **Duplicate code across functions**
- Share logic via helper functions

---

## 8. Environment Management

### Deployment Flow: Dev → Preview → Prod

```
Local dev (convex dev)
  → Push to branch (preview deployment)
    → Merge to main (production deployment)
```

### Environment-Specific Patterns

**Local development**:
```bash
convex dev  # Hot reload, separate backend
```

**Preview deployments** (automatic per branch):
```bash
git push origin feature-branch
# Preview deployment auto-created
# Test migrations, features in isolation
```

**Production**:
```bash
git merge to main
# Auto-deploys to production
```

### Environment Variables

Use dashboard for configuration (not `.env` files in `convex/`).

✅ **Best practice**:
```typescript
export const sendEmail = action({
  handler: async (ctx, { to, subject, body }) => {
    const apiKey = process.env.SENDGRID_API_KEY; // ✅ From dashboard
    await sendEmail({ apiKey, to, subject, body });
  },
});
```

❌ **Anti-pattern**:
```typescript
export const sendEmail = action({
  handler: async (ctx, { to, subject, body }) => {
    const apiKey = "sk-..."; // ❌ Hardcoded!
    await sendEmail({ apiKey, to, subject, body });
  },
});
```

### Testing Migrations Across Environments

✅ **Best practice flow**:
```bash
# 1. Test locally
convex dev
# Apply migration, verify locally

# 2. Test in preview
git push origin feature-branch
# Preview deployment auto-created
# Verify migration works with preview data

# 3. Deploy to prod
git merge to main
# Auto-deploys to production
```

❌ **Anti-pattern**:
- Testing migrations directly in production
- No preview/staging environment
- Schema changes without backfill plan

---

## 9. Quick Reference

### Cost Optimization Checklist

- [ ] **Index what you query** - no full table scans
- [ ] **Paginate all unbounded queries**
- [ ] **Separate hot and cold data** - split frequently-updated fields
- [ ] **Batch mutations** - reduce network overhead
- [ ] **Monitor Functions Log** - identify slow queries
- [ ] **Consider embeddings placement** - separate table only when necessary

### Embeddings Decision Tree

```
Need vector search?
  → One embedding per doc + small source? → Co-locate (same table)
  → Multiple embeddings per doc? → Separate table
  → Very large source docs (>100KB)? → Separate table
  → Frequently fetch docs WITHOUT embeddings? → Separate table
  → Otherwise → Co-locate (default)
```

### New Function Checklist

- [ ] Argument validators defined (`v.object`, `v.id`, etc.)
- [ ] Access control implemented (`ctx.auth.getUserIdentity()`)
- [ ] Use internal functions for scheduling/`ctx.run*`
- [ ] Error handling with `ConvexError` for user-facing errors
- [ ] Proper function type (query/mutation/action/internal)
- [ ] Indexes exist for query patterns
- [ ] No unbounded `.collect()` calls

### Migration Checklist

- [ ] Changes are additive (new fields optional with `v.optional()`)
- [ ] "Expand and Contract" pattern planned
- [ ] Backfill strategy defined (internal action)
- [ ] Tested in dev environment first
- [ ] Tested in preview environment
- [ ] Rollback plan defined
- [ ] Breaking changes have deprecation period
- [ ] Use Convex Migration Component for large datasets

### Performance Review Checklist

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

### Security Review Checklist

- [ ] All public functions have argument validators
- [ ] Auth uses `ctx.auth` (never user-provided data)
- [ ] Internal functions used for scheduling/`ctx.run*`
- [ ] No sensitive data in client-visible errors
- [ ] Environment variables used (not hardcoded)
- [ ] Input sanitization for user-provided content
- [ ] ConvexError used for structured error responses
- [ ] Row-Level Security (RLS) or RBAC implemented

---

## Philosophy

### Cost First

**Bandwidth is often the largest cost.** Index aggressively, paginate everything, separate hot/cold data, batch operations. Monitor Functions Log religiously.

### Embeddings Strategy

**Default to co-location.** Only separate embeddings when you have clear reasons: multiple embeddings per doc, huge source docs, or frequent fetches without embeddings. Separation adds complexity — justify the trade-off.

### Security First

Never trust client input. Always validate. Always use `ctx.auth` for authentication. Centralize authorization logic.

### Deep Modules

Simple interfaces (thin query/mutation wrappers) hiding powerful implementations (`convex/model/` helpers).

### Performance by Design

Create indexes from day one. Use pagination by default. Segment queries by update frequency. Separate hot and cold data.

### Type Safety End-to-End

Convex provides type safety from database → functions → UI. Leverage it fully.

### Safe Migrations

Always use "Expand and Contract" pattern. Test in dev/preview. Have rollback strategy. Never break production.

### Environment Discipline

Separate deployments for dev/preview/prod. Configuration via dashboard, not code. Test migrations before deploying.

### Reactivity is Power

Use `useQuery` for real-time updates. Don't forfeit Convex's core strength with one-off `useEffect` calls.

### Simplicity Over Abstraction

Start with simple patterns. Add abstraction only when proven necessary. Helper functions over complex frameworks.

---

This skill represents battle-tested Convex patterns updated for November 2025. Apply these principles to build secure, performant, cost-effective, maintainable backends.
