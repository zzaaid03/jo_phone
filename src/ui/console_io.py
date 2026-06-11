"""Console input/output helpers shared by all menus.

All ``read_*`` functions loop until the user enters a valid value.
If a ``default`` is given, pressing Enter accepts it (used for edit
forms, where the default is the current value).
"""

from typing import Callable, List, Optional, Sequence, Tuple

from src.utils.errors import AppError, ValidationError

LINE = "=" * 49


def print_banner() -> None:
    print(LINE)
    print("JO_PHONE".center(49))
    print("Mobile Shop Management System".center(49))
    print(LINE)
    print("Manage Customers, Hardware, Tariffs,")
    print("Contracts and Sales")
    print()
    print("Version 1.0")
    print("Developed for WIB22-440")
    print(LINE)


def print_heading(title: str) -> None:
    print()
    print(f"--- {title} ---")


def print_error(message: str) -> None:
    print(f"  [!] {message}")


def print_success(message: str) -> None:
    print(f"  [OK] {message}")


def pause() -> None:
    input("\nPress Enter to continue...")


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ("y", "yes")


# ----------------------------------------------------------------------
# Input helpers
# ----------------------------------------------------------------------
def read_str(
    prompt: str,
    default: Optional[str] = None,
    validator: Optional[Callable[[str], str]] = None,
) -> str:
    """Read a string; applies the validator (which may clean the value)."""
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            raw = str(default)
        try:
            return validator(raw) if validator else raw
        except ValidationError as error:
            print_error(str(error))


def read_int(
    prompt: str,
    default: Optional[int] = None,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            value = int(raw)
        except ValueError:
            print_error("Please enter a whole number.")
            continue
        if min_value is not None and value < min_value:
            print_error(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print_error(f"Value must be at most {max_value}.")
            continue
        return value


def read_float(
    prompt: str,
    default: Optional[float] = None,
    min_value: Optional[float] = None,
) -> float:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip().replace(",", ".")
        if not raw and default is not None:
            return default
        try:
            value = float(raw)
        except ValueError:
            print_error("Please enter a number (e.g. 19.99).")
            continue
        if min_value is not None and value < min_value:
            print_error(f"Value must be at least {min_value}.")
            continue
        return value


def read_optional_int(prompt: str) -> Optional[int]:
    """Read an int, or None when the user just presses Enter."""
    while True:
        raw = input(f"{prompt} (Enter to skip): ").strip()
        if not raw:
            return None
        try:
            return int(raw)
        except ValueError:
            print_error("Please enter a whole number or leave empty.")


# ----------------------------------------------------------------------
# Table rendering
# ----------------------------------------------------------------------
def print_table(
    headers: Sequence[str], rows: Sequence[Sequence[object]], title: str = ""
) -> None:
    if title:
        print_heading(title)
    if not rows:
        print("  (no entries)")
        return
    str_rows = [[_cell(value) for value in row] for row in rows]
    widths = [len(header) for header in headers]
    for row in str_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    line = "  " + " | ".join(
        header.ljust(widths[index]) for index, header in enumerate(headers)
    )
    print(line)
    print("  " + "-+-".join("-" * width for width in widths))
    for row in str_rows:
        print(
            "  "
            + " | ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))
        )


def _cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


# ----------------------------------------------------------------------
# Generic menu loop
# ----------------------------------------------------------------------
MenuOption = Tuple[str, Callable[[], None]]


def run_menu(title: str, options: List[MenuOption], exit_label: str = "Back") -> None:
    """Display a numbered menu in a loop; option 0 leaves the menu.

    Expected application errors (AppError) raised by the chosen action
    are caught and shown to the user, so the menu never crashes.
    """
    while True:
        print()
        print(LINE)
        print(f"  {title}")
        print(LINE)
        for index, (label, _action) in enumerate(options, start=1):
            print(f"  {index}. {label}")
        print(f"  0. {exit_label}")
        choice = read_int("Choose an option", min_value=0, max_value=len(options))
        if choice == 0:
            return
        _label, action = options[choice - 1]
        try:
            action()
        except AppError as error:
            print_error(str(error))
            pause()
