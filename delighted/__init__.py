__title__ = 'delighted'
__version__ = '2.3.0'
__author__ = 'Ben Turner'
__license__ = 'MIT'

from delighted.http_adapter import HTTPAdapter  # noqa

api_key = None
api_base_url = 'https://api.delightedapp.com/v1/'
http_adapter = HTTPAdapter()
shared_client = None


def get_shared_client():
    global shared_client
    if not shared_client:
        shared_client = Client()
    return shared_client


from delighted.client import Client  # noqa
from delighted.resource import (  # noqa
    Metrics,
    Person,
    SurveyRequest,
    SurveyResponse,
    Unsubscribe,
    Bounce,
)
