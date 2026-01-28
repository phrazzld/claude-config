# Async Patterns

## AbortController Timeout Cleanup

**Problem:** Timeout not cleaned up when request succeeds, causing memory leaks or unexpected behavior.

**Anti-pattern:**
```typescript
async function fetchWithTimeout(url: string): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);  // BUG: Never runs if fetch throws
    return response;
  } catch (error) {
    throw error;
  }
}
```

**Pattern:**
```typescript
async function fetchWithTimeout(url: string): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);

  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timeoutId);  // Always runs
  }
}
```

**Rule:** Put `clearTimeout` in `finally` block, not in `try` block.

## Error-Specific Catch Blocks

**Problem:** Generic catch swallows unexpected errors, hiding bugs.

**Anti-pattern:**
```typescript
async function exists(key: string): Promise<boolean> {
  try {
    await storage.head(key);
    return true;
  } catch {
    return false;  // BUG: Network errors, auth failures also return false
  }
}
```

**Pattern:**
```typescript
import { BlobNotFoundError } from '@vercel/blob';

async function exists(key: string): Promise<boolean> {
  try {
    await storage.head(key);
    return true;
  } catch (error) {
    if (error instanceof BlobNotFoundError) {
      return false;  // Expected: key doesn't exist
    }
    throw error;  // Unexpected: network, auth, etc.
  }
}
```

**Rule:** Only catch errors you expect. Rethrow everything else.

## Cancellation Signal Propagation

**Problem:** Nested async operations don't respect cancellation.

**Anti-pattern:**
```typescript
async function processData(items: Item[], signal: AbortSignal) {
  for (const item of items) {
    await processItem(item);  // Ignores signal
  }
}
```

**Pattern:**
```typescript
async function processData(items: Item[], signal: AbortSignal) {
  for (const item of items) {
    if (signal.aborted) throw new DOMException('Aborted', 'AbortError');
    await processItem(item, signal);  // Pass signal down
  }
}
```

**Rule:** Check `signal.aborted` before each long operation. Pass signal to nested calls.
