from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List
from datetime import datetime


class DatasetRequest(BaseModel):
    """Request model for dataset generation."""
    description: str = Field(
        ..., 
        min_length=10, 
        max_length=4000, 
        description="Natural language description of the dataset needs"
    )
    rows: int = Field(
        default=1000, 
        ge=1, 
        le=10000, 
        description="Number of rows to generate"
    )
    format: str = Field(
        default="csv", 
        pattern="^csv$", 
        description="Output format (currently only csv supported)"
    )


class GeneratedSchema(BaseModel):
    """Response model for generated schema."""
    description_hash: str = Field(..., description="SHA-256 hash of the description")
    fields_schema: Dict[str, Any] = Field(..., description="Generated Faker-compatible schema")
    created_at: datetime = Field(..., description="Timestamp when schema was created")
    domain: str = Field(..., description="Inferred domain category")


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error_type: str = Field(..., description="Type of error (validation, generation_failure, rate_limit, api_failure)")
    message: str = Field(..., description="Human-readable error message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class GenerateResponse(BaseModel):
    """Response model for successful schema generation."""
    fields_schema: Dict[str, Any] = Field(..., description="Generated Faker-compatible schema")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata including timing and domain")


class SyntheticDataset(BaseModel):
    """Data model for generated synthetic datasets."""
    data: List[Dict[str, Any]] = Field(..., description="Array of generated data records")
    row_count: int = Field(..., description="Actual number of rows generated")
    field_names: List[str] = Field(..., description="Column headers from schema")
    generation_time: float = Field(..., description="Time taken to generate data in seconds")
    domain: str = Field(..., description="Domain category of the dataset")


class DatasetResponse(BaseModel):
    """Response model for CSV dataset export."""
    csv_content: str = Field(..., description="Generated CSV data as string")
    filename: str = Field(..., description="Suggested filename from description")
    row_count: int = Field(..., description="Number of rows in dataset")
    content_type: str = Field(default="text/csv", description="MIME type for response")