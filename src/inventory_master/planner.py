from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .meta_paths import ensure_meta_layout
from .models import PlanAction


def generate_plan(root: Path) -> Path:
    """Generate a conservative plan.

    Current default rule:
    - Move *.tmp / *.bak into 99_QUARANTINE/
    (This is only a demo rule; expand with explicit user-approved rules.)
    """
    meta = ensure_meta_layout(root)
    plan_id = datetime.now().astimezone().isoformat(timespec="seconds").replace(":", "-")
    actions: list[dict] = []

    quarantine = root / "99_QUARANTINE"
    quarantine.mkdir(parents=True, exist_ok=True)

    counter = 0
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if "_meta" in p.parts:
            continue
        if p.suffix.lower() in {".tmp", ".bak"}:
            counter += 1
            actions.append(
                {
                    "id": f"A-{counter:03d}",
                    "type": "quarantine",
                    "src": str(p),
                    "dst": str(quarantine / p.name),
                }
            )

    plan = {
        "plan_id": plan_id,
        "root": str(root),
        "policy": {
            "allow_delete": False,
            "require_hash_verify": True,
            "require_dry_run": True,
            "max_actions": 200,
        },
        "actions": actions,
    }

    out_path = meta["plans"] / f"plan_{plan_id}.json"
    out_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
