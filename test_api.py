#!/usr/bin/env python3
"""Test FastAPI endpoints without requiring OpenAI API key."""

import sys
import os

# Add project root to path BEFORE importing anything else
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the app BEFORE TestClient
from main import app

# Now import TestClient
from fastapi.testclient import TestClient

from src.api.models import GeneratedSchema, SyntheticDataset

# Create global test client
client = TestClient(app)


def create_mock_generated_schema():
    """Create a mock GeneratedSchema for testing."""
    return GeneratedSchema(
        description_hash="test_hash_12345",
        fields_schema={
            'product_name': {'faker_method': 'catch_phrase'},
            'category': {'faker_method': 'ecommerce'},
            'price': {'faker_method': 'price'},
            'in_stock': {'faker_method': 'boolean'}
        },
        created_at=datetime.now(),
        domain="ecommerce"
    )


def test_health_check():
    """Test the /health endpoint."""
    print("\n" + "="*60)
    print("TEST: Health Check Endpoint")
    print("="*60)

    response = client.get("/health")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "synthetic-data-service"

    print("✅ Health check endpoint working!")
    return True


def test_cache_stats_endpoint():
    """Test the /api/v1/cache/stats endpoint."""
    print("\n" + "="*60)
    print("TEST: Cache Stats Endpoint")
    print("="*60)

    response = client.get("/api/v1/cache/stats")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "cache_enabled" in data

    print("✅ Cache stats endpoint working!")
    return True


@patch('src.api.routes.get_csv_exporter')
@patch('src.api.routes.get_data_generator')
@patch('src.api.routes.get_schema_generator')
def test_generate_endpoint_success(mock_get_schema_gen, mock_get_data_gen, mock_get_csv_exp):
    """Test successful dataset generation via /api/v1/generate endpoint."""
    print("\n" + "="*60)
    print("TEST: Generate Dataset Endpoint (Success)")
    print("="*60)

    # Mock the schema generator
    mock_schema_gen = MagicMock()
    mock_schema = create_mock_generated_schema()

    # Create an async mock for generate_schema
    async def async_generate_schema(desc):
        return mock_schema

    mock_schema_gen.generate_schema = async_generate_schema
    mock_get_schema_gen.return_value = mock_schema_gen

    # Mock the data generator
    mock_data_gen = MagicMock()
    mock_dataset = SyntheticDataset(
        data=[
            {
                'product_name': 'Test Product 1',
                'category': 'Electronics',
                'price': '99.99',
                'in_stock': True
            },
            {
                'product_name': 'Test Product 2',
                'category': 'Books',
                'price': '19.99',
                'in_stock': False
            }
        ],
        row_count=2,
        field_names=['product_name', 'category', 'price', 'in_stock'],
        generation_time=0.123,
        domain=mock_schema.domain
    )
    mock_data_gen.generate_data.return_value = mock_dataset
    mock_get_data_gen.return_value = mock_data_gen

    # Mock the CSV exporter
    mock_csv_exp = MagicMock()
    from src.api.models import DatasetResponse
    mock_csv_response = DatasetResponse(
        csv_content='"product_name","category","price","in_stock"\n"Test Product 1","Electronics","99.99","True"\n"Test Product 2","Books","19.99","False"',
        filename="test_ecommerce.csv",
        row_count=2
    )
    mock_csv_exp.export_to_csv.return_value = mock_csv_response
    mock_csv_exp.get_csv_headers.return_value = {
        "Content-Disposition": "attachment; filename=test_ecommerce.csv"
    }
    mock_get_csv_exp.return_value = mock_csv_exp

    # Make request to generate endpoint
    request_data = {
        "description": "E-commerce product catalog",
        "rows": 2
    }

    print(f"Request: {request_data}")
    response = client.post("/api/v1/generate", json=request_data)

    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content Preview (first 200 chars): {response.text[:200]}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "X-Generation-Time" in response.headers
    assert "X-Domain" in response.headers
    assert response.headers["X-Domain"] == "ecommerce"

    # Check CSV content
    csv_content = response.text
    assert "product_name" in csv_content
    assert "category" in csv_content
    assert "price" in csv_content
    assert "in_stock" in csv_content

    print("✅ Generate endpoint working successfully!")
    return True


