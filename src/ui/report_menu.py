"""Reports menu: renders the data produced by ReportService."""

from src.ui import console_io as io


class ReportMenu:
    def __init__(self, context):
        self._reports = context.report_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Reports",
            [
                ("Inventory & low-stock report", self._inventory),
                ("Sales summary", self._sales),
                ("Contracts & recurring revenue", self._contracts),
                ("Customer overview", self._customers),
            ],
        )

    # ------------------------------------------------------------------
    def _inventory(self) -> None:
        report = self._reports.inventory_report()
        rows = [
            (
                item["id"],
                item["name"],
                item["brand"],
                item["category"],
                item["price"],
                item["stock"],
                item["stock_value"],
                "LOW" if item["low_stock"] else "",
            )
            for item in report["items"]
        ]
        io.print_table(
            ("Id", "Name", "Brand", "Category", "Price", "Stock", "Value", "Alert"),
            rows,
            "Inventory Report",
        )
        print(f"\n  Total units in stock: {report['total_units']}")
        print(f"  Total inventory value: {report['total_value']:.2f} JOD")
        print(
            f"  Low-stock items (<= {report['threshold']} units): "
            f"{len(report['low_stock_items'])}"
        )
        io.pause()

    def _sales(self) -> None:
        report = self._reports.sales_summary()
        io.print_heading("Sales Summary")
        print(f"  Number of sales: {report['sale_count']}")
        print(f"  Total revenue:   {report['total_revenue']:.2f} JOD")
        if report["best_seller"]:
            best = report["best_seller"]
            print(
                f"  Best seller:     {best['hardware']} "
                f"({best['quantity']} units, {best['revenue']:.2f} JOD)"
            )
        io.print_table(
            ("Hardware", "Units Sold", "Revenue"),
            [
                (row["hardware"], row["quantity"], row["revenue"])
                for row in report["by_hardware"]
            ],
            "Revenue by Hardware",
        )
        io.print_table(
            ("Month", "Revenue"),
            list(report["by_month"].items()),
            "Revenue by Month",
        )
        io.pause()

    def _contracts(self) -> None:
        report = self._reports.contract_summary()
        io.print_heading("Contract Summary")
        print(f"  Total contracts:      {report['total_contracts']}")
        print(f"  Active contracts:     {report['active_contracts']}")
        print(f"  Terminated contracts: {report['terminated_contracts']}")
        print(
            "  Monthly recurring revenue: "
            f"{report['monthly_recurring_revenue']:.2f} JOD"
        )
        print(f"  Committed contract value:  {report['committed_value']:.2f} JOD")
        io.print_table(
            ("Tariff", "Fee/Month", "Active Contracts", "Monthly Revenue"),
            [
                (
                    row["tariff"],
                    row["monthly_fee"],
                    row["active_contracts"],
                    row["monthly_revenue"],
                )
                for row in report["by_tariff"]
            ],
            "Active Contracts by Tariff",
        )
        io.pause()

    def _customers(self) -> None:
        rows = [
            (
                row["id"],
                row["name"],
                row["city"],
                row["active_contracts"],
                row["purchases"],
                row["purchases_total"],
                row["committed_contract_value"],
                row["customer_value"],
            )
            for row in self._reports.customer_overview()
        ]
        io.print_table(
            (
                "Id",
                "Name",
                "City",
                "Active Contracts",
                "Purchases",
                "Purchases (JOD)",
                "Contract Value (JOD)",
                "Total Value (JOD)",
            ),
            rows,
            "Customer Overview (sorted by total value)",
        )
        io.pause()
