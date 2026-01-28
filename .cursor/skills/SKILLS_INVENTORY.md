# Skills Inventory & Status

> **Last Updated**: 2026-01-28 (Enhanced baseline 5-pack)  
> **Purpose**: Track all skills, their status, and alignment with `docs/AGENTS_AND_SKILLS_GUIDE.md`

---

## Skills Overview

### Total Skills: 15

| # | Skill | Status | In Guide | Lines | Last Enhanced |
|---|-------|--------|----------|-------|---------------|
| 1 | `agent-selector` | ✅ Complete | ✅ Yes | 255 | 2026-01-28 |
| 2 | `approval-gate` | ✅ Complete | ✅ Yes | 61 | - |
| 3 | `audit-query` | ✅ Complete | ✅ Yes | 56 | - |
| 4 | `ci-precommit` | ✅ Complete | ✅ Yes | 200+ | 2026-01-28 |
| 5 | `everything-provider-setup` | ✅ Complete | ✅ Yes | 239 | 2026-01-28 |
| 6 | `everything-test` | ✅ Complete | ✅ Yes | 58 | - |
| 7 | `inventory-report` | ✅ Complete | ✅ Yes | 137 | 2026-01-28 |
| 8 | `plan-gated-apply` | ✅ Complete | ✅ Yes | 300+ | 2026-01-28 |
| 9 | `plan-validate` | ✅ Complete | ✅ Yes | 57 | - |
| 10 | `quarantine-audit` | ✅ Complete | ✅ Yes | 300+ | 2026-01-28 |
| 11 | `release-check` | ✅ Complete | ✅ Yes | 300+ | 2026-01-28 |
| 12 | `repo-bootstrap` | ✅ Complete | ✅ Yes | 200+ | 2026-01-28 |
| 13 | `rules-vs-skills` | ✅ Complete | ✅ Yes | 300+ | 2026-01-28 |
| 14 | `snapshot-verify` | ✅ Complete | ✅ Yes | 48 | - |
| 15 | `tdd-go` | ✅ Complete | ✅ Yes | 232 | 2026-01-28 |

---

## Skills by Category

### Setup & Configuration
- `repo-bootstrap` - Repository initialization
- `everything-provider-setup` - Everything integration setup
- `ci-precommit` - CI/Pre-commit hooks setup

### Development Workflows
- `tdd-go` - TDD cycle execution
- `agent-selector` - Agent selection guidance

### File Operations (Safety)
- `plan-gated-apply` - Plan→Approve→Apply workflow
- `plan-validate` - Plan validation
- `approval-gate` - Approval workflow management
- `quarantine-audit` - Delete request handling

### Reporting & Analysis
- `inventory-report` - Inventory reports
- `audit-query` - Audit log queries

### Testing & Verification
- `everything-test` - Everything connectivity test
- `snapshot-verify` - Snapshot integrity verification
- `release-check` - Pre-release checklist

### Documentation & Guidance
- `rules-vs-skills` - Rules vs Skills explanation

---

## Skills Status

### ✅ Complete (15 skills)
All skills now have comprehensive documentation with:
- Clear descriptions
- Detailed instructions
- Examples
- Integration points
- Troubleshooting

1. `agent-selector` - Comprehensive agent selection guide
2. `approval-gate` - Complete approval workflow
3. `audit-query` - Full audit query documentation
4. `ci-precommit` - Complete CI/Pre-commit setup guide (enhanced 2026-01-28)
5. `everything-provider-setup` - Complete setup guide
6. `everything-test` - Comprehensive testing guide
7. `inventory-report` - Detailed report generation
8. `plan-gated-apply` - Complete workflow documentation
9. `plan-validate` - Full validation guide
10. `quarantine-audit` - Complete quarantine workflow guide (enhanced 2026-01-28)
11. `release-check` - Complete pre-release checklist (enhanced 2026-01-28)
12. `repo-bootstrap` - Complete bootstrap guide (enhanced 2026-01-28)
13. `rules-vs-skills` - Comprehensive comparison guide
14. `snapshot-verify` - Complete verification guide
15. `tdd-go` - Full TDD workflow guide

---

## Alignment with Guide

### Skills in Guide (15)
All skills listed in `docs/AGENTS_AND_SKILLS_GUIDE.md` exist:
- ✅ `everything-provider-setup`
- ✅ `everything-test`
- ✅ `tdd-go`
- ✅ `plan-gated-apply`
- ✅ `plan-validate`
- ✅ `approval-gate`
- ✅ `inventory-report`
- ✅ `quarantine-audit`
- ✅ `snapshot-verify`
- ✅ `audit-query`
- ✅ `repo-bootstrap`
- ✅ `ci-precommit`
- ✅ `release-check`
- ✅ `agent-selector` - Agent selection guidance (added to guide 2026-01-28)
- ✅ `rules-vs-skills` - Rules vs Skills explanation (added to guide 2026-01-28)

### All Skills Documented
All 15 skills are now documented in `docs/AGENTS_AND_SKILLS_GUIDE.md` with usage guidance and examples.

---

## Enhancement History

### Completed (2026-01-28)
1. ✅ **`repo-bootstrap`** - Enhanced with detailed instructions, PowerShell examples, troubleshooting, integration points
2. ✅ **`ci-precommit`** - Enhanced with comprehensive setup guide, hook details, CI integration, troubleshooting
3. ✅ **`release-check`** - Enhanced with detailed checklist, validation script, success/failure outputs, troubleshooting
4. ✅ **`quarantine-audit`** - Enhanced with workflow examples, 30-day policy, audit trail, rollback process
5. ✅ Updated guide to include `agent-selector` and `rules-vs-skills` (2026-01-28)
6. ✅ Verified all 15 skills are documented in `docs/AGENTS_AND_SKILLS_GUIDE.md` (2026-01-28)

### All Skills Complete
All 15 skills now have comprehensive documentation. No further enhancements needed at this time.

---

## Quick Reference

### Skill Call Patterns
```bash
/use agent-selector          # Select appropriate agent
/use approval-gate           # Approval workflow
/use audit-query             # Query audit logs
/use ci-precommit            # CI/Pre-commit setup
/use everything-provider-setup  # Everything setup
/use everything-test         # Test Everything
/use inventory-report        # Generate reports
/use plan-gated-apply        # Plan→Approve→Apply
/use plan-validate           # Validate plan
/use quarantine-audit        # Handle deletes
/use release-check           # Pre-release checklist
/use repo-bootstrap          # Initialize repo
/use rules-vs-skills         # Rules vs Skills guide
/use snapshot-verify         # Verify snapshots
/use tdd-go                  # TDD cycle
```

### Skills by Workflow

**New Project Setup:**
```
repo-bootstrap → everything-provider-setup → ci-precommit
```

**File Organization:**
```
inventory-report → plan-gated-apply → verifier
```

**Development:**
```
tdd-go → implementer → verifier
```

**Release:**
```
release-check → reviewer → ci-precommit
```

---

## Notes

- All skills follow the standard SKILL.md format
- Skills are located in `.cursor/skills/<skill-name>/SKILL.md`
- Skills should be under 500 lines (most are well under)
- Skills should include: description, when to use, instructions, examples, integration points
- Enhanced skills include troubleshooting and best practices

---

## Related Documents
- `docs/AGENTS_AND_SKILLS_GUIDE.md` - Main guide (SSOT for documented skills)
- `docs/DEPENDENCY_MAP.md` - Skill dependencies
- `docs/WORKFLOW_EXAMPLES.md` - Usage examples
- `.cursor/agents/` - Agent definitions