def test_generate_endpoint_validation_error():
    """Test validation error handling in generate endpoint."""
    print("\n" + "="*60)
    print("TEST: Generate Dataset Endpoint (Validation Error)")
    print("="*60)

    # Send invalid request (missing required field)
    request_data = {
        "rows": 10
        # Missing "description" field
    }

    print(f"Request (invalid): {request_data}")
    response = client.post("/api/v1/generate", json=request_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 422  # Unprocessable Entity

    print("✅ Validation error handling working!")
    return True


@patch('src.services.schema_generator.SchemaGenerator.generate_schema')
def test_generate_endpoint_missing_api_key(mock_generate_schema):
    """Test handling of missing OpenAI API key."""
    print("\n" + "="*60)
    print("TEST: Generate Dataset Endpoint (Missing API Key)")
    print("="*60)

    # Mock schema generator to raise ValueError about missing API key
    mock_generate_schema.side_effect = ValueError("OPENAI_API_KEY not found")

    request_data = {
        "description": "Test dataset",
        "rows": 5
    }

    print(f"Request: {request_data}")
    response = client.post("/api/v1/generate", json=request_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 503  # Service Unavailable
    error_detail = response.json()["detail"]
    assert error_detail["error_type"] == "api_failure"
    assert "configuration" in error_detail["details"]

    print("✅ Missing API key error handling working!")
    return True


@patch('src.api.routes.get_schema_generator')
def test_generate_endpoint_rate_limit(mock_get_schema_gen):
    """Test rate limit error handling."""
    print("\n" + "="*60)
    print("TEST: Generate Dataset Endpoint (Rate Limit)")
    print("="*60)

    # Mock schema generator to raise RateLimitError
    from src.core.exceptions import RateLimitError
    mock_schema_gen = MagicMock()

    async def async_generate_schema_fail(desc):
        raise RateLimitError("Rate limit exceeded")

    mock_schema_gen.generate_schema = async_generate_schema_fail
    mock_get_schema_gen.return_value = mock_schema_gen

    request_data = {
        "description": "Test dataset",
        "rows": 5
    }

    print(f"Request: {request_data}")
    response = client.post("/api/v1/generate", json=request_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 429  # Too Many Requests
    error_detail = response.json()["detail"]
    assert error_detail["error_type"] == "rate_limit"
    assert "retry_after" in error_detail["details"]

    print("✅ Rate limit error handling working!")
    return True


def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    print("\n" + "="*60)
    print("TEST: OpenAPI Schema")
    print("="*60)

    response = client.get("/openapi.json")

    print(f"Status Code: {response.status_code}")

    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "Synthetic Data Service"
    assert "paths" in schema
    assert "/health" in schema["paths"]
    assert "/api/v1/generate" in schema["paths"]

    print("✅ OpenAPI schema accessible!")
    return True


def test_cors_headers():
    """Test that CORS headers are properly set."""
    print("\n" + "="*60)
    print("TEST: CORS Headers")
    print("="*60)

    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })

    print(f"Status Code: {response.status_code}")
    print(f"CORS Headers: {dict(response.headers)}")

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

    print("✅ CORS headers properly configured!")
    return True


def main():
    """Run all API tests."""
    print("🚀 TESTING FASTAPI ENDPOINTS")
    print("="*60)

    test_results = []

    tests = [
        ("Health Check", test_health_check),
        ("Cache Stats", test_cache_stats_endpoint),
        ("Generate Success", test_generate_endpoint_success),
        ("Validation Error", test_generate_endpoint_validation_error),
        ("Missing API Key", test_generate_endpoint_missing_api_key),
        ("Rate Limit", test_generate_endpoint_rate_limit),
        ("OpenAPI Schema", test_openapi_schema),
        ("CORS Headers", test_cors_headers),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                test_results.append((test_name, "PASSED"))
                passed += 1
            else:
                test_results.append((test_name, "FAILED"))
                failed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            test_results.append((test_name, "FAILED"))
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            test_results.append((test_name, "ERROR"))
            failed += 1

    # Summary
    print("\n" + "="*60)
    print("🎉 API TEST SUMMARY")
    print("="*60)

    print(f"{'Test Name':<30} {'Result':<10}")
    print("-" * 40)

    for test_name, result in test_results:
        status_emoji = "✅" if result == "PASSED" else "❌"
        print(f"{status_emoji} {test_name:<28} {result:<10}")

    print("-" * 40)
    print(f"Total: {len(tests)} | Passed: {passed} | Failed: {failed}")

    if failed == 0:
        print("\n✅ All API tests passed!")
        print("✅ FastAPI application working correctly!")
        print("✅ Ready for deployment!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
