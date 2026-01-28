---
name: plan-gated-apply
description: Generate/approve/apply plans safely with dry-run + audit + snapshots. Use when moving files, organizing directories, or performing any file operations that require safety guarantees. Enforces Plan→Approve→Apply workflow with mandatory human gate.
---

# Plan → Approve → Apply

## When to Use
- Any operation that moves/renames/quarantines files
- File organization and directory cleanup
- Batch file operations requiring safety guarantees
- Operations requiring audit trail and rollback capability

## Prerequisites
- `planner` agent available (for plan generation)
- `plan-validate` skill (for plan validation)
- `approval-gate` skill (for approval workflow)
- `approver` agent (for token validation)
- `executor` agent (for applying plan)
- `verifier` agent (for post-apply verification)

## Complete Workflow

### Step 1: Generate Plan
**Purpose**: Create plan.json with file operations

```bash
python -m inventory_master plan --root "C:\inventory_master\"
```

**Output**: 
- `_meta/plans/plan_YYYY-MM-DDTHHMMSS__ROOT-ID.json`
- Plan contains: plan_id, root, policy, actions[]

**Agent**: `planner` (automatically invoked)

**What happens**:
- Analyzes directory structure
- Applies classification rules
- Detects path conflicts
- Generates plan.json with actions

### Step 2: Validate Plan (Recommended)
**Purpose**: Ensure plan is safe before approval

```bash
# Use plan-validate skill
python -m inventory_master validate --plan "_meta/plans/plan_2026-01-28.json"
```

**Checks**:
- Plan schema correctness
- Policy compliance (allow_delete=false, max_actions, etc.)
- Path conflicts
- Long paths (Windows 260 char limit)
- Invalid paths
- Risk assessment

**Skill**: `plan-validate`

### Step 3: Human Review
**Purpose**: Review plan.json before approval

```bash
# Review the plan
cat _meta/plans/plan_2026-01-28.json
# or
type _meta\plans\plan_2026-01-28.json
```

**What to check**:
- Actions are correct
- No unintended file operations
- Paths are valid
- No conflicts detected
- Policy compliance

### Step 4: Approve (Human Gate)
**Purpose**: Create approval token (human-only step)

```bash
python -m inventory_master approve --plan "_meta/plans/plan_2026-01-28.json"
```

**Output**:
- `_meta/approvals/APPROVED__<plan_id>.token`
- Approval token file created

**⚠️ Critical**: 
- **Only humans can create approval tokens**
- Agents cannot approve plans
- This is the mandatory human gate

**Skill**: `approval-gate`

### Step 5: Dry-Run (Required)
**Purpose**: Preview changes without applying

```bash
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json" --dry-run
```

**Output**:
- Preview of all actions: `[DRY] move: src -> dst`
- Audit log entry: `{"event": "dry_run", "plan_id": "...", "actions": N}`
- No files are modified

**⚠️ Mandatory**: 
- Dry-run **must** be executed before apply
- Apply will fail if dry-run not found in audit log
- This is a safety requirement

**Agent**: `executor` (dry-run mode)

### Step 6: Apply (Execute)
**Purpose**: Actually perform file operations

```bash
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json"
```

**What happens**:
1. Verify approval token exists
2. Check dry-run was executed (from audit log)
3. Create before snapshot
4. Apply actions atomically (all or nothing)
5. Create after snapshot
6. Verify hash consistency
7. Record in audit.jsonl

**Agent**: `executor` (apply mode)

**Safety checks**:
- ✅ Approval token required
- ✅ Dry-run required
- ✅ Hash verification
- ✅ Atomic transaction (all or nothing)

### Step 7: Verify (Recommended)
**Purpose**: Validate applied changes

```bash
# Agent: verifier (automatically invoked)
# Checks:
# - All files moved correctly
# - Snapshots match
# - Hash consistency
# - No missing files
```

**Agent**: `verifier`

## Integration Points

### Works With
- **`inventory-report`**: Current state analysis (before planning)
- **`planner` agent**: Plan generation
- **`plan-validate` skill**: Plan validation
- **`approval-gate` skill**: Approval workflow
- **`approver` agent**: Token validation
- **`executor` agent**: Plan execution
- **`verifier` agent**: Post-apply verification
- **`quarantine-audit` skill**: Delete request handling
- **`snapshot-verify` skill**: Snapshot integrity check

### Typical Workflow
```
inventory-report
  → planner (generate plan)
  → plan-validate (validate plan)
  → approval-gate (human approval)
  → executor (dry-run)
  → executor (apply)
  → verifier (verify)
```

## Safety Requirements

### Mandatory Checks
1. **Approval token exists**: `_meta/approvals/APPROVED__<plan_id>.token`
2. **Dry-run executed**: Found in `_meta/audit/audit.jsonl`
3. **Policy compliance**: max_actions, allow_delete, etc.
4. **Hash verification**: File integrity checked

