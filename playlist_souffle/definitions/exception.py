"""Module for custom Souffle exceptions.

Available classes:
- SouffleException: Base class for custom exceptions emitted by Souffle.
- SouffleParameterError: Error raised if a parameter provided to Souffle is invalid.
"""

import attr


class SouffleException(Exception):
    """Base class for exceptions emitted by Souffle."""


class SouffleParameterError(SouffleException):
    """Custom error raised if an ingredient (parameter) to the souffle is invalid."""


@attr.s
class SouffleSpotifyError(SouffleException):
    """Custom error raised on errors with the spotify web api."""
    http_status = attr.ib()
    message = attr.ib()
