---
name: plan-validate
description: Validate plan.json structure, policy compliance, and action safety. Use before approval to ensure plan is safe to execute.
---

# Plan Validate

## When to Use
- Plan 생성 후 검증
- 승인 전 안전성 확인
- Policy 준수 검증
- 충돌 및 위험 요소 탐지

## Instructions
```bash
# 1. Plan 구조 검증
python -m inventory_master validate \
  --plan "_meta/plans/plan_2026-01-28.json"

# 2. Policy 준수 확인
python -m inventory_master validate \
  --plan "_meta/plans/plan_2026-01-28.json" \
  --check-policy

# 3. 충돌 검사
python -m inventory_master validate \
  --plan "_meta/plans/plan_2026-01-28.json" \
  --check-conflicts

# 4. 위험 요소 탐지
python -m inventory_master validate \
  --plan "_meta/plans/plan_2026-01-28.json" \
  --check-risks
```

## Validation Checks
- Plan schema correctness (JSON structure)
- Policy compliance (allow_delete=false, max_actions, etc.)
- Path conflicts (destination already exists)
- Long paths (Windows 260 char limit)
- Invalid paths (non-existent sources)
- Circular dependencies
- Quarantine requirements (for delete requests)

## Output
- Validation status (valid/invalid)
- Policy violations (if any)
- Conflict list
- Risk assessment (Critical/High/Medium/Low)
- Recommendations for fixes

## Failure Cases
- Schema invalid → JSON 구조 오류 안내
- Policy violation → 정책 위반 항목 리스트
- Path conflict → 충돌 경로 및 해결 방법
- High risk → 승인 전 위험 요소 제거 권장
