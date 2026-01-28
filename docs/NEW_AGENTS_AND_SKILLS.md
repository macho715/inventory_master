# 새로 추가된 Agents & Skills

> **작성일**: 2026-01-28  
> **최종 업데이트**: 2026-01-28  
> **목적**: agent.md의 요구사항에 따라 추가된 새로운 sub agents와 skills를 소개합니다. 현재 총 10개 agents와 15개 skills로 확장되었습니다.

---

## 📋 추가된 Agents (5개)

### 1. `researcher` - Everything 연동 전문가

**역할**: Everything 연동 방식 및 보안 제약 사항 문서화

**특징**:
- Read-only (실행 금지, 문서화만)
- Everything ES CLI / HTTP Server / SDK 가이드 작성
- 보안 정책 문서화
- Provider 우선순위 및 fallback 전략 정리

**사용 시점**:
- Everything 연동 방법을 문서화할 때
- 보안 정책을 정리할 때
- Provider 설정 가이드를 작성할 때

**파일**: `.cursor/agents/researcher.md`

---

### 2. `executor` - 트랜잭션 실행자

**역할**: 승인된 plan.json을 실제로 적용 (파일 이동/이름변경)

**특징**:
- Write 권한 (승인 후만 사용)
- 트랜잭션 원자적 적용 (all or nothing)
- Audit 로그 기록
- Before/After 스냅샷 생성
- 해시 검증 및 롤백 지원

**사용 시점**:
- 승인된 plan.json을 실제로 적용할 때
- 파일 이동/이름변경이 필요할 때

**안전 요구사항**:
- 승인 토큰 필수
- Dry-run 필수
- Pre/post 스냅샷 필수
- 해시 검증 필수

**파일**: `.cursor/agents/executor.md`

---

### 3. `qa` - 테스트 케이스 전문가

**역할**: 실패 케이스 및 edge case 테스트 작성

**특징**:
- Write 권한 (테스트 파일만)
- 실패 케이스 테스트 작성
- Edge case 시나리오 추가
- 통합 테스트 및 스모크 테스트

**테스트 카테고리**:
- 경로 충돌 (overwrite prevention)
- 파일 잠김 (permission errors)
- 긴 경로 (Windows 260 char limit)
- 네트워크 실패 (Everything connection)
- 디스크 공간 부족
- 잘못된 plan.json 구조

**사용 시점**:
- 새로운 실패 케이스를 발견했을 때
- Edge case 테스트가 필요할 때

**파일**: `.cursor/agents/qa.md`

---

### 4. `approver` - 승인 게이트 관리자

**역할**: 승인 게이트 프로세스 관리 및 승인 토큰 검증

**특징**:
- Read-only (승인 토큰 생성 불가)
- 승인 토큰 검증
- 승인 게이트 상태 확인
- 승인 이력 추적

**사용 시점**:
- Plan 승인 전 검증이 필요할 때
- 승인 토큰 유효성을 확인할 때

**제한사항**:
- 승인 토큰 생성 불가 (사용자만 가능)
- 승인/거절 결정 불가 (사용자만 가능)
- 검증 및 상태 확인만 가능

**파일**: `.cursor/agents/approver.md`

---

### 5. `coordinator` - 워크플로우 조정자

**역할**: 복잡한 워크플로우 조정 및 Agent/Skill 조합 관리

**특징**:
- Read-only (실제 실행은 사용자가 수행)
- Multi-agent 워크플로우 설계
- 의존성 순서 검증
- 워크플로우 단계별 가이드 제공

**사용 시점**:
- 복잡한 워크플로우가 필요할 때
- 여러 Agent/Skill을 순차적으로 사용해야 할 때
- 의존성 순서를 확인하고 싶을 때

**파일**: `.cursor/agents/coordinator.md`

---

## 📋 추가된 Skills (7개)

### 1. `everything-test` - Everything 연동 테스트

**역할**: Everything 연동 상태 확인 및 Provider 가용성 테스트

**기능**:
- ES CLI 테스트
- HTTP Server 테스트
- SDK 연결 테스트
- Fallback 권장사항 제공

**사용 시점**:
- Everything 연동 상태를 확인할 때
- Provider 가용성을 테스트할 때

