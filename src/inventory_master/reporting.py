from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from .meta_paths import ensure_meta_layout
from .providers.everything_es import EverythingESProvider, is_available as es_available
from .providers.everything_http import EverythingHTTPProvider, is_available as http_available
from .providers.everything_sdk import EverythingSDKProvider, is_available as sdk_available
from .providers.local_walk import LocalWalkProvider

# Type: any provider + backend name for fallback
_ReportProvider = LocalWalkProvider | EverythingESProvider | EverythingHTTPProvider | EverythingSDKProvider


def _get_report_provider(root: Path) -> tuple[_ReportProvider, str]:
    """Return (provider, backend_name). Prefer ES > HTTP > SDK > Local."""
    if es_available():
        try:
            return EverythingESProvider(hash_files=False), "everything_es"
        except (FileNotFoundError, RuntimeError):
            pass
    if http_available():
        try:
            return EverythingHTTPProvider(hash_files=False), "everything_http"
        except (FileNotFoundError, RuntimeError):
            pass
    if sdk_available():
        try:
            return EverythingSDKProvider(hash_files=False), "everything_sdk"
        except (FileNotFoundError, RuntimeError):
            pass
    return LocalWalkProvider(hash_files=False), "local"


def generate_report(root: Path) -> Path:
    meta = ensure_meta_layout(root)
    provider, backend = _get_report_provider(root)
    try:
        records = provider.iter_files(root)
    except (RuntimeError, OSError) as e:
        if backend != "local":
            provider = LocalWalkProvider(hash_files=False)
            records = provider.iter_files(root)
        else:
            raise e

    ext = Counter([r.path.suffix.lower() or "<noext>" for r in records])
    top_ext = ext.most_common(30)

    report_id = datetime.now().strftime("%Y-%m-%d")
    out_path = meta["reports"] / f"report_{report_id}.md"
    lines = [
        f"# Report {report_id}",
        "",
        f"- files: {len(records)}",
        "",
        "## Top extensions",
        "",
        "| ext | count |",
        "|---|---:|",
    ]
    for e, c in top_ext:
        lines.append(f"| {e} | {c} |")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
