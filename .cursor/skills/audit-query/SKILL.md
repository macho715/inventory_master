---
name: audit-query
description: Query audit logs for operations history. Use to review past operations, track changes, and investigate issues.
---

# Audit Query

## When to Use
- 과거 작업 이력 조회
- 특정 작업 추적
- 문제 발생 시 원인 분석
- 감사 목적의 로그 검토

## Instructions
```bash
# 1. 전체 감사 로그 조회
cat _meta/audit/audit.jsonl

# 2. 특정 plan_id로 필터링
python -m inventory_master audit \
  --plan-id "2026-01-28T08:00:00+04:00__ROOT-A"

# 3. 날짜 범위로 필터링
python -m inventory_master audit \
  --from "2026-01-01" \
  --to "2026-01-31"

# 4. 작업 유형으로 필터링
python -m inventory_master audit \
  --action-type "move"

# 5. 실패한 작업만 조회
python -m inventory_master audit \
  --status "failed"
```

## Query Options
- By plan_id
- By date range
- By action type (move/rename/quarantine)
- By status (success/failed/rolled-back)
- By user/approver

## Output
- Filtered audit entries
- Operation summary
- Timeline visualization
- Failure analysis (if any)
- Statistics (total operations, success rate)

## Use Cases
- **Audit trail**: 모든 파일 이동 이력 확인
- **Troubleshooting**: 실패한 작업 원인 분석
- **Compliance**: 규정 준수 검증
- **Recovery**: 롤백 필요한 작업 식별
