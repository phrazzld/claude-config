# Python Testing Patterns

## Test Behavior, Not Implementation

```python
# Good: Tests outcome
def test_user_creation_sets_active_status():
    user = create_user(email="test@example.com")
    assert user.is_active is True
    assert user.email == "test@example.com"

# Bad: Tests implementation details
def test_user_creation_calls_db_insert():
    mock_db.insert.assert_called_once()  # Don't do this
```

## Fixtures

```python
@pytest.fixture
def sample_user() -> User:
    return User(id=1, email="test@example.com", is_active=True)

@pytest.fixture
def user_service(sample_user) -> UserService:
    return UserService(initial_users=[sample_user])

def test_user_lookup(user_service, sample_user):
    result = user_service.get(sample_user.id)
    assert result == sample_user
```

## Parametrization

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("user@test.org", True),
    ("", False),
    ("invalid", False),
    ("@no-local.com", False),
])
def test_email_validation(email: str, valid: bool):
    result = is_valid_email(email)
    assert result == valid
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("http://example.com")
    assert result.status_code == 200
```

## Coverage Configuration

```toml
[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
fail_under = 85
```

## Test Organization

```
tests/
  unit/
    test_models.py
    test_services.py
  integration/
    test_api.py
    test_database.py
  conftest.py  # Shared fixtures
```
