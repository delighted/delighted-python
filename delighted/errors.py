class Error(Exception):
    """Base error """

    # def __init__(self, response):
    #     self.response = response

    # def __repr__(self):
    #     return "<#{@response.status_code}: #{@response.body}>"

    # __str__ = __repr__


class AuthenticationError(Error):
    """401, api auth missing or incorrect."""
    pass


class UnsupportedFormatRequestedError(Error):
    """406, invalid format in Accept header."""


class ResourceValidationError(Error):
    """422, validation errors."""
    pass


class GeneralAPIError(Error):
    """500, general/unknown error."""
    pass


class ServiceUnavailableError(Error):
    """503, maintenance or overloaded."""
    pass
