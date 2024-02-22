"""
Utility functions for PyPacter.

This module contains utility functions for the PyPacter application, which are
generally self-contained and do not depend on other parts of the application.
"""

import pypacter


def get_version() -> str:
    """
    Get the version of PyPacter.

    Returns:
        The version of PyPacter.
    """
    return pypacter.__version__
