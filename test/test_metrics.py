from test import email, delighted


class TestGetMetrics(object):

    def now(self):

        from datetime import datetime

        return datetime.now()

    def addSeconds(self, date_time, seconds):

        from datetime import timedelta

        return date_time + timedelta(seconds=seconds)

    def assert_between(self, date_time, start, end):

        from time import mktime

        assert (date_time >= mktime(start.timetuple()))
        assert (date_time <= mktime(end.timetuple()))

    def test_get_metrics(self, delighted):

        from datetime import timedelta

        until = self.now()

        since = until - timedelta(days=365)

        response = delighted.metrics.get(since=since, until=until)

        assert isinstance(response['nps'], int)
        assert isinstance(response['promoter_count'], int)
        assert isinstance(response['promoter_percent'], float)
        assert isinstance(response['passive_count'], int)
        assert isinstance(response['passive_percent'], float)
        assert isinstance(response['detractor_count'], int)
        assert isinstance(response['detractor_percent'], float)
        assert isinstance(response['response_count'], int)

    def test_get_metrics_with_no_range(self, delighted):

        response = delighted.metrics.get()

        assert isinstance(response['nps'], int)
        assert isinstance(response['promoter_count'], int)
        assert isinstance(response['promoter_percent'], float)
        assert isinstance(response['passive_count'], int)
        assert isinstance(response['passive_percent'], float)
        assert isinstance(response['detractor_count'], int)
        assert isinstance(response['detractor_percent'], float)
        assert isinstance(response['response_count'], int)
