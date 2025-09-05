# Security

## Input Validation

- **Validation Library:** Pydantic (built into FastAPI)
- **Validation Location:** API boundary before business logic processing
- **Required Rules:**
  - All external inputs MUST be validated against defined schemas
  - Description length limits enforced (10-4000 characters)
  - Row count limits enforced (1-10000 rows)

## Authentication & Authorization

- **Auth Method:** None for MVP (educational use case)
- **Session Management:** Stateless API design
- **Required Patterns:**
  - No authentication required per PRD specification
  - Future implementation should consider API key authentication

## Secrets Management

- **Development:** .env file with python-dotenv (git-ignored)
- **Production:** Environment variables (future implementation)
- **Code Requirements:**
  - NEVER hardcode OpenAI API keys
  - Access via environment variables only
  - No secrets in logs or error messages

## API Security

- **Rate Limiting:** Not implemented for MVP (delegated to OpenAI API limits)
- **CORS Policy:** Allow all origins for educational testing flexibility
- **Security Headers:** Basic FastAPI defaults
- **HTTPS Enforcement:** Not required for local development MVP

## Data Protection

- **Encryption at Rest:** Not implemented for MVP (local file system)
- **Encryption in Transit:** HTTPS for OpenAI API calls
- **PII Handling:** No personal data collection or storage
- **Logging Restrictions:** No user descriptions or generated data in logs

## Dependency Security

- **Scanning Tool:** Not implemented for MVP
- **Update Policy:** Pin specific versions in pyproject.toml
- **Approval Process:** Manual review for new dependencies
