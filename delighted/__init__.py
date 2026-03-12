__title__ = 'delighted'
__version__ = '4.2.0'
__author__ = 'Ben Turner'
__license__ = 'MIT'

import warnings
warnings.warn(
    "Delighted is being sunset on June 30, 2026. This package is deprecated "
    "and will no longer be maintained or receive updates. For more "
    "information, visit the Delighted Sunset FAQ: "
    "https://help.delighted.com/article/840-delighted-sunset-faq",
    FutureWarning,
    stacklevel=2,
)

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
    AutopilotConfiguration,
    AutopilotMembership,
    AutopilotMembershipForEmail,
    AutopilotMembershipForSms,
)
