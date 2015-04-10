import unittest

from mock import Mock, patch


class DelightedTestCase(unittest.TestCase):

    def setUp(self):
        super(DelightedTestCase, self).setUp()

        self.request_patcher = patch('delighted.http_adapter.requests.request')
        self.request_mock = self.request_patcher.start()

    def tearDown(self):
        super(DelightedTestCase, self).tearDown()

        self.request_patcher.stop()

    def mock_response(self, data):
        mock_response = Mock()
        mock_response.json.return_value = data

        self.request_mock.return_value = mock_response

    def mock_error(self, mock):
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, meth, url, post_data, headers):
        self.request_mock.assert_called_once_with(meth, url,
                                                  headers=headers,
                                                  data=post_data)
