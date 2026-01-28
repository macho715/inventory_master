---
name: tdd-go
description: Run the strict TDD loop using plan.md as SoT. Use when the user says 'go' or asks to implement next test. Follows Kent Beck's TDD methodology with RED→GREEN→REFACTOR cycle.
---

# TDD Go

## When to Use
- User says **"go"** (primary trigger)
- User asks to implement next test
- TDD cycle execution needed
- Implementing from `plan.md` test queue

## Prerequisites
- `plan.md` exists with unchecked tests
- Test framework available (`pytest` for Python, `cargo test` for Rust)
- `implementer` agent available (for code implementation)
- `verifier` agent available (for validation)

## plan.md Structure

### Format
```markdown
# plan.md (SoT)

## Tests
- [ ] test: <description> (file: <path>, name: <test_function_name>)
- [x] test: <description> (file: <path>, name: <test_function_name>) # passed @YYYY-MM-DD <commit:hash>
```

### Parsing Rules
- **Unchecked test**: `- [ ] test: ...`
- **Checked test**: `- [x] test: ... # passed @...`
- **Next test**: First unchecked test from top
- **Metadata**: Extract `file:` and `name:` from parentheses

## Instructions

### Step 1: Select Next Test
1. Read `plan.md`
2. Find first `- [ ] test:` line
3. Extract metadata: `file:` (test file path) and `name:` (test function name)
4. **Only process this one test** (do not skip ahead)

### Step 2: RED Phase
1. Check if test already exists in the file
2. If not, write the **simplest failing test**:
   ```python
   def test_example():
       assert False  # Intentionally failing
   ```
3. Run test to confirm it fails:
   ```bash
   pytest tests/test_file.py::test_name -v
   # or
   cargo test test_name
   ```
4. Verify failure message is clear

### Step 3: GREEN Phase
1. Implement **minimum code** to make test pass
2. Hardcoding is acceptable initially
3. Run test to confirm it passes:
   ```bash
   pytest tests/test_file.py::test_name -v
   ```
4. Run **all tests** to ensure nothing broke:
   ```bash
   pytest -q
   # or
   cargo test
   ```

### Step 4: REFACTOR Phase
1. **Only refactor if all tests pass**
2. Improve structure without changing behavior:
   - Extract methods/functions
   - Rename variables
   - Remove duplication
   - Improve naming
3. **Behavior must remain identical**
4. Run all tests after each refactoring step:
   ```bash
   pytest -q
   ```

### Step 5: Update plan.md
1. Mark test as completed:
   ```markdown
   - [x] test: <description> (file: <path>, name: <name>) # passed @2026-01-28 <commit:abcd1234>
   ```
2. Use actual date and commit hash (or placeholder if not committed yet)

## Integration Points

### Works With
- **`implementer` agent**: Automatically called for code implementation
- **`verifier` agent**: Validates test execution and results
- **`plan.md`**: Source of truth for test queue

### Workflow
```
User: "go"
  → tdd-go skill
    → Read plan.md (select next test)
    → RED: Write failing test
    → implementer agent (GREEN: minimal code)
    → REFACTOR: Structure improvement
    → verifier agent (validate all tests)
    → Update plan.md
```

## TDD Principles

### RED Phase
- Write the **simplest** failing test
- Test should clearly express the requirement
- Failure message should be informative
- **One test at a time**

### GREEN Phase
- Write **minimum** code to pass
- Hardcoding is fine initially
- No premature optimization
- **Just make it pass**

### REFACTOR Phase
- **Only when all tests pass**
- Improve structure, not behavior
- Small, incremental changes
- Run tests after each change
- **Behavior must remain identical**

## Example Workflow

### Input (plan.md)
```markdown
## Tests
- [ ] test: CLI report works on temp dir (file: tests/test_cli_smoke.py, name: test_cli_report_smoke)
```

### RED Phase
```python
# tests/test_cli_smoke.py
def test_cli_report_smoke():
    result = run_cli_report()
    assert result.status == "ok"  # This will fail
```

### GREEN Phase
```python
# src/inventory_master/cli.py
def report_command():
    return {"status": "ok"}  # Minimal implementation
```

### REFACTOR Phase
```python
# Extract to function, improve naming
def generate_report(root: Path) -> ReportResult:
    return ReportResult(status="ok", files=0)
```

### Output (plan.md updated)
```markdown
## Tests
- [x] test: CLI report works on temp dir (file: tests/test_cli_smoke.py, name: test_cli_report_smoke) # passed @2026-01-28 <commit:abcd1234>
```

## Output Format

### ExecSummary
- Test selected from plan.md
- Phase completed (RED/GREEN/REFACTOR)
- Files modified
- Test status

### Diff Summary
- Minimal changes only
- Test file changes
- Implementation changes
- plan.md update

### Verification Commands
```bash
# Run specific test
pytest tests/test_file.py::test_name -v

# Run all tests
pytest -q

# Check coverage (if applicable)
pytest --cov=src --cov-report=term-missing
```

## Restrictions

### Must Follow
- **One test at a time**: Never skip ahead
- **All tests pass**: Before refactoring
- **Behavior preservation**: Refactoring must not change behavior
- **plan.md is SoT**: Always read from plan.md, update after completion

### Commit Discipline
- **Structural commits**: Refactoring only (no behavior change)
  - Example: `[Structural] Extract method for clarity`
- **Behavioral commits**: New functionality or bug fixes
  - Example: `[Behavioral] Add report command to pass test`
- **Never mix**: Structural and behavioral in same commit

## Troubleshooting

### Test Already Exists
- If test exists but fails → proceed to GREEN phase
- If test exists and passes → check plan.md, may need to mark as complete

### All Tests Fail After Change
- Revert to last green state
- Make smaller incremental changes
- Run tests more frequently

### plan.md Format Error
- Verify format matches expected structure
- Check for proper `- [ ]` or `- [x]` syntax
- Ensure metadata (file:, name:) is present

## Additional Resources
- For TDD methodology: Kent Beck's "Test-Driven Development"
- For implementer details: `.cursor/agents/implementer.md`
- For verification: `.cursor/agents/verifier.md`
- For workflow examples: `docs/AGENTS_AND_SKILLS_GUIDE.md`
