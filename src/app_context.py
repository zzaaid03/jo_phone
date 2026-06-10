"""Application wiring: builds repositories and services for a data directory.

This acts as a lightweight dependency-injection container, so the UI,
tests and the sample-data generator all assemble the application in
exactly the same way.
"""

from pathlib import Path

from src.models import Contract, Customer, Hardware, Sale, Tariff
from src.services import (
    ContractService,
    CustomerService,
    HardwareService,
    ReportService,
    SaleService,
    TariffService,
)
from src.storage import JsonRepository


class AppContext:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Repositories (one JSON file per entity)
        self.customer_repo = JsonRepository(self.data_dir / "customers.json", Customer)
        self.hardware_repo = JsonRepository(self.data_dir / "hardware.json", Hardware)
        self.tariff_repo = JsonRepository(self.data_dir / "tariffs.json", Tariff)
        self.contract_repo = JsonRepository(self.data_dir / "contracts.json", Contract)
        self.sale_repo = JsonRepository(self.data_dir / "sales.json", Sale)

        # Services (business logic)
        self.customer_service = CustomerService(self.customer_repo, self.contract_repo)
        self.hardware_service = HardwareService(
            self.hardware_repo, self.contract_repo, self.sale_repo
        )
        self.tariff_service = TariffService(self.tariff_repo, self.contract_repo)
        self.contract_service = ContractService(
            self.contract_repo,
            self.customer_service,
            self.tariff_service,
            self.hardware_service,
        )
        self.sale_service = SaleService(
            self.sale_repo, self.customer_service, self.hardware_service
        )
        self.report_service = ReportService(
            self.customer_repo,
            self.hardware_repo,
            self.tariff_repo,
            self.contract_repo,
            self.sale_repo,
        )
