"""Domain models (plain dataclasses, persistence-agnostic)."""

from src.models.contract import Contract, ContractStatus
from src.models.customer import Customer
from src.models.hardware import Hardware
from src.models.sale import Sale
from src.models.tariff import Tariff

__all__ = ["Customer", "Hardware", "Tariff", "Contract", "ContractStatus", "Sale"]
