"""Generic JSON file repository.

One repository instance manages one entity type stored in one JSON
file (e.g. ``data/customers.json``). The file holds a JSON array of
objects; every model class provides ``to_dict`` / ``from_dict`` for
(de)serialization.

Design decisions:
- Data is loaded once on startup and kept in memory.
- Every mutating operation (add / update / delete) writes the file
  immediately, so no explicit "save" step is needed and data survives
  any way the program exits.
- IDs are auto-incremented integers managed by the repository.
"""

import json
from pathlib import Path
from typing import Any, Callable, Generic, List, Optional, Protocol, TypeVar


class Persistable(Protocol):
    """Anything storable in a JsonRepository: has an id and is JSON-mappable."""

    id: int

    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Any: ...


T = TypeVar("T", bound=Persistable)


class JsonRepository(Generic[T]):
    def __init__(self, file_path: Path, model_cls: type[T]):
        self.file_path: Path = Path(file_path)
        self.model_cls: type[T] = model_cls
        self._items: List[T] = self._load()

    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------
    def _load(self) -> List[T]:
        if not self.file_path.exists():
            return []
        raw = self.file_path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        return [self.model_cls.from_dict(entry) for entry in data]

    def _save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            [item.to_dict() for item in self._items], indent=2, ensure_ascii=False
        )
        self.file_path.write_text(payload + "\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def get_all(self) -> List[T]:
        """Return a copy of all items (sorted by id)."""
        return sorted(self._items, key=lambda item: item.id)

    def get_by_id(self, item_id: int) -> Optional[T]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]

    def add(self, item: T) -> T:
        item.id = self._next_id()
        self._items.append(item)
        self._save()
        return item

    def update(self, item: T) -> T:
        for index, existing in enumerate(self._items):
            if existing.id == item.id:
                self._items[index] = item
                self._save()
                return item
        raise KeyError(f"No {self.model_cls.__name__} with id {item.id} to update.")

    def delete(self, item_id: int) -> None:
        for index, existing in enumerate(self._items):
            if existing.id == item_id:
                del self._items[index]
                self._save()
                return
        raise KeyError(f"No {self.model_cls.__name__} with id {item_id} to delete.")

    def count(self) -> int:
        return len(self._items)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _next_id(self) -> int:
        return max((item.id for item in self._items), default=0) + 1
