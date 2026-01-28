# inventory_master — Plan→Approve→Apply Folder Tidy (Everything Read‑only)

> Target root (default): `C:\\inventory_master\\` (Windows)

## Goals
- **Inventory/Search = read-only** via Everything (ES CLI / HTTP / SDK) or local batch scan fallback.
- **Folder tidy write actions (move/rename/delete)** are **Plan → Approve → Apply** gated.
- Default safety: **write OFF**, **delete OFF** (quarantine instead), **audit + snapshots required**.

## Quickstart (Windows)
```powershell
# 1) Unzip this pack into C:\inventory_master\ (or a dedicated repo folder)
# 2) Create venv (Python 3.13 recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install tooling
python -m pip install --upgrade pip
pip install -e .[dev]

# 4) Run a read-only report (fallback local scanner)
python -m inventory_master report --root "C:\inventory_master\"

# 5) Generate a plan (no writes)
python -m inventory_master plan --root "C:\inventory_master\"

# 6) Human approve (creates an approval token file under _meta/approvals/)
python -m inventory_master approve --plan "_meta\plans\<plan_file>.json"

# 7) Apply (requires --dry-run first; then without dry-run)
python -m inventory_master apply --plan "_meta\plans\<plan_file>.json" --dry-run
python -m inventory_master apply --plan "_meta\plans\<plan_file>.json"
```

## Cursor
- Rules: `.cursor/rules/*.mdc` (alwaysApply + opt-in mix)
- Commands: `.cursor/commands/*.md`
- Subagents: `.cursor/agents/`
- Skills: `.cursor/skills/`
- **Guides**: 
  - [`docs/AGENTS_AND_SKILLS_GUIDE.md`](docs/AGENTS_AND_SKILLS_GUIDE.md) - Agents & Skills 통합 사용 가이드
  - [`docs/DEPENDENCY_MAP.md`](docs/DEPENDENCY_MAP.md) - 의존성 맵 및 호출 순서
  - [`docs/WORKFLOW_EXAMPLES.md`](docs/WORKFLOW_EXAMPLES.md) - 실전 워크플로우 예시
  - [`docs/NEW_AGENTS_AND_SKILLS.md`](docs/NEW_AGENTS_AND_SKILLS.md) - 새로 추가된 Agents & Skills

## Implementation Status

✅ **Core features implemented** (2026-01-28)
- CLI commands: `report`, `plan`, `approve`, `apply`
- Planner with default quarantine rule
- Executor with transactional apply
- Approval gate system
- Audit logging system
- Snapshot system
- LocalWalkProvider (fallback)
- Basic test coverage (6/6 tests passing)

See [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) for detailed status.

## Safety defaults
- Apply refuses unless:
  - `--dry-run` has been executed (recorded in audit)
  - approval token exists for the plan_id
  - pre/post snapshot + hash verification pass

See:
- `agents.md` (SSOT for safety)
- `docs/constitution.md` (non‑negotiables)
- `docs/ARCHITECTURE.md` (architecture details)
- `docs/IMPLEMENTATION_STATUS.md` (implementation status)
- `docs/AGENTS_AND_SKILLS_GUIDE.md` (Agents & Skills 사용 가이드)
- `docs/DEPENDENCY_MAP.md` (의존성 맵)
- `docs/WORKFLOW_EXAMPLES.md` (실전 워크플로우 예시)
