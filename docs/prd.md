# Synthetic Data Generation Service Product Requirements Document (PRD)

## Goals and Background Context

### Goals
- Enable data science learners to generate custom synthetic datasets through natural language descriptions in under 2 minutes
- Eliminate the technical barrier to synthetic data creation by abstracting schema definition complexity
- Provide 1000+ row CSV datasets that support meaningful ML/data science exercises (train/test splitting, pattern detection)
- Reduce data acquisition time from hours to minutes for learning projects
- Support diverse domain-specific data generation (e-commerce, healthcare, finance, education, social media)
- Minimize API costs through intelligent schema caching while maintaining generation quality

### Background Context

Data science and ML learners currently face a significant bottleneck in their educational journey: acquiring appropriate datasets for their projects. The overreliance on common public datasets (Titanic, Iris) limits portfolio differentiation, while the complexity of existing data generation tools creates unnecessary barriers to learning. This service addresses the gap by combining GPT-4o-mini's natural language understanding with Faker's efficient data generation capabilities, creating a hybrid solution that makes synthetic data as accessible as describing what you need in plain English.

The 1-hour MVP implementation constraint drives a focused approach: a single FastAPI endpoint that processes natural language requests, generates schemas via AI, and produces CSV files with realistic data. By targeting learners specifically, we can optimize for educational value over enterprise features, prioritizing ease of use and domain variety over complex relational structures or authentication systems.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2025-09-05 | 1.0 | Initial PRD creation | John (PM) |

## Requirements

### Functional

- **FR1:** The service SHALL accept natural language descriptions via REST API POST endpoint with a 'description' field containing the dataset requirements in plain English
- **FR2:** The service SHALL process natural language input through GPT-4o-mini to generate a JSON schema mapping field names to Faker library methods
- **FR3:** The service SHALL cache generated schemas using a hash of the description to avoid redundant API calls for identical requests
- **FR4:** The service SHALL generate a minimum of 1000 rows of synthetic data using the Faker library based on the generated schema
- **FR5:** The service SHALL return data in CSV format with appropriate headers matching the schema field names
- **FR6:** The service SHALL complete the entire generation process (request to CSV delivery) within 30 seconds for standard requests
- **FR7:** The service SHALL support common data types including names, emails, dates, numbers, categories, and addresses without additional configuration
- **FR8:** The service SHALL handle at least 5 domain types: e-commerce, healthcare, finance, education, and social media
- **FR9:** The service SHALL provide meaningful error messages when unable to interpret a natural language request

### Non Functional

- **NFR1:** The service MUST operate within GPT-4o-mini token limits (approximately 4000 tokens per request)
- **NFR2:** The service MUST minimize OpenAI API costs by caching schemas and making single API calls per unique request
- **NFR3:** The service MUST be implementable by a single developer within a 1-hour timeframe
- **NFR4:** The service MUST run on Python 3.12+ across Linux, Mac, and Windows platforms
- **NFR5:** The service MUST handle concurrent requests without file corruption in the schema cache
- **NFR6:** The service MUST protect the OpenAI API key through environment variable configuration
- **NFR7:** The service MUST generate data with sufficient variety to avoid obvious repetition patterns in 1000+ row datasets
- **NFR8:** The service MUST operate as a stateless REST API requiring no user authentication for MVP

## Technical Assumptions

### Repository Structure: Monorepo

Single repository containing all service code. Given the MVP's simplicity (single main.py file), a monorepo approach is most appropriate. All configuration, schemas, and service logic will reside in one repository for easy deployment and maintenance.

### Service Architecture

**Monolithic REST API** - A single FastAPI application handling all functionality. The service will be stateless with file-based schema caching. No microservices or complex orchestration needed for MVP. The architecture prioritizes rapid implementation over scalability, appropriate for a 1-hour build targeting educational use cases.

### Testing Requirements

**Manual Testing Only for MVP** - Given the 1-hour implementation constraint, automated testing is out of scope. Testing will consist of manual API calls with sample requests covering the 5 required domains. Post-MVP, unit tests for schema generation and integration tests for the full pipeline should be added.

### Additional Technical Assumptions and Requests

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

## Epic List

**Epic 1: Foundation & Core Data Generation Pipeline**
Establish project infrastructure, API endpoint, and complete end-to-end synthetic data generation functionality with GPT-4o-mini integration and Faker implementation.

## Epic 1: Foundation & Core Data Generation Pipeline

**Goal:** Create a fully functional REST API service that accepts natural language descriptions and returns synthetic CSV datasets, establishing all necessary infrastructure, integrations, and core functionality to enable data science learners to generate custom datasets for their projects.

### Story 1.1: Project Setup and Infrastructure

As a developer,
I want to set up the Python project with FastAPI and all required dependencies,
so that I have a working foundation for building the data generation service.

#### Acceptance Criteria
1. Python project initialized with uv virtual environment (Python 3.12+)
2. pyproject.toml created with FastAPI, uvicorn, pandas, faker, openai, and python-dotenv dependencies
3. Basic FastAPI app structure created in main.py with health check endpoint
4. .env file configured for OpenAI API key storage
5. Server starts successfully with uvicorn and health check returns 200 OK