**파일**: `.cursor/skills/everything-test/SKILL.md`

---

### 2. `snapshot-verify` - 스냅샷 검증

**역할**: 스냅샷 무결성 및 해시 일관성 검증

**기능**:
- Before/After 스냅샷 비교
- 해시 검증 (SHA256)
- 파일 존재 확인
- 크기 일관성 확인
- 누락/중복 파일 탐지

**사용 시점**:
- Apply 작업 후 파일 무결성 검증
- 스냅샷 간 차이점 분석

**파일**: `.cursor/skills/snapshot-verify/SKILL.md`

---

### 3. `audit-query` - 감사 로그 조회

**역할**: 감사 로그 조회 및 작업 이력 추적

**기능**:
- Plan ID로 필터링
- 날짜 범위로 필터링
- 작업 유형으로 필터링
- 상태별 필터링 (success/failed)
- 통계 및 타임라인 시각화

**사용 시점**:
- 과거 작업 이력 조회
- 문제 발생 시 원인 분석
- 감사 목적의 로그 검토

**파일**: `.cursor/skills/audit-query/SKILL.md`

---

### 4. `plan-validate` - Plan 검증

**역할**: plan.json 구조, 정책 준수, 안전성 검증

**기능**:
- Plan schema 검증
- Policy 준수 확인
- 경로 충돌 검사
- 위험 요소 탐지
- 긴 경로 검사

**사용 시점**:
- Plan 생성 후 검증
- 승인 전 안전성 확인

**파일**: `.cursor/skills/plan-validate/SKILL.md`

---

### 5. `approval-gate` - 승인 게이트 관리

**역할**: 승인 워크플로우 관리 및 승인 토큰 검증

**기능**:
- 승인 상태 확인
- 승인 토큰 검증
- 승인 이력 조회
- 승인 프로세스 안내

**사용 시점**:
- Plan 승인 상태 확인
- 승인 토큰 검증

**안전 규칙**:
- Human gate 필수 (자동 승인 불가)
- 토큰 필수 (승인 토큰 없이는 apply 불가)
- 일회용 (승인 토큰은 한 번만 사용)

**파일**: `.cursor/skills/approval-gate/SKILL.md`

---

### 6. `agent-selector` - Agent 선택 가이드

**역할**: 적절한 Agent 선택 및 Agent 역할 이해

**기능**:
- Agent capabilities matrix 제공
- Agent 선택 가이드
- Workflow patterns
- Decision tree

**사용 시점**:
- 어떤 Agent를 사용해야 할지 모를 때
- Agent 역할과 권한을 이해해야 할 때
- Multi-agent 워크플로우를 계획할 때

**파일**: `.cursor/skills/agent-selector/SKILL.md`

---

### 7. `rules-vs-skills` - Rules vs Skills 가이드

**역할**: Rules와 Skills의 차이 및 사용 시점 가이드

**기능**:
- Rules vs Skills 구분
- Decision matrix
- When to use each
- Migration guide

**사용 시점**:
- Rules와 Skills의 차이를 이해해야 할 때
- 새로운 가이드라인을 Rules에 넣을지 Skills에 넣을지 결정할 때
- 팀이 Rules vs Skills 구분에 혼란스러워할 때

**파일**: `.cursor/skills/rules-vs-skills/SKILL.md`

---

## 🔄 업데이트된 워크플로우

### 파일 정리 워크플로우 (개선됨)

```
1. inventory-report (현재 상태 파악)
   ↓
2. planner (plan.json 생성)
   ↓
3. plan-validate (Plan 검증) ← NEW
   ↓
4. approval-gate (승인 게이트) ← NEW
   ↓
5. plan-gated-apply (Dry-run)
   ↓
6. executor (실제 적용) ← NEW
   ↓
7. snapshot-verify (스냅샷 검증) ← NEW
   ↓
8. verifier (최종 검증)
```

### Everything 연동 워크플로우 (개선됨)

```
1. everything-provider-setup (설정)
   ↓
2. everything-test (연동 테스트) ← NEW
   ↓
3. researcher (문서화) ← NEW
   ↓
4. inventory-report (리포트 생성)
```

