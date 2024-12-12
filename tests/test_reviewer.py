from unittest.mock import MagicMock

import pytest
from langchain_core.runnables import RunnableSerializable
from pydantic import ValidationError

from pypacter.language_detector import (
    LanguageDetectionInput,
    LanguageDetectionOutput,
)
from pypacter.reviewer import Recommendation, Recommendations, Reviewer


@pytest.fixture
def mock_model() -> MagicMock:
    """Mock model to simulate LLM responses."""
    return MagicMock(spec=RunnableSerializable)


@pytest.fixture
def mock_chain() -> MagicMock:
    """Mock the chain to control its behavior in the full invocation."""
    return MagicMock(spec=RunnableSerializable)


@pytest.fixture
def language_detector() -> MagicMock:
    """Instantiate a LanguageDetector with a mocked model."""
    # detector = LanguageDetector(mock_model)
    # detector.chain = mock_chain
    return MagicMock(spec=RunnableSerializable)


@pytest.fixture
def reviewer(language_detector: MagicMock, mock_model: MagicMock, mock_chain: MagicMock) -> Reviewer:
    """Instantiate a Reviewer with mocked LanguageDetector and model."""
    reviewer = Reviewer(model=mock_model)
    reviewer.language_detector = language_detector
    reviewer.chain = mock_chain
    return reviewer


def test_code_review_success_no_recommendations(
    reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful code review."""
    # Arrange: Mock the LLM response
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.95,
        message="Language successfully detected.",
        result="detection successful",
    )
    mock_chain.invoke.return_value = Recommendations(
        recommendations=[], review_result="Success"
    )

    input_data = LanguageDetectionInput(code="print('Hello, World!')")

    # Act
    output = reviewer.invoke(input_data)

    # Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()


def test_code_review_success_with_recommendations(
     reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful code review."""
    # Arrange: Mock the LLM response
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.95,
        message="Language successfully detected.",
        result="detection successful",
    )

    mock_chain.invoke.return_value = Recommendations(
        recommendations=[
            Recommendation(line=1, severity="error", message="Syntax error.")
        ],
        review_result="Success",
    )

    input_data = LanguageDetectionInput(code="print 'Hello, World!' ")

    # Act
    output = reviewer.invoke(input_data)

    # Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) > 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()


def test_code_review_no_language_detection(
    reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful code review."""
    # Arrange: Mock the LLM response
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="unknown",
        message="unknown language or no language detected",
        result="unknown language or no language detected",
        confidence=0.0,
    )

    mock_chain.invoke.return_value = Recommendations(
        recommendations=[], review_result="Success"
    )

    input_data = LanguageDetectionInput(code=" this is a sunday ")

    # Act
    output = reviewer.invoke(input_data)

    # Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()


def test_code_review_multiple_language_detection(
    reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test successful code review."""
    # Arrange: Mock the LLM response
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.6,
        message="Language successfully detected.",
        result="possibility of multiple languages need more context",
    )

    mock_chain.invoke.return_value = Recommendations(
        recommendations=[], review_result="Success"
    )

    input_data = LanguageDetectionInput(code="x=5 ")

    # Act
    output = reviewer.invoke(input_data)

    # Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()


def test_code_review_chain_invocation_error(
    reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test code review when LLM chain fails."""
    # Arrange: Mock the language detector to raise an exception
    mock_chain.invoke.side_effect = Exception()

    input_data = LanguageDetectionInput(code="print('Hello World')")

    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="python",
        confidence=0.95,
        message="Language successfully detected.",
        result="detection successful",
    )

    input_data = LanguageDetectionInput(code="print('Hello, World!')")

    # Act
    output = reviewer.invoke(input_data)

    # Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Failed"
    mock_chain.invoke.assert_called_once()


def test_code_review_language_detection_failure(
   reviewer: Reviewer, mock_chain: MagicMock, language_detector: MagicMock, mock_model: MagicMock
) -> None:
    """Test code review when language detection fails."""
    # Arrange: Mock the language detector to raise an exception
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="unknown",
        confidence=0.0,
        message="unsuccesfull detection. model exception occured",
        result="unsuccesfull detection. model exception occured",
    )
    mock_chain.invoke.return_value = Recommendations(
        recommendations=[], review_result="Success"
    )

    input_data = LanguageDetectionInput(code="8")
    output = reviewer.invoke(input_data)
    # Act & Assert
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()


def test_code_review_invalid_input(reviewer: Reviewer) -> None:
    """Testing code review with invalid input."""
    # Arrange: Provide invalid code snippet
    input_data = {"some_var": "some_value"}
    # Act: Mock the LLM response
    with pytest.raises(ValidationError):
        reviewer.invoke(input_data)


def test_code_review_no_input(
    reviewer: Reviewer, mock_model: MagicMock, mock_chain: MagicMock, language_detector: MagicMock
) -> None:
    mock_chain.invoke.return_value = Recommendations(
        recommendations=[], review_result="Success"
    )
    language_detector.invoke.return_value = LanguageDetectionOutput(
        language="unknown",
        confidence=0.0,
        message="Code snippet is empty.",
        result="unknown language or no language detected",
    )
    input_data = LanguageDetectionInput(code="")

    output = reviewer.invoke(input_data)
    assert isinstance(output, Recommendations)
    assert len(output.recommendations) == 0
    assert output.review_result == "Success"
    mock_chain.invoke.assert_called_once()
