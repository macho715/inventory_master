"""Everything SDK provider (read-only, Windows only).

Requires Everything running and Everything SDK DLL (Everything64.dll / Everything32.dll).
DLL is typically in Everything install folder or SDK folder.
"""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path

from ..hashing import sha256_file
from ..models import FileRecord
from .base import InventoryProvider

# Request flags (from Everything SDK)
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040

_SDK_COMMON_PATHS = (
    r"C:\Program Files\Everything\Everything64.dll",
    r"C:\Program Files\Everything\Everything32.dll",
    r"C:\Program Files (x86)\Everything\Everything32.dll",
    r"C:\Tools\Everything\Everything64.dll",
    r"C:\Tools\Everything\Everything32.dll",
)

# Windows FILETIME: 100-nanosecond intervals since 1601-01-01
# Epoch 1970 is 11644473600 seconds after 1601 -> 11644473600 * 10^7 ticks
_WIN_FILETIME_EPOCH_OFFSET = 116444736000000000  # ticks


def _find_dll() -> str | None:
    if sys.platform != "win32":
        return None
    for p in _SDK_COMMON_PATHS:
        if Path(p).exists():
            return p
    return None


def is_available(dll_path: str | None = None) -> bool:
    """Return True if we are on Windows and the Everything SDK DLL can be loaded."""
    if sys.platform != "win32":
        return False
    path = dll_path or _find_dll()
    if not path or not Path(path).exists():
        return False
    try:
        dll = ctypes.WinDLL(path)
        dll.Everything_GetNumResults.restype = ctypes.c_uint
        dll.Everything_QueryW(1)
        return True
    except (OSError, AttributeError):
        return False


class EverythingSDKProvider(InventoryProvider):
    """Everything SDK provider (read-only, Windows only).

    Uses Everything SDK DLL for fast indexed search.
    """

    def __init__(
        self,
        *,
        dll_path: str | None = None,
        hash_files: bool = False,
        max_results: int = 0,
    ) -> None:
        if sys.platform != "win32":
            raise RuntimeError("Everything SDK provider is Windows-only")
        self._dll_path = dll_path or _find_dll()
        if not self._dll_path or not Path(self._dll_path).exists():
            raise FileNotFoundError(
                "Everything SDK DLL not found. Install Everything and ensure Everything64.dll or Everything32.dll is available."
            )
        self._dll = ctypes.WinDLL(self._dll_path)
        self._hash_files = hash_files
        self._max_results = max_results or 0

        # Set up function signatures (W = wide/Unicode)
        self._dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
        self._dll.Everything_SetSearchW.restype = ctypes.c_int

        self._dll.Everything_SetMatchPath.argtypes = [ctypes.c_int]
        self._dll.Everything_SetMatchPath.restype = ctypes.c_int

        self._dll.Everything_SetRequestFlags.argtypes = [ctypes.c_uint]
        self._dll.Everything_SetRequestFlags.restype = ctypes.c_int

        self._dll.Everything_SetMax.argtypes = [ctypes.c_uint]
        self._dll.Everything_SetMax.restype = ctypes.c_int

        self._dll.Everything_QueryW.argtypes = [ctypes.c_int]
        self._dll.Everything_QueryW.restype = ctypes.c_int

        self._dll.Everything_GetNumResults.restype = ctypes.c_uint
        self._dll.Everything_IsFileResult.argtypes = [ctypes.c_uint]
        self._dll.Everything_IsFileResult.restype = ctypes.c_int

        self._dll.Everything_GetResultFullPathNameW.argtypes = [
            ctypes.c_uint,
            ctypes.c_wchar_p,
            ctypes.c_uint,
        ]
        self._dll.Everything_GetResultFullPathNameW.restype = ctypes.c_int

        self._dll.Everything_GetResultSize.argtypes = [ctypes.c_uint, ctypes.POINTER(ctypes.c_ulonglong)]
        self._dll.Everything_GetResultSize.restype = ctypes.c_int

        self._dll.Everything_GetResultDateModified.argtypes = [
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_ulonglong),
        ]
        self._dll.Everything_GetResultDateModified.restype = ctypes.c_int

    def iter_files(self, root: Path) -> list[FileRecord]:
        root = root.resolve()
        root_str = str(root)
        # Search under path: use path match and search = root (Everything syntax: path under root)
        self._dll.Everything_SetSearchW(root_str)
        self._dll.Everything_SetMatchPath(1)
        self._dll.Everything_SetRequestFlags(
            EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME
            | EVERYTHING_REQUEST_SIZE
            | EVERYTHING_REQUEST_DATE_MODIFIED
        )
        if self._max_results > 0:
            self._dll.Everything_SetMax(self._max_results)
        if not self._dll.Everything_QueryW(1):
            raise RuntimeError("Everything SDK query failed (is Everything running?).")
        n = self._dll.Everything_GetNumResults()
        max_path = 32767
        buf = ctypes.create_unicode_buffer(max_path)
        size_val = ctypes.c_ulonglong()
        date_val = ctypes.c_ulonglong()
        records: list[FileRecord] = []
        for i in range(n):
            if not self._dll.Everything_IsFileResult(i):
                continue
            if self._dll.Everything_GetResultFullPathNameW(i, buf, max_path) == 0:
                continue
            path_str = buf.value
            if not path_str or "_meta" in path_str.replace("\\", "/").split("/"):
                continue
            p = Path(path_str)
            try:
                if not p.is_file():
                    continue
                st = p.stat()
            except OSError:
                continue
            size_bytes = st.st_size
            mtime_ns = st.st_mtime_ns
            if self._dll.Everything_GetResultSize(i, ctypes.byref(size_val)):
                size_bytes = size_val.value
            if self._dll.Everything_GetResultDateModified(i, ctypes.byref(date_val)) and date_val.value:
                # Windows FILETIME (100-ns since 1601) -> ns since Unix epoch
                ticks = date_val.value
                mtime_ns = (ticks - _WIN_FILETIME_EPOCH_OFFSET) * 100
            sha = sha256_file(p) if self._hash_files else None
            records.append(
                FileRecord(path=p, size_bytes=size_bytes, mtime_ns=mtime_ns, sha256=sha)
            )
        return records
