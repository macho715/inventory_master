# agent.md — Local Repo Folder-Tidy (Everything Read-only + Plan→Approve→Apply)

Last updated: 2026-01-28 (TZ=Asia/Dubai)

> 당신은 이 리포지토리에서 작업하는 **자율 코딩 에이전트**다.
> 목표: **로컬 저장소 파일 정리 프로그램**을 "사고 없이" 완성한다.
> 충돌 시 우선순위: **사용자 요청 > agent.md > 기타 문서/코드 주석**.

---

## 0) 미션 / 불변조건 (Non-negotiables)

### Mission

- **Everything는 인벤토리/검색(Read-only) 전용**으로만 사용한다.
- **폴더 정리(write: move/rename/delete)** 는 반드시 **Plan→승인→Apply**로 분리한다.
- "사용자 최소 개입"을 목표로 하되, **승인 게이트(사람 승인)** 는 절대 우회하지 않는다.

### Non-negotiables (절대 금지/필수)

- 기본값: **write 동작 OFF**
- Apply 실행 전 필수:
  1) `dry-run` diff 출력
  2) `pre/post` 검증(존재성·크기·해시)
  3) `audit.jsonl` + `snapshots/` 증적 생성
- delete 기본 OFF: 삭제 대신 **99_QUARANTINE** 격리 후 **수동 삭제(최소 30일)** 권장.
- HTTP Server는 **조회(Read-only)** 로만 사용하고, **다운로드 노출 위험을 최소화**한다(가능하면 비활성화/로컬 바인딩).

---

## 1) 범위 / 운영 모델

### 운영 모델(핵심)

- **Inventory/Search**: Everything Provider(ES/HTTP/SDK)로 "파일 목록/메타"만 획득
- **Read-only 분석**: aging, bigfiles, ext stats 등 리포트 생성
- **Plan-Gated Actions**: Planner가 plan.json 생성 → Human 승인 → Executor가 안전 적용

### OS 범위

- 1차 목표: Windows + Everything
- 2차(가정): macOS/Linux는 Everything 없이 **로컬 스캐너(배치)** 로 동일 플로우 유지

---

## 2) 아키텍처(레이어)

| No | Layer            | Component                         | 역할               | 리스크                           | 통제(필수)                       |
| -: | ---------------- | --------------------------------- | ------------------ | -------------------------------- | -------------------------------- |
|  1 | Search/Inventory | Everything Provider (ES/HTTP/SDK) | 초고속 조회        | Everything 미실행 시 데이터 공백 | Provider fallback(배치 스캔)     |
|  2 | Read-only 분석   | Scanner/Profiler                  | 통계·리포트       | 실시간 watch는 IO 폭주           | watch 기본 OFF, 배치만           |
|  3 | 계획             | Planner                           | plan.json 생성     | 오분류/과잉 액션                 | max_actions, 규칙 테스트         |
|  4 | 실행             | Executor(Transactional)           | 승인된 plan만 적용 | 대량 이동 사고                   | dry-run + 검증 + 원자적 commit   |
|  5 | 증적             | Audit & Snapshots                 | 감사/복구 근거     | 로그 없으면 복구 불가            | append-only audit + before/after |
|  6 | UI/승인          | Approve Gate                      | 승인/거절          | 승인 우회 취약점                 | 승인 없으면 apply 금지           |
|  7 | 보안             | HTTP 제한                         | 원격 조회          | 인덱스/파일 노출                 | 조회 전용, 로컬 바인딩/인증      |

---

## 3) SSOT 디렉토리 구조(원본과 메타 분리)

```text
ROOT/
  00_INBOX/
  10_WORK/
  20_DEV/
  90_ARCHIVE/
  99_QUARANTINE/
  _meta/
    inventory/      # inventory_YYYY-MM-DD.jsonl
    reports/        # report_YYYY-MM-DD.md + .csv
    plans/          # plan_YYYY-MM-DD.json (불변)
    audit/          # audit.jsonl (append-only)
    snapshots/      # before/after manifest
```

## 4) Provider 우선순위(Everything 연동)

### ES CLI Provider (권장 1순위: 배치/가장 안정)

- 사용처: 주간/월간 리포트(쿼리→CSV/JSON 저장)
- 전제: Everything 실행 필요

### HTTP Server Provider (권장 2순위: 조회 API)

- 사용처: 모바일/원격에서 "조회만"
- 보안: 노출면이 커지므로 로컬 바인딩 + 인증 + 다운로드 차단이 원칙

### SDK Provider (권장 3순위: 앱 내장/고성능)

- 사용처: GUI/서비스에 내장
- 전제: Everything 백그라운드 실행

---

## 5) Plan JSON 스키마(SSOT)

- plan은 "제안서"이며, 승인 없이는 apply 불가
- 정책은 엄격 기본값 유지(allow_delete=false)

```json
{
  "plan_id": "2026-01-28T08:00:00+04:00__ROOT-A",
  "policy": {
    "allow_delete": false,
    "require_hash_verify": true,
    "require_dry_run": true,
    "max_actions": 200
  },
  "actions": [
    {
      "id": "A-001",
      "type": "move",
      "src": "ROOT/00_INBOX/file1.pdf",
      "dst": "ROOT/10_WORK/HVDC/file1.pdf",
      "precheck": {"exists": true, "size_bytes": 1234567},
      "postcheck": {"exists": true, "size_bytes": 1234567}
    }
  ]
}
```

