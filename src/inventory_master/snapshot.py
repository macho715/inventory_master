from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .hashing import sha256_file
from .models import FileRecord
from .providers.local_walk import LocalWalkProvider


def create_snapshot(root: Path, snapshot_path: Path, *, hash_files: bool = True) -> list[FileRecord]:
    provider = LocalWalkProvider(hash_files=hash_files)
    records = provider.iter_files(root)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "path": str(r.path.relative_to(root)),
            "size_bytes": r.size_bytes,
            "mtime_ns": r.mtime_ns,
            "sha256": r.sha256,
        }
        for r in records
    ]
    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return records


def load_snapshot(snapshot_path: Path) -> list[dict]:
    return json.loads(snapshot_path.read_text(encoding="utf-8"))
