import unittest

import delighted


class ClientTest(unittest.TestCase):

    def test_instantiating_client_requires_api_key(self):
        self.assertRaises(ValueError, lambda: delighted.Client())
        delighted.Client(api_key='abc123')
