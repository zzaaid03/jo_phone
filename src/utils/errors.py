"""Domain-specific exceptions used across the application.

All errors raised by the service layer derive from :class:`AppError`,
so the UI layer can catch a single exception type and display the
message to the user without crashing the application.
"""


class AppError(Exception):
    """Base class for all expected application errors."""


class ValidationError(AppError):
    """Raised when user input fails validation (format, range, ...)."""


class NotFoundError(AppError):
    """Raised when an entity with the requested id does not exist."""


class BusinessRuleError(AppError):
    """Raised when an operation would violate a business rule
    (e.g. selling more units than are in stock)."""
