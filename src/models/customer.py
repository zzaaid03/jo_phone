"""Customer model."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Customer:
    id: int = 0
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    city: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Customer":
        return cls(**data)
