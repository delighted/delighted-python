import unittest

from delighted import Client


class ClientTest(unittest.TestCase):

    def test_api_key_required(self):
        with self.assertRaises(ValueError):
            Client()
