from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from pypacter.language_detector import (
    LanguageDetectionOutput,
    LanguageDetector,
)
from pypacter.reviewer import Recommendations, Reviewer
from pypacter_api import __version__
from pypacter_api.base import router

app = FastAPI()
app.include_router(router)


# Mock the external services
@pytest.fixture
def mock_detector() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_reviewer() -> MagicMock:
    return MagicMock()


@pytest.fixture
def client(mock_detector: MagicMock, mock_reviewer: MagicMock) -> TestClient:
    """Fixture to instantiate the FastAPI test client."""
    # Replace the real detector and reviewer with mocks in the app.
    app.dependency_overrides[LanguageDetector] = mock_detector
    app.dependency_overrides[Reviewer] = mock_reviewer
    return TestClient(app)


# Test the /health endpoint
def test_health(client: TestClient) -> None:
    """Test the health check route."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Test the /version endpoint
def test_version(client: TestClient) -> None:
    """Test the version check route."""
    expected_version = __version__
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": expected_version}


# Test the /detect-language endpoint - Success
def test_detect_language(client: TestClient, mock_detector: MagicMock) -> None:
    """Test successful language detection."""
    # Arrange: Mock the LanguageDetector's invoke method to return a successful output
    mock_detector.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.95,
        message="Language successfully detected.",
        result="detection successful",
    )
    input_data = {"code": "print('Hello, World!')"}

    # Act
    response = client.post("/detect-language", json=input_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["language"] == "python"
    assert response.json()["confidence"] == 0.95
    assert response.json()["result"] == "detection successful"


# Test the /code-review endpoint - Success
def test_code_review(client: TestClient, mock_reviewer: MagicMock) -> None:
    """Test successful code review generation."""
    # Arrange: Mock the Reviewer invoke method to return a successful output
    mock_reviewer.invoke.return_value = Recommendations(
        recommendation=[],
        review_result="Success",
    )
    input_data = {"code": ""}

    # Act
    response = client.post("/code-review", json=input_data)

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json()["recommendations"], list)
