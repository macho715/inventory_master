---
name: approval-gate
description: Manage approval workflow and validate approval tokens. Use to check approval status and manage human gate process.
---

# Approval Gate

## When to Use
- Plan 승인 상태 확인
- 승인 토큰 검증
- 승인 게이트 프로세스 관리
- 승인 이력 조회

## Instructions
```bash
# 1. 승인 상태 확인
python -m inventory_master approve \
  --status \
  --plan "_meta/plans/plan_2026-01-28.json"

# 2. 승인 토큰 검증
python -m inventory_master approve \
  --verify \
  --plan "_meta/plans/plan_2026-01-28.json"

# 3. 승인 이력 조회
python -m inventory_master approve \
  --history \
  --plan-id "2026-01-28T08:00:00+04:00__ROOT-A"

# 4. 승인 요청 (사용자만 가능)
python -m inventory_master approve \
  --plan "_meta/plans/plan_2026-01-28.json"
# → _meta/approvals/approval_<plan_id>.json 생성
```

## Approval Process
1) Plan validation (plan-validate skill)
2) Human review (사용자)
3) Approval token creation (사용자만 가능)
4) Token verification (approver agent)
5) Apply execution (executor agent)

## Output
- Approval status (approved/rejected/pending)
- Approval token path
- Approval timestamp
- Approver information
- Next steps

## Safety Rules
- **Human gate required**: 자동 승인 불가
- **Token required**: 승인 토큰 없이는 apply 불가
- **One-time use**: 승인 토큰은 한 번만 사용 가능
- **Non-transferable**: 승인 토큰은 plan_id에 고유

## Restrictions
- Agent는 승인 토큰 생성 불가 (사용자만 가능)
- Agent는 승인/거절 결정 불가 (사용자만 가능)
- Agent는 승인 상태 확인 및 검증만 가능
