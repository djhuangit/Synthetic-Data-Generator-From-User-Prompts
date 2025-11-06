from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response
from typing import Dict, Any
import time
from datetime import datetime

from src.api.models import DatasetRequest, GenerateResponse, ErrorResponse
from src.services.schema_generator import SchemaGenerator
from src.services.data_generator import DataGenerator
from src.services.csv_exporter import CSVExporter
from src.core.config import settings
from src.core.exceptions import (
    SchemaGenerationError, 
    RateLimitError, 
    APIConnectionError,
    ValidationError
)

router = APIRouter()

# Initialize services lazily to allow server to start without API key
_schema_generator = None
_mock_schema_generator = None
_data_generator = None
_csv_exporter = None

def get_schema_generator():
    """
    Get schema generator instance, initializing if needed.
    Returns MockSchemaGenerator in demo mode, SchemaGenerator otherwise.
    """
    global _schema_generator, _mock_schema_generator

    # Debug: Log what mode we're in
    import logging
    logger = logging.getLogger("uvicorn")
    logger.info(f"get_schema_generator called - DEMO_MODE={settings.DEMO_MODE}")

    # Use mock generator in demo mode
    if settings.DEMO_MODE:
        logger.info("Using MockSchemaGenerator")
        if _mock_schema_generator is None:
            from src.services.mock_schema_generator import MockSchemaGenerator
            _mock_schema_generator = MockSchemaGenerator()
        return _mock_schema_generator

    # Use real generator in production mode
    logger.info("Using real SchemaGenerator")
    if _schema_generator is None:
        _schema_generator = SchemaGenerator()
    return _schema_generator

def get_data_generator() -> DataGenerator:
    """Get data generator instance, initializing if needed."""
    global _data_generator
    if _data_generator is None:
        _data_generator = DataGenerator()
    return _data_generator

def get_csv_exporter() -> CSVExporter:
    """Get CSV exporter instance, initializing if needed."""
    global _csv_exporter
    if _csv_exporter is None:
        _csv_exporter = CSVExporter()
    return _csv_exporter


@router.post(
    "/generate",
    status_code=status.HTTP_200_OK,
    summary="Generate synthetic dataset",
    description="Generate a complete synthetic dataset as CSV from natural language description"
)
async def generate_dataset(request: DatasetRequest) -> Response:
    """
    Generate a complete synthetic dataset as CSV from natural language description.
    
    Args:
        request: Dataset request containing description, rows, and format
        
    Returns:
        CSV file response with generated synthetic data
        
    Raises:
        HTTPException: On validation, generation, or API failures
    """
    start_time = time.time()
    
    try:
        # Get service instances
        schema_generator = get_schema_generator()
        data_generator = get_data_generator()
        csv_exporter = get_csv_exporter()
        
        # Step 1: Generate schema using OpenAI
        generated_schema = await schema_generator.generate_schema(request.description)
        
        # Step 2: Generate synthetic data using Faker
        synthetic_dataset = data_generator.generate_data(generated_schema, request.rows)
        
        # Step 3: Export to CSV
        csv_response = csv_exporter.export_to_csv(synthetic_dataset, request.description)
        
        # Calculate total processing time
        total_time = time.time() - start_time
        
        # Get CSV response headers
        headers = csv_exporter.get_csv_headers(csv_response)
        headers["X-Generation-Time"] = str(round(total_time, 3))
        headers["X-Domain"] = generated_schema.domain
        headers["X-Description-Hash"] = generated_schema.description_hash
        if settings.DEMO_MODE:
            headers["X-Demo-Mode"] = "true"
        
        # Return CSV as response
        return Response(
            content=csv_response.csv_content,
            media_type="text/csv",
            headers=headers
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_type": "validation",
                "message": str(e),
                "details": {"description": request.description},
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error_type": "rate_limit",
                "message": str(e),
                "details": {"retry_after": 60},
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except APIConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error_type": "api_failure",
                "message": str(e),
                "details": {"provider": "openai"},
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except SchemaGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "generation_failure",
                "message": str(e),
                "details": {"description_preview": request.description[:100]},
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except ValueError as e:
        # Handle configuration errors (like missing API key)
        if "OPENAI_API_KEY" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error_type": "api_failure",
                    "message": "Service is not properly configured. Please check API key settings.",
                    "details": {"configuration": "missing_api_key"},
                    "timestamp": datetime.now().isoformat()
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error_type": "configuration_error",
                    "message": "Service configuration error",
                    "details": {"error_id": str(hash(str(e)))[:8]},
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except Exception as e:
        # Never log sensitive information like API keys
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "generation_failure",
                "message": "An unexpected error occurred during dataset generation",
                "details": {"error_id": str(hash(str(e)))[:8]},
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get(
    "/cache/stats",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get cache statistics",
    description="Retrieve cache performance and health statistics"
)
async def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics for monitoring and debugging.
    
    Returns:
        dict: Cache statistics including total schemas, file sizes, health status
    """
    try:
        # Try to get cache stats without initializing full schema generator
        if settings.CACHE_ENABLED:
            from src.services.cache_service import SchemaCache
            cache = SchemaCache()
            stats = cache.get_cache_stats()
            stats["cache_enabled"] = True
            stats["cache_healthy"] = cache.is_cache_healthy()
            return stats
        else:
            return {
                "cache_enabled": False,
                "message": "Caching is disabled in configuration"
            }
    except Exception as e:
        return {
            "cache_enabled": False,
            "error": f"Failed to get cache stats: {str(e)}"
        }