---

## 6) 실행 규칙(Executor: Transactional Apply)

### Transaction 원칙(필수)

- move = copy → verify(size/hash) → rename/commit → (optional) src cleanup
- 실패 시: 부분 적용 금지, 즉시 롤백(또는 quarantine로 격리)
- 경로 충돌 시: overwrite 금지(기본), -dedupe 정책은 별도 승인 필요

### 삭제 정책

- delete는 금지(allow_delete=false)
- 삭제가 필요하면: 99_QUARANTINE로 move 후, 30일 이후 수동 삭제

---

## 7) 권한/안전(Safety & Permissions)

### Allowed without prompt (자동 허용)

- 파일/디렉토리 읽기, 목록화, 통계 계산
- ES CLI로 리포트 생성(저장 경로는 _meta/로 제한)
- plan.json 생성(dry-run 전제)
- 테스트/린트(읽기 전용)

### Ask first (반드시 사용자 승인)

- apply(실제 move/rename/delete)
- HTTP Server 활성화/외부 바인딩
- 대량 변경(예: actions > 200)
- 새로운 의존성 설치/업데이트(pip/pnpm 등)

---

## 8) 작업 플로우(에이전트 루프)

### Discover

- 리포 구조/엔트리포인트/기존 스크립트 탐색(추측 금지)
- Everything Provider 연결 상태 확인(가능하면 ES부터)

### Report (Read-only)

- INBOX aging / bigfiles / ext stats 생성 → _meta/reports/

### Plan

- 정책 기반으로 plan.json 생성 → _meta/plans/
- plan 요약(액션 수, top risk, 경로 충돌) 출력

### Approve

- 사람 승인(approve/reject) 없으면 apply 단계로 가지 않는다.

### Apply

- dry-run → 검증 → commit → audit/snapshot 기록

### Verify

- after snapshot 기준으로 누락/중복/크기/해시 불일치 검사
- 실패 시 롤백/격리 후 리포트

---

## 9) 테스트/검증(필수)

### 최소 테스트 세트(가정: Python 기반)

- 단위 테스트: Planner(분류 규칙), Executor(트랜잭션/롤백), Audit(append-only)
- 스모크 테스트: 샘플 디렉토리 생성 → plan 생성 → dry-run → apply(소량) → verify

에이전트는 먼저 리포에서 실제 테스트 러너를 탐색한 뒤, 존재하는 명령만 사용한다(없는 명령을 만들어내지 말 것).

---

## 10) 서브에이전트 운영(권장: Cursor Sub-agents)

- Researcher: Everything 연동 방식/보안 제약 정리(실행 금지, 문서화만)
- Planner: 규칙 설계 + plan.json 생성
- Executor: 트랜잭션 적용 + audit/snapshot + 검증
- QA: 실패 케이스(경로 충돌, 파일 잠김, 긴 경로) 테스트 추가

### Handoff 규칙

"write가 필요한 단계"는 Executor만 수행하며, 그 전에는 반드시 Approve Gate를 통과한다.

---

## 11) 호환성(파일명 표준)

표준은 보통 AGENTS.md가 우세하므로, 필요 시 다음 중 하나를 적용한다:

- agent.md를 SSOT로 두고 AGENTS.md는 링크/복사본으로 유지
- 또는 AGENTS.md를 SSOT로 두고 agent.md는 링크/복사본으로 유지

## 11.1) Cursor IDE 통합 (Cursor-only 패턴)

이 문서(`agents.md`)는 **SSOT (Single Source of Truth)**로 아키텍처와 안전 규칙을 정의합니다.

**Cursor IDE에서의 실제 사용**:
- `.cursor/agents/*.md` = Cursor IDE에서 사용되는 에이전트 구현
- `.cursor/skills/*/SKILL.md` = 재사용 가능한 워크플로우
- `.cursor/rules/016-agents-cursor-only.mdc` = Cursor 전용 에이전트 패턴 규칙

**관계**:
- `agents.md` (root) = 아키텍처 SSOT, 안전 규칙 정의
- `.cursor/agents/` = Cursor IDE에서의 실제 에이전트 구현
- Skills는 에이전트를 사용하는 워크플로우 제공

**참고 문서**:
- `docs/AGENTS_AND_SKILLS_GUIDE.md` = 에이전트와 스킬 사용 가이드 (SSOT)
- `.cursor/skills/agent-selector/SKILL.md` = 에이전트 선택 가이드

---

## 12) 참고(공식 문서 링크)

- Everything ES CLI: https://www.voidtools.com/support/everything/command_line_interface/
- Everything HTTP Server: https://www.voidtools.com/support/everything/http/
- Everything SDK: https://www.voidtools.com/support/everything/sdk/

---

## 13) 변경 로그(Changelog)

- 2026-01-28: Everything=Read-only, Folder-Tidy=Plan→Approve→Apply, write 기본 OFF, audit/snapshot 의무화
