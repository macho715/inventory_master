# inventory_master 프로젝트 전체 개발 플랜

> **작성일**: 2026-01-28  
> **버전**: v1.0  
> **목적**: `.cursor/agents/`와 `.cursor/skills/` 프로젝트의 전체 개발 계획 및 로드맵

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [현재 상태 분석](#현재-상태-분석)
3. [개발 목표 및 범위](#개발-목표-및-범위)
4. [아키텍처 설계](#아키텍처-설계)
5. [개발 계획](#개발-계획)
6. [테스트 전략](#테스트-전략)
7. [마일스톤](#마일스톤)
8. [리스크 및 대응 방안](#리스크-및-대응-방안)
9. [참고 문서](#참고-문서)

---

## 프로젝트 개요

### Mission
**Plan→Approve→Apply 기반의 안전한 폴더 정리 도구** 개발

- **Everything**: Read-only 인벤토리/검색 전용
- **Folder Tidy**: Plan→Approve→Apply 게이트 통과 필수
- **Safety First**: Write 기본 OFF, Delete 금지 (Quarantine 대체), Audit + Snapshots 필수

### 핵심 원칙
1. **Read-only 우선**: Everything은 조회 전용
2. **승인 게이트**: 모든 write 작업은 승인 필수
3. **트랜잭션 안전성**: Dry-run → 검증 → Apply → Verify
4. **감사 추적**: 모든 작업은 audit.jsonl에 기록
5. **롤백 가능**: Before/After 스냅샷으로 복구 가능

---

## 현재 상태 분석

### ✅ 완료된 항목

#### Agents (10개)
| Agent | 상태 | 설명 |
|-------|------|------|
| `approver` | ✅ | 승인 게이트 관리 |
| `coordinator` | ✅ | 복잡한 워크플로우 조정 |
| `executor` | ✅ | 파일 이동 실행 (승인 후) |
| `explore` | ✅ | 코드베이스 탐색 |
| `implementer` | ✅ | 코드 구현 (승인 후) |
| `planner` | ✅ | plan.json 설계 |
| `qa` | ✅ | 테스트 케이스 작성 |
| `researcher` | ✅ | Everything 연동 문서화 |
| `reviewer` | ✅ | 보안/품질 검토 |
| `verifier` | ✅ | 작업 검증 |

#### Skills (15개)
| Skill | 상태 | 설명 |
|-------|------|------|
| `agent-selector` | ✅ | Agent 선택 가이드 |
| `approval-gate` | ✅ | 승인 워크플로우 |
| `audit-query` | ✅ | 감사 로그 조회 |
| `ci-precommit` | ✅ | CI/Pre-commit 설정 |
| `everything-provider-setup` | ✅ | Everything 연동 설정 |
| `everything-test` | ✅ | Everything 연결 테스트 |
| `inventory-report` | ✅ | 인벤토리 리포트 생성 |
| `plan-gated-apply` | ✅ | Plan→Approve→Apply 워크플로우 |
| `plan-validate` | ✅ | Plan 검증 |
| `quarantine-audit` | ✅ | 삭제 요청 처리 (30일 정책) |
| `release-check` | ✅ | 릴리즈 전 체크리스트 |
| `repo-bootstrap` | ✅ | 저장소 초기화 |
| `rules-vs-skills` | ✅ | Rules vs Skills 가이드 |
| `snapshot-verify` | ✅ | 스냅샷 무결성 검증 |
| `tdd-go` | ✅ | TDD 사이클 실행 |

#### 문서화
- ✅ `agents.md` - SSOT 아키텍처 문서
- ✅ `docs/AGENTS_AND_SKILLS_GUIDE.md` - 통합 사용 가이드
- ✅ `docs/WORKFLOW_EXAMPLES.md` - 실전 워크플로우 예시
- ✅ `.cursor/skills/SKILLS_INVENTORY.md` - Skills 상태 추적

### ✅ 구현 완료된 항목 (2026-01-28)

#### 구현 코드
- ✅ `src/inventory_master/` - 핵심 기능 구현 완료
  - ✅ CLI 엔트리포인트 (`cli.py`) - report, plan, approve, apply 명령
  - ✅ Planner (`planner.py`) - Plan JSON 생성, 기본 quarantine 규칙
  - ✅ Executor (`executor.py`) - 트랜잭션 apply, dry-run, 승인 검증
  - ✅ Approval (`approve.py`) - 승인 토큰 생성
  - ✅ Audit (`audit.py`) - Append-only 감사 로그
  - ✅ Snapshot (`snapshot.py`) - Before/After 스냅샷 생성
  - ✅ Reporting (`reporting.py`) - 인벤토리 리포트 생성
  - ✅ Hashing (`hashing.py`) - SHA-256 스트리밍 해시
  - ✅ Meta Paths (`meta_paths.py`) - 메타 디렉토리 관리
  - ✅ Models (`models.py`) - 데이터 모델 (FileRecord, PlanAction)
  - ✅ LocalWalkProvider (`providers/local_walk.py`) - 로컬 파일 스캔 (fallback)
  - ✅ Provider Base (`providers/base.py`) - Provider 추상화 인터페이스
  - ⚠️ Everything ES Provider (`providers/everything_es.py`) - 기본 구조만 (미완성)

#### 테스트
- ✅ `tests/` - 기본 테스트 구현 완료
  - ✅ `test_scaffold.py` - 프로젝트 구조 확인
  - ✅ `test_cli_smoke.py` - CLI report 명령 테스트
  - ✅ `test_planner.py` - Plan 생성 테스트
  - ✅ `test_executor.py` - Apply 승인 및 dry-run 테스트
  - ✅ `test_snapshot.py` - 스냅샷 해시 검증 테스트
  - ✅ 6개 테스트 모두 통과 (100%)

#### 통합
- ✅ Local Batch Scanner (fallback) - 구현 완료
- ⚠️ Everything ES Provider - 기본 구조만 (미완성)
- ⚠️ HTTP Server Provider - 미구현
- ⚠️ SDK Provider - 미구현

---

## 개발 목표 및 범위

### Phase 1: 핵심 인프라 (Foundation)
**목표**: 기본 구조 및 안전 메커니즘 구축

1. **프로젝트 스캐폴딩**
   - 폴더 구조 생성 (`repo-bootstrap` skill 활용)
   - 메타 디렉토리 초기화 (`_meta/*`)
   - 기본 설정 파일 생성

2. **CLI 엔트리포인트**
   - `report` 명령 (read-only)
   - `plan` 명령 (plan.json 생성)
   - `approve` 명령 (승인 토큰 생성)
   - `apply` 명령 (dry-run + 실제 적용)
   - `verify` 명령 (스냅샷 검증)

3. **Everything Provider 통합**
   - ES CLI Provider (우선순위 1)
   - Local Batch Scanner (fallback)
   - Provider 추상화 인터페이스

### Phase 2: 핵심 기능 (Core Features)
**목표**: Plan→Approve→Apply 워크플로우 완성

1. **Planner 구현**
   - 분류 규칙 엔진
   - Plan.json 생성
   - 충돌 검사
   - Pre-check (exists, size, hash)

2. **Executor 구현**
   - 트랜잭션 Apply
   - Dry-run 모드
   - Before/After 스냅샷
   - Audit 로그 기록
   - 롤백 메커니즘

3. **Approval Gate**
   - 승인 토큰 생성/검증
   - 승인 상태 추적
   - 승인 만료 정책

### Phase 3: 고급 기능 (Advanced Features)
**목표**: 리포트, 검증, 통합 강화

1. **리포트 시스템**
   - 인벤토리 리포트 (aging, bigfiles, ext stats)
   - Audit 쿼리
   - 스냅샷 비교 리포트

2. **검증 시스템**
   - 스냅샷 무결성 검증
   - 해시 검증
   - Edge case 탐지 (경로 충돌, 파일 잠김, 긴 경로)

3. **Everything Provider 확장**
   - HTTP Server Provider (read-only, 로컬 바인딩)
   - SDK Provider (선택적)

### Phase 4: 품질 및 안정성 (Quality & Stability)
**목표**: 테스트 커버리지, CI/CD, 문서화 완성

1. **테스트 커버리지**
   - Unit 테스트 (≥85%)
   - Integration 테스트
   - Edge case 테스트
   - E2E 워크플로우 테스트

2. **CI/CD 파이프라인**
   - Pre-commit hooks
   - GitHub Actions
   - 자동화된 품질 게이트

3. **문서화 완성**
   - API 문서
   - 사용자 가이드
   - 개발자 가이드
   - 트러블슈팅 가이드

---

## 아키텍처 설계

### 레이어 구조

```
┌─────────────────────────────────────────────────────────┐
│ Layer 7: UI/승인 (Approval Gate)                         │
│   - 승인 토큰 생성/검증                                   │
│   - 승인 상태 추적                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 6: 증적 (Audit & Snapshots)                       │
│   - audit.jsonl (append-only)                           │
│   - snapshots/ (before/after)                            │
│   - approvals/ (승인 토큰)                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 5: 실행 (Executor - Transactional)                │
│   - Dry-run                                              │
│   - 트랜잭션 Apply                                        │
│   - 롤백 메커니즘                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 4: 계획 (Planner)                                  │
│   - 분류 규칙 엔진                                        │
│   - plan.json 생성                                        │
│   - 충돌 검사                                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: 분석 (Read-only Analysis)                      │
│   - Scanner/Profiler                                     │
│   - 리포트 생성                                           │
│   - 통계 계산                                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: 검색/인벤토리 (Search/Inventory)               │
│   - Everything Provider (ES/HTTP/SDK)                    │
│   - Local Batch Scanner (fallback)                       │
│   - Provider 추상화                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 1: 파일 시스템 (File System)                      │
│   - Windows 파일 시스템                                  │
│   - Everything (선택적)                                    │
└─────────────────────────────────────────────────────────┘
```

### 컴포넌트 상세

#### 1. Provider Layer
```python
# src/inventory_master/providers/base.py
class Provider(ABC):
    """Provider 추상화 인터페이스"""
    
    @abstractmethod
    def search(self, query: str) -> List[FileInfo]:
        """파일 검색 (read-only)"""
        pass
    
    @abstractmethod
    def list_files(self, root: Path) -> List[FileInfo]:
        """파일 목록 조회 (read-only)"""
        pass

# src/inventory_master/providers/es_cli.py
class ESCLIProvider(Provider):
    """Everything ES CLI Provider (우선순위 1)"""
    pass

# src/inventory_master/providers/local.py
class LocalScannerProvider(Provider):
    """Local Batch Scanner Provider (fallback)"""
    pass
```

#### 2. Planner
```python
# src/inventory_master/planner.py
class Planner:
    """Plan.json 생성 및 검증"""
    
    def generate_plan(
        self,
        root: Path,
        rules: List[ClassificationRule],
        policy: PlanPolicy
    ) -> Plan:
        """Plan 생성"""
        pass
    
    def validate_plan(self, plan: Plan) -> ValidationResult:
        """Plan 검증"""
        pass
```

#### 3. Executor
```python
# src/inventory_master/executor.py
class Executor:
    """트랜잭션 Apply 실행"""
    
    def apply(
        self,
        plan: Plan,
        approval_token: str,
        dry_run: bool = True
    ) -> ApplyResult:
        """Apply 실행 (dry-run 또는 실제)"""
        pass
    
    def rollback(self, snapshot_id: str) -> RollbackResult:
        """롤백 실행"""
        pass
```

#### 4. Audit System
```python
# src/inventory_master/audit.py
class AuditLogger:
    """감사 로그 기록 (append-only)"""
    
    def log_operation(self, operation: Operation) -> None:
        """작업 기록"""
        pass
```

#### 5. Snapshot System
```python
# src/inventory_master/snapshot.py
class SnapshotManager:
    """Before/After 스냅샷 관리"""
    
    def create_snapshot(self, root: Path) -> Snapshot:
        """스냅샷 생성"""
        pass
    
    def verify_snapshot(self, snapshot_id: str) -> VerificationResult:
        """스냅샷 검증"""
        pass
```

---

## 개발 계획

### Phase 1: 핵심 인프라 (Week 1-2)

#### Week 1: 프로젝트 스캐폴딩 및 CLI
- [ ] Day 1-2: 프로젝트 구조 생성
  - `repo-bootstrap` skill 활용
  - 폴더 구조 생성 (`00_INBOX/`, `_meta/*` 등)
  - 기본 설정 파일 생성
  
- [ ] Day 3-4: CLI 엔트리포인트 구현
  - `cli.py` 기본 구조
  - `report` 명령 (read-only, Local Scanner)
  - 기본 에러 핸들링
  
- [ ] Day 5: 테스트 작성
  - `test_cli_smoke.py` - CLI 기본 동작 테스트
  - `test_scaffold.py` - 프로젝트 구조 테스트

#### Week 2: Everything Provider 통합
- [ ] Day 1-2: Provider 추상화 인터페이스
  - `Provider` ABC 정의
  - `FileInfo` 데이터 클래스
  
- [ ] Day 3-4: ES CLI Provider 구현
  - `es_cli.py` 구현
  - Everything 실행 상태 확인
  - 쿼리 실행 및 파싱
  
- [ ] Day 5: Local Scanner Provider 구현
  - `local.py` 구현 (fallback)
  - 디렉토리 재귀 스캔
  - Provider 선택 로직

### Phase 2: 핵심 기능 (Week 3-4)

#### Week 3: Planner 구현
- [ ] Day 1-2: 분류 규칙 엔진
  - `ClassificationRule` 정의
  - 규칙 매칭 로직
  
- [ ] Day 3-4: Plan 생성
  - `plan.json` 스키마 정의
  - Plan 생성 로직
  - Pre-check (exists, size, hash)
  
- [ ] Day 5: 충돌 검사 및 검증
  - 경로 충돌 탐지
  - `plan-validate` skill 통합

#### Week 4: Executor 구현
- [ ] Day 1-2: 트랜잭션 Apply
  - Dry-run 모드
  - 실제 Apply (move, rename)
  - 원자적 커밋
  
- [ ] Day 3: 스냅샷 시스템
  - Before 스냅샷 생성
  - After 스냅샷 생성
  - 스냅샷 비교
  
- [ ] Day 4: Audit 시스템
  - `audit.jsonl` 기록
  - Append-only 보장
  
- [ ] Day 5: 롤백 메커니즘
  - 롤백 로직
  - 스냅샷 기반 복구

### Phase 3: 고급 기능 (Week 5-6)

#### Week 5: Approval Gate 및 리포트
- [ ] Day 1-2: Approval Gate
  - 승인 토큰 생성/검증
  - 승인 상태 추적
  - `approval-gate` skill 통합
  
- [ ] Day 3-4: 리포트 시스템
  - 인벤토리 리포트 (aging, bigfiles, ext stats)
  - `inventory-report` skill 통합
  
- [ ] Day 5: Audit 쿼리
  - `audit-query` skill 통합
  - 로그 필터링 및 검색

#### Week 6: 검증 및 Everything 확장
- [ ] Day 1-2: 검증 시스템
  - 스냅샷 무결성 검증
  - 해시 검증
  - `snapshot-verify` skill 통합
  
- [ ] Day 3-4: Edge case 처리
  - 경로 충돌 처리
  - 파일 잠김 처리
  - 긴 경로 처리 (Windows 260자 제한)
  
- [ ] Day 5: Everything Provider 확장 (선택적)
  - HTTP Server Provider (read-only, 로컬 바인딩)
  - SDK Provider (선택적)

### Phase 4: 품질 및 안정성 (Week 7-8)

#### Week 7: 테스트 커버리지
- [ ] Day 1-2: Unit 테스트 확장
  - Planner 테스트
  - Executor 테스트
  - Provider 테스트
  
- [ ] Day 3-4: Integration 테스트
  - End-to-end 워크플로우 테스트
  - Edge case 테스트
  
- [ ] Day 5: 테스트 커버리지 확인
  - `pytest --cov` 실행
  - 커버리지 ≥85% 달성

#### Week 8: CI/CD 및 문서화
- [ ] Day 1-2: CI/CD 파이프라인
  - `ci-precommit` skill 활용
  - GitHub Actions 설정
  - 자동화된 품질 게이트
  
- [ ] Day 3-4: 문서화 완성
  - API 문서
  - 사용자 가이드
  - 개발자 가이드
  
- [ ] Day 5: 릴리즈 준비
  - `release-check` skill 실행
  - 최종 검증

---

## 테스트 전략

### 테스트 피라미드

```
        ┌─────────────┐
        │   E2E Tests  │  (핵심 워크플로우만)
        │   (5-10%)   │
        └─────────────┘
              ↓
        ┌─────────────┐
        │ Integration │  (컴포넌트 간 통합)
        │   (15-20%)  │
        └─────────────┘
              ↓
        ┌─────────────┐
        │  Unit Tests  │  (대부분의 테스트)
        │   (70-80%)  │
        └─────────────┘
```

### 테스트 범주

#### 1. Unit Tests
- **Planner**: 분류 규칙, Plan 생성, 충돌 검사
- **Executor**: 트랜잭션 Apply, 롤백
- **Provider**: ES CLI, Local Scanner
- **Audit**: 로그 기록, 쿼리
- **Snapshot**: 생성, 검증

#### 2. Integration Tests
- **Plan→Approve→Apply 워크플로우**
- **Provider 선택 및 fallback**
- **스냅샷 기반 롤백**

#### 3. E2E Tests
- **전체 워크플로우**: Report → Plan → Approve → Apply → Verify
- **Edge Cases**: 경로 충돌, 파일 잠김, 긴 경로

### 테스트 목표

- **커버리지**: ≥85%
- **실행 시간**: 전체 테스트 ≤5분
- **안정성**: 모든 테스트 통과 필수

---

## 마일스톤

### Milestone 1: Foundation (Week 2)
**목표**: 기본 인프라 구축 완료

- ✅ 프로젝트 구조 생성
- ✅ CLI 엔트리포인트 구현
- ✅ Everything Provider 통합 (ES CLI + Local fallback)
- ✅ 기본 테스트 작성

**검증 기준**:
- `python -m inventory_master report --root "C:\inventory_master\"` 실행 성공
- 기본 테스트 통과

### Milestone 2: Core Workflow (Week 4)
**목표**: Plan→Approve→Apply 워크플로우 완성

- ✅ Planner 구현
- ✅ Executor 구현
- ✅ Approval Gate 구현
- ✅ Audit/Snapshot 시스템

**검증 기준**:
- `plan → approve → apply` 워크플로우 성공
- Dry-run 및 실제 Apply 동작 확인
- 스냅샷 및 Audit 로그 생성 확인

### Milestone 3: Advanced Features (Week 6)
**목표**: 리포트 및 검증 시스템 완성

- ✅ 리포트 시스템
- ✅ 검증 시스템
- ✅ Edge case 처리

**검증 기준**:
- 인벤토리 리포트 생성 성공
- 스냅샷 검증 동작 확인
- Edge case 테스트 통과

### Milestone 4: Production Ready (Week 8)
**목표**: 품질 및 안정성 확보

- ✅ 테스트 커버리지 ≥85%
- ✅ CI/CD 파이프라인 구축
- ✅ 문서화 완성

**검증 기준**:
- `pytest --cov` 커버리지 ≥85%
- CI 파이프라인 통과
- `release-check` skill 통과

---

## 리스크 및 대응 방안

### 기술적 리스크

| 리스크 | 영향도 | 확률 | 대응 방안 |
|--------|--------|------|-----------|
| Everything 미실행 | High | Medium | Local Scanner fallback 구현 |
| Windows 경로 제한 (260자) | Medium | High | 경로 검증 및 에러 처리 |
| 파일 잠김 (다른 프로세스 사용 중) | Medium | Medium | 재시도 로직 및 에러 처리 |
| 대량 파일 처리 성능 | Low | Low | 배치 처리 및 진행률 표시 |
| 트랜잭션 롤백 실패 | High | Low | 스냅샷 기반 복구 메커니즘 |

### 프로세스 리스크

| 리스크 | 영향도 | 확률 | 대응 방안 |
|--------|--------|------|-----------|
| 테스트 커버리지 미달 | Medium | Medium | TDD 방식으로 개발, 지속적 모니터링 |
| 문서화 부족 | Low | Medium | 문서화를 개발과 병행 |
| 일정 지연 | Medium | Medium | 우선순위 조정, MVP 먼저 |

---

## 참고 문서

### SSOT 문서
- `agents.md` - 아키텍처 SSOT
- `docs/constitution.md` - Non-negotiables
- `plan.md` - TDD 테스트 계획 (SoT)

### 가이드 문서
- `docs/AGENTS_AND_SKILLS_GUIDE.md` - Agents & Skills 통합 사용 가이드
- `docs/WORKFLOW_EXAMPLES.md` - 실전 워크플로우 예시
- `docs/DEPENDENCY_MAP.md` - 의존성 맵

### Agent/Skill 정의
- `.cursor/agents/*.md` - Agent 정의
- `.cursor/skills/*/SKILL.md` - Skill 정의
- `.cursor/skills/SKILLS_INVENTORY.md` - Skills 상태 추적

### 외부 문서
- Everything ES CLI: https://www.voidtools.com/support/everything/command_line_interface/
- Everything HTTP Server: https://www.voidtools.com/support/everything/http/
- Everything SDK: https://www.voidtools.com/support/everything/sdk/

---

## 다음 단계

1. **즉시 시작**: `plan.md`의 첫 번째 테스트부터 TDD 사이클 시작
2. **우선순위**: Phase 1 (핵심 인프라)부터 순차적으로 진행
3. **검증**: 각 마일스톤마다 검증 기준 확인

---

**문서 버전**: v1.0  
**최종 업데이트**: 2026-01-28  
**작성자**: AI Assistant (Cursor IDE)