### Story 1.2: Schema Generation via GPT-4o-mini

As a data science learner,
I want to submit a natural language description of my dataset needs,
so that the system can understand and create an appropriate schema for data generation.

#### Acceptance Criteria
1. POST endpoint `/generate` accepts JSON with 'description' and optional 'rows' fields
2. OpenAI client configured and successfully connects to GPT-4o-mini
3. Prompt template created that instructs GPT-4o-mini to output Faker-compatible schema
4. GPT-4o-mini response parsed into valid JSON schema object
5. Error handling returns meaningful message if schema generation fails

### Story 1.3: Schema Caching Implementation

As a service operator,
I want generated schemas to be cached,
so that identical requests don't incur additional API costs.

#### Acceptance Criteria
1. Hash function implemented for description text (consistent across requests)
2. schemas.json file created/loaded for persistent cache storage
3. Cache checked before making OpenAI API call
4. New schemas saved to cache after successful generation
5. Cache hit returns stored schema without API call

### Story 1.4: Synthetic Data Generation with Faker

As a data science learner,
I want the service to generate realistic synthetic data based on the schema,
so that I receive high-quality datasets for my projects.

#### Acceptance Criteria
1. Faker instance initialized and schema fields mapped to Faker methods
2. 1000+ rows generated based on schema (or user-specified count)
3. Common data types supported: names, emails, dates, numbers, categories, addresses
4. Data variety maintained across rows (no obvious repetition patterns)
5. Custom domain values handled via random.choice when Faker method unavailable

### Story 1.5: CSV Export and Response

As a data science learner,
I want to receive my generated data as a CSV file,
so that I can immediately use it in pandas, Excel, or other data science tools.

#### Acceptance Criteria
1. Generated data converted to pandas DataFrame
2. DataFrame exported to CSV format with proper headers
3. CSV returned as response with appropriate content-type headers
4. Response includes suggested filename based on description
5. Complete request-to-CSV process executes within 30 seconds

## Checklist Results Report

### Executive Summary

- **Overall PRD Completeness:** 85%
- **MVP Scope Appropriateness:** Just Right - Perfectly scoped for 1-hour implementation
- **Readiness for Architecture Phase:** Ready - All critical requirements defined
- **Most Critical Gaps:** Missing some operational details and data persistence strategy

### Category Analysis

| Category                         | Status  | Critical Issues |
| -------------------------------- | ------- | --------------- |
| 1. Problem Definition & Context  | PASS    | None |
| 2. MVP Scope Definition          | PASS    | None |
| 3. User Experience Requirements  | PARTIAL | API-only, no UI requirements needed |
| 4. Functional Requirements       | PASS    | None |
| 5. Non-Functional Requirements   | PASS    | None |
| 6. Epic & Story Structure        | PASS    | Single epic appropriate for scope |
| 7. Technical Guidance            | PASS    | None |
| 8. Cross-Functional Requirements | PARTIAL | Limited data persistence details |
| 9. Clarity & Communication       | PASS    | None |

### Top Issues by Priority

**BLOCKERS:** None - PRD is ready for implementation

**HIGH:**
- Data persistence strategy for schemas.json could be more detailed
- Concurrency handling for file-based cache needs clarification

**MEDIUM:**
- No monitoring/observability strategy (acceptable for MVP)
- Manual testing only may slow validation

**LOW:**
- No versioning strategy for schema evolution
- No rate limiting specified

### MVP Scope Assessment

**Scope Appropriateness:**
- Features are perfectly minimal for educational use case
- Single epic structure matches 1-hour constraint
- No unnecessary features included

**Essential Features Confirmed:**
- Natural language input ✓
- GPT-4o-mini schema generation ✓
- Schema caching ✓
- Faker data generation ✓
- CSV export ✓

**Complexity Assessment:**
- Appropriately simple architecture
- No over-engineering detected
- Clear separation of concerns

### Technical Readiness

**Clarity:** Excellent - all technical decisions documented
**Identified Risks:** Schema generation accuracy, cache concurrency
**Investigation Needs:** Optimal GPT-4o-mini prompting strategy

### Recommendations

1. **Immediate Actions:** None required - ready to proceed
2. **Post-MVP Improvements:**
   - Add integration tests
   - Implement proper logging
   - Add rate limiting
   - Consider database for schema storage

3. **Next Steps:**
   - Proceed to architecture design
   - Begin implementation with Story 1.1

### Final Decision

**READY FOR ARCHITECT** - The PRD is comprehensive, properly structured, and ready for implementation. The single-epic structure and focused scope are appropriate for the 1-hour MVP constraint.

## Next Steps

### UX Expert Prompt

Since this is an API-only service with no user interface for the MVP, no UX expert involvement is needed at this stage. Future iterations may benefit from UX consultation if a web interface is added.

### Architect Prompt

Please review this PRD and create the technical architecture for the Synthetic Data Generation Service. Focus on:
1. Simple, implementable design that can be built in 1 hour
2. FastAPI application structure with single main.py file
3. Integration pattern for GPT-4o-mini API calls
4. File-based schema caching implementation
5. Faker library integration for data generation

The architecture should enable data science learners to generate custom synthetic datasets through natural language descriptions, delivering 1000+ row CSV files efficiently.