---
name: quarantine-audit
description: Quarantine policy + audit evidence handling. Use when delete is requested or risk is high.
---

# Quarantine + Audit

## When to Use
- Delete operation is requested
- High-risk file operations
- Files need to be removed but kept for recovery
- Compliance with 30-day retention policy
- Before permanent deletion

## Policy (Non-Negotiable)

### Delete is Forbidden
- **Default**: `delete` operations are **forbidden** by default
- **Exception**: Only after 30-day quarantine period
- **Requirement**: Must use `99_QUARANTINE/` instead of direct delete

### Quarantine Process
1. **Move to quarantine**: Files moved to `99_QUARANTINE/` directory
2. **30-day hold**: Files kept for minimum 30 days
3. **Manual review**: Human review required before permanent deletion
4. **Audit trail**: All operations logged in `audit.jsonl`

## Complete Workflow

### Step 1: Identify Files for Quarantine

Files that should be quarantined:
- Duplicate files
- Obsolete/unused files
- Files marked for deletion
- High-risk files (suspicious, corrupted)

**Example**:
```powershell
# Files identified for deletion
$filesToQuarantine = @(
    "C:\inventory_master\00_INBOX\duplicate_file.pdf",
    "C:\inventory_master\10_WORK\obsolete_doc.docx"
)
```

### Step 2: Create Quarantine Plan

Use `plan-gated-apply` skill with quarantine action type:

```json
{
  "plan_id": "2026-01-28T10:00:00__QUARANTINE-001",
  "policy": {
    "allow_delete": false,
    "require_hash_verify": true,
    "require_dry_run": true,
    "max_actions": 200
  },
  "actions": [
    {
      "id": "Q-001",
      "type": "quarantine",
      "src": "00_INBOX/duplicate_file.pdf",
      "dst": "99_QUARANTINE/2026-01-28/duplicate_file.pdf",
      "reason": "Duplicate file identified",
      "precheck": {"exists": true, "size_bytes": 1234567},
      "postcheck": {"exists": true, "size_bytes": 1234567}
    }
  ]
}
```

### Step 3: Execute Quarantine (Plan→Approve→Apply)

Follow standard `plan-gated-apply` workflow:

```powershell
# 1. Generate plan
python -m inventory_master plan --root "C:\inventory_master\" --quarantine

# 2. Review plan
cat _meta\plans\plan_2026-01-28__QUARANTINE-001.json

# 3. Approve (human gate)
python -m inventory_master approve --plan "_meta\plans\plan_2026-01-28__QUARANTINE-001.json"

# 4. Dry-run
python -m inventory_master apply --plan "_meta\plans\plan_2026-01-28__QUARANTINE-001.json" --dry-run

# 5. Apply
python -m inventory_master apply --plan "_meta\plans\plan_2026-01-28__QUARANTINE-001.json"
```

### Step 4: Audit Trail

All quarantine operations are logged:

**Location**: `_meta/audit/audit.jsonl` (append-only)

**Format**:
```json
{
  "timestamp": "2026-01-28T10:00:00+04:00",
  "operation": "quarantine",
  "plan_id": "2026-01-28T10:00:00__QUARANTINE-001",
  "action_id": "Q-001",
  "src": "00_INBOX/duplicate_file.pdf",
  "dst": "99_QUARANTINE/2026-01-28/duplicate_file.pdf",
  "reason": "Duplicate file identified",
  "hash_before": "sha256:abc123...",
  "hash_after": "sha256:abc123...",
  "verified": true
}
```

### Step 5: Snapshot Evidence

Before/after snapshots saved:

**Location**: `_meta/snapshots/`

**Files**:
- `before_2026-01-28T10:00:00__QUARANTINE-001.json`
- `after_2026-01-28T10:00:00__QUARANTINE-001.json`

**Purpose**: Recovery evidence, integrity verification

## 30-Day Retention Policy

### Quarantine Structure
```
99_QUARANTINE/
├── 2026-01-28/          # Date-based organization
│   ├── duplicate_file.pdf
│   └── obsolete_doc.docx
├── 2026-01-15/          # Older quarantine (can be reviewed)
└── README.md            # Policy reminder
```

### Review Process (After 30 Days)

