from __future__ import annotations

import json
from pathlib import Path

import pytest

from inventory_master.approve import approve_plan
from inventory_master.executor import ApplyError, apply_plan
from inventory_master.planner import generate_plan


def test_apply_requires_approval(tmp_path: Path):
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "x.tmp").write_text("tmp")
    plan_path = generate_plan(root)

    with pytest.raises(ApplyError):
        apply_plan(plan_path, dry_run=True)


def test_dry_run_required(tmp_path: Path):
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "x.tmp").write_text("tmp")
    plan_path = generate_plan(root)

    # approve
    approve_plan(plan_path)

    # apply without dry-run should fail
    with pytest.raises(ApplyError):
        apply_plan(plan_path, dry_run=False)

    # dry-run then apply should work
    apply_plan(plan_path, dry_run=True)
    apply_plan(plan_path, dry_run=False)

    assert not (root / "x.tmp").exists()
    assert (root / "99_QUARANTINE" / "x.tmp").exists()
