import unittest

import delighted


class ClientTest(unittest.TestCase):

    def test_instantiating_client_requires_api_key(self):
        original_api_key = delighted.api_key
        try:
            delighted.api_key = None
            self.assertRaises(ValueError, lambda: delighted.Client())
            delighted.Client(api_key='abc123')
        except:
            delighted.api_key = original_api_key
