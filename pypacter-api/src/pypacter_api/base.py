"""
Base routes for the API.

The routes in this module serve a very basic purpose, such as health checks and
version information.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from pypacter.language_detector import (
    LanguageDetectionInput,
    LanguageDetectionOutput,
    LanguageDetector,
)
from pypacter.reviewer import Recommendations, Reviewer
from pypacter_api import get_version

router = APIRouter()


class HealthResponse(BaseModel):
    """
    Model for Healthcheck api response.
    """

    status: str


class VersionResponse(BaseModel):
    """
    Model for Healthcheck api response.
    """

    version: str


@router.get("/health", tags=["health"])
async def health() -> HealthResponse:
    """
    Health check.

    Returns:
        A JSON response indicating the health of the API.
    """
    return HealthResponse(status="ok")


@router.get("/version", tags=["version"])
async def version() -> VersionResponse:
    """
    Get the version of the API.

    Returns:
        A JSON response containing the version of the API.
    """
    return VersionResponse(version=get_version())


def get_detector() -> LanguageDetector:
    """
    Provides an instance of the LanguageDetector.

    This function is used to inject the LanguageDetector dependency into the
    endpoint handlers.

    Returns:
        An instance of LanguageDetector.
    """
    return LanguageDetector()


def get_reviewer() -> Reviewer:
    """
    Provides an instance of the Reviewer.

    This function is used to inject the Reviewer dependency into the
    endpoint handlers.

    Returns:
        An instance of Reviewer.
    """
    return Reviewer()


@router.post(
    "/detect-language",
    tags=["language detection"],
)
async def detect_language(
    snippet: LanguageDetectionInput,
    detector: Annotated[LanguageDetector, Depends(get_detector)],
) -> LanguageDetectionOutput:
    """
    Detect the programming language of a given code snippet.

    Args:
        snippet (LanguageDetectionInput): The code snippet input from the user.
        detector (LanguageDetector): Dependency-injected language detector.

    Returns:
        LanguageDetectionOutput: Detected programming language with confidence.
    """
    return detector.invoke(snippet)


@router.post("/code-review", tags=["Code Review"])
async def code_review(
    snippet: LanguageDetectionInput,
    reviewer: Annotated[Reviewer, Depends(get_reviewer)],
) -> Recommendations:
    """
    Generate a code review for a given code snippet.

    Args:
        snippet (LanguageDetectionInput): The code snippet input from the user.
        reviewer (Reviewer): Dependency-injected code reviewer.

    Returns:
        Recommendations: Generated code review output.
    """
    return reviewer.invoke(snippet)
