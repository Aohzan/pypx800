"""Exceptions for IPX800."""


class Ipx800CannotConnectError(Exception):
    """Exception to indicate an error in connection."""


class Ipx800InvalidAuthError(Exception):
    """Exception to indicate an error in authentication."""


class Ipx800RequestError(Exception):
    """Exception to indicate an error with an API request."""
