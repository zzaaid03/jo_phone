"""Tariff (mobile plan) model."""

from dataclasses import asdict, dataclass
from typing import Any

UNLIMITED = -1  # sentinel for unlimited data / minutes


@dataclass
class Tariff:
    id: int = 0
    name: str = ""
    monthly_fee: float = 0.0  # JOD per month
    data_gb: float = 0.0  # UNLIMITED for unlimited data
    minutes: int = 0  # UNLIMITED for unlimited minutes
    min_duration_months: int = 12  # minimum contract duration

    @property
    def data_display(self) -> str:
        return "Unlimited" if self.data_gb == UNLIMITED else f"{self.data_gb:g} GB"

    @property
    def minutes_display(self) -> str:
        return "Unlimited" if self.minutes == UNLIMITED else f"{self.minutes} min"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Tariff":
        return cls(**data)
