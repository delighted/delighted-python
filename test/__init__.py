import json
import unittest

from mock import Mock, patch

from delighted import __version__ as version
from delighted.http_response import HTTPResponse


get_headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic YWJjMTIz',
    'User-Agent': "Delighted Python %s" % version
}
post_headers = get_headers.copy()
post_headers.update({'Content-Type': 'application/json'})


class DelightedTestCase(unittest.TestCase):

    def setUp(self):
        super(DelightedTestCase, self).setUp()

        self.request_patcher = patch('requests.request')
        self.request_mock = self.request_patcher.start()

    def tearDown(self):
        super(DelightedTestCase, self).tearDown()

        self.request_patcher.stop()

    def mock_response(self, status_code, headers, data):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.headers = headers
        mock_response.text = json.dumps(data)

        self.request_mock.return_value = mock_response

    def mock_error(self, mock):
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, meth, url, headers, post_data):
        self.request_mock.assert_called_once_with(meth, url,
                                                  headers=headers,
                                                  data=json.dumps(post_data))
