"""Contract management menu."""

from datetime import date

from src.ui import console_io as io
from src.utils import validators


class ContractMenu:
    def __init__(self, context):
        self._contracts = context.contract_service
        self._customers = context.customer_service
        self._tariffs = context.tariff_service
        self._hardware = context.hardware_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Contracts",
            [
                ("List all contracts", self._list_all),
                ("List active contracts", self._list_active),
                ("Create contract", self._create),
                ("Terminate contract", self._terminate),
            ],
        )

    # ------------------------------------------------------------------
    def _list_all(self) -> None:
        self._print_contracts(self._contracts.list_all(), "All Contracts")
        io.pause()

    def _list_active(self) -> None:
        self._print_contracts(self._contracts.list_active(), "Active Contracts")
        io.pause()

    def _create(self) -> None:
        io.print_heading("Create Contract")

        customers = self._customers.list_all()
        io.print_table(
            ("Id", "Name"),
            [(c.id, c.full_name) for c in customers],
            "Customers",
        )
        customer_id = io.read_int("Customer id", min_value=1)
        self._customers.get(customer_id)  # fail early with a clear message

        tariffs = self._tariffs.list_all()
        io.print_table(
            ("Id", "Name", "Fee/Month", "Min. Months"),
            [(t.id, t.name, t.monthly_fee, t.min_duration_months) for t in tariffs],
            "Tariffs",
        )
        tariff_id = io.read_int("Tariff id", min_value=1)
        tariff = self._tariffs.get(tariff_id)

        start_date = io.read_str(
            "Start date (YYYY-MM-DD)",
            default=str(date.today()),
            validator=validators.validate_date,
        )
        duration = io.read_int(
            "Duration in months", default=tariff.min_duration_months, min_value=1
        )

        hardware_id = None
        if io.confirm("Bundle a device with this contract?"):
            available = [h for h in self._hardware.list_all() if h.stock > 0]
            io.print_table(
                ("Id", "Name", "Price", "Stock"),
                [(h.id, h.name, h.price, h.stock) for h in available],
                "Available Hardware",
            )
            hardware_id = io.read_optional_int("Hardware id")

        contract = self._contracts.create(
            customer_id=customer_id,
            tariff_id=tariff_id,
            start_date=start_date,
            duration_months=duration,
            hardware_id=hardware_id,
        )
        details = self._contracts.describe(contract)
        io.print_success(
            f"Contract #{contract.id} created for {details['customer']} "
            f"({details['tariff']}, {contract.duration_months} months, "
            f"total value {contract.total_value:.2f} JOD)."
        )
        io.pause()

    def _terminate(self) -> None:
        contract = self._contracts.get(io.read_int("Contract id", min_value=1))
        details = self._contracts.describe(contract)
        print(
            f"  Contract #{contract.id}: {details['customer']} - "
            f"{details['tariff']} ({contract.status})"
        )
        if io.confirm("Really terminate this contract?"):
            self._contracts.terminate(contract.id)
            io.print_success(f"Contract #{contract.id} terminated.")
        else:
            print("  Cancelled.")
        io.pause()

    # ------------------------------------------------------------------
    def _print_contracts(self, contracts, title: str) -> None:
        rows = [
            (
                d["id"],
                d["customer"],
                d["tariff"],
                d["hardware"],
                d["start"],
                d["end"],
                d["monthly_fee"],
                d["total_value"],
                d["status"],
            )
            for d in (self._contracts.describe(c) for c in contracts)
        ]
        io.print_table(
            (
                "Id",
                "Customer",
                "Tariff",
                "Hardware",
                "Start",
                "End",
                "Fee/Month",
                "Total Value",
                "Status",
            ),
            rows,
            title,
        )
