# Coding Standards

## Core Standards

- **Languages & Runtimes:** Python 3.12.0 with type hints mandatory
- **Style & Linting:** Black formatter, no linter for MVP (time constraint)
- **Test Organization:** pytest structure ready for post-MVP implementation

## Critical Rules

- **Never log OpenAI API keys:** All sensitive data excluded from logs and error messages
- **Always use type hints:** Function signatures must include parameter and return types
- **File operations must use context managers:** Ensure proper resource cleanup
- **Cache operations must be atomic:** Use file locking to prevent corruption
- **All external API calls must have timeouts:** Prevent hanging requests
