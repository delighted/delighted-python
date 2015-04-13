import unittest

from delighted import Client


class ClientTest(unittest.TestCase):

    def test_instantiating_client_requires_api_key(self):
        with self.assertRaises(ValueError):
            Client()
        Client(api_key='abc123')
