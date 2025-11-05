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


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring service status."""
    return {"status": "healthy", "service": "synthetic-data-service"}


@app.get("/")
async def root():
    """Redirect root to Gradio interface."""
    return RedirectResponse(url="/gradio")


# Mount Gradio app
# Import here to avoid issues if gradio is not installed
try:
    from src.frontend.gradio_app import app as gradio_app
    import gradio as gr

    # Mount Gradio interface at /gradio path
    app = gr.mount_gradio_app(app, gradio_app, path="/gradio")
    print("✅ Gradio interface mounted at /gradio")
except ImportError as e:
    print(f"⚠️ Gradio not available: {e}")
    print("API-only mode: Install gradio to enable the web interface")


if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable (for Heroku) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
