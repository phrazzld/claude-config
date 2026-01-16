# Ruff Configuration

## Comprehensive Rule Selection

```toml
[tool.ruff]
target-version = "py311"
line-length = 88

select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
    "S",    # flake8-bandit (security)
    "N",    # pep8-naming
    "PLR",  # pylint refactor
    "D",    # pydocstyle
    "ANN",  # flake8-annotations
    "PT",   # flake8-pytest-style
]

ignore = [
    "E501",   # Line length (handled by formatter)
    "D100",   # Missing docstring in public module
    "ANN101", # Missing type for self
    "S101",   # Assert usage (allowed in tests)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false

[tool.ruff.isort]
known-first-party = ["myproject"]
force-single-line = false
combine-as-imports = true

[tool.ruff.pydocstyle]
convention = "google"

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "D",      # No docstrings required in tests
    "S101",   # Assert allowed
    "PLR2004", # Magic values allowed
    "ANN",    # Annotations relaxed
]
"__init__.py" = ["F401"]  # Allow unused imports
```

## Daily Commands

```bash
# Lint with auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .

# CI (no fix, fail on issues)
uv run ruff check . --no-fix
uv run ruff format --check .
```

## Migration from Legacy Tools

Ruff replaces:
- black (formatting)
- isort (import sorting)
- flake8 (linting)
- pylint (extended checks)
- bandit (security)

Speed: 10-100x faster than legacy combinations.
