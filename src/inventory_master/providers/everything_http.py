"""Everything HTTP Server provider (read-only).

Requires Everything HTTP Server enabled (Tools → Options → HTTP Server).
Security: use localhost only; disable file download in Everything options.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from ..hashing import sha256_file
from ..models import FileRecord
from .base import InventoryProvider

_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 8080
_DEFAULT_TIMEOUT = 30


def is_available(
    host: str = _DEFAULT_HOST,
    port: int = _DEFAULT_PORT,
    timeout: float = 5.0,
) -> bool:
    """Return True if Everything HTTP Server is reachable."""
    url = f"http://{host}:{port}/"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status in (200, 204)
    except (OSError, urllib.error.URLError, TimeoutError):
        return False


class EverythingHTTPProvider(InventoryProvider):
    """Everything HTTP Server provider (read-only).

    Requires Everything running with HTTP Server enabled (default port 8080).
    Use localhost/127.0.0.1 only; disable file download in Everything options.
    """

    def __init__(
        self,
        *,
        host: str = _DEFAULT_HOST,
        port: int = _DEFAULT_PORT,
        hash_files: bool = False,
        max_results: int = 0,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        self._host = host
        self._port = port
        self._base_url = f"http://{host}:{port}"
        self._hash_files = hash_files
        self._max_results = max_results or 4294967295
        self._timeout = timeout

    def iter_files(self, root: Path) -> list[FileRecord]:
        root = root.resolve()
        root_str = str(root)
        # Search under path: use path match (p=1) and search = root path
        # Search: path match (p=1), limit to results under root (path: prefix in Everything syntax)
        params = {
            "s": root_str + "\\",
            "p": 1,
            "c": min(self._max_results, 100_000),
            "j": 1,
            "path_column": 1,
            "size_column": 1,
            "date_modified_column": 1,
            "sort": "path",
            "ascending": 1,
        }
        query = urllib.parse.urlencode(params)
        url = f"{self._base_url}/?{query}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Everything HTTP error {e.code}: {e.reason}") from e
        except (OSError, urllib.error.URLError, TimeoutError) as e:
            raise RuntimeError(f"Everything HTTP failed: {e}") from e

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Everything HTTP returned invalid JSON: {e}") from e

        # Accept list of rows or {"results": [...]}; columns may be named path, size, date_modified
        rows = data if isinstance(data, list) else data.get("results", data.get("items", []))
        if not isinstance(rows, list):
            rows = []

        records: list[FileRecord] = []
        for row in rows:
            if isinstance(row, dict):
                path_val = row.get("path") or row.get("full_path_and_name") or row.get("path_and_name")
            else:
                path_val = row
            if not path_val:
                continue
            p = Path(path_val)
            if "_meta" in p.parts:
                continue
            try:
                if not p.is_file():
                    continue
                st = p.stat()
            except OSError:
                continue
            size = st.st_size if hasattr(st, "st_size") else (row.get("size") if isinstance(row, dict) else 0)
            mtime_ns = st.st_mtime_ns if hasattr(st, "st_mtime_ns") else 0
            if isinstance(row, dict) and "date_modified" in row and not mtime_ns:
                try:
                    from datetime import datetime
                    dm = row["date_modified"]
                    if isinstance(dm, (int, float)):
                        mtime_ns = int(dm * 1e9)
                    elif isinstance(dm, str):
                        dt = datetime.fromisoformat(dm.replace("Z", "+00:00"))
                        mtime_ns = int(dt.timestamp() * 1e9)
                except Exception:
                    pass
            sha = sha256_file(p) if self._hash_files else None
            records.append(
                FileRecord(path=p, size_bytes=size or 0, mtime_ns=mtime_ns, sha256=sha)
            )
        return records
