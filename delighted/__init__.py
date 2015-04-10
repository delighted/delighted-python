__title__ = 'delighted'
__version__ = '0.1.0'
__author__ = 'Robby Colvin'
__license__ = 'MIT'

api_key = None
api_base_url = 'https://api.delightedapp.com/v1'
api_version = 1

from delighted.client import Client


singleton_client = None


def shared_client():
    global singleton_client
    if not singleton_client:
        singleton_client = Client(api_key=api_key)
    return singleton_client

### Resources ###

from delighted.resource import (  # noqa
    Metrics)

metrics = Metrics
