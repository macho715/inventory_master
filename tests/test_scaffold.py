from pathlib import Path


def test_scaffold_exists():
    assert (Path("src") / "inventory_master" / "cli.py").exists()
