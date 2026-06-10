"""Unit tests for the validation helpers."""

import unittest

from src.utils import validators
from src.utils.errors import ValidationError


class ValidatorTests(unittest.TestCase):
    def test_valid_email_is_normalized(self):
        self.assertEqual(
            validators.validate_email("  Ahmad.Khalil@Example.JO "),
            "ahmad.khalil@example.jo",
        )

    def test_invalid_email_raises(self):
        for bad in ("", "no-at-sign", "a@b", "a@@b.com"):
            with self.assertRaises(ValidationError):
                validators.validate_email(bad)

    def test_valid_jordanian_phone_numbers(self):
        self.assertEqual(validators.validate_phone("0791234567"), "0791234567")
        self.assertEqual(validators.validate_phone("+962781234567"), "+962781234567")

    def test_invalid_phone_raises(self):
        for bad in ("", "1234", "0751234567", "07912345678"):
            with self.assertRaises(ValidationError):
                validators.validate_phone(bad)

    def test_date_validation(self):
        self.assertEqual(validators.validate_date("2026-06-10"), "2026-06-10")
        with self.assertRaises(ValidationError):
            validators.validate_date("10.06.2026")
        with self.assertRaises(ValidationError):
            validators.validate_date("2026-13-01")

    def test_required_text(self):
        self.assertEqual(validators.require_text("  Amman ", "City"), "Amman")
        with self.assertRaises(ValidationError):
            validators.require_text("   ", "City")

    def test_positive_numbers(self):
        self.assertEqual(validators.validate_positive_number(9.99, "Fee"), 9.99)
        with self.assertRaises(ValidationError):
            validators.validate_positive_number(0, "Fee")
        with self.assertRaises(ValidationError):
            validators.validate_positive_int(-3, "Months")


if __name__ == "__main__":
    unittest.main()
