"""Top-level menu of the JO_PHONE application."""

from src.ui import console_io as io
from src.ui.contract_menu import ContractMenu
from src.ui.customer_menu import CustomerMenu
from src.ui.hardware_menu import HardwareMenu
from src.ui.report_menu import ReportMenu
from src.ui.sale_menu import SaleMenu
from src.ui.tariff_menu import TariffMenu


class MainMenu:
    def __init__(self, context):
        self._customer_menu = CustomerMenu(context)
        self._hardware_menu = HardwareMenu(context)
        self._tariff_menu = TariffMenu(context)
        self._contract_menu = ContractMenu(context)
        self._sale_menu = SaleMenu(context)
        self._report_menu = ReportMenu(context)

    def run(self) -> None:
        io.print_banner()
        io.run_menu(
            "JO_PHONE - Main Menu",
            [
                ("Customers", self._customer_menu.run),
                ("Hardware", self._hardware_menu.run),
                ("Tariffs", self._tariff_menu.run),
                ("Contracts", self._contract_menu.run),
                ("Sales", self._sale_menu.run),
                ("Reports", self._report_menu.run),
            ],
            exit_label="Exit",
        )
        print("\nThank you for using JO_PHONE. Goodbye!")
