# Error Handling Strategy

## General Approach

- **Error Model:** Exception-based error handling with structured error responses
- **Exception Hierarchy:** Custom exceptions inheriting from base ApplicationError class
- **Error Propagation:** Bubble up with context, transform to HTTP responses at API boundary

## Logging Standards

- **Library:** Python standard logging module
- **Format:** Structured JSON logging for consistency
- **Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL with appropriate usage
- **Required Context:**
  - Correlation ID: UUID4 format for request tracking
  - Service Context: Component and method names
  - User Context: Request IP and timestamp (no personal data)

## Error Handling Patterns

### External API Errors

- **Retry Policy:** Exponential backoff with max 3 attempts for OpenAI API calls
- **Circuit Breaker:** Not implemented for MVP (single external dependency)
- **Timeout Configuration:** 30 seconds for OpenAI API requests, 10 seconds for file operations
- **Error Translation:** Map OpenAI API errors to user-friendly messages

### Business Logic Errors

- **Custom Exceptions:** ValidationError, SchemaGenerationError, DataGenerationError, CacheError
- **User-Facing Errors:** Structured JSON responses with error_type and user-friendly messages
- **Error Codes:** HTTP status codes (400, 429, 500) with detailed error_type field

### Data Consistency

- **Transaction Strategy:** File-level locking for atomic cache operations
- **Compensation Logic:** Cache rollback on write failures
- **Idempotency:** Hash-based cache keys ensure identical requests produce identical results
