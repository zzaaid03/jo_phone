"""JO_PHONE - Mobile Shop Management System.

Entry point of the application.

Usage:
    python main.py            start the application
    python main.py --seed     reset the data files with fresh sample data
"""

import argparse
import sys
from pathlib import Path

from src.sample_data import seed

from src.app_context import AppContext
from src.ui.main_menu import MainMenu

DATA_DIR = Path(__file__).resolve().parent / "data"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="JO_PHONE",
        description="JO_PHONE - Mobile Shop Management System (WIB22-440)",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="reset the data files in ./data with fresh sample data",
    )
    args = parser.parse_args()

    if args.seed:
        seed(DATA_DIR, force=True)
        print(f"Sample data has been generated in: {DATA_DIR}")

    # First start ever (no data files yet): provide sample data so the
    # application is immediately usable and demonstrable.
    if seed(DATA_DIR, force=False):
        print("No data found - created the JO_PHONE sample data set.")

    context = AppContext(DATA_DIR)
    try:
        MainMenu(context).run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nJO_PHONE closed. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
