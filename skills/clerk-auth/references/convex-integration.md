# Clerk + Convex Integration

## Setup Flow

1. Create Clerk application
2. Create JWT template named `convex`
3. Configure `convex/auth.config.ts`
4. Set environment variables
5. Use `ctx.auth.getUserIdentity()` in backend

## JWT Template Configuration

In Clerk Dashboard → JWT Templates → Create new:

**Name**: `convex` (case-sensitive!)

**Claims**:
```json
{
  "sub": "{{user.id}}",
  "iss": "https://clerk.your-domain.com",
  "email": "{{user.primary_email_address}}",
  "name": "{{user.full_name}}",
  "picture": "{{user.image_url}}"
}
```

## Environment Variables

```bash
# Convex (.env.local and npx convex env set)
CLERK_JWT_ISSUER_DOMAIN=https://clerk.your-domain.com

# Verify with:
npx convex env list --prod | grep CLERK
```

## Backend Patterns

### Get Current User

```typescript
export const getCurrentUser = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) return null

    // Find user in our database by Clerk ID
    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .unique()
  },
})
```

### Protected Mutation

```typescript
export const createPost = mutation({
  args: { content: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) {
      throw new Error("Unauthenticated")
    }

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .unique()

    if (!user) {
      throw new Error("User not found")
    }

    return await ctx.db.insert("posts", {
      authorId: user._id,
      content: args.content,
      createdAt: Date.now(),
    })
  },
})
```

### User Schema

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server"
import { v } from "convex/values"

export default defineSchema({
  users: defineTable({
    clerkId: v.string(),
    email: v.string(),
    name: v.optional(v.string()),
    imageUrl: v.optional(v.string()),
    // Application-specific fields
    subscriptionStatus: v.optional(v.string()),
    createdAt: v.number(),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),
})
```

## Frontend Integration

```typescript
// ConvexClientProvider.tsx
"use client"

import { ConvexProviderWithClerk } from "convex/react-clerk"
import { ClerkProvider, useAuth } from "@clerk/nextjs"
import { ConvexReactClient } from "convex/react"

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!)

export function ConvexClientProvider({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        {children}
      </ConvexProviderWithClerk>
    </ClerkProvider>
  )
}
```

## Debugging

```typescript
// Debug identity in Convex
export const debugIdentity = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity()
    console.log("Identity:", JSON.stringify(identity, null, 2))
    return identity
  },
})
```

If identity is null:
1. Check JWT template name is exactly `convex`
2. Verify CLERK_JWT_ISSUER_DOMAIN matches Clerk domain
3. Check ConvexProviderWithClerk is wrapping app
