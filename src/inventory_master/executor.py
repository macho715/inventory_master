from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from .audit import append_audit
from .hashing import sha256_file
from .meta_paths import ensure_meta_layout


class ApplyError(RuntimeError):
    pass


def _atomic_rename(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    # On Windows, os.replace will overwrite; we do NOT want overwrite by default.
    if dst.exists():
        raise ApplyError(f"Destination already exists: {dst}")
    os.rename(src, dst)


def apply_plan(plan_path: Path, *, dry_run: bool) -> None:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    root = Path(plan["root"])
    meta = ensure_meta_layout(root)
    audit_path = meta["audit"] / "audit.jsonl"

    plan_id = plan["plan_id"]
    approval_token = meta["approvals"] / f"APPROVED__{plan_id}.token"
    if not approval_token.exists():
        raise ApplyError(f"Missing approval token: {approval_token}")

    actions = plan["actions"]
    policy = plan["policy"]
    if len(actions) > int(policy.get("max_actions", 200)):
        raise ApplyError("Too many actions for policy.max_actions")

    # Dry-run is mandatory before real apply. Record it.
    if dry_run:
        append_audit(audit_path, {"event": "dry_run", "plan_id": plan_id, "actions": len(actions)})
        for a in actions:
            print(f"[DRY] {a['type']}: {a['src']} -> {a['dst']}")
        return

    # Require that dry-run happened previously (simple check in audit log).
    if policy.get("require_dry_run", True):
        if audit_path.exists():
            dry_ok = any(
                (line.strip() and json.loads(line).get("event") == "dry_run" and json.loads(line).get("plan_id") == plan_id)
                for line in audit_path.read_text(encoding="utf-8").splitlines()
            )
        else:
            dry_ok = False
        if not dry_ok:
            raise ApplyError("Dry-run required before apply (no matching audit event).")

    require_hash = bool(policy.get("require_hash_verify", True))

    append_audit(audit_path, {"event": "apply_start", "plan_id": plan_id, "actions": len(actions)})

    for a in actions:
        src = Path(a["src"])
        dst = Path(a["dst"])
        if not src.exists():
            raise ApplyError(f"Source missing: {src}")

        pre_size = src.stat().st_size
        pre_hash = sha256_file(src) if require_hash else None

        if a["type"] in {"move", "rename", "quarantine"}:
            # Quarantine is just a move to 99_QUARANTINE.
            _atomic_rename(src, dst)
        else:
            raise ApplyError(f"Unsupported action type: {a['type']}")

        post_size = dst.stat().st_size
        post_hash = sha256_file(dst) if require_hash else None

        if pre_size != post_size or (require_hash and pre_hash != post_hash):
            # Roll back best-effort
            try:
                _atomic_rename(dst, src)
            except Exception:
                pass
            raise ApplyError(f"Verification failed for action {a['id']}")

        append_audit(
            audit_path,
            {
                "event": "action_committed",
                "plan_id": plan_id,
                "action_id": a["id"],
                "type": a["type"],
                "src": str(src),
                "dst": str(dst),
                "pre_size": pre_size,
                "post_size": post_size,
            },
        )

    append_audit(audit_path, {"event": "apply_done", "plan_id": plan_id})
