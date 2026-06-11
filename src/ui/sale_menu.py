"""Sales (direct hardware sales) menu."""

from datetime import date

from src.ui import console_io as io
from src.utils import validators


class SaleMenu:
    def __init__(self, context):
        self._sales = context.sale_service
        self._customers = context.customer_service
        self._hardware = context.hardware_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Sales",
            [
                ("List all sales", self._list),
                ("List sales of a customer", self._list_by_customer),
                ("Record new sale", self._create),
            ],
        )

    # ------------------------------------------------------------------
    def _list(self) -> None:
        self._print_sales(self._sales.list_all(), "All Sales")
        io.pause()

    def _list_by_customer(self) -> None:
        customer = self._customers.get(io.read_int("Customer id", min_value=1))
        self._print_sales(
            self._sales.list_by_customer(customer.id),
            f"Sales for {customer.full_name}",
        )
        io.pause()

    def _create(self) -> None:
        io.print_heading("Record New Sale")

        customers = self._customers.list_all()
        io.print_table(
            ("Id", "Name"),
            [(c.id, c.full_name) for c in customers],
            "Customers",
        )
        customer_id = io.read_int("Customer id", min_value=1)
        self._customers.get(customer_id)  # fail early with a clear message

        available = [h for h in self._hardware.list_all() if h.stock > 0]
        io.print_table(
            ("Id", "Name", "Price", "Stock"),
            [(h.id, h.name, h.price, h.stock) for h in available],
            "Available Hardware",
        )
        hardware_id = io.read_int("Hardware id", min_value=1)
        quantity = io.read_int("Quantity", default=1, min_value=1)
        sale_date = io.read_str(
            "Sale date (YYYY-MM-DD)",
            default=str(date.today()),
            validator=validators.validate_date,
        )

        sale = self._sales.create(customer_id, hardware_id, quantity, sale_date)
        details = self._sales.describe(sale)
        io.print_success(
            f"Sale #{sale.id} recorded: {sale.quantity} x {details['hardware']} "
            f"for {details['customer']} - total {sale.total:.2f} JOD."
        )
        io.pause()

    # ------------------------------------------------------------------
    def _print_sales(self, sales, title: str) -> None:
        rows = [
            (
                d["id"],
                d["date"],
                d["customer"],
                d["hardware"],
                d["quantity"],
                d["unit_price"],
                d["total"],
            )
            for d in (self._sales.describe(s) for s in sales)
        ]
        io.print_table(
            ("Id", "Date", "Customer", "Hardware", "Qty", "Unit Price", "Total"),
            rows,
            title,
        )
        total = sum(s.total for s in sales)
        if sales:
            print(f"\n  Total revenue: {total:.2f} JOD")
