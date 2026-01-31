"""
Custom exceptions for the Text-to-SQL agent.

This module defines custom exception classes for better
error handling and debugging.
"""


class TextToSQLError(Exception):
    """Base exception for all Text-to-SQL errors."""
    pass


class ConfigurationError(TextToSQLError):
    """Raised when there's a configuration problem."""
    pass


class DatabaseError(TextToSQLError):
    """Raised when there's a database-related error."""
    pass


class SQLGenerationError(TextToSQLError):
    """Raised when SQL generation fails."""
    pass


class SQLExecutionError(TextToSQLError):
    """Raised when SQL execution fails."""
    pass


class UnsafeQueryError(TextToSQLError):
    """Raised when attempting to execute an unsafe SQL query."""
    pass


class SchemaRetrievalError(DatabaseError):
    """Raised when database schema cannot be retrieved."""
    pass
