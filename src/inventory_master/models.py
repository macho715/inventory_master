from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


ActionType = Literal["move", "rename", "quarantine"]


@dataclass(frozen=True)
class FileRecord:
    path: Path
    size_bytes: int
    mtime_ns: int
    sha256: str | None = None


@dataclass(frozen=True)
class PlanAction:
    id: str
    type: ActionType
    src: Path
    dst: Path
