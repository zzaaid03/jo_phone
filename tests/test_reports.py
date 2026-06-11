"""Tests for the reporting service, including a check that the shipped
sample data set is generated consistently."""

import tempfile
import unittest
from pathlib import Path

from src.app_context import AppContext
from src.sample_data import seed


class ReportServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.ctx = AppContext(Path(self._tmp.name))
        self.customer = self.ctx.customer_service.create(
            "Layla", "Haddad", "layla@example.jo", "0781234562", "Irbid"
        )
        self.phone = self.ctx.hardware_service.create(
            "Galaxy S24", "Samsung", "Smartphone", 799.0, 10
        )
        self.buds = self.ctx.hardware_service.create(
            "Galaxy Buds 2", "Samsung", "Accessory", 99.0, 3
        )
        self.tariff = self.ctx.tariff_service.create("JO Max", 27.99, -1, -1, 24)

    def test_sales_summary_totals(self):
        self.ctx.sale_service.create(self.customer.id, self.phone.id, 1, "2026-05-01")
        self.ctx.sale_service.create(self.customer.id, self.buds.id, 2, "2026-06-01")
        report = self.ctx.report_service.sales_summary()
        self.assertEqual(report["sale_count"], 2)
        self.assertEqual(report["total_revenue"], 799.0 + 2 * 99.0)
        self.assertEqual(report["best_seller"]["hardware"], "Galaxy S24")
        self.assertEqual(report["by_month"], {"2026-05": 799.0, "2026-06": 198.0})

    def test_contract_summary_mrr(self):
        self.ctx.contract_service.create(
            self.customer.id, self.tariff.id, "2026-06-01", 24
        )
        report = self.ctx.report_service.contract_summary()
        self.assertEqual(report["active_contracts"], 1)
        self.assertEqual(report["monthly_recurring_revenue"], 27.99)
        self.assertEqual(report["committed_value"], round(27.99 * 24, 2))

    def test_inventory_report_flags_low_stock(self):
        report = self.ctx.report_service.inventory_report()
        low_names = [item["name"] for item in report["low_stock_items"]]
        self.assertEqual(low_names, ["Galaxy Buds 2"])
        self.assertEqual(report["total_units"], 13)

    def test_customer_overview_combines_sales_and_contracts(self):
        self.ctx.sale_service.create(self.customer.id, self.buds.id, 1, "2026-06-01")
        self.ctx.contract_service.create(
            self.customer.id, self.tariff.id, "2026-06-01", 24, self.phone.id
        )
        row = self.ctx.report_service.customer_overview()[0]
        self.assertEqual(row["name"], "Layla Haddad")
        self.assertEqual(row["purchases_total"], 99.0)
        self.assertEqual(row["committed_contract_value"], round(27.99 * 24 + 799.0, 2))


class SampleDataTests(unittest.TestCase):
    def test_seed_creates_consistent_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            self.assertTrue(seed(data_dir, force=True))
            ctx = AppContext(data_dir)
            self.assertEqual(ctx.customer_repo.count(), 8)
            self.assertEqual(ctx.hardware_repo.count(), 10)
            self.assertEqual(ctx.tariff_repo.count(), 5)
            self.assertEqual(ctx.contract_repo.count(), 8)
            self.assertEqual(ctx.sale_repo.count(), 12)
            # seeding without force keeps the existing data
            self.assertFalse(seed(data_dir, force=False))
            # no negative stock anywhere
            for hardware in ctx.hardware_service.list_all():
                self.assertGreaterEqual(hardware.stock, 0)


if __name__ == "__main__":
    unittest.main()
