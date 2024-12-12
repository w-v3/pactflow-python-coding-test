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

from pypacter.models import DEFAULT_MODEL

_DIR = Path(__file__).parent
INSTRUCTIONS_DETECTOR = SystemMessagePromptTemplate.from_template_file(
    template_file=(_DIR / "instructions.md"),
    input_variables=["format_instructions"],
)
CODE_TEMPLATE_DETECTOR = HumanMessagePromptTemplate.from_template_file(
    template_file=(_DIR / "code_template.md"),
    input_variables=["code"],
)


# Pydantic Models for Input and Output
class LanguageDetectionInput(BaseModel):
    """
    Input model for language detection.
    """

    code: str = Field(
        ..., description="The code snippet to analyze for language detection."
    )


class LanguageDetectionOutput(BaseModel):
    """
    Output model for singular language detection.
    """

    language: str = Field(..., description="The detected programming language.")
    confidence: float = Field(
        default=0.0, description="The confidence score of the detection, if available."
    )
    message: str = Field(..., description="Additional information regarding result")
    result: typing.Literal[
        "detection successful",
        "unknown language or no language detected",
        "possibility of multiple languages need more context",
        "unsuccesfull detection. model exception occured",
    ] = Field(
        description="Result of detection",
    )


class LanguageDetector(Runnable[LanguageDetectionInput, LanguageDetectionOutput]):
    """
    A detector to identify programming language of a code snippet.
    """

    def __init__(self, model: RunnableSerializable = DEFAULT_MODEL) -> None:
        """
        Initializes the multi-language detector with optional LLM integration.

        Args:
            model : The primary LLM Model to use for language detection

        """
        self.model = model

        parser: PydanticOutputParser[LanguageDetectionOutput] = PydanticOutputParser(
            pydantic_object=LanguageDetectionOutput
        )

        self.prompt_template = (
            INSTRUCTIONS_DETECTOR.format(
                format_instructions=parser.get_format_instructions()
            )
            + CODE_TEMPLATE_DETECTOR
        )
        self.chain = typing.cast(
            RunnableSerializable[dict[str, str], LanguageDetectionOutput],
            self.prompt_template | self.model | parser,
        )

    @property
    def InputType(self) -> type[LanguageDetectionInput]:
        """
        The input type for the code reviewer.
        """
        return LanguageDetectionInput

    @property
    def OutputType(self) -> type[LanguageDetectionOutput]:
        """
        The input type for the code reviewer.
        """
        return LanguageDetectionOutput

    def _preprocess_code(self, code: str) -> str:
        """
        Preprocess the code snippet for better language detection results.

        Args:
            code: The raw code snippet.

        Returns:
            Preprocessed code snippet.
        """
        return code.strip()

    def invoke(
        self,
        input: LanguageDetectionInput | dict[str, str],
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> LanguageDetectionOutput:
        """
        Detect programming language in the given code snippet.

        Args:
            input:
                The code snippet to analyze.
            config:
                An optional configuration for the LLM.
            kwargs:
                Additional arguments. These are required by the parent class,
                but are not used in this method.

        Returns:
            Detected language and confidence scores.
        """
        if isinstance(input, dict):
            input = LanguageDetectionInput(**input)

        try:
            # Preprocess the input code snippet
            preprocessed_code = self._preprocess_code(input.code)
            input.code = preprocessed_code
            output = self.chain.invoke(input.model_dump(), config=config)

        except Exception:
            output = LanguageDetectionOutput(
                language="unknown",
                confidence=0.0,
                message="unsuccesfull detection. model exception occured",
                result="unsuccesfull detection. model exception occured",
            )
        return output
