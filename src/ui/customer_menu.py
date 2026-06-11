"""Customer management menu."""

from src.ui import console_io as io
from src.utils import validators


class CustomerMenu:
    def __init__(self, context):
        self._customers = context.customer_service
        self._contracts = context.contract_service
        self._sales = context.sale_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Customers",
            [
                ("List all customers", self._list),
                ("Search customers", self._search),
                ("Show customer details", self._details),
                ("Add customer", self._add),
                ("Edit customer", self._edit),
                ("Delete customer", self._delete),
            ],
        )

    # ------------------------------------------------------------------
    def _list(self) -> None:
        self._print_customers(self._customers.list_all(), "All Customers")
        io.pause()

    def _search(self) -> None:
        term = io.read_str("Search term (name, e-mail or city)")
        self._print_customers(self._customers.search(term), f"Results for '{term}'")
        io.pause()

    def _details(self) -> None:
        customer = self._customers.get(io.read_int("Customer id", min_value=1))
        io.print_heading(f"Customer #{customer.id}: {customer.full_name}")
        print(f"  E-mail: {customer.email}")
        print(f"  Phone:  {customer.phone}")
        print(f"  City:   {customer.city}")

        contracts = self._contracts.list_by_customer(customer.id)
        rows = [
            (
                d["id"],
                d["tariff"],
                d["hardware"],
                d["start"],
                d["end"],
                d["monthly_fee"],
                d["status"],
            )
            for d in (self._contracts.describe(c) for c in contracts)
        ]
        io.print_table(
            ("Id", "Tariff", "Hardware", "Start", "End", "Fee/Month", "Status"),
            rows,
            "Contracts",
        )

        sales = self._sales.list_by_customer(customer.id)
        rows = [
            (d["id"], d["date"], d["hardware"], d["quantity"], d["total"])
            for d in (self._sales.describe(s) for s in sales)
        ]
        io.print_table(("Id", "Date", "Hardware", "Qty", "Total"), rows, "Purchases")
        io.pause()

    def _add(self) -> None:
        io.print_heading("Add Customer")
        customer = self._customers.create(
            first_name=io.read_str("First name"),
            last_name=io.read_str("Last name"),
            email=io.read_str("E-mail", validator=validators.validate_email),
            phone=io.read_str(
                "Phone (07XXXXXXXX)", validator=validators.validate_phone
            ),
            city=io.read_str("City"),
        )
        io.print_success(f"Customer #{customer.id} '{customer.full_name}' created.")
        io.pause()

    def _edit(self) -> None:
        customer = self._customers.get(io.read_int("Customer id", min_value=1))
        io.print_heading(f"Edit Customer #{customer.id} (Enter keeps current value)")
        updated = self._customers.update(
            customer.id,
            first_name=io.read_str("First name", default=customer.first_name),
            last_name=io.read_str("Last name", default=customer.last_name),
            email=io.read_str(
                "E-mail", default=customer.email, validator=validators.validate_email
            ),
            phone=io.read_str(
                "Phone", default=customer.phone, validator=validators.validate_phone
            ),
            city=io.read_str("City", default=customer.city),
        )
        io.print_success(f"Customer #{updated.id} updated.")
        io.pause()

    def _delete(self) -> None:
        customer = self._customers.get(io.read_int("Customer id", min_value=1))
        if io.confirm(f"Really delete '{customer.full_name}'?"):
            self._customers.delete(customer.id)
            io.print_success(f"Customer '{customer.full_name}' deleted.")
        else:
            print("  Cancelled.")
        io.pause()

    # ------------------------------------------------------------------
    @staticmethod
    def _print_customers(customers, title: str) -> None:
        rows = [(c.id, c.full_name, c.email, c.phone, c.city) for c in customers]
        io.print_table(("Id", "Name", "E-mail", "Phone", "City"), rows, title)
