from __future__ import annotations

import os
from pathlib import Path

from ..hashing import sha256_file
from ..models import FileRecord
from .base import InventoryProvider


class LocalWalkProvider(InventoryProvider):
    """Fallback provider (slow): walk the filesystem.

    NOTE: This is read-only and does not watch; batch scan only.
    """

    def __init__(self, *, hash_files: bool = False) -> None:
        self._hash_files = hash_files

    def iter_files(self, root: Path) -> list[FileRecord]:
        records: list[FileRecord] = []
        root = root.resolve()
        for dirpath, _, filenames in os.walk(root):
            # skip _meta and any path under it
            try:
                rel = Path(dirpath).resolve().relative_to(root)
            except ValueError:
                continue
            if "_meta" in rel.parts:
                continue
            for fn in filenames:
                p = Path(dirpath) / fn
                try:
                    st = p.stat()
                except OSError:
                    continue
                sha = sha256_file(p) if self._hash_files else None
                records.append(
                    FileRecord(
                        path=p,
                        size_bytes=st.st_size,
                        mtime_ns=st.st_mtime_ns,
                        sha256=sha,
                    )
                )
        return records
