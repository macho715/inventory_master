---
name: inventory-report
description: Generate read-only inventory reports with file statistics under _meta/reports/. Use for weekly/monthly audits, before planning tidy actions, or when analyzing repository structure.
---

# Inventory Report

## When to Use
- Regular audits (weekly/monthly)
- Before planning tidy actions
- Analyzing repository structure
- Understanding file distribution patterns
- Preparing for file organization

## Prerequisites
- `everything-provider-setup` skill (optional, for faster scanning)
- Root directory path available
- `_meta/reports/` directory exists (auto-created)

## Instructions

### Basic Usage
```bash
python -m inventory_master report --root "C:\inventory_master\"
```

### Output Location
Reports are automatically saved to:
```
_meta/reports/report_YYYY-MM-DD.md
```

### Command Details
- **Read-only**: No file modifications, only analysis
- **Provider**: Uses `LocalWalkProvider` (local file system scan)
- **Hash calculation**: Disabled for performance (hash_files=False)
- **Date-based naming**: Report filename includes date (YYYY-MM-DD)

## Report Contents

### Current Output
- **Total file count**: Number of files scanned
- **Top 30 extensions**: Most common file extensions with counts
- **Extension statistics**: Table format with extension and count

### Report Format
```markdown
# Report YYYY-MM-DD

- files: <total_count>

## Top extensions

| ext | count |
|---|---:|
| .py | 456 |
| .md | 234 |
| .json | 123 |
...
```

## Integration Points

### Works With
- **`everything-provider-setup`**: Optional, for faster Everything-based scanning
- **`planner` agent**: Uses report data to create organization plans
- **`explore` agent**: Analyzes report results for patterns
- **`plan-gated-apply` skill**: Report informs planning decisions

### Typical Workflow
```
everything-provider-setup (optional) 
  → inventory-report 
  → planner (creates plan.json)
  → plan-gated-apply
```

## Example Output

### Successful Execution
```
Report generated: _meta/reports/report_2026-01-28.md
- Total files: 1,234
- Top extensions: .py (456), .md (234), .json (123)
```

### Report File Location
The command prints the full path to the generated report:
```
_meta/reports/report_2026-01-28.md
```

## Use Cases

### Weekly Audit
```bash
# Generate weekly report
python -m inventory_master report --root "C:\inventory_master\"
# Review: _meta/reports/report_2026-01-28.md
```

### Before File Organization
```bash
# 1. Generate current state report
python -m inventory_master report --root "C:\inventory_master\"

# 2. Review report to understand structure

# 3. Create organization plan
python -m inventory_master plan --root "C:\inventory_master\"
```

## Notes

### Current Limitations
- Extension statistics only (top 30)
- No file size analysis (bigfiles)
- No age analysis (aging)
- Local scan only (no Everything integration yet)

### Future Enhancements
- Big file detection (largest files)
- File age analysis (oldest files)
- Everything provider integration for faster scanning
- Custom report formats

## Restrictions
- **Read-only**: No file modifications
- **No writes**: Only generates reports
- **Safe to run**: Can be executed anytime without risk

## Additional Resources
- For Everything integration: `everything-provider-setup` skill
- For planning: `planner` agent
- For file organization: `plan-gated-apply` skill
- For workflow examples: `docs/AGENTS_AND_SKILLS_GUIDE.md`
