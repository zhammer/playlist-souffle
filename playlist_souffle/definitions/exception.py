"""Module for custom Souffle exceptions.

Available classes:
- SouffleException: Base class for custom exceptions emitted by playlist_souffle.
- SouffleParameterError: Error raised if a parameter provided to Souffle is invalid.
- SouffleSpotifyError: Error raised if there is an error with the spotify web api.
"""

import attr


class SouffleException(Exception):
    """Base class for exceptions emitted by Souffle."""


class SouffleParameterError(SouffleException):
    """Custom error raised if a parameter to the souffle is invalid."""


@attr.s
class SouffleSpotifyError(SouffleException):
    """Custom error raised on errors with the spotify web api."""
    http_status = attr.ib()
    message = attr.ib()

    def __str__(self):
        """Stringify a SouffleSpotifyError.

        >>> e = SouffleSpotifyError(http_status=401, message='Authorization failed!')
        >>> str(e)
        '401: Authorization failed!'
        """
        return '{http_status}: {message}'.format(**self.__dict__)
