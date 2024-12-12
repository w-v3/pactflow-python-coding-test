"""
Main EntryPoint for deployment of uvicorn server.
"""
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pypacter_api.__version__ import __version__
from pypacter_api.base import router as api_router

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="PyPacter API",
    description="PyPacter API for code review, language detection, and more.",
    version=__version__,
    openapi_url="/openapi.json",  # Endpoint for OpenAPI documentation
    docs_url="/docs",  # Swagger UI for interactive API docs
    redoc_url="/redoc",  # ReDoc UI for an alternative view of docs
)

# CORS middleware configuration for development/production environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust as needed for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (adjust for production)
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")  # Prefix for API routes (versioning)


def main() -> None:
    """
    Run the FastAPI app with uvicorn.
    This function will be called when the script is executed directly.
    """
    uvicorn.run(
        "main:app",
        host=os.getenv("PYPACTER_DEV_HOST", "localhost"),  # Default to localhost
        port=int(os.getenv("PYPACTER_DEV_PORT", "5000")),  # Default to port 8000
        reload=True,  # Enables auto-reload in development (remove for production)
    )


# Run the application if the script is executed directly
if __name__ == "__main__":
    main()
