# Technical Assumptions

## Repository Structure: Monorepo

Single repository containing all service code. Given the MVP's simplicity (single main.py file), a monorepo approach is most appropriate. All configuration, schemas, and service logic will reside in one repository for easy deployment and maintenance.

## Service Architecture

**Monolithic REST API** - A single FastAPI application handling all functionality. The service will be stateless with file-based schema caching. No microservices or complex orchestration needed for MVP. The architecture prioritizes rapid implementation over scalability, appropriate for a 1-hour build targeting educational use cases.

## Testing Requirements

**Manual Testing Only for MVP** - Given the 1-hour implementation constraint, automated testing is out of scope. Testing will consist of manual API calls with sample requests covering the 5 required domains. Post-MVP, unit tests for schema generation and integration tests for the full pipeline should be added.

## Additional Technical Assumptions and Requests

- **Language:** Python 3.12+ (specified in brief)
- **Framework:** FastAPI for REST API implementation
- **AI Integration:** OpenAI Python SDK for GPT-4o-mini integration
- **Data Generation:** Faker library for synthetic data creation
- **Data Processing:** Pandas for CSV generation and data manipulation
- **Configuration:** Environment variables for OpenAI API key management
- **Caching:** JSON file-based schema storage with hash-based keys
- **Deployment:** Local development server via uvicorn for MVP
- **Error Handling:** Basic try-catch blocks with JSON error responses
- **Logging:** Console logging only for MVP debugging
- **Dependencies:** Managed via pyproject.toml with uv for virtual environment and dependency management
- **CORS:** Enabled for all origins to support various client testing tools
