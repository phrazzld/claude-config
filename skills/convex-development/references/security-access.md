# Security & Access Control

## Critical Rule: Trust `ctx.auth`, Never User Input

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

## Row-Level Security (RLS) Pattern

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

## Centralize Authorization with convex-helpers

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

## Parametrized Custom Functions (RBAC)

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

## Argument Validators for All Public Functions

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

## Only Schedule and `ctx.run*` Internal Functions

Public functions are exposed to attackers. Use `internal.*` for scheduling and `ctx.run*` calls.

❌ **Scheduling public function**
```typescript
crons.daily(
  "send reminder",
  { hourUTC: 17, minuteUTC: 30 },
  api.messages.sendMessage, // ❌ Public function - anyone can call!
  { author: "System", body: "Daily reminder" }
);
```

✅ **Schedule internal function**
```typescript
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

## Security Review Checklist

- [ ] All public functions have argument validators
- [ ] Auth uses `ctx.auth` (never user-provided data)
- [ ] Internal functions used for scheduling/`ctx.run*`
- [ ] No sensitive data in client-visible errors
- [ ] Environment variables used (not hardcoded)
- [ ] Input sanitization for user-provided content
- [ ] ConvexError used for structured error responses
- [ ] Row-Level Security (RLS) or RBAC implemented