### Safety Guarantees
- **Atomic operations**: All actions succeed or all fail
- **Audit trail**: All operations logged
- **Snapshots**: Before/after states saved
- **Rollback support**: Can revert using snapshots
- **No partial apply**: All or nothing

## Output

### Plan Generation
- Plan file path: `_meta/plans/plan_<id>.json`
- Action count
- Policy summary
- Conflict warnings (if any)

### Approval
- Approval token path: `_meta/approvals/APPROVED__<plan_id>.token`
- Approval timestamp
- Status: approved

### Dry-Run
- Preview of all actions
- Audit log entry
- No file modifications

### Apply
- Applied actions summary
- Audit log path: `_meta/audit/audit.jsonl`
- Snapshot paths: `_meta/snapshots/`
  - Before: `snapshot_<plan_id>_before.json`
  - After: `snapshot_<plan_id>_after.json`
- Verification results
- Rollback instructions (if needed)

## Example Workflow

### Scenario: Organize INBOX files

```bash
# 1. Current state
python -m inventory_master report --root "C:\inventory_master\"

# 2. Generate plan
python -m inventory_master plan --root "C:\inventory_master\"
# Output: _meta/plans/plan_2026-01-28T08:00:00+04:00__ROOT-A.json

# 3. Validate plan (optional but recommended)
python -m inventory_master validate --plan "_meta/plans/plan_2026-01-28T08:00:00+04:00__ROOT-A.json"

# 4. Review plan
type _meta\plans\plan_2026-01-28T08:00:00+04:00__ROOT-A.json

# 5. Approve (human gate)
python -m inventory_master approve --plan "_meta/plans/plan_2026-01-28T08:00:00+04:00__ROOT-A.json"
# Output: _meta/approvals/APPROVED__2026-01-28T08:00:00+04:00__ROOT-A.token

# 6. Dry-run (mandatory)
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28T08:00:00+04:00__ROOT-A.json" --dry-run
# Output: [DRY] move: 00_INBOX/file1.pdf -> 01_DOCS/file1.pdf

# 7. Apply
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28T08:00:00+04:00__ROOT-A.json"
# Output: Applied 15 actions, snapshots created

# 8. Verify (automatic)
# verifier agent checks results
```

## Troubleshooting

### Error: "Missing approval token"
**Cause**: Approval token not created
**Solution**: Run `approve` command (Step 4)
**Check**: Token file exists in `_meta/approvals/`

### Error: "Dry-run required before apply"
**Cause**: Dry-run not executed
**Solution**: Run apply with `--dry-run` flag first (Step 5)
**Check**: Audit log contains dry_run event

### Error: "Too many actions for policy.max_actions"
**Cause**: Plan exceeds max_actions limit (default: 200)
**Solution**: Split plan into smaller batches
**Check**: `plan.json` policy section

### Error: "Path conflict detected"
**Cause**: Destination already exists
**Solution**: Review plan, resolve conflicts
**Check**: Use `plan-validate` skill

### Approval Token Not Found
**Cause**: Token file missing or wrong plan_id
**Solution**: Verify plan_id matches token filename
**Check**: `_meta/approvals/APPROVED__<plan_id>.token`

## Restrictions

### Agent Limitations
- **Agents cannot approve**: Only humans can create approval tokens
- **Agents cannot skip dry-run**: Dry-run is mandatory
- **Agents cannot bypass validation**: Safety checks are enforced

### Policy Restrictions
- **delete OFF by default**: Use quarantine instead
- **max_actions limit**: Default 200 actions per plan
- **require_dry_run**: Always true (cannot disable)
- **require_hash_verify**: Always true (cannot disable)

## Best Practices

### Before Planning
- ✅ Run `inventory-report` to understand current state
- ✅ Review existing plans and approvals
- ✅ Check for conflicts

### During Planning
- ✅ Use `planner` agent for plan generation
- ✅ Validate plan with `plan-validate` skill
- ✅ Review plan.json carefully before approval

### During Approval
- ✅ Human review is mandatory
- ✅ Verify all actions are correct
- ✅ Check for conflicts and risks

### During Execution
- ✅ Always run dry-run first
- ✅ Review dry-run output carefully
- ✅ Verify approval token exists
- ✅ Run apply only after confirmation

### After Execution
- ✅ Use `verifier` agent to validate results
- ✅ Check audit log for completeness
- ✅ Verify snapshots were created
- ✅ Test rollback if needed

## Additional Resources
- For plan validation: `plan-validate` skill
- For approval workflow: `approval-gate` skill
- For execution details: `.cursor/agents/executor.md`
- For verification: `.cursor/agents/verifier.md`
- For workflow examples: `docs/WORKFLOW_EXAMPLES.md`
- For safety policies: `docs/constitution.md`
