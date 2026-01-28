from __future__ import annotations

from pathlib import Path

from inventory_master.snapshot import create_snapshot


def test_hash_verify_mismatch(tmp_path: Path):
    root = tmp_path / "ROOT"
    root.mkdir()
    f = root / "a.txt"
    f.write_text("one")

    snap1 = root / "_meta" / "snapshots" / "before.json"
    create_snapshot(root, snap1, hash_files=True)

    # change file
    f.write_text("two")

    snap2 = root / "_meta" / "snapshots" / "after.json"
    create_snapshot(root, snap2, hash_files=True)

    assert snap1.read_text() != snap2.read_text()
