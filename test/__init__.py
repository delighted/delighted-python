import json
import unittest

from mock import Mock, patch

import delighted


get_headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic YWJjMTIz',
    'User-Agent': "Delighted Python %s" % delighted.__version__
}
post_headers = get_headers.copy()
post_headers.update({'Content-Type': 'application/json'})


class DelightedTestCase(unittest.TestCase):

    def setUp(self):
        super(DelightedTestCase, self).setUp()

        delighted.api_key = 'abc123'

        self.request_patcher = patch('requests.request')
        self.request_mock = self.request_patcher.start()

    def tearDown(self):
        super(DelightedTestCase, self).tearDown()

        self.request_patcher.stop()

    def mock_response(self, status_code, headers, data, links=None):
        self.mock_multiple_responses([delighted.http_response.HTTPResponse(status_code, headers, data, links)])

    def mock_multiple_responses(self, responses):
        mock_responses = []
        for response in responses:
            mock_response = Mock()
            mock_response.status_code = response.status_code
            mock_response.headers = response.headers
            mock_response.text = json.dumps(response.body)
            mock_response.links = response.links
            mock_responses.append(mock_response)

        self.request_mock.side_effect = mock_responses

    def mock_error(self, mock):
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, meth, url, headers, post_data, get_params):
        if post_data is not None:
            post_data = json.dumps(post_data)
        self.request_mock.assert_called_once_with(meth, url,
                                                  headers=headers,
                                                  data=post_data,
                                                  params=get_params)

    def check_multiple_call(self, calls):
        self.assertEqual(self.request_mock.call_count, len(calls))
        for call in calls:
            if call['kwargs']['data'] is not None:
                call['kwargs']['data'] = json.dumps(call['kwargs']['data'])
            self.request_mock.assert_any_call(call['meth'], call['url'], **call['kwargs'])
