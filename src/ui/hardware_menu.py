"""Hardware (inventory) management menu."""

from typing import Optional

from src.models.hardware import CATEGORIES
from src.ui import console_io as io


class HardwareMenu:
    def __init__(self, context):
        self._hardware = context.hardware_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Hardware",
            [
                ("List all hardware", self._list),
                ("Search hardware", self._search),
                ("Add hardware", self._add),
                ("Edit hardware", self._edit),
                ("Restock hardware", self._restock),
                ("Delete hardware", self._delete),
                ("Show low-stock items", self._low_stock),
            ],
        )

    # ------------------------------------------------------------------
    def _list(self) -> None:
        self._print_hardware(self._hardware.list_all(), "All Hardware")
        io.pause()

    def _search(self) -> None:
        term = io.read_str("Search term (name or brand)")
        self._print_hardware(self._hardware.search(term), f"Results for '{term}'")
        io.pause()

    def _add(self) -> None:
        io.print_heading("Add Hardware")
        hardware = self._hardware.create(
            name=io.read_str("Name"),
            brand=io.read_str("Brand"),
            category=self._read_category(),
            price=io.read_float("Price (JOD)", min_value=0.01),
            stock=io.read_int("Initial stock", min_value=0),
        )
        io.print_success(f"Hardware #{hardware.id} '{hardware.name}' created.")
        io.pause()

    def _edit(self) -> None:
        hardware = self._hardware.get(io.read_int("Hardware id", min_value=1))
        io.print_heading(f"Edit Hardware #{hardware.id} (Enter keeps current value)")
        updated = self._hardware.update(
            hardware.id,
            name=io.read_str("Name", default=hardware.name),
            brand=io.read_str("Brand", default=hardware.brand),
            category=self._read_category(default=hardware.category),
            price=io.read_float("Price (JOD)", default=hardware.price, min_value=0.01),
            stock=io.read_int("Stock", default=hardware.stock, min_value=0),
        )
        io.print_success(f"Hardware #{updated.id} updated.")
        io.pause()

    def _restock(self) -> None:
        hardware = self._hardware.get(io.read_int("Hardware id", min_value=1))
        quantity = io.read_int(
            f"Units to add to '{hardware.name}' (current: {hardware.stock})",
            min_value=1,
        )
        updated = self._hardware.restock(hardware.id, quantity)
        io.print_success(f"'{updated.name}' restocked - new stock: {updated.stock}.")
        io.pause()

    def _delete(self) -> None:
        hardware = self._hardware.get(io.read_int("Hardware id", min_value=1))
        if io.confirm(f"Really delete '{hardware.name}'?"):
            self._hardware.delete(hardware.id)
            io.print_success(f"Hardware '{hardware.name}' deleted.")
        else:
            print("  Cancelled.")
        io.pause()

    def _low_stock(self) -> None:
        self._print_hardware(self._hardware.list_low_stock(), "Low-Stock Items")
        io.pause()

    # ------------------------------------------------------------------
    @staticmethod
    def _read_category(default: Optional[str] = None) -> str:
        return io.read_str(f"Category ({'/'.join(CATEGORIES)})", default=default)

    @staticmethod
    def _print_hardware(items, title: str) -> None:
        rows = [
            (h.id, h.name, h.brand, h.category, h.price, h.stock, h.stock_value)
            for h in items
        ]
        io.print_table(
            ("Id", "Name", "Brand", "Category", "Price", "Stock", "Stock Value"),
            rows,
            title,
        )
