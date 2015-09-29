from base64 import b64encode
import json
from six import b
from six.moves.urllib_parse import urljoin

import delighted
from delighted.errors import (
    AuthenticationError,
    GeneralAPIError,
    ResourceValidationError,
    ServiceUnavailableError,
    UnsupportedFormatRequestedError,
)
from delighted.http_adapter import HTTPAdapter
from delighted.util import encode


class Client(object):

    def __init__(self, api_key=None, api_base_url=delighted.api_base_url,
                 http_adapter=HTTPAdapter()):
        if api_key is None:
            raise ValueError("You must provide an API key by setting " +
                             "delighted.api_key = '123abc' or passing " +
                             "api_key='abc123' when instantiating client.")

        self.api_key = api_key
        self.api_base_url = api_base_url
        self.http_adapter = http_adapter

    def request(self, method, resource, headers={}, params={}):
        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Basic %s' % \
            (b64encode(b(delighted.api_key)).decode('ascii'))
        headers['User-Agent'] = "Delighted Python %s" % delighted.__version__
        if method in ('post', 'put', 'delete'):
            headers['Content-Type'] = 'application/json'

        url = urljoin(delighted.api_base_url, resource)

        if method == 'get' and params:
            params = dict((key, value) for (key, value) in encode(params))
            data = None
        else:
            data = json.dumps(params)
            params = None

        response = self.http_adapter.request(method, url, headers, data,
                                             params)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in (200, 201, 202):
            return json.loads(response.body)
        if response.status_code == 401:
            raise AuthenticationError(response)
        if response.status_code == 406:
            raise UnsupportedFormatRequestedError(response)
        if response.status_code == 422:
            raise ResourceValidationError(response)
        if response.status_code == 503:
            raise ServiceUnavailableError(response)
        raise GeneralAPIError(response)
