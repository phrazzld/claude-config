# TypeScript Type Patterns

## Result Type for Error Handling

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseJson<T>(input: string): Result<T, SyntaxError> {
  try {
    return { ok: true, value: JSON.parse(input) };
  } catch (e) {
    return { ok: false, error: e as SyntaxError };
  }
}

// Usage
const result = parseJson<User>(data);
if (result.ok) {
  console.log(result.value.name);
} else {
  console.error(result.error.message);
}
```

## Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Discriminated union guard
function isSuccess<T>(state: AsyncState<T>): state is { status: 'success'; data: T } {
  return state.status === 'success';
}
```

## Branded Types

```typescript
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function createUserId(id: string): UserId {
  if (!id.startsWith('usr_')) throw new Error('Invalid user ID');
  return id as UserId;
}

// Now UserId and OrderId are incompatible
function getUser(id: UserId): Promise<User> { ... }
getUser(orderId); // Type error!
```

## Utility Types

```typescript
// Extract keys of specific type
type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];

// Make all properties optional deeply
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

// Require at least one of the properties
type RequireAtLeastOne<T> = {
  [K in keyof T]: Required<Pick<T, K>> & Partial<Omit<T, K>>;
}[keyof T];
```

## When Types Become Gymnastics

**Stop if:**
- Error messages are longer than the code
- IDE autocomplete stops working
- Compilation slows noticeably
- Colleagues can't understand the types

**Simplify by:**
- Breaking into smaller, named types
- Using runtime validation instead (zod, valibot)
- Accepting `unknown` with guards
- Adding comments explaining intent
