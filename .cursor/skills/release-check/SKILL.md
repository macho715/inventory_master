---
name: release-check
description: Pre-release checklist (tests, lint, security, docs). Use before tagging or shipping.
---

# Release Check

## When to Use
- Before creating release tag
- Before merging to main branch
- Before shipping to production
- Pre-release validation
- Final quality gate before deployment

## Prerequisites
- All development work completed
- Tests written and passing
- Code reviewed
- Documentation updated

## Complete Release Checklist

### 1. Test Coverage (≥ 85.00%)

```powershell
# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Verify coverage threshold
# Must show: coverage ≥ 85.00%
```

**Requirement**: Coverage must be ≥ 85.00% (from `.cursor/rules/040-ci.mdc`)

**If failing**:
- Add tests for uncovered code
- Check `--cov-report=term-missing` output
- Focus on critical paths first

### 2. Linting & Formatting

```powershell
# Ruff lint check
ruff check src tests

# Ruff format check
ruff format --check src tests

# Black format check (backup)
black --check src tests

# isort import sorting check
isort --check-only src tests
```

**Requirement**: All checks must pass with 0 warnings (from `.cursor/rules/040-ci.mdc`)

**If failing**:
- Run `ruff check --fix src tests` to auto-fix
- Run `ruff format src tests` to format
- Run `isort src tests` to sort imports

### 3. Security Scanning

```powershell
# Bandit security scan (High severity = 0 required)
bandit -q -r src

# pip-audit dependency vulnerabilities
pip-audit --strict
```

**Requirements** (from `.cursor/rules/040-ci.mdc`):
- `bandit High=0` (no High severity issues)
- `pip-audit --strict` must pass

**If failing**:
- Review bandit output for security issues
- Update dependencies with known CVEs
- Review false positives in `pyproject.toml` [tool.bandit] skips

### 4. Documentation Updates

Verify these documents are up-to-date:
- [ ] `agents.md` - Architecture and safety rules
- [ ] `docs/constitution.md` - Non-negotiable principles
- [ ] `README.md` - Project overview and quickstart
- [ ] `CHANGELOG.md` - Release notes (if exists)
- [ ] `.cursor/rules/*.mdc` - Cursor rules (if modified)

**Check commands**:
```powershell
# Verify files exist and are recent
Get-Item agents.md, docs\constitution.md, README.md | Select-Object Name, LastWriteTime
```

### 5. Safety Defaults Verification

Verify no unsafe defaults (from `agents.md`):
- [ ] `write` operations default to OFF
- [ ] `delete` operations default to OFF (quarantine instead)
- [ ] HTTP server is read-only (if applicable)
- [ ] Approval gates enforced for file operations
- [ ] Audit trails enabled

**Check locations**:
- `src/inventory_master/` - Default values in code
- `config/project_profile.yaml` - Policy settings
- `agents.md` - Safety rules

### 6. Pre-commit Hooks

```powershell
# Run all pre-commit hooks
pre-commit run --all-files

# Or if hooks not installed
pre-commit run --all-files --hook-stage manual
```

**Requirement**: All hooks must pass

### 7. Integration Tests

```powershell
# Run full test suite
pytest -q

# Run with verbose output (if needed)
pytest -v

# Run specific test categories
pytest -m "not slow"  # Exclude slow tests
```

**Requirement**: All tests must pass

## Complete Validation Script

Run all checks in sequence:

```powershell
# 1. Tests + Coverage
Write-Host "Running tests with coverage..." -ForegroundColor Cyan
pytest --cov=src --cov-report=term-missing
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Linting
Write-Host "Running lint checks..." -ForegroundColor Cyan
ruff check src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. Formatting
Write-Host "Checking code formatting..." -ForegroundColor Cyan
ruff format --check src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Import sorting
Write-Host "Checking import sorting..." -ForegroundColor Cyan
isort --check-only src tests
if ($LASTEXITCODE -ne 0) { exit 1 }

# 5. Security scan
Write-Host "Running security scan..." -ForegroundColor Cyan
bandit -q -r src
if ($LASTEXITCODE -ne 0) { exit 1 }

# 6. Dependency audit
Write-Host "Auditing dependencies..." -ForegroundColor Cyan
pip-audit --strict
if ($LASTEXITCODE -ne 0) { exit 1 }

# 7. Pre-commit hooks
Write-Host "Running pre-commit hooks..." -ForegroundColor Cyan
pre-commit run --all-files
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "✅ All release checks passed!" -ForegroundColor Green
```

## Release Checklist Summary

| Check | Command | Requirement | Status |
|-------|---------|-------------|--------|
| **Tests + Coverage** | `pytest --cov=src --cov-report=term-missing` | Coverage ≥ 85.00% | ⬜ |
| **Ruff Lint** | `ruff check src tests` | 0 warnings | ⬜ |
| **Ruff Format** | `ruff format --check src tests` | All formatted | ⬜ |
| **isort** | `isort --check-only src tests` | Imports sorted | ⬜ |
| **Bandit** | `bandit -q -r src` | High = 0 | ⬜ |
| **pip-audit** | `pip-audit --strict` | No CVEs | ⬜ |
| **Pre-commit** | `pre-commit run --all-files` | All hooks pass | ⬜ |
| **Docs** | Manual check | Updated | ⬜ |
| **Safety** | Manual check | No unsafe defaults | ⬜ |

## Output

### Success Output
```
✅ Release Check Complete

All checks passed:
✅ Tests: 42 passed, coverage 87.50%
✅ Linting: 0 warnings
✅ Formatting: All files formatted
✅ Security: 0 High severity issues
✅ Dependencies: No known CVEs
✅ Pre-commit: All hooks passed
✅ Documentation: Up to date
✅ Safety: No unsafe defaults

Ready for release!
```

### Failure Output
```
❌ Release Check Failed

Failed checks:
❌ Coverage: 82.30% (required: ≥ 85.00%)
❌ Bandit: 1 High severity issue found
❌ Documentation: agents.md not updated

Fix plan:
1. Add tests to increase coverage to ≥ 85.00%
2. Address bandit security issue in src/planner.py:45
3. Update agents.md with latest changes

Re-run after fixes: release-check skill
```

## Integration Points

- Uses `ci-precommit` skill setup
- Enforces `.cursor/rules/040-ci.mdc` quality gates
- Validates `.cursor/rules/100-python.mdc` Python standards
- Works with `reviewer` agent for final validation

## Related Skills
- `ci-precommit` - Setup quality automation
- `tdd-go` - Ensure tests are written
- `rules-vs-skills` - Understand quality rules

## Troubleshooting

### Coverage Below Threshold
- **Issue**: Coverage < 85.00%
- **Solution**: Add tests for uncovered branches
- **Solution**: Use `--cov-report=term-missing` to find gaps

### Security Issues
- **Issue**: Bandit finds High severity issues
- **Solution**: Review and fix security vulnerabilities
- **Solution**: Check if false positive (add to skips if legitimate)

### Dependency CVEs
- **Issue**: pip-audit finds known CVEs
- **Solution**: Update vulnerable dependencies
- **Solution**: Review if CVE affects this project's usage

### Documentation Outdated
- **Issue**: Docs not updated
- **Solution**: Update relevant documentation files
- **Solution**: Ensure CHANGELOG.md reflects changes
