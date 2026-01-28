from __future__ import annotations

from pathlib import Path

from inventory_master.cli import main


def test_cli_report_smoke(tmp_path: Path):
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "a.txt").write_text("x")

    rc = main(["report", "--root", str(root)])
    assert rc == 0
    assert (root / "_meta" / "reports").exists()
