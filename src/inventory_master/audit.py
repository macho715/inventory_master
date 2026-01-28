from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def append_audit(audit_path: Path, event: dict[str, Any]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event.setdefault("ts", datetime.now(timezone.utc).isoformat())
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
