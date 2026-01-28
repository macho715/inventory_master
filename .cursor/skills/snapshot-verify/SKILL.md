---
name: snapshot-verify
description: Verify snapshot integrity and hash consistency. Use after apply operations to ensure file integrity.
---

# Snapshot Verify

## When to Use
- Apply 작업 후 파일 무결성 검증
- 스냅샷 간 차이점 분석
- 해시 불일치 탐지

## Instructions
```bash
# 1. 스냅샷 디렉토리 확인
ls _meta/snapshots/

# 2. Before/After 스냅샷 비교
python -m inventory_master verify \
  --before "_meta/snapshots/before_<plan_id>.json" \
  --after "_meta/snapshots/after_<plan_id>.json"

# 3. 해시 검증
python -m inventory_master verify \
  --plan "_meta/plans/<plan_id>.json" \
  --verify-hash
```

## Verification Checks
- File existence (all files present)
- File size consistency
- Hash matches (SHA256)
- Path correctness
- Missing files detection
- Duplicate files detection

## Output
- Verification status (pass/fail)
- Mismatch details (if any)
- Missing files list
- Hash comparison results
- Rollback recommendations (if needed)

## Failure Handling
- Hash mismatch → 롤백 권장
- Missing files → 복구 절차 안내
- Size mismatch → 파일 손상 가능성 알림
