"""
AI Models.

Collection of LLMs (large language models) that have been pre-configured.
"""

import os

from langchain_openai import ChatOpenAI

__all__ = [
    "DEFAULT_MODEL",
    "GPT_4",
]

TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))
"""
A lower temperature will cause the model to make more likely, but also more
boring and conservative predictions. A high temperature on the other hand will
generate more creative but also more unpredictable outputs.
"""

GPT_4 = ChatOpenAI(temperature=TEMPERATURE, model="gpt-4o")
"""
OpenAI's GPT-4 model.

This model is the most powerful model available in the OpenAI API. It is capable
of ingesting a large amount of text and generating coherent responses. This
model is also the most expensive to use and therefore should be used sparingly.
"""

DEFAULT_MODEL = GPT_4
"""
The default model to use for generations.
"""
