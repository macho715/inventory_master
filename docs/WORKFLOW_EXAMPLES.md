# 실전 워크플로우 예시

> **목적**: 실제 작업 시나리오에서 Agents와 Skills를 어떻게 사용하는지 구체적인 예시를 제공합니다.

---

## 📋 목차

1. [일일 작업 워크플로우](#일일-작업-워크플로우)
2. [주간 리포트 워크플로우](#주간-리포트-워크플로우)
3. [파일 정리 워크플로우](#파일-정리-워크플로우)
4. [TDD 개발 워크플로우](#tdd-개발-워크플로우)
5. [릴리즈 준비 워크플로우](#릴리즈-준비-워크플로우)
6. [문제 해결 워크플로우](#문제-해결-워크플로우)

---

## 일일 작업 워크플로우

### 시나리오: 아침에 프로젝트 상태 확인

**목표**: 오늘 작업할 항목 파악

**단계별 실행**:

```bash
# 1. 코드베이스 구조 확인 (explore agent 자동 호출)
# Cursor에서 프로젝트 열기 → explore agent가 자동으로 구조 파악

# 2. 현재 테스트 상태 확인
pytest -q

# 3. plan.md에서 다음 작업 확인
# plan.md 열기 → 다음 미체크 테스트 확인
```

**사용되는 Agent/Skill**:
- `explore` agent (자동)
- `tdd-go` skill (필요시)

**예상 결과**:
- ✅ 프로젝트 구조 파악
- ✅ 다음 작업 항목 확인
- ✅ 테스트 상태 확인

---

## 주간 리포트 워크플로우

### 시나리오: 매주 월요일 인벤토리 리포트 생성

**목표**: 주간 감사를 위한 리포트 생성

**단계별 실행**:

```bash
# 1. Everything 연동 설정
# Skill: everything-provider-setup
es.exe test
# 또는 HTTP Server 확인
curl http://localhost:8080/

# 2. Everything 연동 테스트 (권장)
# Skill: everything-test
# → ES CLI, HTTP Server, SDK 연결 테스트

# 3. 인벤토리 리포트 생성
# Skill: inventory-report
python -m inventory_master report --root "C:\inventory_master\"

# 4. 리포트 확인
# _meta/reports/ 디렉토리에서 최신 리포트 확인
```

**사용되는 Agent/Skill**:
- `everything-provider-setup` skill
- `everything-test` skill (권장)
- `inventory-report` skill
- `explore` agent (선택적, 리포트 분석)

**예상 결과**:
- ✅ `_meta/reports/report_YYYY-MM-DD.md` 생성
- ✅ 확장자 통계, 큰 파일 목록 확인
- ✅ 다음 정리 작업 계획 수립

**실제 출력 예시**:
```
Report generated: _meta/reports/report_2026-01-28.md
- Total files: 1,234
- Top extensions: .py (456), .md (234), .json (123)
- Largest files:
  1. data/archive.zip (500 MB)
  2. logs/app.log (200 MB)
```

---

## 파일 정리 워크플로우

### 시나리오: INBOX의 파일들을 적절한 폴더로 이동

**목표**: `00_INBOX/`의 파일들을 분류하여 이동

**단계별 실행**:

```bash
# 1. 현재 상태 파악
# Skill: inventory-report
python -m inventory_master report --root "C:\inventory_master\"

# 2. 계획 생성
# Agent: planner (자동 호출)
python -m inventory_master plan --root "C:\inventory_master\"
# → _meta/plans/plan_2026-01-28.json 생성

# 3. 계획 검증 (권장)
# Skill: plan-validate
python -m inventory_master validate --plan "_meta/plans/plan_2026-01-28.json"
# → Plan 구조, 정책 준수, 충돌 검사

# 4. 계획 검토
# planner agent가 생성한 plan.json 확인
cat _meta/plans/plan_2026-01-28.json

# 5. 승인 (Human Gate)
# Skill: approval-gate
python -m inventory_master approve --plan "_meta/plans/plan_2026-01-28.json"
# → _meta/approvals/APPROVED__<plan_id>.token 생성

# 6. Dry-run (필수)
# Skill: plan-gated-apply
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json" --dry-run
# → 변경 사항 미리보기, audit.jsonl에 기록

# 7. 실제 적용
# Agent: executor (자동 호출)
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json"
# → 파일 이동 실행, 스냅샷 생성

# 8. 스냅샷 검증 (권장)
# Skill: snapshot-verify
# → Before/After 스냅샷 비교, 해시 검증

# 9. 최종 검증
# Agent: verifier (자동 호출)
# → 스냅샷 비교, 해시 검증
```

**사용되는 Agent/Skill**:
- `inventory-report` skill
- `planner` agent
- `plan-validate` skill (권장)
- `approval-gate` skill
- `plan-gated-apply` skill
- `executor` agent
- `snapshot-verify` skill (권장)
- `quarantine-audit` skill (삭제가 필요한 경우)
- `verifier` agent

**예상 결과**:
- ✅ `00_INBOX/`의 파일들이 적절한 폴더로 이동
- ✅ `_meta/audit/audit.jsonl`에 작업 기록
- ✅ `_meta/snapshots/`에 before/after 스냅샷 저장
- ✅ 검증 완료

**주의사항**:
- ⚠️ 승인 없이는 apply 불가
- ⚠️ dry-run 없이는 apply 불가
- ⚠️ delete는 금지, `99_QUARANTINE/`으로 이동

---

## TDD 개발 워크플로우

### 시나리오: plan.md의 다음 테스트 구현

**목표**: TDD 사이클로 기능 구현

**단계별 실행**:

```bash
# 1. 사용자가 "go" 명령 실행
# Skill: tdd-go

# 2. plan.md에서 다음 미체크 테스트 선택
# 예: test: CLI report works on temp dir

# 3. RED: 실패하는 테스트 작성
# tests/test_cli_smoke.py에 테스트 추가
def test_cli_report_smoke():
    # 실패하는 테스트
    assert False  # 일단 실패

# 4. 테스트 실행 (실패 확인)
pytest tests/test_cli_smoke.py::test_cli_report_smoke -v
# → 실패 확인 (RED)

# 5. GREEN: 최소 구현
# Agent: implementer (자동 호출)
# src/inventory_master/cli.py에 최소 코드 추가
def report_command():
    return {"status": "ok"}  # 최소 구현

# 6. 테스트 실행 (통과 확인)
pytest tests/test_cli_smoke.py::test_cli_report_smoke -v
# → 통과 확인 (GREEN)

# 7. REFACTOR: 구조 개선 (행위 불변)
# 코드 구조 개선 (함수 추출, 변수명 개선 등)
# 테스트는 여전히 통과해야 함

# 8. 검증
# Agent: verifier (자동 호출)
pytest -q

# 9. plan.md 업데이트
# - [x] test: CLI report works on temp dir # passed @2026-01-28 <commit:abcd1234>
```

**사용되는 Agent/Skill**:
- `tdd-go` skill
- `implementer` agent
- `qa` agent (edge case 테스트 추가 시)
- `verifier` agent

**예상 결과**:
- ✅ 테스트 통과
- ✅ `plan.md` 업데이트
- ✅ 커밋 준비 완료

**TDD 사이클 요약**:
```
RED → GREEN → REFACTOR
 ↓      ↓        ↓
실패   통과    개선
```

---

## 릴리즈 준비 워크플로우

### 시나리오: v1.0.0 릴리즈 전 최종 검증

**목표**: 모든 품질 게이트 통과

**단계별 실행**:

```bash
# 1. 릴리즈 체크리스트 실행
# Skill: release-check

# 2. Coverage 확인 (≥ 85.00%)
pytest --cov=src --cov-report=term-missing
# → Coverage: 87.50% ✓

# 3. Lint/Format 검증
ruff check .
ruff format --check .
black --check .
isort --check-only .
# → 모두 통과 ✓

# 4. Security 스캔
bandit -q -r src
# → High: 0 ✓

pip-audit --strict
# → 취약점 없음 ✓

# 5. 보안/품질 검토
# Agent: reviewer (자동 호출)
# → Critical/High/Medium/Low 위험도 평가

# 6. 문서 업데이트 확인
# agent.md, constitution.md, README.md 확인

# 7. Pre-commit 최종 실행
# Skill: ci-precommit
pre-commit run --all-files
# → 모두 통과 ✓

# 8. 최종 검증
# Agent: verifier (자동 호출)
pytest -q
# → 모든 테스트 통과 ✓
```

**사용되는 Agent/Skill**:
- `release-check` skill
- `reviewer` agent
- `ci-precommit` skill
- `verifier` agent

**예상 결과**:
- ✅ Coverage ≥ 85.00%
- ✅ Lint/Format 경고 0
- ✅ Security 취약점 0
- ✅ 문서 업데이트 완료
- ✅ 릴리즈 준비 완료

**체크리스트**:
- [ ] Coverage ≥ 85.00%
- [ ] Lint/Format 경고 0
- [ ] Bandit High = 0
- [ ] pip-audit --strict 통과
- [ ] 문서 업데이트 완료
- [ ] Unsafe defaults 없음

---

## 문제 해결 워크플로우

### 시나리오 1: Everything 연동 실패

**문제**: `inventory-report` 실행 시 Everything을 찾을 수 없음

**해결 단계**:

```bash
# 1. Everything 실행 상태 확인
# Skill: everything-provider-setup
es.exe test
# → 오류: Everything을 찾을 수 없음

# 2. Everything 설치 확인
# C:\Program Files\Everything\es.exe 존재 확인

# 3. PATH 확인
$env:PATH
# → Everything 경로가 PATH에 있는지 확인

# 4. 수동 경로 지정 (임시)
python -m inventory_master report \
  --root "C:\inventory_master\" \
  --everything-path "C:\Program Files\Everything\es.exe"

# 5. Fallback: 로컬 스캔 사용
# Everything 없이도 로컬 스캐너로 동작
```

**사용되는 Agent/Skill**:
- `everything-provider-setup` skill
- `inventory-report` skill (fallback)

---

### 시나리오 2: Apply 실패 (승인 토큰 없음)

**문제**: `apply` 실행 시 승인 토큰이 없다는 오류

**해결 단계**:

```bash
# 1. 오류 확인
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json"
# → 오류: Approval token not found

# 2. Plan 확인
cat _meta/plans/plan_2026-01-28.json
# → plan_id 확인

# 3. Plan 검증 (권장)
# Skill: plan-validate
python -m inventory_master validate --plan "_meta/plans/plan_2026-01-28.json"

# 4. 승인 실행 (필수)
# Skill: approval-gate
python -m inventory_master approve --plan "_meta/plans/plan_2026-01-28.json"
# → _meta/approvals/APPROVED__<plan_id>.token 생성

# 5. Dry-run 실행 (필수)
# Skill: plan-gated-apply
python -m inventory_master apply \
  --plan "_meta/plans/plan_2026-01-28.json" \
  --dry-run

# 6. Apply 재시도
# Agent: executor
python -m inventory_master apply --plan "_meta/plans/plan_2026-01-28.json"
# → 성공
```

**사용되는 Agent/Skill**:
- `plan-validate` skill (권장)
- `approval-gate` skill
- `plan-gated-apply` skill
- `executor` agent

**주의사항**:
- ⚠️ 승인 없이는 apply 불가 (안전 정책)
- ⚠️ dry-run 없이는 apply 불가 (안전 정책)

---

### 시나리오 3: 테스트 실패

**문제**: `pytest` 실행 시 테스트 실패

**해결 단계**:

```bash
# 1. 실패한 테스트 확인
pytest -v
# → test_cli_report_smoke 실패

# 2. 상세 오류 확인
pytest tests/test_cli_smoke.py::test_cli_report_smoke -v
# → AssertionError 확인

# 3. 코드 확인
# Agent: explore (자동 호출)
# → 관련 코드 파일 확인

# 4. 수정
# Agent: implementer (승인 후)
# → 코드 수정

# 5. 재검증
# Agent: verifier (자동 호출)
pytest -q
# → 통과 확인
```

**사용되는 Agent/Skill**:
- `explore` agent
- `implementer` agent
- `verifier` agent

---

## 워크플로우 요약표

| 워크플로우 | 주요 Skill | 주요 Agent | 예상 소요 시간 |
|-----------|-----------|-----------|--------------|
| 일일 작업 | `tdd-go` | `explore` | 5-10분 |
| 주간 리포트 | `inventory-report` | - | 10-15분 |
| 파일 정리 | `plan-gated-apply` | `planner`, `verifier` | 30-60분 |
| TDD 개발 | `tdd-go` | `implementer`, `verifier` | 15-30분/테스트 |
| 릴리즈 준비 | `release-check` | `reviewer`, `verifier` | 1-2시간 |

---

## 빠른 참조

### 자주 사용하는 명령어

```bash
# 리포트 생성
python -m inventory_master report --root "C:\inventory_master\"

# 계획 생성
python -m inventory_master plan --root "C:\inventory_master\"

# 승인
python -m inventory_master approve --plan "_meta/plans/<plan>.json"

# Dry-run
python -m inventory_master apply --plan "_meta/plans/<plan>.json" --dry-run

# Apply
python -m inventory_master apply --plan "_meta/plans/<plan>.json"

# 테스트
pytest -q

# 릴리즈 체크
pytest --cov=src --cov-report=term-missing
ruff check .
bandit -q -r src
```

---

## 버전 정보

- **문서 버전**: v1.0
- **작성일**: 2026-01-28
- **관련 문서**: 
  - `docs/AGENTS_AND_SKILLS_GUIDE.md` (통합 가이드)
  - `docs/DEPENDENCY_MAP.md` (의존성 맵)

---

> **요약**: 실제 작업 시나리오에서 Agents와 Skills를 효과적으로 사용하는 방법을 구체적인 예시로 제공합니다. 각 워크플로우는 Plan→Approve→Apply 플로우를 준수합니다.
