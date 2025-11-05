#!/usr/bin/env python3
"""
Test script for demo mode - verifies full stack works without OpenAI API key.
Tests: Config, Mock Schema Generator, Data Generator, CSV Exporter, FastAPI routes, Gradio integration.
"""

import os
import sys
import asyncio
from typing import Dict, Any

# Set demo mode before importing any modules
os.environ["DEMO_MODE"] = "true"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_test(message: str):
    """Print test message."""
    print(f"{BLUE}[TEST]{RESET} {message}")


def print_success(message: str):
    """Print success message."""
    print(f"{GREEN}✅ {message}{RESET}")


def print_error(message: str):
    """Print error message."""
    print(f"{RED}❌ {message}{RESET}")


def print_info(message: str):
    """Print info message."""
    print(f"{YELLOW}ℹ️  {message}{RESET}")


def print_section(title: str):
    """Print section header."""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{title:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


async def test_config():
    """Test configuration and demo mode."""
    print_section("Testing Configuration")

    try:
        from src.core.config import settings

        print_test("Checking DEMO_MODE setting...")
        assert settings.DEMO_MODE is True, "DEMO_MODE should be True"
        print_success(f"DEMO_MODE is enabled: {settings.DEMO_MODE}")

        print_test("Checking API key requirement...")
        # Should not raise error in demo mode even without API key
        settings.validate_settings()
        print_success("Config validation passed (API key not required in demo mode)")

        return True
    except Exception as e:
        print_error(f"Config test failed: {e}")
        return False


async def test_mock_schema_generator():
    """Test mock schema generator."""
    print_section("Testing Mock Schema Generator")

    try:
        from src.services.mock_schema_generator import MockSchemaGenerator

        generator = MockSchemaGenerator()
        print_success("Mock schema generator initialized")

        # Test different domains
        test_cases = [
            ("E-commerce product catalog with names and prices", "ecommerce"),
            ("Healthcare patient records with medical data", "healthcare"),
            ("Financial transactions and accounts", "finance"),
            ("Employee database with salaries", "business"),
            ("Social media user profiles", "social_media"),
            ("Student records with grades", "education"),
            ("General dataset with names and emails", "general"),
        ]

        for description, expected_domain in test_cases:
            print_test(f"Testing: '{description[:50]}...'")
            schema = await generator.generate_schema(description)

            assert schema is not None, "Schema should not be None"
            assert schema.domain == expected_domain, f"Expected domain {expected_domain}, got {schema.domain}"
            assert len(schema.fields_schema) > 0, "Schema should have fields"
            assert schema.description_hash, "Should have description hash"

            print_success(f"Domain: {schema.domain}, Fields: {list(schema.fields_schema.keys())}")

        return True
    except Exception as e:
        print_error(f"Mock schema generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_data_generation():
    """Test data generation with mock schemas."""
    print_section("Testing Data Generation")

    try:
        from src.services.mock_schema_generator import MockSchemaGenerator
        from src.services.data_generator import DataGenerator

        schema_gen = MockSchemaGenerator()
        data_gen = DataGenerator()
        print_success("Generators initialized")

        # Generate schema
        description = "E-commerce products with names, prices, and ratings"
        schema = await schema_gen.generate_schema(description)
        print_success(f"Generated schema for: {description}")

        # Generate data
        rows = 10
        print_test(f"Generating {rows} rows of synthetic data...")
        dataset = data_gen.generate_data(schema, rows)

        assert dataset.row_count == rows, f"Expected {rows} rows, got {dataset.row_count}"
        assert len(dataset.data) == rows, "Data count mismatch"
        assert len(dataset.field_names) > 0, "Should have field names"
        assert dataset.domain == "ecommerce", "Domain mismatch"

        print_success(f"Generated {dataset.row_count} rows successfully")
        print_info(f"Fields: {', '.join(dataset.field_names)}")
        print_info(f"Sample row: {dataset.data[0]}")

        return True
    except Exception as e:
        print_error(f"Data generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_csv_export():
    """Test CSV export functionality."""
    print_section("Testing CSV Export")

    try:
        from src.services.mock_schema_generator import MockSchemaGenerator
        from src.services.data_generator import DataGenerator
        from src.services.csv_exporter import CSVExporter

        # Generate data
        schema_gen = MockSchemaGenerator()
        data_gen = DataGenerator()
        csv_exporter = CSVExporter()

        schema = await schema_gen.generate_schema("Healthcare patient data")
        dataset = data_gen.generate_data(schema, 5)
        print_success("Generated test dataset")

        # Export to CSV
        print_test("Exporting to CSV...")
        csv_response = csv_exporter.export_to_csv(dataset, "Healthcare patient data")

        assert csv_response.csv_content, "CSV content should not be empty"
        assert csv_response.row_count == 5, "Row count mismatch"
        assert csv_response.filename, "Filename should be generated"

        print_success(f"CSV exported: {csv_response.filename}")
        print_info(f"Rows: {csv_response.row_count}")
        print_info(f"Preview:\n{csv_response.csv_content[:200]}...")

        return True
    except Exception as e:
        print_error(f"CSV export test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fastapi_routes():
    """Test FastAPI routes with demo mode."""
    print_section("Testing FastAPI Routes")

    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)
        print_success("Test client created")

        # Test health check
        print_test("Testing /health endpoint...")
        response = client.get("/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "healthy", "Health status should be healthy"
        assert data["demo_mode"] is True, "Demo mode should be True"
        print_success(f"Health check passed: {data}")

        # Test generate endpoint
        print_test("Testing /api/v1/generate endpoint...")
        response = client.post(
            "/api/v1/generate",
            json={
                "description": "E-commerce product catalog with names, prices, and categories",
                "rows": 20,
                "format": "csv"
            }
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "X-Demo-Mode" in response.headers, "Should have demo mode header"
        assert "X-Domain" in response.headers, "Should have domain header"
        assert "X-Generation-Time" in response.headers, "Should have generation time header"

        csv_content = response.text
        assert len(csv_content) > 0, "CSV content should not be empty"
        lines = csv_content.strip().split('\n')
        assert len(lines) >= 21, f"Expected at least 21 lines (header + 20 rows), got {len(lines)}"

        print_success(f"Generated {len(lines)-1} rows of CSV data")
        print_info(f"Domain: {response.headers.get('X-Domain')}")
        print_info(f"Generation time: {response.headers.get('X-Generation-Time')}s")
        print_info(f"Demo mode: {response.headers.get('X-Demo-Mode')}")

        # Test cache stats
        print_test("Testing /api/v1/cache/stats endpoint...")
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print_success(f"Cache stats: {response.json()}")

        return True
    except Exception as e:
        print_error(f"FastAPI routes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_gradio_integration():
    """Test Gradio integration."""
    print_section("Testing Gradio Integration")

    try:
        print_test("Importing Gradio app...")
        from src.frontend.gradio_app import create_gradio_interface
        import gradio as gr

        print_success(f"Gradio version: {gr.__version__}")

        print_test("Creating Gradio interface...")
        interface = create_gradio_interface()
        assert interface is not None, "Interface should not be None"
        print_success("Gradio interface created successfully")

        print_test("Checking if Gradio is mounted in main app...")
        from main import app
        # Check if Gradio routes are registered
        routes = [route.path for route in app.routes]
        has_gradio = any("/gradio" in path for path in routes)
        if has_gradio:
            print_success("Gradio is mounted at /gradio")
        else:
            print_info("Gradio routes not found (may be mounted dynamically)")

        return True
    except Exception as e:
        print_error(f"Gradio integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}Demo Mode Test Suite - Full Stack Testing{RESET}")
    print(f"{BOLD}{GREEN}Testing without OpenAI API Key{RESET}")
    print(f"{BOLD}{GREEN}{'='*60}{RESET}")

    results = []

    # Run tests
    results.append(("Configuration", await test_config()))
    results.append(("Mock Schema Generator", await test_mock_schema_generator()))
    results.append(("Data Generation", await test_data_generation()))
    results.append(("CSV Export", await test_csv_export()))
    results.append(("FastAPI Routes", await test_fastapi_routes()))
    results.append(("Gradio Integration", await test_gradio_integration()))

    # Print summary
    print_section("Test Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"  {test_name:.<40} {status}")

    print(f"\n{BOLD}Results: {passed}/{total} tests passed{RESET}")

    if passed == total:
        print(f"\n{BOLD}{GREEN}{'='*60}{RESET}")
        print(f"{BOLD}{GREEN}🎉 All tests passed! Demo mode is working perfectly!{RESET}")
        print(f"{BOLD}{GREEN}{'='*60}{RESET}\n")
        print(f"{BOLD}You can now run the application without an API key:{RESET}")
        print(f"  {YELLOW}DEMO_MODE=true uv run python main.py{RESET}")
        print(f"\n{BOLD}Or for testing:{RESET}")
        print(f"  {YELLOW}DEMO_MODE=true uv run uvicorn main:app --reload{RESET}\n")
        return 0
    else:
        print(f"\n{BOLD}{RED}{'='*60}{RESET}")
        print(f"{BOLD}{RED}❌ Some tests failed. Please check the output above.{RESET}")
        print(f"{BOLD}{RED}{'='*60}{RESET}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
