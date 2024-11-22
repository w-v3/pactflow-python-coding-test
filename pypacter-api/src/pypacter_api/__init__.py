"""
PyPacter API.
"""

from __future__ import annotations

import contextlib
import logging
import os
import socket

from fastapi import FastAPI

from pypacter_api.__version__ import __version__, __version_tuple__

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__license__",
    "__url__",
    "__version__",
    "__version_tuple__",
    "get_version",
    "local",
]

__author__ = "Joshua Ellis"
__email__ = "joshua.ellis@smartbear.com"
__url__ = "https://github.com/pactflow/pactflow-python-coding-test"
__license__ = "Proprietary"
__copyright__ = "SmartBear Software and PactFlow"

logger = logging.getLogger(__name__)


def get_version() -> str:
    """
    Get the version of Accord API.

    Returns:
        The version of Accord API.
    """
    return __version__


def _find_free_port() -> int:
    """
    Find a free port.

    This is used to find a free port to host the API on when running locally. It
    is allocated, and then released immediately so that it can be used by the
    API.

    Returns:
        The port number.
    """
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def local() -> None:
    """
    Host API locally.

    This must not be used in production. It is used to host the API locally for
    testing/development.

    The API is hosted using [`uvicorn`](https://www.uvicorn.org/), bound to
    `localhost` (thereby preventing it from being accessed from outside the
    machine), and uses a randomly allocated port.

    It is possible to override the host and port by setting the environment
    variables `ACCORD_DEV_HOST` and `ACCORD_DEV_PORT` respectively.
    """
    import uvicorn

    import pypacter_api.base

    local_app = FastAPI(
        title="PyPacter (local)",
        description="Development version of PyPacter API.",
        version=__version__,
    )
    local_app.include_router(pypacter_api.base.router, prefix="/")

    uvicorn.run(
        local_app,
        host=os.getenv("PYPACTER_DEV_HOST", "localhost"),
        port=int(os.getenv("PYPACTER_DEV_PORT", str(_find_free_port()))),
    )
