# Agents & Skills 의존성 맵

> **목적**: Agents와 Skills 간의 의존성 관계와 호출 순서를 시각화합니다.

---

## 전체 의존성 그래프

### 텍스트 기반 그래프

```
┌─────────────────────────────────────────────────────────────┐
│                    개발 워크플로우                            │
└─────────────────────────────────────────────────────────────┘

explore → planner → plan-gated-apply → implementer → verifier
  ↓         ↓            ↓                ↓            ↓
구조파악  계획설계    승인게이트      코드구현    검증


┌─────────────────────────────────────────────────────────────┐
│                  리포트 생성 워크플로우                       │
└─────────────────────────────────────────────────────────────┘

everything-provider-setup → inventory-report
        ↓
   Everything 연동 확인


┌─────────────────────────────────────────────────────────────┐
│                  초기 설정 워크플로우                         │
└─────────────────────────────────────────────────────────────┘

repo-bootstrap → ci-precommit → release-check
     ↓              ↓              ↓
  폴더구조      품질게이트      릴리즈체크


┌─────────────────────────────────────────────────────────────┐
│                안전한 파일 이동 워크플로우                    │
└─────────────────────────────────────────────────────────────┘

plan-gated-apply → quarantine-audit (필요시)
        ↓
   Plan→Approve→Apply


┌─────────────────────────────────────────────────────────────┐
│                    TDD 개발 워크플로우                        │
└─────────────────────────────────────────────────────────────┘

tdd-go → plan.md → implementer → verifier
   ↓        ↓          ↓           ↓
 TDD루프  테스트큐   최소구현    검증
```

---

## 상세 의존성 테이블

### Agents 의존성

| Agent | 의존하는 Agent | 의존하는 Skill | 호출 시점 |
|-------|---------------|---------------|-----------|
| `explore` | - | - | 코드베이스 탐색 시작 시 |
| `planner` | `explore` (선택) | `inventory-report` (선택) | 계획 설계 전 |
| `implementer` | `planner` | `tdd-go`, `plan-gated-apply` | 승인 후 구현 시 |
| `reviewer` | - | `ci-precommit`, `release-check` | 검토 필요 시 |
| `verifier` | `implementer` | - | 작업 완료 후 |

### Skills 의존성

| Skill | 의존하는 Agent | 의존하는 Skill | 필수 전제 조건 |
|-------|---------------|---------------|----------------|
| `everything-provider-setup` | - | - | Everything 설치 |
| `tdd-go` | `implementer` | - | `plan.md` 존재 |
| `plan-gated-apply` | `planner` | - | `plan.json` 생성 |
| `inventory-report` | - | `everything-provider-setup` | Everything 연동 |
| `quarantine-audit` | - | `plan-gated-apply` | Plan 승인 완료 |
| `repo-bootstrap` | - | - | - |
| `ci-precommit` | - | - | Python 환경 |
| `release-check` | `reviewer` | `ci-precommit` | 모든 테스트 통과 |

---

## 호출 순서 가이드

### 1. 새 프로젝트 초기화

```
1. repo-bootstrap
   ↓
2. everything-provider-setup
   ↓
3. ci-precommit
   ↓
4. explore (자동)
```

### 2. 주간 리포트 생성

```
1. everything-provider-setup (확인)
   ↓
2. inventory-report
   ↓
3. explore (선택적, 분석용)
```

### 3. 파일 정리 (Plan→Approve→Apply)

```
1. inventory-report
   ↓
2. planner
   ↓
3. plan-gated-apply
   ├─ 3-1. Plan 생성
   ├─ 3-2. Approve (Human Gate)
   ├─ 3-3. Dry-run
   └─ 3-4. Apply
   ↓
4. quarantine-audit (필요시)
   ↓
5. verifier
```

### 4. TDD 개발 사이클

```
1. tdd-go
   ├─ RED: 테스트 작성
   ├─ GREEN: 최소 구현
   └─ REFACTOR: 구조 개선
   ↓
2. implementer (자동 호출)
   ↓
3. verifier
   ↓
4. plan.md 업데이트
```

### 5. 릴리즈 전 검증

```
1. release-check
   ↓
2. reviewer
   ↓
3. ci-precommit (재실행, 필요시)
```

---

## 순환 의존성 체크

### ✅ 순환 의존성 없음

모든 의존성은 단방향이며, 순환 참조가 없습니다.

### 의존성 깊이

| 경로 | 깊이 | 설명 |
|------|------|------|
| `explore → planner → plan-gated-apply → implementer → verifier` | 5 | 최대 깊이 |
| `everything-provider-setup → inventory-report` | 2 | 리포트 생성 |
| `repo-bootstrap → ci-precommit → release-check` | 3 | 초기 설정 |

---

## 병렬 실행 가능한 작업

다음 작업들은 의존성이 없어 병렬 실행 가능합니다:

- `explore` + `everything-provider-setup`
- `repo-bootstrap` + `everything-provider-setup`
- `inventory-report` + `ci-precommit` (초기 설정 후)

---

## 의존성 위반 시 영향

### ❌ `inventory-report`를 `everything-provider-setup` 없이 실행
- **영향**: Everything 미연동 시 로컬 스캔으로 fallback (느림)
- **해결**: `everything-provider-setup` 먼저 실행

### ❌ `plan-gated-apply`를 `planner` 없이 실행
- **영향**: `plan.json`이 없어 실행 불가
- **해결**: `planner` agent로 plan 생성 후 실행

### ❌ `implementer`를 승인 없이 실행
- **영향**: 안전 정책 위반, 작업 거부
- **해결**: `plan-gated-apply`의 approve 단계 필수

### ❌ `release-check`를 `ci-precommit` 없이 실행
- **영향**: Pre-commit 훅 미설치로 일부 검사 실패
- **해결**: `ci-precommit` 먼저 실행

---

## 의존성 해결 전략

### 자동 해결
- Cursor가 Agent/Skill 호출 시 자동으로 의존성 확인
- 필수 전제 조건이 없으면 경고 표시

### 수동 해결
1. 의존성 맵 확인
2. 필수 전제 조건 실행
3. 원하는 작업 재시도

---

## 버전 정보

- **문서 버전**: v1.0
- **작성일**: 2026-01-28
- **관련 문서**: 
  - `docs/AGENTS_AND_SKILLS_GUIDE.md` (통합 가이드)
  - `.cursor/agents/*.md` (Agent 정의)
  - `.cursor/skills/*/SKILL.md` (Skill 정의)

---

> **요약**: 의존성 순서를 준수하면 안전하고 효율적으로 작업할 수 있습니다. 순환 의존성은 없으며, 모든 경로는 단방향입니다.
