class DelightedError(Exception):

    def __init__(self, response):
        self.response = response

    def __repr__(self):
        return "<%d: %s>" % (self.response.status_code, self.response.body)

    __str__ = __repr__


class AuthenticationError(DelightedError):
    """401, api auth missing or incorrect."""
    pass


class UnsupportedFormatRequestedError(DelightedError):
    """406, invalid format in Accept header."""


class ResourceValidationError(DelightedError):
    """422, validation errors."""
    pass


class GeneralAPIError(DelightedError):
    """500, general/unknown error."""
    pass


class ServiceUnavailableError(DelightedError):
    """503, maintenance or overloaded."""
    pass