```powershell
# 1. List files older than 30 days
Get-ChildItem "99_QUARANTINE\" -Recurse | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }

# 2. Review each file
# - Verify no longer needed
# - Check audit trail
# - Confirm safe to delete

# 3. Create deletion plan (after 30 days)
# Use plan-gated-apply with allow_delete=true (special approval)
```

### Permanent Deletion (After 30 Days)

**Special approval required**:
- 30-day period must have elapsed
- Human review completed
- Audit trail verified
- Explicit approval token created

```json
{
  "plan_id": "2026-02-28T10:00:00__DELETE-001",
  "policy": {
    "allow_delete": true,  // Special approval required
    "quarantine_period_elapsed": true,
    "reviewed_by": "human",
    "require_hash_verify": true
  },
  "actions": [
    {
      "id": "D-001",
      "type": "delete",
      "src": "99_QUARANTINE/2026-01-28/duplicate_file.pdf",
      "reason": "30-day quarantine period elapsed, reviewed and approved for deletion"
    }
  ]
}
```

## Evidence Requirements

### Audit Log (Append-Only)
- **File**: `_meta/audit/audit.jsonl`
- **Format**: JSONL (one JSON object per line)
- **Requirement**: Never modify, only append
- **Content**: All operations with timestamps, hashes, verification

### Snapshots
- **Location**: `_meta/snapshots/`
- **Format**: JSON manifest files
- **Content**: Before/after file lists, hashes, metadata
- **Purpose**: Recovery and integrity verification

### Approval Tokens
- **Location**: `_meta/approvals/`
- **Format**: `APPROVED__<plan_id>.token`
- **Purpose**: Human gate evidence

## Risk Assessment

### Low Risk
- Duplicate files (verified)
- Obsolete documentation
- Temporary files

### Medium Risk
- User-created content
- Configuration files
- Log files

### High Risk
- System files
- Database files
- Encrypted files
- Files with unknown origin

**High-risk files**: Require additional review before quarantine

## Rollback Process

If quarantine was incorrect:

```powershell
# 1. Find original location from audit log
# Check: _meta/audit/audit.jsonl

# 2. Create restore plan
python -m inventory_master plan --restore --from-quarantine "99_QUARANTINE/2026-01-28/duplicate_file.pdf"

# 3. Review and approve restore plan
python -m inventory_master approve --plan "_meta\plans\plan_restore_*.json"

# 4. Apply restore
python -m inventory_master apply --plan "_meta\plans\plan_restore_*.json"
```

## Output

### Success Output
```
✅ Quarantine Complete

Quarantined files:
- 00_INBOX/duplicate_file.pdf → 99_QUARANTINE/2026-01-28/duplicate_file.pdf
- 10_WORK/obsolete_doc.docx → 99_QUARANTINE/2026-01-28/obsolete_doc.docx

Audit trail:
- Logged in: _meta/audit/audit.jsonl
- Snapshots: _meta/snapshots/before_*.json, after_*.json

Next steps:
- Files will be held for 30 days
- Review after 30 days for permanent deletion
- Use audit-query skill to review operations
```

### Risk Warning Output
```
⚠️ High-Risk Quarantine Detected

Files with high risk:
- system_config.json (system file)
- database_backup.db (database file)

Recommendations:
1. Verify these files are safe to quarantine
2. Create backup before quarantine
3. Review audit trail carefully
4. Consider additional approval

Proceed with caution!
```

## Integration Points

- Works with `plan-gated-apply` skill (quarantine action type)
- Uses `audit-query` skill for reviewing operations
- Uses `snapshot-verify` skill for integrity checks
- Enforces `agents.md` safety policies

## Related Skills
- `plan-gated-apply` - Execute quarantine operations
- `audit-query` - Review audit trail
- `snapshot-verify` - Verify snapshot integrity

## Troubleshooting

### Quarantine Directory Full
- **Issue**: `99_QUARANTINE/` directory growing large
- **Solution**: Review and delete files older than 30 days
- **Solution**: Archive old quarantine to `90_ARCHIVE/`

### Audit Log Missing
- **Issue**: Audit log not created
- **Solution**: Verify `_meta/audit/` directory exists
- **Solution**: Check write permissions

### Hash Verification Fails
- **Issue**: Hash mismatch after quarantine
- **Solution**: Do not proceed with operation
- **Solution**: Investigate file corruption or modification
- **Solution**: Use snapshot to verify original state
