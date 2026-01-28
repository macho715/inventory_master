from __future__ import annotations

from pathlib import Path


def meta_root(root: Path) -> Path:
    return root / "_meta"


def ensure_meta_layout(root: Path) -> dict[str, Path]:
    m = meta_root(root)
    paths = {
        "inventory": m / "inventory",
        "reports": m / "reports",
        "plans": m / "plans",
        "audit": m / "audit",
        "snapshots": m / "snapshots",
        "approvals": m / "approvals",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths
