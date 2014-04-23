
class DelightedError(Exception):
    pass


class APIKeyMissing(DelightedError):
    """Without an API key this library cannot connect to Delighted."""
    pass


class Unauthorized(DelightedError):
    """401 Indicates the API key was invalid."""
    pass


class NotAcceptable(DelightedError):
    """406 Indicates that the format of the request was not correct.
    Endpoints only support JSON. You can either pass the Accept:
    application/json header or suffix the request URL with .json."""
    pass


class NotFound(DelightedError):
    """404 Indicates that the requested resource could not be found."""
    pass


class UnprocessableEntity(DelightedError):
    """422 Indicates the request was invalid. This usually means some of
    the required parameters were missing. Information about the specific
    errors will be returned in the response."""
    pass


class InternalServerError(DelightedError):
    """500 Indicates that we are having trouble on our end."""
    pass


class ServiceUnavailable(DelightedError):
    """503 Indicates that we are currently down for maintenance."""
    pass


API_ERRORS = {
    401: Unauthorized,
    404: NotFound,
    406: NotAcceptable,
    422: UnprocessableEntity,
    500: InternalServerError,
    503: ServiceUnavailable,
}
