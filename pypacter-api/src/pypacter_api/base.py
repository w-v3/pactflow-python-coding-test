"""
Base routes for the API.

The routes in this module serve a very basic purpose, such as health checks and
version information.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pypacter_api import get_version

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> JSONResponse:
    """
    Health check.

    Returns:
        A JSON response indicating the health of the API.
    """
    return JSONResponse(content={"status": "ok"})


@router.get("/version", tags=["version"])
async def version() -> JSONResponse:
    """
    Get the version of the API.

    Returns:
        A JSON response containing the version of the API.
    """
    return JSONResponse(content={"version": get_version()})
