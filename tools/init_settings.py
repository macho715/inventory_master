from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.check_call(cmd)


def main() -> int:
    p = argparse.ArgumentParser(description="Initialize repo settings (safe, idempotent).")
    p.add_argument("--git-init", action="store_true", help="Initialize git repo (main branch).")
    p.add_argument("--install-precommit", action="store_true", help="Install pre-commit hooks.")
    args = p.parse_args()

    root = Path.cwd()
    (root / ".cursor" / "config").mkdir(parents=True, exist_ok=True)
    (root / ".cursor" / "hooks").mkdir(parents=True, exist_ok=True)

    # Basic sanity: don't touch user data folders outside repo.
    # (This script expects to be run inside the intended repo root.)
    if not (root / "pyproject.toml").exists():
        print("ERROR: pyproject.toml not found. Run this from the repo root.", file=sys.stderr)
        return 2

    if args.git_init and not (root / ".git").exists():
        run(["git", "init", "-b", "main"])

    if args.install_precommit:
        run([sys.executable, "-m", "pip", "install", "pre-commit"])
        run(["pre-commit", "install"])
        run(["pre-commit", "install", "--hook-type", "commit-msg"])

    print(json.dumps({"ok": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
