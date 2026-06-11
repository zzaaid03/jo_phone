"""Tariff (mobile plan) management menu."""

from src.ui import console_io as io


class TariffMenu:
    def __init__(self, context):
        self._tariffs = context.tariff_service

    def run(self) -> None:
        io.run_menu(
            "JO_PHONE > Tariffs",
            [
                ("List all tariffs", self._list),
                ("Add tariff", self._add),
                ("Edit tariff", self._edit),
                ("Delete tariff", self._delete),
            ],
        )

    # ------------------------------------------------------------------
    def _list(self) -> None:
        rows = [
            (
                t.id,
                t.name,
                t.monthly_fee,
                t.data_display,
                t.minutes_display,
                f"{t.min_duration_months} months",
            )
            for t in self._tariffs.list_all()
        ]
        io.print_table(
            ("Id", "Name", "Fee/Month", "Data", "Minutes", "Min. Duration"),
            rows,
            "All Tariffs",
        )
        io.pause()

    def _add(self) -> None:
        io.print_heading("Add Tariff (-1 = unlimited for data/minutes)")
        tariff = self._tariffs.create(
            name=io.read_str("Name"),
            monthly_fee=io.read_float("Monthly fee (JOD)", min_value=0.01),
            data_gb=io.read_float("Data volume (GB, -1 = unlimited)", min_value=-1),
            minutes=io.read_int("Included minutes (-1 = unlimited)", min_value=-1),
            min_duration_months=io.read_int("Minimum duration (months)", min_value=1),
        )
        io.print_success(f"Tariff #{tariff.id} '{tariff.name}' created.")
        io.pause()

    def _edit(self) -> None:
        tariff = self._tariffs.get(io.read_int("Tariff id", min_value=1))
        io.print_heading(f"Edit Tariff #{tariff.id} (Enter keeps current value)")
        updated = self._tariffs.update(
            tariff.id,
            name=io.read_str("Name", default=tariff.name),
            monthly_fee=io.read_float(
                "Monthly fee (JOD)", default=tariff.monthly_fee, min_value=0.01
            ),
            data_gb=io.read_float(
                "Data volume (GB, -1 = unlimited)", default=tariff.data_gb, min_value=-1
            ),
            minutes=io.read_int(
                "Included minutes (-1 = unlimited)",
                default=tariff.minutes,
                min_value=-1,
            ),
            min_duration_months=io.read_int(
                "Minimum duration (months)",
                default=tariff.min_duration_months,
                min_value=1,
            ),
        )
        io.print_success(f"Tariff #{updated.id} updated.")
        io.pause()

    def _delete(self) -> None:
        tariff = self._tariffs.get(io.read_int("Tariff id", min_value=1))
        if io.confirm(f"Really delete tariff '{tariff.name}'?"):
            self._tariffs.delete(tariff.id)
            io.print_success(f"Tariff '{tariff.name}' deleted.")
        else:
            print("  Cancelled.")
        io.pause()
