---
name: repo-bootstrap
description: Bootstrap repo structure, safety docs, and meta folders. Use when initializing a new folder-tidy repo.
---

# Repo Bootstrap

## When to Use
- New repo setup
- Re-generating baseline folders (`00_INBOX`, `99_QUARANTINE`, `_meta/*`)
- Restoring repository structure after cleanup
- Setting up new inventory_master instance

## Prerequisites
- Python 3.13+ installed
- Target root path identified (default: `C:\inventory_master\`)

## Complete Bootstrap Process

### Step 1: Confirm Target Root
```powershell
# Default root (Windows)
$ROOT = "C:\inventory_master\"

# Or specify custom root
$ROOT = "D:\my_inventory\"
```

### Step 2: Create SSOT Folder Structure

#### Main Directories
```powershell
# Create main organization folders
New-Item -ItemType Directory -Force -Path "$ROOT\00_INBOX"
New-Item -ItemType Directory -Force -Path "$ROOT\10_WORK"
New-Item -ItemType Directory -Force -Path "$ROOT\20_DEV"
New-Item -ItemType Directory -Force -Path "$ROOT\90_ARCHIVE"
New-Item -ItemType Directory -Force -Path "$ROOT\99_QUARANTINE"
```

**Purpose**:
- `00_INBOX/` - New files awaiting classification
- `10_WORK/` - Active work files
- `20_DEV/` - Development/testing files
- `90_ARCHIVE/` - Long-term storage
- `99_QUARANTINE/` - Files marked for deletion (30-day hold)

#### Meta Directories
```powershell
# Create metadata folders
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\inventory"
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\reports"
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\plans"
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\audit"
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\snapshots"
New-Item -ItemType Directory -Force -Path "$ROOT\_meta\approvals"
```

**Purpose**:
- `_meta/inventory/` - Inventory snapshots (JSONL format)
- `_meta/reports/` - Generated reports (MD, CSV)
- `_meta/plans/` - Plan.json files (immutable)
- `_meta/audit/` - Audit logs (append-only JSONL)
- `_meta/snapshots/` - Before/after snapshots
- `_meta/approvals/` - Approval tokens

### Step 3: Verify Core Documents

Ensure these files exist:
- `agents.md` - SSOT for file operations safety
- `docs/constitution.md` - Non-negotiable principles
- `README.md` - Project overview
- `pyproject.toml` - Python project config

If missing, create minimal versions:
```powershell
# Check for agents.md
if (-not (Test-Path "$ROOT\agents.md")) {
    Write-Warning "agents.md missing - create from template"
}

# Check for docs/constitution.md
if (-not (Test-Path "$ROOT\docs\constitution.md")) {
    Write-Warning "docs/constitution.md missing - create from template"
}
```

### Step 4: Initialize Python Environment (Optional)

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -e .[dev]
```

### Step 5: Initialize Cursor Structure (Optional)

If using Cursor IDE:
```powershell
# Ensure .cursor structure exists
New-Item -ItemType Directory -Force -Path "$ROOT\.cursor\rules"
New-Item -ItemType Directory -Force -Path "$ROOT\.cursor\agents"
New-Item -ItemType Directory -Force -Path "$ROOT\.cursor\skills"
New-Item -ItemType Directory -Force -Path "$ROOT\.cursor\commands"
```

## Safety Rules

### ⚠️ Critical Restrictions
- **Never perform moves/deletes during bootstrap**
- **Read-only operations only**
- **No file modifications**
- **Structure creation only**

### Validation Checklist
- [ ] All main directories created
- [ ] All meta directories created
- [ ] Core documents verified
- [ ] No files moved or deleted
- [ ] Structure matches SSOT from `agents.md`

## Output

### Success Output
```
✅ Bootstrap Complete

Created directories:
- 00_INBOX/
- 10_WORK/
- 20_DEV/
- 90_ARCHIVE/
- 99_QUARANTINE/
- _meta/inventory/
- _meta/reports/
- _meta/plans/
- _meta/audit/
- _meta/snapshots/
- _meta/approvals/

Next steps:
1. Run: python -m inventory_master report --root "$ROOT"
2. Review: docs/AGENTS_AND_SKILLS_GUIDE.md
3. Setup: Use 'everything-provider-setup' skill
```

### Error Handling
- If directory creation fails → report path and permission issues
- If documents missing → provide template locations
- If structure incomplete → list missing components

## Integration Points

- Works with `everything-provider-setup` skill (next step)
- Prepares for `inventory-report` skill (after setup)
- Required before `plan-gated-apply` skill usage
- Foundation for all other skills

## Examples

### Example 1: Fresh Setup
```powershell
# 1. Bootstrap structure
# Use repo-bootstrap skill

# 2. Setup Everything integration
# Use everything-provider-setup skill

# 3. Generate first report
python -m inventory_master report --root "C:\inventory_master\"
```

### Example 2: Restore Structure
```powershell
# If _meta/ folders were accidentally deleted
# Use repo-bootstrap skill to recreate
# Note: Existing plans/reports will not be restored
```

## Troubleshooting

### Permission Denied
- **Issue**: Cannot create directories
- **Solution**: Run PowerShell as Administrator or check folder permissions

### Path Too Long
- **Issue**: Windows 260 character limit
- **Solution**: Use shorter root path or enable long path support

### Missing Documents
- **Issue**: agents.md or constitution.md not found
- **Solution**: Copy from template or create minimal versions

## Related Skills
- `everything-provider-setup` - Next step after bootstrap
- `inventory-report` - Generate first inventory report
- `plan-gated-apply` - Start file organization workflow
