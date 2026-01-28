from __future__ import annotations

import json
from pathlib import Path

from .meta_paths import ensure_meta_layout


def approve_plan(plan_path: Path) -> Path:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_id = plan["plan_id"]

    root = Path(plan["root"])
    meta = ensure_meta_layout(root)
    token_path = meta["approvals"] / f"APPROVED__{plan_id}.token"

    # Human gate: this command exists, but it still requires explicit user invocation.
    token_path.write_text(plan_id, encoding="utf-8")
    return token_path
