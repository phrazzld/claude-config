# TypeScript Testing Strategy

## Test Pyramid

| Level | Coverage | Focus | Speed |
|-------|----------|-------|-------|
| Unit | 70% | Pure functions, utilities | Fast |
| Integration | 20% | Component interactions, APIs | Medium |
| E2E | 10% | Critical user flows | Slow |

## File Organization

```
src/
  features/auth/
    auth.ts
    auth.test.ts           # Unit tests
    auth.integration.test.ts  # Integration
```

## Behavior-First Tests

```typescript
// Good: Test behavior
describe('UserService', () => {
  it('returns user when found', async () => {
    const user = await service.getUser('123');
    expect(user.email).toBe('test@example.com');
  });

  it('throws NotFoundError when user missing', async () => {
    await expect(service.getUser('999'))
      .rejects.toThrow(NotFoundError);
  });
});

// Bad: Test implementation
it('calls repository.findById', async () => {
  await service.getUser('123');
  expect(mockRepo.findById).toHaveBeenCalledWith('123');
});
```

## Mock Boundaries Only

```typescript
// Good: Mock external boundary
const mockPaymentGateway = {
  charge: vi.fn().mockResolvedValue({ id: 'txn_123' }),
};

// Bad: Mock internal component
const mockUserRepository = vi.fn(); // Don't mock your own code
```

## Test Data Factories

```typescript
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: 'usr_123',
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date(),
    ...overrides,
  };
}

it('formats user name', () => {
  const user = createUser({ name: 'John Doe' });
  expect(formatName(user)).toBe('J. Doe');
});
```

## Async Testing

```typescript
// Proper async/await
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// Testing rejections
it('rejects invalid input', async () => {
  await expect(validate(null)).rejects.toThrow('Invalid');
});

// Testing timeouts
it('times out slow requests', async () => {
  vi.useFakeTimers();
  const promise = fetchWithTimeout(100);
  vi.advanceTimersByTime(101);
  await expect(promise).rejects.toThrow('Timeout');
});
```

## Coverage Thresholds

```typescript
// vitest.config.ts
coverage: {
  thresholds: {
    global: { lines: 80 },
    'src/features/payments/': { lines: 95 }, // Critical path
  },
}
```
