
class Metrics(object):
    def __init__(self, master):
        self.master = master

    def get(self, since=None, until=None, trend=None):
        """general description

        Args:
           since (int): An optional Unix timestamp to restrict metrics to
           those created on or after this time. Formatting example (for 1
            hour ago): 1398189756.
           until (int): An optional Unix timestamp to restrict metrics to
           those created on or before this time. Formatting example (for
            the current time): 1398193356.
           trend (string): An optional ID of a trend to restrict metrics
           to that trend. To obtain the ID for a trend, visit the trends
           page. For example, if the URL for the desired trend ends with
           /trends/1234 the ID of that trend is 1234.

        Returns:
           nps (int)
           promoter_count (int)
           promoter_percent (float)
           passive_count (int)
           passive_percent (float)
           detractor_count (int)
           detractor_percent (float)
           response_count (int)

        Raises:
           DelightedError: A general Delighted error has occurred
           Unauthorized: No API key provided
           NotAcceptable: Request format was incorrect
           UnprocessableEntity: Request parameters were missing
           InternalServerError: Indicates that we are having trouble on our end
           ServiceUnavailable: Indicates that we are currently down for
           maintenance
        """

        _params = {}

        if since is not None and isinstance(since, int):
            _params['since'] = since

        if until is not None and isinstance(until, int):
            _params['until'] = until

        if trend is not None and isinstance(trend, str):
            _params['trend'] = trend

        return self.master.get('metrics', _params)
