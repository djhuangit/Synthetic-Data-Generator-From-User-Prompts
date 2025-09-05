# Test Strategy and Standards

## Testing Philosophy

- **Approach:** Manual testing for MVP, automated testing framework prepared for post-MVP
- **Coverage Goals:** Not applicable for MVP (manual testing only)
- **Test Pyramid:** Future implementation will focus on unit tests for services, integration tests for API

## Test Types and Organization

### Unit Tests

- **Framework:** pytest (ready for post-MVP)
- **File Convention:** test_*.py pattern in tests/ directory
- **Location:** tests/ directory mirroring src/ structure
- **Mocking Library:** pytest-mock for external dependencies
- **Coverage Requirement:** Not enforced for MVP

### Integration Tests

- **Scope:** End-to-end API testing with mock OpenAI responses
- **Location:** tests/integration/
- **Test Infrastructure:**
  - **OpenAI API:** Mock responses using responses library
  - **File System:** Temporary directories for cache testing

### End-to-End Tests

- **Framework:** Manual testing for MVP
- **Scope:** Complete user workflows from request to CSV response
- **Environment:** Local development environment
- **Test Data:** Sample requests covering all 5 required domains
