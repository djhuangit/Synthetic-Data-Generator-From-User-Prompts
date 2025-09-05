"""Custom exceptions for the synthetic data service."""


class BaseServiceException(Exception):
    """Base exception for service-specific errors."""
    pass


class ValidationError(BaseServiceException):
    """Raised when input validation fails."""
    pass


class SchemaGenerationError(BaseServiceException):
    """Raised when schema generation fails."""
    pass


class RateLimitError(BaseServiceException):
    """Raised when API rate limits are exceeded."""
    pass


class APIConnectionError(BaseServiceException):
    """Raised when external API connection fails."""
    pass


class CacheError(BaseServiceException):
    """Raised when cache operations fail."""
    pass


class ParsingError(BaseServiceException):
    """Raised when response parsing fails."""
    pass