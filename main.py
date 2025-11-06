from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import Dict
import os

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


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    import logging
    logger = logging.getLogger("uvicorn")

    from src.core.config import settings
    logger.info(f"Demo Mode: {settings.DEMO_MODE}")

    # Check if Gradio routes exist
    routes = [route.path for route in app.routes]
    has_gradio = any("/gradio" in path for path in routes)

    if has_gradio:
        logger.info("✅ Gradio routes detected")
    else:
        logger.warning("⚠️ No Gradio routes found - Gradio may not be mounted")

    logger.info(f"Total routes registered: {len(routes)}")


@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint for monitoring service status."""
    from src.core.config import settings
    response = {
        "status": "healthy",
        "service": "synthetic-data-service",
        "demo_mode": settings.DEMO_MODE
    }
    if settings.DEMO_MODE:
        response["note"] = "Running in demo mode - using mock data (no OpenAI API required)"
    return response


@app.get("/")
async def root():
    """Redirect root to Gradio interface."""
    return RedirectResponse(url="/gradio")


# Mount Gradio app
# Import here to avoid issues if gradio is not installed
import logging
logger = logging.getLogger("uvicorn")

try:
    from src.frontend.gradio_app import app as gradio_app
    import gradio as gr

    # Mount Gradio interface at /gradio path
    app = gr.mount_gradio_app(app, gradio_app, path="/gradio")
    logger.info("✅ Gradio interface mounted at /gradio")
except ImportError as e:
    logger.warning(f"⚠️ Gradio not available: {e}")
    logger.warning("API-only mode: Install gradio to enable the web interface")
except Exception as e:
    logger.error(f"❌ Failed to mount Gradio: {e}")
    import traceback
    logger.error(traceback.format_exc())


if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable (for Heroku) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
