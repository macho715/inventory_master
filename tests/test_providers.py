"""Tests for inventory providers (Everything ES, LocalWalk, fallback)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from inventory_master.providers.everything_es import (
    EverythingESProvider,
    find_es_exe,
    is_available,
)
from inventory_master.providers.local_walk import LocalWalkProvider
from inventory_master.reporting import _get_report_provider, generate_report


def test_find_es_exe_returns_str_or_none() -> None:
    """find_es_exe() returns a path string or None."""
    result = find_es_exe()
    assert result is None or isinstance(result, str)
    if result is not None:
        assert result.endswith("es.exe") or "es" in result.lower()


def test_is_available_returns_bool() -> None:
    """is_available() returns a boolean."""
    assert isinstance(is_available(), bool)


def test_get_report_provider_returns_provider_and_backend() -> None:
    """_get_report_provider returns a provider and backend name."""
    from inventory_master.providers.everything_http import EverythingHTTPProvider
    from inventory_master.providers.everything_sdk import EverythingSDKProvider

    provider, backend = _get_report_provider(Path("."))
    assert backend in ("everything_es", "everything_http", "everything_sdk", "local")
    assert provider is not None
    assert isinstance(
        provider,
        (LocalWalkProvider, EverythingESProvider, EverythingHTTPProvider, EverythingSDKProvider),
    )


def test_everything_es_provider_nonexistent_es_raises() -> None:
    """EverythingESProvider with non-existent es_exe raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="not found"):
        EverythingESProvider(es_exe="C:\\nonexistent\\es.exe")


def test_report_uses_local_fallback_when_es_unavailable(tmp_path: Path) -> None:
    """generate_report works with local fallback when Everything is unavailable."""
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "a.txt").write_text("x")
    out = generate_report(root)
    assert out.exists()
    assert "_meta" in str(out)
    assert "reports" in str(out)
    content = out.read_text(encoding="utf-8")
    assert "files:" in content
    assert "a.txt" in content or "1" in content or ".txt" in content


def test_local_walk_provider_skips_meta(tmp_path: Path) -> None:
    """LocalWalkProvider skips _meta directory."""
    root = tmp_path / "ROOT"
    root.mkdir()
    (root / "a.txt").write_text("a")
    (root / "_meta" / "reports").mkdir(parents=True)
    (root / "_meta" / "reports" / "x.md").write_text("meta")
    provider = LocalWalkProvider(hash_files=False)
    records = provider.iter_files(root)
    paths = [r.path for r in records]
    assert any("a.txt" in str(p) for p in paths)
    assert not any("_meta" in str(p) for p in paths)


def test_everything_http_provider_mock_urlopen_request_and_parsing(tmp_path: Path) -> None:
    """Mock urllib.request.urlopen: assert request URL params and JSON parsed into FileRecord list."""
    from inventory_master.providers.everything_http import EverythingHTTPProvider
    from inventory_master.models import FileRecord

    root = tmp_path / "ROOT"
    root.mkdir()
    f = root / "f.txt"
    f.write_text("x")
    path_str = str(f.resolve())

    # Minimal Everything HTTP JSON: list of rows with path (and optional size/date_modified)
    mock_json = [{"path": path_str, "size": 1, "date_modified": None}]
    mock_body = json.dumps(mock_json).encode("utf-8")

    captured_url: list[str] = []

    def fake_urlopen(req, timeout=None):
        # Capture URL from the Request (full_url in 3.9+)
        url = getattr(req, "full_url", None)
        if url is None and callable(getattr(req, "get_full_url", None)):
            url = req.get_full_url()
        if url is None:
            url = str(req)
        captured_url.append(url if isinstance(url, str) else str(url))
        resp = MagicMock()
        resp.read.return_value = mock_body
        resp.__enter__ = MagicMock(return_value=resp)
        resp.__exit__ = MagicMock(return_value=False)
        return resp

    with patch("inventory_master.providers.everything_http.urllib.request.urlopen", side_effect=fake_urlopen):
        provider = EverythingHTTPProvider(host="127.0.0.1", port=8080, hash_files=False)
        records = provider.iter_files(root)

    assert len(captured_url) == 1
    url = captured_url[0]
    assert "s=" in url or "search=" in url
    assert "j=1" in url or "json=1" in url
    assert "path_column=1" in url

    assert len(records) == 1
    assert isinstance(records[0], FileRecord)
    assert records[0].path == f.resolve() or str(records[0].path) == path_str
    assert records[0].size_bytes >= 0
    assert records[0].sha256 is None
