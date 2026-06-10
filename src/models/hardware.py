"""Hardware model (smartphones and accessories)."""

from dataclasses import asdict, dataclass
from typing import Any

CATEGORIES = ("Smartphone", "Accessory")


@dataclass
class Hardware:
    id: int = 0
    name: str = ""
    brand: str = ""
    category: str = "Smartphone"  # one of CATEGORIES
    price: float = 0.0  # unit price in JOD
    stock: int = 0  # units currently in stock

    @property
    def stock_value(self) -> float:
        """Total value of the units currently in stock."""
        return round(self.price * self.stock, 2)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Hardware":
        return cls(**data)
