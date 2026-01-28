from __future__ import annotations

import json
from pathlib import Path

from inventory_master.planner import generate_plan


def test_generate_plan_json(tmp_path: Path):
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "x.tmp").write_text("tmp")
    plan_path = generate_plan(root)

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["policy"]["allow_delete"] is False
    assert plan_path.exists()
    assert len(plan["actions"]) == 1
