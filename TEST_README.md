# Testing Guide

This project includes two comprehensive test suites to validate both the pipeline and the FastAPI endpoints.

## Test Files

### 1. `test_full_pipeline.py` - Pipeline Integration Tests
Tests the complete data generation pipeline without requiring an OpenAI API key.

**What it tests:**
- Mock schema creation
- Data generation using Faker
- CSV export functionality
- Performance across different row counts
- Multiple domains (ecommerce, healthcare, finance)

**Run with:**
```bash
uv run python test_full_pipeline.py
```

**Expected Results:**
- ✅ 6 pipeline tests across 3 domains
- ✅ Performance tests with 5, 10, 50, and 100 rows
- ✅ Generated CSV files saved to disk

---

### 2. `test_api.py` - FastAPI Endpoint Tests
Tests all FastAPI endpoints using TestClient.

**What it tests:**
- Health check endpoint (`/health`)
- Cache statistics endpoint (`/api/v1/cache/stats`)
- Dataset generation endpoint (`/api/v1/generate`)
- Error handling (validation, rate limits, missing API key)
- OpenAPI schema availability
- CORS configuration

**Run with:**
```bash
uv run python test_api.py
```

**Expected Results:**
- ✅ 8 API endpoint tests
- ✅ All HTTP status codes validated
- ✅ Error responses properly formatted
- ✅ CORS headers configured correctly

---

## Running Both Tests

To run both test suites sequentially:

```bash
uv run python test_full_pipeline.py && uv run python test_api.py
```

---

## Test Coverage Summary

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| Pipeline Tests | 6 | Data generation, CSV export, performance |
| API Tests | 8 | All endpoints, error handling, CORS |
| **Total** | **14** | **Full end-to-end coverage** |

---

## Dependencies

Both test suites work **without requiring an OpenAI API key** by using:
- Mocked schema generation
- Faker library for synthetic data
- FastAPI TestClient for API testing

---

## Troubleshooting

### Issue: httpx version mismatch
If you see errors about `TestClient` initialization:
```bash
uv sync
```

### Issue: Missing dependencies
Ensure all dependencies are installed:
```bash
uv pip install -e .
```

---

## CI/CD Integration

These tests can be integrated into your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run Pipeline Tests
  run: uv run python test_full_pipeline.py

- name: Run API Tests
  run: uv run python test_api.py
```

---

## Test Philosophy

- **No External Dependencies**: Tests run without API keys or external services
- **Fast Execution**: All tests complete in under 5 seconds
- **Comprehensive Coverage**: Tests cover happy paths and error scenarios
- **Clear Output**: Human-readable test results with emojis and formatting
