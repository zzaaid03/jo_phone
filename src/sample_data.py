"""Sample data generator for JO_PHONE.

The data is created through the regular services, so all business
rules apply (e.g. stock levels are reduced by sales and bundled
contract devices) and the resulting JSON files are guaranteed to be
consistent.

Usage:  python main.py --seed
"""

from pathlib import Path

from src.app_context import AppContext

DATA_FILES = (
    "customers.json",
    "hardware.json",
    "tariffs.json",
    "contracts.json",
    "sales.json",
)

# (first_name, last_name, email, phone, city)
CUSTOMERS = [
    ("Ahmad", "Khalil", "ahmad.khalil@example.jo", "0791234561", "Amman"),
    ("Layla", "Haddad", "layla.haddad@example.jo", "0781234562", "Irbid"),
    ("Omar", "Nassar", "omar.nassar@example.jo", "0771234563", "Zarqa"),
    ("Rana", "Qasem", "rana.qasem@example.jo", "0791234564", "Amman"),
    ("Yousef", "Tahat", "yousef.tahat@example.jo", "0781234565", "Aqaba"),
    ("Dana", "Shami", "dana.shami@example.jo", "0771234566", "Salt"),
    ("Hassan", "Odeh", "hassan.odeh@example.jo", "0791234567", "Madaba"),
    ("Noor", "Zoubi", "noor.zoubi@example.jo", "0781234568", "Irbid"),
]

# (name, brand, category, price JOD, initial stock)
HARDWARE = [
    ("iPhone 15", "Apple", "Smartphone", 899.00, 14),
    ("Galaxy S24", "Samsung", "Smartphone", 799.00, 12),
    ("Redmi Note 13", "Xiaomi", "Smartphone", 229.00, 22),
    ("Pixel 8", "Google", "Smartphone", 649.00, 8),
    ("Galaxy A55", "Samsung", "Smartphone", 329.00, 17),
    ("AirPods Pro 2", "Apple", "Accessory", 189.00, 27),
    ("Galaxy Buds 2", "Samsung", "Accessory", 99.00, 32),
    ("PowerCore 20K", "Anker", "Accessory", 39.00, 42),
    ("USB-C Cable 1m", "Anker", "Accessory", 9.50, 63),
    ("Rugged Case iPhone 15", "Spigen", "Accessory", 19.00, 38),
]

# (name, monthly fee JOD, data GB (-1 = unlimited), minutes (-1 = unlimited), min months)
TARIFFS = [
    ("JO Basic", 9.99, 5, 200, 12),
    ("JO Smart", 14.99, 15, 500, 12),
    ("JO Plus", 19.99, 30, -1, 18),
    ("JO Max", 27.99, -1, -1, 24),
    ("JO Youth", 7.49, 10, 100, 6),
]

# (customer_id, tariff_id, start_date, duration_months, hardware_id or None)
CONTRACTS = [
    (1, 2, "2026-01-15", 24, 1),  # Ahmad: JO Smart + iPhone 15
    (2, 4, "2026-02-01", 24, 2),  # Layla: JO Max + Galaxy S24
    (3, 1, "2026-02-20", 12, None),  # Omar: JO Basic, SIM only
    (4, 3, "2026-03-05", 18, 4),  # Rana: JO Plus + Pixel 8
    (5, 5, "2026-03-18", 6, None),  # Yousef: JO Youth, SIM only
    (6, 2, "2026-04-02", 12, 5),  # Dana: JO Smart + Galaxy A55
    (7, 1, "2026-04-25", 12, None),  # Hassan: JO Basic, SIM only
    (8, 3, "2026-05-10", 18, 3),  # Noor: JO Plus + Redmi Note 13
]

# (customer_id, hardware_id, quantity, date)
SALES = [
    (1, 6, 1, "2026-01-15"),  # Ahmad buys AirPods with his new iPhone
    (2, 7, 1, "2026-02-01"),
    (3, 3, 1, "2026-02-20"),
    (4, 9, 2, "2026-03-05"),
    (5, 8, 1, "2026-03-18"),
    (1, 10, 1, "2026-04-02"),
    (6, 9, 3, "2026-04-12"),
    (7, 5, 1, "2026-04-25"),
    (8, 6, 1, "2026-05-10"),
    (2, 8, 2, "2026-05-21"),
    (4, 1, 1, "2026-06-01"),
    (6, 7, 1, "2026-06-08"),
]

# Terminated for demo purposes (shows both contract states in reports)
TERMINATED_CONTRACT_IDS = [3]


def seed(data_dir: Path, force: bool = False) -> bool:
    """(Re)create the sample data set.

    Returns True if data was written, False if existing data was kept.
    """
    data_dir = Path(data_dir)
    existing = [name for name in DATA_FILES if (data_dir / name).exists()]
    if existing and not force:
        return False
    for name in DATA_FILES:
        file = data_dir / name
        if file.exists():
            file.unlink()

    context = AppContext(data_dir)

    for first, last, email, phone, city in CUSTOMERS:
        context.customer_service.create(first, last, email, phone, city)

    for name, brand, category, price, stock in HARDWARE:
        context.hardware_service.create(name, brand, category, price, stock)

    for name, fee, data_gb, minutes, min_months in TARIFFS:
        context.tariff_service.create(name, fee, data_gb, minutes, min_months)

    for customer_id, tariff_id, start, months, hardware_id in CONTRACTS:
        context.contract_service.create(
            customer_id, tariff_id, start, months, hardware_id
        )

    for customer_id, hardware_id, quantity, sale_date in SALES:
        context.sale_service.create(customer_id, hardware_id, quantity, sale_date)

    for contract_id in TERMINATED_CONTRACT_IDS:
        context.contract_service.terminate(contract_id)

    return True
