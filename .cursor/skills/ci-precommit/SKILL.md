---
name: ci-precommit
description: Install and validate pre-commit and CI gates. Use when enabling quality/security automation.
---

# CI + Pre-commit

## When to Use
- Before first commit
- After changing lint/test tooling
- When CI is failing
- Setting up new development environment
- After pulling changes that modify tooling config
- Before creating PR (validate locally)

## Prerequisites
- Python 3.13+ installed
- Virtual environment activated (recommended)
- Project dependencies installed: `pip install -e .[dev]`

## Complete Setup Process

### Step 1: Install Pre-commit

```powershell
# Install pre-commit (if not already in dev dependencies)
pip install pre-commit>=4.5.0

# Or install from project dev dependencies
pip install -e .[dev]
```

### Step 2: Verify Configuration

Ensure `.pre-commit-config.yaml` exists in project root:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.14
    hooks:
      - id: ruff-check
        args: ["--fix"]
      - id: ruff-format
  - repo: https://github.com/psf/black
    rev: 26.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 7.0.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.5
    hooks:
      - id: bandit
        args: ["-q", "-r", "src"]
```

### Step 3: Install Git Hooks

```powershell
# Install hooks into .git/hooks/
pre-commit install

# Install commit-msg hook (optional, for commit message validation)
pre-commit install --hook-type commit-msg
```

### Step 4: Run Pre-commit on All Files

```powershell
# Run all hooks on all files (first time setup)
pre-commit run --all-files

# This will:
# - Download hook repositories
# - Install hook environments
# - Run all hooks on all files
# - Auto-fix issues where possible (ruff-check --fix)
```

### Step 5: Validate Tests

```powershell
# Run test suite
pytest -q

# With coverage (must be ≥ 85.00%)
pytest --cov=src --cov-report=term-missing
```

## Hook Details

### Ruff (Linting + Formatting)
- **ruff-check**: Lint check with auto-fix
- **ruff-format**: Code formatting
- **Config**: `pyproject.toml` [tool.ruff]

### Black (Formatting)
- **black**: Code formatting (backup to ruff-format)
- **Config**: `pyproject.toml` [tool.black]

### isort (Import Sorting)
- **isort**: Import statement sorting
- **Config**: `pyproject.toml` [tool.isort] (profile: black)

### Bandit (Security)
- **bandit**: Security vulnerability scanning
- **Args**: `-q -r src` (quiet mode, scan src directory)
- **Config**: `pyproject.toml` [tool.bandit]

## Manual Validation Commands

If pre-commit hooks are not installed, run manually:

```powershell
# Lint check
ruff check src tests

# Format check
ruff format --check src tests

# Or use black
black --check src tests

# Import sorting check
isort --check-only src tests

# Security scan
bandit -q -r src

# Tests
pytest -q

# Coverage
pytest --cov=src --cov-report=term-missing
```

## CI Integration

### GitHub Actions Example

```yaml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install -e .[dev]
      - run: pre-commit run --all-files
      - run: pytest --cov=src --cov-report=xml
      - run: pip-audit --strict
```

## Troubleshooting

### Hook Installation Fails
- **Issue**: `pre-commit install` fails
- **Solution**: Ensure Git repository is initialized (`git init`)
- **Solution**: Check Git version (pre-commit requires Git 2.9+)

### Hooks Run Slowly
- **Issue**: First run is slow (downloading repos)
- **Solution**: Normal on first run, subsequent runs are cached
- **Solution**: Use `pre-commit run --all-files` only when needed

### Auto-fix Conflicts
- **Issue**: ruff and black both try to format
- **Solution**: ruff-format is primary, black is backup
- **Solution**: Configure both to use same line-length (100)

### Bandit False Positives
- **Issue**: Bandit flags legitimate code
- **Solution**: Add to `pyproject.toml` [tool.bandit] skips
- **Example**: `skips = ["B101"]` (allow assert in tests)

### Coverage Below 85%
- **Issue**: Coverage < 85.00%
- **Solution**: Add tests for uncovered code
- **Solution**: Check `pytest --cov-report=term-missing` for gaps

## Output

### Success Output
```
✅ Pre-commit Setup Complete

Installed hooks:
- ruff-check (with --fix)
- ruff-format
- black
- isort
- bandit

Validation results:
- ✅ All hooks passed
- ✅ Tests passing
- ✅ Coverage ≥ 85.00%

Next steps:
1. Commit changes (hooks will run automatically)
2. Run: pre-commit run --all-files (before PR)
```

### Failure Output
```
❌ Pre-commit Validation Failed

Failed hooks:
- ruff-check: 3 issues found (auto-fixed: 2)
- bandit: 1 High severity issue

Fix plan:
1. Review ruff-check output (1 issue needs manual fix)
2. Address bandit security issue
3. Re-run: pre-commit run --all-files
```

## Integration Points

- Works with `release-check` skill (pre-release validation)
- Required for CI/CD pipeline
- Enforces `.cursor/rules/040-ci.mdc` quality gates
- Validates `.cursor/rules/100-python.mdc` Python standards

## Related Skills
- `release-check` - Pre-release validation (uses same tools)
- `tdd-go` - TDD workflow (tests must pass)
- `rules-vs-skills` - Understand quality rules
