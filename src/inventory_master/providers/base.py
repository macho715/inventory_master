from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import FileRecord


class InventoryProvider(ABC):
    @abstractmethod
    def iter_files(self, root: Path) -> list[FileRecord]:
        raise NotImplementedError