### 테스트 개발 워크플로우 (개선됨)

```
1. tdd-go (TDD 사이클)
   ↓
2. implementer (코드 구현)
   ↓
3. qa (테스트 케이스 추가) ← NEW
   ↓
4. verifier (검증)
```

---

## 📊 Agents & Skills 전체 목록

### Agents (10개)
1. `explore` - 코드베이스 탐색
2. `planner` - 계획 설계
3. `implementer` - 코드 구현
4. `reviewer` - 보안/품질 검토
5. `verifier` - 작업 검증
6. **`researcher`** - Everything 연동 문서화 (NEW)
7. **`executor`** - 트랜잭션 실행 (NEW)
8. **`qa`** - 테스트 케이스 작성 (NEW)
9. **`approver`** - 승인 게이트 관리 (NEW)
10. **`coordinator`** - 워크플로우 조정 (NEW)

### Skills (15개)
1. `everything-provider-setup` - Everything 설정
2. **`everything-test`** - Everything 테스트 (NEW)
3. `tdd-go` - TDD 사이클
4. `plan-gated-apply` - 안전한 적용
5. **`plan-validate`** - Plan 검증 (NEW)
6. **`approval-gate`** - 승인 게이트 (NEW)
7. `inventory-report` - 인벤토리 리포트
8. `quarantine-audit` - 격리 정책
9. **`snapshot-verify`** - 스냅샷 검증 (NEW)
10. **`audit-query`** - 감사 로그 조회 (NEW)
11. `repo-bootstrap` - 저장소 초기화
12. `ci-precommit` - CI/Pre-commit 설정
13. `release-check` - 릴리즈 체크
14. **`agent-selector`** - Agent 선택 가이드 (NEW)
15. **`rules-vs-skills`** - Rules vs Skills 가이드 (NEW)

---

## 🎯 주요 개선 사항

### 1. **안전성 강화**
- `plan-validate`: Plan 검증 추가
- `approval-gate`: 승인 게이트 명시적 관리
- `snapshot-verify`: 스냅샷 무결성 검증

### 2. **Everything 연동 개선**
- `researcher`: Everything 연동 문서화 전문가
- `everything-test`: 연동 테스트 자동화

### 3. **트랜잭션 실행 분리**
- `executor`: 파일 이동 실행 전용 agent
- `implementer`: 코드 구현 전용 agent
- 역할 명확화

### 4. **테스트 자동화**
- `qa`: 실패 케이스 테스트 자동 작성
- Edge case 커버리지 향상

### 5. **감사 및 추적**
- `audit-query`: 감사 로그 조회 기능
- 작업 이력 추적 강화

---

## 📚 관련 문서

- [`docs/AGENTS_AND_SKILLS_GUIDE.md`](AGENTS_AND_SKILLS_GUIDE.md) - 통합 사용 가이드 (업데이트됨)
- [`docs/DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md) - 의존성 맵
- [`docs/WORKFLOW_EXAMPLES.md`](WORKFLOW_EXAMPLES.md) - 실전 워크플로우 예시
- `agent.md` - SSOT (요구사항 출처)

---

## ✅ 체크리스트

새로운 agents와 skills 사용 전 확인:

- [ ] `researcher` - Everything 연동 문서화 필요 시
- [ ] `executor` - 파일 이동 실행 시 (승인 필수)
- [ ] `qa` - 테스트 케이스 추가 시
- [ ] `approver` - 승인 게이트 관리 시
- [ ] `everything-test` - Everything 연동 테스트 시
- [ ] `snapshot-verify` - 스냅샷 검증 시
- [ ] `audit-query` - 감사 로그 조회 시
- [ ] `plan-validate` - Plan 검증 시
- [ ] `approval-gate` - 승인 게이트 관리 시

---

> **요약**: agent.md의 요구사항에 따라 5개의 새로운 agents와 7개의 새로운 skills를 추가했습니다. 현재 총 10개 agents와 15개 skills로 확장되었습니다. 안전성, Everything 연동, 트랜잭션 실행, 테스트 자동화, 감사 추적, 워크플로우 조정 기능이 강화되었습니다.
