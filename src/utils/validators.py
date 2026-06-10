"""Reusable validation functions.

Each validator returns the cleaned value on success and raises
:class:`ValidationError` with a human-readable message on failure.
"""

import re
from datetime import date, datetime

from src.utils.errors import ValidationError

# Simple, pragmatic e-mail pattern (full RFC 5322 is overkill here).
_EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

# Jordanian mobile numbers: 07XXXXXXXX or +9627XXXXXXXX
# (second digit of the subscriber part must be 7, 8 or 9).
_PHONE_RE = re.compile(r"^(?:\+962|0)7[789]\d{7}$")

DATE_FORMAT = "%Y-%m-%d"


def require_text(
    value: str, field: str, min_length: int = 1, max_length: int = 60
) -> str:
    value = (value or "").strip()
    if len(value) < min_length:
        raise ValidationError(f"{field} must not be empty.")
    if len(value) > max_length:
        raise ValidationError(f"{field} must be at most {max_length} characters long.")
    return value


def validate_email(value: str) -> str:
    value = (value or "").strip().lower()
    if not _EMAIL_RE.match(value):
        raise ValidationError(f"'{value}' is not a valid e-mail address.")
    return value


def validate_phone(value: str) -> str:
    value = (value or "").strip().replace(" ", "")
    if not _PHONE_RE.match(value):
        raise ValidationError(
            f"'{value}' is not a valid Jordanian mobile number "
            "(expected 07XXXXXXXX or +9627XXXXXXXX)."
        )
    return value


def validate_date(value: str, field: str = "Date") -> str:
    value = (value or "").strip()
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        raise ValidationError(
            f"{field} must use the format YYYY-MM-DD (e.g. {date.today()})."
        )
    return value


def validate_positive_number(value: float, field: str) -> float:
    if value is None or value <= 0:
        raise ValidationError(f"{field} must be greater than 0.")
    return value


def validate_non_negative_number(value: float, field: str) -> float:
    if value is None or value < 0:
        raise ValidationError(f"{field} must be 0 or greater.")
    return value


def validate_positive_int(value: int, field: str) -> int:
    if value is None or int(value) != value or value <= 0:
        raise ValidationError(f"{field} must be a whole number greater than 0.")
    return int(value)
