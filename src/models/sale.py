"""Sale model: a direct (one-off) hardware sale to a customer.

The unit price is stored as a snapshot at the time of sale, so later
price changes never alter historical sales.
"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Sale:
    id: int = 0
    customer_id: int = 0
    hardware_id: int = 0
    quantity: int = 1
    unit_price: float = 0.0  # snapshot of the hardware price at sale time
    date: str = ""  # ISO date YYYY-MM-DD

    @property
    def total(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    @property
    def month(self) -> str:
        """The YYYY-MM part of the sale date (used for monthly reports)."""
        return self.date[:7]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Sale":
        return cls(**data)
