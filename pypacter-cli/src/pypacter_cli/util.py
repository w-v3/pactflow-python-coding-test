"""
Utility functions for the CLI.
"""

from __future__ import annotations

import asyncio
import logging
import typing
from functools import wraps

from typing_extensions import ParamSpec, TypeVar

if typing.TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

logger = logging.getLevelName(__name__)


_P = ParamSpec("_P")
_T = TypeVar("_T")


def make_sync(f: Callable[_P, Coroutine[None, None, _T]]) -> Callable[_P, _T]:
    """
    Wrap a function to run it in an asyncio event loop.

    The click library does not support async functions, so we need to wrap the
    async functions in a sync function that runs the async function in an
    asyncio event loop.

    See [pallets/click#2033](https://github.com/pallets/click/issues/2033) for
    the status of this issue.
    """

    @wraps(f)
    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        return asyncio.run(f(*args, **kwargs))

    return wrapper
