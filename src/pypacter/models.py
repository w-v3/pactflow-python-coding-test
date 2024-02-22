"""
AI Models.

Collection of LLMs (large language models) that have been pre-configured.
"""

import os

from langchain_openai import ChatOpenAI

__all__ = [
    "GPT_4",
    "DEFAULT_MODEL",
]

TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))
"""
A lower temperature will cause the model to make more likely, but also more
boring and conservative predictions. A high temperature on the other hand will
generate more creative but also more unpredictable outputs.
"""

GPT_4 = ChatOpenAI(
    temperature=TEMPERATURE,
    model="gpt-4-1106-preview",
)
"""
OpenAI's GPT-4 model.

This model is pinned to the 6 November version in order to avoid drifts in the
output generated.

!!! warning

    This model will be deprecated in April 2024.
"""

DEFAULT_MODEL = GPT_4
"""
The default model to use for generations.
"""
