from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from src.api.routes import router as api_router

app = FastAPI(
    title="Synthetic Data Service",
    description="FastAPI service for generating synthetic data using AI",
    version="0.1.0"
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring service status."""
    return {"status": "healthy", "service": "synthetic-data-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
