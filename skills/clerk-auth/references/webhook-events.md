# Clerk Webhook Events

## User Events

### user.created
Fired when a new user signs up.

```typescript
{
  type: "user.created",
  data: {
    id: "user_xxx",
    email_addresses: [{ email_address: "user@example.com" }],
    first_name: "John",
    last_name: "Doe",
    image_url: "https://...",
    created_at: 1234567890
  }
}
```

**Action**: Create user record in your database.

### user.updated
Fired when user profile changes.

```typescript
{
  type: "user.updated",
  data: {
    id: "user_xxx",
    // Full user object with updated fields
  }
}
```

**Action**: Update user record in your database.

### user.deleted
Fired when user is deleted (from dashboard or API).

```typescript
{
  type: "user.deleted",
  data: {
    id: "user_xxx",
    deleted: true
  }
}
```

**Action**: Handle user deletion (soft delete, anonymize, etc.)

## Session Events

### session.created
User signs in.

### session.ended
User signs out.

### session.revoked
Session forcibly revoked (password change, etc.)

## Organization Events (If using organizations)

### organization.created
### organization.updated
### organization.deleted
### organizationMembership.created
### organizationMembership.updated
### organizationMembership.deleted

## Handling Pattern

```typescript
export async function POST(req: Request) {
  const evt = await verifyWebhook(req)

  const eventHandlers: Record<string, (data: any) => Promise<void>> = {
    'user.created': async (data) => {
      await createUserInDatabase({
        clerkId: data.id,
        email: data.email_addresses[0]?.email_address,
        name: `${data.first_name} ${data.last_name}`.trim(),
      })
    },
    'user.updated': async (data) => {
      await updateUserInDatabase(data.id, {
        email: data.email_addresses[0]?.email_address,
        name: `${data.first_name} ${data.last_name}`.trim(),
      })
    },
    'user.deleted': async (data) => {
      await deleteUserFromDatabase(data.id)
    },
  }

  const handler = eventHandlers[evt.type]
  if (handler) {
    await handler(evt.data)
  }

  return new Response('OK', { status: 200 })
}
```

## Webhook Verification

Always verify webhook signatures using svix:

```typescript
import { Webhook } from 'svix'

const wh = new Webhook(process.env.CLERK_WEBHOOK_SECRET!)

try {
  const evt = wh.verify(body, {
    'svix-id': svix_id,
    'svix-timestamp': svix_timestamp,
    'svix-signature': svix_signature,
  })
  // Event is valid
} catch (err) {
  // Invalid signature - reject
  return new Response('Invalid signature', { status: 400 })
}
```
