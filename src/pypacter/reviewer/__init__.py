"""
Code verification.

This module contains a code verifier. It takes a code snippet, and identifies
any issues with the code.
"""

import typing
from pathlib import Path

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import Runnable, RunnableConfig, RunnableSerializable
from pydantic import BaseModel, Field

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


class Input(BaseModel):
    """
    Input for the LLM.
    """

    code: str = Field(
        description="The code snippet to verify.",
    )


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

    This is a list of recommendations for the code snippet.
    """

    recommendations: list[Recommendation] = Field(
        description="The issues identified in the code snippet.",
    )


class Reviewer(Runnable[Input, Recommendations]):
    """
    Code reviewer.
    """

    def __init__(self) -> None:
        """
        Instantiates a new code reviewer.
        """
        parser = PydanticOutputParser(pydantic_object=Recommendations)
        self.prompt_template = (
            INSTRUCTIONS.format(format_instructions=parser.get_format_instructions())
            + CODE_TEMPLATE
        )
        self.chain = typing.cast(
            RunnableSerializable[dict[str, str], Recommendations],
            self.prompt_template | DEFAULT_MODEL | parser,
        )

    @property
    def InputType(self) -> type[Input]:  # noqa: N802
        """
        The input type for the code reviewer.
        """
        return Input

    @property
    def OutputType(self) -> type[Recommendations]:  # noqa: N802
        """
        The output type for the code reviewer.
        """
        return Recommendations

    def invoke(
        self,
        input: Input | dict[str, str],
        config: RunnableConfig | None = None,
    ) -> Recommendations:
        """
        Perform the code review.

        Args:
            input: The HTTP request-response pair.
            config: An optional configuration for the LLM.

        Returns:
            The generated code snippet.
        """
        if isinstance(input, dict):
            input = Input(**input)

        return self.chain.invoke(input.dict(), config=config)
