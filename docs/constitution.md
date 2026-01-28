# Project Constitution — inventory_master (v1)

## 1) Non‑Negotiables
1. Everything is **inventory/search only** (read-only).
2. Any filesystem write (move/rename/delete) MUST follow: **Plan → Human Approve → Apply**.
3. Default safety:
   - write OFF
   - delete OFF (use `99_QUARANTINE/` + 30-day manual delete policy)
   - HTTP server is read-only; prefer local binding + auth; disable downloads.

## 2) Evidence & Recoverability
- Before Apply: must produce **dry-run diff**, **pre snapshot**, and **hash manifest**.
- After Apply: must produce **post snapshot** and verify (exists/size/hash).
- `audit.jsonl` is **append-only**.

## 3) Engineering Gates
- Python: **3.13**
- CI gates:
  - tests pass
  - coverage ≥ 85.00
  - ruff/format/black/isort pass
  - bandit High=0
  - pip-audit --strict pass (best-effort; should be green for releases)

## 4) Scope Guard
- Default code edits limited to `src/**` and `tests/**`.
- Setup/scaffolding edits allowed: `.cursor/**`, `.github/**`, `config/**`, `tools/**`, `pyproject.toml`, `plan.md`, `CODEOWNERS`, `README.md`.

## 5) Fail‑Safe
- If anything is unclear, stop at **Plan** stage and output risks + questions.
