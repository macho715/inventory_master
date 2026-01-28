from __future__ import annotations

import argparse
from pathlib import Path

from .approve import approve_plan
from .executor import ApplyError, apply_plan
from .planner import generate_plan
from .reporting import generate_report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="inventory_master", description="Plan-gated folder tidy tool.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_report = sub.add_parser("report", help="Generate read-only report under _meta/reports/")
    p_report.add_argument("--root", required=True)

    p_plan = sub.add_parser("plan", help="Generate plan JSON under _meta/plans/")
    p_plan.add_argument("--root", required=True)

    p_approve = sub.add_parser("approve", help="Create approval token for a plan (human gate).")
    p_approve.add_argument("--plan", required=True)

    p_apply = sub.add_parser("apply", help="Apply an approved plan (transactional).")
    p_apply.add_argument("--plan", required=True)
    p_apply.add_argument("--dry-run", action="store_true", help="Required first: prints diff only.")

    args = p.parse_args(argv)

    if args.cmd == "report":
        out = generate_report(Path(args.root))
        print(str(out))
        return 0

    if args.cmd == "plan":
        out = generate_plan(Path(args.root))
        print(str(out))
        return 0

    if args.cmd == "approve":
        out = approve_plan(Path(args.plan))
        print(str(out))
        return 0

    if args.cmd == "apply":
        try:
            apply_plan(Path(args.plan), dry_run=bool(args.dry_run))
        except ApplyError as e:
            print(f"ERROR: {e}")
            return 2
        return 0

    return 1
