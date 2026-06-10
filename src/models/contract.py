"""Contract model: links a customer to a tariff, optionally with a device.

Price-relevant values (monthly fee, hardware price) are stored as
snapshots on the contract, so later changes to tariff or hardware
prices never alter existing contracts.
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional


class ContractStatus:
    ACTIVE = "ACTIVE"
    TERMINATED = "TERMINATED"


@dataclass
class Contract:
    id: int = 0
    customer_id: int = 0
    tariff_id: int = 0
    hardware_id: Optional[int] = None  # optional device bundled with the contract
    start_date: str = ""  # ISO date YYYY-MM-DD
    duration_months: int = 12
    monthly_fee: float = 0.0  # snapshot of the tariff fee at signing
    hardware_price: float = 0.0  # snapshot of the device price (0 if none)
    status: str = ContractStatus.ACTIVE

    @property
    def is_active(self) -> bool:
        return self.status == ContractStatus.ACTIVE

    @property
    def end_date(self) -> str:
        """Exclusive end date: start date shifted by the duration."""
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        month_index = start.month - 1 + self.duration_months
        year = start.year + month_index // 12
        month = month_index % 12 + 1
        # clamp the day for short months (e.g. Jan 31 + 1 month -> Feb 28)
        day = min(start.day, _days_in_month(year, month))
        return f"{year:04d}-{month:02d}-{day:02d}"

    @property
    def total_value(self) -> float:
        """Total committed value: all monthly fees plus the device price."""
        return round(self.monthly_fee * self.duration_months + self.hardware_price, 2)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        return cls(**data)


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month.toordinal() - 1
    return datetime.fromordinal(last_day).day
