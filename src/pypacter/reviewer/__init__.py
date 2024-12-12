"""
Code verification.

This module contains a code verifier. It takes a code snippet, and identifies
any issues with the code.
"""

import typing
from pathlib import Path
from typing import Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import Runnable, RunnableConfig, RunnableSerializable
from pydantic import BaseModel, Field

from pypacter.language_detector import LanguageDetectionInput, LanguageDetector
from pypacter.models import DEFAULT_MODEL

_DIR = Path(__file__).parent
INSTRUCTIONS = SystemMessagePromptTemplate.from_template_file(
    template_file=(_DIR / "instructions.md"),
    input_variables=["format_instructions"],
)
CODE_TEMPLATE = HumanMessagePromptTemplate.from_template_file(
    template_file=(_DIR / "code_template.md"),
    input_variables=["code"],
)


class ReviewerLLMInput(BaseModel):
    """
    Input for the Reviewer LLM.
    """

    code: str = Field(
        description="The code snippet to verify.",
    )
    language: str = Field(
        default="unknown", description="The detected programming language."
    )
    confidence: float = Field(
        0.0, description="The confidence score of the language detection."
    )
    summary: str = Field(..., description="summary of the language detection process")


class Recommendation(BaseModel):
    """
    Individual recommendation for the code snippet.
    """

    line: int = Field(
        description="The line number of the recommendation.",
    )
    severity: typing.Literal["critical", "error", "warning"] = Field(
        description="The severity of the recommendation.",
    )
    message: str = Field(
        description="The message for the recommendation.",
    )


class Recommendations(BaseModel):
    """
    Output for the LLM.

    This is the output model for code reviewer.
    """

    recommendations: list[Recommendation] = Field(
        default=[],
        description="The issues identified in the code snippet.",
    )
    review_result: typing.Literal["Success", "Failed"] = Field(
        description="Describes if the code snippet was reviewed or not"
    )


class Reviewer(Runnable[LanguageDetectionInput, Recommendations]):
    """
    Code reviewer class.
    """

    def __init__(self, model: RunnableSerializable = DEFAULT_MODEL) -> None:
        """
        Instantiates a new code reviewer.
        """
        self.language_detector = LanguageDetector()
        self.model = model

        parser: PydanticOutputParser[Recommendations] = PydanticOutputParser(
            pydantic_object=Recommendations
        )
        self.prompt_template = (
            INSTRUCTIONS.format(format_instructions=parser.get_format_instructions())
            + CODE_TEMPLATE
        )
        self.chain = typing.cast(
            RunnableSerializable[dict[str, str], Recommendations],
            self.prompt_template | self.model | parser,
        )

    @property
    def InputType(self) -> type[LanguageDetectionInput]:  # noqa: N802
        """
        The input type for the code reviewer.
        """
        return LanguageDetectionInput

    @property
    def OutputType(self) -> type[Recommendations]:  # noqa: N802
        """
        The output type for the code reviewer.
        """
        return Recommendations

    def invoke(
        self,
        input: LanguageDetectionInput | dict[str, str],
        config: RunnableConfig | None = None,
        **kwargs: Any,  # noqa: ANN401, ARG002
    ) -> Recommendations:
        """
        Perform the code review.

        Args:
            input:
                The HTTP request-response pair.
            config:
                An optional configuration for the LLM.
            kwargs:
                Additional arguments. These are required by the parent class,
                but are not used in this method.

        Returns:
            The generated code snippet.
        """
        if isinstance(input, dict):
            input = LanguageDetectionInput(**input)

        try:
            result = self.language_detector.invoke(input)
            final_input = ReviewerLLMInput(
                language=result.language,
                confidence=result.confidence,
                summary=result.result + result.message,
                code=input.code,
            )
            output = self.chain.invoke(final_input.model_dump(), config=config)
        except Exception:
            output = Recommendations(recommendations=[], review_result="Failed")
        return output
