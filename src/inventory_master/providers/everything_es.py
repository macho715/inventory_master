"""Everything ES CLI provider (read-only)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ..hashing import sha256_file
from ..models import FileRecord
from .base import InventoryProvider

# Common install locations for es.exe (Windows)
_ES_COMMON_PATHS = (
    r"C:\Program Files\Everything\es.exe",
    r"C:\Program Files (x86)\Everything\es.exe",
    r"C:\Tools\Everything\es.exe",
)

# Default timeout for ES CLI (ms); ES doc uses -timeout <ms>
_DEFAULT_TIMEOUT_MS = 30_000


def find_es_exe() -> str | None:
    """Find es.exe in PATH or common install paths. Returns None if not found."""
    exe = shutil.which("es") or shutil.which("es.exe")
    if exe:
        return exe
    for p in _ES_COMMON_PATHS:
        if Path(p).exists():
            return p
    return None


def is_available(es_exe: str | None = None) -> bool:
    """Return True if Everything is running and es.exe can be used."""
    exe = es_exe or find_es_exe()
    if not exe:
        return False
    try:
        # -get-result-count with empty search: just checks IPC
        result = subprocess.run(
            [exe, "-get-result-count"],
            capture_output=True,
            text=True,
            timeout=5,
            errors="replace",
        )
        # Return code 0 = success; 8 = Everything not running
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


class EverythingESProvider(InventoryProvider):
    """Everything ES CLI provider (read-only).

    Requires:
    - Everything installed and running
    - es.exe in PATH or common install path

    Uses ES options:
    - -path <path>: search under path
    - /a-d: files only (no folders)
    - -s: sort by full path
    - -n <num>: max results (optional)
    """

    def __init__(
        self,
        *,
        es_exe: str | None = None,
        hash_files: bool = False,
        max_results: int = 0,
        timeout_ms: int = _DEFAULT_TIMEOUT_MS,
    ) -> None:
        self._es_exe = es_exe or find_es_exe()
        if not self._es_exe:
            raise FileNotFoundError(
                "es.exe not found. Install Everything and ensure es.exe is in PATH or at a common path."
            )
        if not Path(self._es_exe).exists():
            raise FileNotFoundError(f"es.exe not found at: {self._es_exe}")
        self._hash_files = hash_files
        self._max_results = max_results  # 0 = no limit
        self._timeout_sec = max(1, timeout_ms // 1000)

    def iter_files(self, root: Path) -> list[FileRecord]:
        root = root.resolve()
        root_str = str(root)
        # ES: -path <path> = search under path; /a-d = files only; -s = sort by path
        cmd = [self._es_exe, "-path", root_str, "/a-d", "-s"]
        if self._max_results > 0:
            cmd.extend(["-n", str(self._max_results)])
        try:
            out = subprocess.check_output(
                cmd,
                text=True,
                timeout=self._timeout_sec,
                errors="replace",
            )
        except subprocess.CalledProcessError as e:
            if e.returncode == 8:
                raise RuntimeError(
                    "Everything is not running. Start Everything and try again."
                ) from e
            raise RuntimeError(f"ES provider failed (exit {e.returncode}): {e}") from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"ES provider timed out after {self._timeout_sec}s") from e

        records: list[FileRecord] = []
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            p = Path(line)
            # Skip _meta (same as LocalWalkProvider)
            if "_meta" in p.parts:
                continue
            try:
                if not p.is_file():
                    continue
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
