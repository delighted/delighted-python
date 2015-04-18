import unittest

import delighted


class ClientTest(unittest.TestCase):

    def test_instantiating_client_requires_api_key(self):
        with self.assertRaises(ValueError):
            delighted.Client()
        delighted.Client(api_key='abc123')
