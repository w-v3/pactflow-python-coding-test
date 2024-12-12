from unittest.mock import MagicMock

import pytest
from langchain_core.runnables import RunnableSerializable
from pydantic import ValidationError

from pypacter.language_detector import (
    LanguageDetectionInput,
    LanguageDetectionOutput,
    LanguageDetector,
)


@pytest.fixture
def mock_model() -> MagicMock:
    """Mock model to simulate LLM responses."""
    return MagicMock(spec=RunnableSerializable)


@pytest.fixture
def mock_chain() -> MagicMock:
    """Mock the chain to control its behavior in the full invocation."""
    return MagicMock(spec=RunnableSerializable)

@pytest.fixture
def language_detector(mock_model: MagicMock, mock_chain: MagicMock) -> LanguageDetector:
    """Instantiate a LanguageDetector with a mocked model."""
    detector = LanguageDetector(mock_model)
    detector.chain = mock_chain
    return detector


def test_single_language_detection_success(
    language_detector: LanguageDetector, mock_chain: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful language detection."""
    # Arrange
    mock_chain.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.95,
        message="Language successfully detected.",
        result="detection successful",
    )
    input_data = LanguageDetectionInput(code="print('Hello, World!')")
    # Act
    output = language_detector.invoke(input_data)

    # Assert
    assert output.language == "python"
    assert output.confidence == 0.95
    assert output.message == "Language successfully detected."
    assert output.result == "detection successful"
    mock_chain.invoke.assert_called_once()


def test_no_language_detection(
    language_detector: LanguageDetector, mock_chain: MagicMock, mock_model: MagicMock
) -> None:
    """Testing successful language detection."""
    # Arrange
    mock_chain.invoke.return_value = LanguageDetectionOutput(
        language="unknown",
        message="unknown language or no language detected",
        result="unknown language or no language detected",
        confidence=0.0,
    )
    input_data = LanguageDetectionInput(code="this is a good day")
    # Act
    output = language_detector.invoke(input_data)

    # Assert
    assert output.language == "unknown"
    assert output.result == "unknown language or no language detected"
    mock_chain.invoke.assert_called_once()


def test_multiple_language_detection_success(
    language_detector: LanguageDetector, mock_chain: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful language detection."""
    # Arrange
    mock_chain.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.6,
        message="Language successfully detected.",
        result="possibility of multiple languages need more context",
    )
    input_data = LanguageDetectionInput(code="x=5")
    # Act
    output = language_detector.invoke(input_data)

    # Assert
    assert output.confidence < 0.9
    assert output.result == "possibility of multiple languages need more context"
    mock_chain.invoke.assert_called_once()


def test_language_chain_error(
    language_detector: LanguageDetector, mock_chain: MagicMock, mock_model: MagicMock
) -> None:
    """Test language detection failure due to error in while invoking chain"""
    # Arrange
    mock_chain.invoke.side_effect = Exception("Model error")
    input_data = LanguageDetectionInput(code="print('Hello, World!')")

    # Act
    output = language_detector.invoke(input_data)

    # Assert
    assert output.language == "unknown"
    assert output.confidence == 0.0
    assert output.message == "unsuccesfull detection. model exception occured"
    assert output.result == "unsuccesfull detection. model exception occured"
    mock_chain.invoke.assert_called_once()


def test_language_detection_preprocessing(language_detector: LanguageDetector, mock_model: MagicMock) -> None:
    """Test preprocessing of the code snippet before detection."""
    # Arrange
    input_data = LanguageDetectionInput(code="   print('Hello, World!')   ")

    # Act
    output = language_detector._preprocess_code(input_data.code)

    # Assert
    assert output == "print('Hello, World!')"


def test_invalid_input() -> None:
    """Test that invalid input raises a ValidationError."""
    # Arrange
    invalid_input = {"invalid_field": "some value"}

    # Act & Assert
    with pytest.raises(ValidationError):
        LanguageDetectionInput(**invalid_input)


def test_empty_input(
    language_detector: LanguageDetector, mock_model: MagicMock, mock_chain: MagicMock
) -> None:
    """Test handling of empty code snippet."""
    # Arrange
    mock_chain.invoke.return_value = LanguageDetectionOutput(
        language="unknown",
        confidence=0.0,
        message="Code snippet is empty.",
        result="unknown language or no language detected",
    )
    input_data = LanguageDetectionInput(code="")

    # Act
    output = language_detector.invoke(input_data)
    print(output)

    # Assert
    assert output.language == "unknown"
    assert output.confidence == 0.0
    assert output.result == "unknown language or no language detected"
    mock_chain.invoke.assert_called_once()
