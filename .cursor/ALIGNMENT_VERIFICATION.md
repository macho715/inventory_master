# Agents & Skills Alignment Verification

> **Last Updated**: 2026-01-28  
> **Purpose**: Verify alignment between `.cursor/agents/`, `.cursor/skills/`, and `docs/AGENTS_AND_SKILLS_GUIDE.md`

---

## ✅ Verification Status: ALIGNED

All agents and skills are properly documented and aligned.

---

## Agents Verification

### Agents in Directory: 10
1. `approver.md` ✅
2. `coordinator.md` ✅
3. `executor.md` ✅
4. `explore.md` ✅
5. `implementer.md` ✅
6. `planner.md` ✅
7. `qa.md` ✅
8. `researcher.md` ✅
9. `reviewer.md` ✅
10. `verifier.md` ✅

### Agents in Guide: 10 ✅
All agents from directory are documented in `docs/AGENTS_AND_SKILLS_GUIDE.md`:
- ✅ `explore` - 코드베이스 구조 파악
- ✅ `planner` - plan.json 설계/검증
- ✅ `implementer` - 코드 구현 (승인 후)
- ✅ `reviewer` - 보안/품질 검토
- ✅ `verifier` - 작업 완료 검증
- ✅ `researcher` - Everything 연동/보안 문서화
- ✅ `executor` - 파일 이동 실행 (승인 후)
- ✅ `qa` - 테스트 케이스 작성
- ✅ `approver` - 승인 게이트 관리
- ✅ `coordinator` - 워크플로우 조정 (added 2026-01-28)

---

## Skills Verification

### Skills in Directory: 15
1. `agent-selector/` ✅
2. `approval-gate/` ✅
3. `audit-query/` ✅
4. `ci-precommit/` ✅
5. `everything-provider-setup/` ✅
6. `everything-test/` ✅
7. `inventory-report/` ✅
8. `plan-gated-apply/` ✅
9. `plan-validate/` ✅
10. `quarantine-audit/` ✅
11. `release-check/` ✅
12. `repo-bootstrap/` ✅
13. `rules-vs-skills/` ✅
14. `snapshot-verify/` ✅
15. `tdd-go/` ✅

### Skills in Guide: 15 ✅
All skills from directory are documented in `docs/AGENTS_AND_SKILLS_GUIDE.md`:
- ✅ `everything-provider-setup` - Everything 연동 초기 설정
- ✅ `everything-test` - Everything 연동 테스트
- ✅ `tdd-go` - TDD 사이클 실행
- ✅ `plan-gated-apply` - 파일 이동/정리
- ✅ `plan-validate` - Plan 검증 (승인 전)
- ✅ `approval-gate` - 승인 게이트 관리
- ✅ `inventory-report` - 주간/월간 감사
- ✅ `quarantine-audit` - 삭제 요청 처리
- ✅ `snapshot-verify` - 스냅샷 무결성 검증
- ✅ `audit-query` - 감사 로그 조회
- ✅ `repo-bootstrap` - 새 저장소 설정
- ✅ `ci-precommit` - CI/Pre-commit 설정
- ✅ `release-check` - 릴리즈 전 체크
- ✅ `agent-selector` - 적절한 Agent 선택 시 (added 2026-01-28)
- ✅ `rules-vs-skills` - Rules vs Skills 구분이 필요할 때 (added 2026-01-28)

---

## Guide Sections Verification

### ✅ Section 2: Agents vs Skills 구분
- Agents table: 10 agents ✅
- Skills table: 15 skills ✅
- All entries match directory contents ✅

### ✅ Section 5: 사용 시나리오
- Agent selection guide: All 10 agents covered ✅
- Skill selection guide: All 15 skills covered ✅
- Scenario matrix: Complete ✅

### ✅ Section 6: 빠른 참조
- Agent call patterns: All 10 agents listed ✅
- Skill call patterns: All 15 skills listed ✅
- Workflow checklists: Complete ✅

---

## Recent Updates (2026-01-28)

### Added to Guide
1. ✅ `coordinator` agent - Added to agents table, selection guide, and call patterns
2. ✅ `agent-selector` skill - Added to skills table, selection guide, and call patterns
3. ✅ `rules-vs-skills` skill - Added to skills table, selection guide, and call patterns

### Enhanced Skills
1. ✅ `agent-selector` - Comprehensive agent selection guide (255 lines)
2. ✅ `everything-provider-setup` - Complete setup guide (239 lines)
3. ✅ `inventory-report` - Detailed report generation (137 lines)
4. ✅ `plan-gated-apply` - Complete workflow documentation (300+ lines)
5. ✅ `rules-vs-skills` - Comprehensive comparison guide (300+ lines)
6. ✅ `tdd-go` - Full TDD workflow guide (232 lines)

---

## Summary

### Totals
- **Agents**: 10 (all documented) ✅
- **Skills**: 15 (all documented) ✅
- **Guide Sections**: All complete ✅
- **Alignment**: 100% ✅

### Status
🎉 **All agents and skills are properly aligned and documented in the guide.**

The `docs/AGENTS_AND_SKILLS_GUIDE.md` serves as the single source of truth (SSOT) for all agents and skills in the project.

---

## Related Documents
- `docs/AGENTS_AND_SKILLS_GUIDE.md` - Main guide (SSOT)
- `.cursor/skills/SKILLS_INVENTORY.md` - Skills inventory
- `docs/DEPENDENCY_MAP.md` - Dependency relationships
- `docs/WORKFLOW_EXAMPLES.md` - Usage examples
