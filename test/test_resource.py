import delighted
from . import DelightedTestCase


class TestResource(DelightedTestCase):

    def test_retreive_metrics(self):
        data = {'nps': 10}
        headers = {'Authorization': 'Basic YWJjMTIz', 'User-Agent': 'pytest'}
        url = 'https://api.delightedapp.com/v1/metrics'
        delighted.api_key = 'abc123'
        self.mock_response(data)

        metrics = delighted.metrics.retrieve()
        assert metrics == data
        self.check_call('get', url, '{}', headers)
        with self.assertRaises(AttributeError):
            metrics.id
