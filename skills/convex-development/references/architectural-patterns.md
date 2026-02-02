# Architectural Patterns

## Dynamic Validators from Constants

When deriving `v.union` validators from a constant array, TypeScript loses literal type inference. Use this pattern:

```typescript
import { v, Validator } from "convex/values";

// Define constants with literal types (single source of truth)
export const GOAL_TYPES = [
  "build_muscle",
  "lose_weight",
  "maintain_fitness",
  "get_stronger",
] as const;

export type GoalType = (typeof GOAL_TYPES)[number];

// Derive validator with type assertion to preserve inference
const goalValidator = v.union(
  ...(GOAL_TYPES.map((g) => v.literal(g)) as unknown as [
    Validator<GoalType>,
    ...Validator<GoalType>[],
  ])
) as unknown as Validator<GoalType>;

// Use in schema or mutation args
export default defineSchema({
  users: defineTable({
    goals: v.optional(v.array(goalValidator)),
  }),
});
```

**Why the double `as unknown as`:** Convex's `v.union` with spread loses the literal union inference. The intermediate `unknown` cast is needed because TypeScript's `VUnion` type doesn't directly overlap with `Validator`.

## File Organization

```
convex/
  _generated/           # MUST commit to git!
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

## Deep Modules via `convex/model/` Pattern

Most logic should be plain TypeScript functions; query/mutation/action wrappers should be thin.

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

## Transactional State Machines

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

## CQRS-like Separation

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

## Function Type Selection

**When to use**:
- **Query**: Read-only, reactive, cached (UI updates automatically)
- **Mutation**: Write data, atomic transactions
- **Action**: External API calls, non-deterministic operations (time, random, fetch), vector search
- **Internal**: Scheduled functions, `ctx.run*` calls, administrative tasks

## Transaction Boundaries

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

## Naming Conventions

❌ **Avoid generic names**:
- `Manager`, `Util`, `Helper` → Vague, non-specific
- `Service`, `Handler`, `Processor` → Sometimes justified, often lazy

✅ **Use intention-revealing names**:
- `listMessages` not `getData`
- `createTeam` not `doStuff`
- `sendWelcomeEmail` not `helper`
- `getTeamBySlug` not `find`

## Version Control Generated Files

**ALWAYS commit `convex/_generated/` to git.** This is official Convex recommendation.

**Generated files include:**
- `api.js` - JavaScript API exports
- `api.d.ts` - TypeScript API type definitions
- `dataModel.d.ts` - Database schema types
- `server.js` - Server runtime code
- `server.d.ts` - Server type definitions

**Critical benefits:**
1. Frontend type-checking without backend server running
2. CI/CD compatibility - builds work immediately
3. Team productivity - clone repo, types work
4. Type safety chain - schema → types → frontend

**What to do:**
```bash
# ✅ CORRECT - Commit generated files
git add convex/_generated/
git commit -m "chore: update generated Convex types"
```

**What NOT to do:**
```bash
# ❌ WRONG - Never add generated files to .gitignore
echo "convex/_generated/" >> .gitignore
```
