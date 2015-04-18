from base64 import b64encode
import json
import urllib
import urlparse

import delighted
from delighted.http_adapter import HTTPAdapter
from delighted.util import query_encode


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
        data = json.dumps(params)

        headers['Accept'] = 'application/json'
        headers['Authorization'] = 'Basic %s' % (b64encode(delighted.api_key))
        headers['User-Agent'] = "Delighted Python %s" % delighted.__version__
        if method in ('post', 'put', 'delete'):
            headers['Content-Type'] = 'application/json'

        url = "%s%s" % (delighted.api_base_url, resource)
        if method is 'get' and params != {}:
            scheme, netloc, path, base_query, fragment = urlparse.urlsplit(url)
            url += '?' + urllib.urlencode(list(query_encode(params)))
            data = '{}'

        response = self.http_adapter.request(method, url, headers, data)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in (200, 201, 202):
            return json.loads(response.body)
        if response.status_code is 401:
            raise delighted.errors.AuthenticationError(response)
        if response.status_code is 406:
            raise delighted.errors.UnsupportedFormatRequestedError(response)
        if response.status_code is 422:
            raise delighted.errors.ResourceValidationError(response)
        if response.status_code is 500:
            raise delighted.errors.GeneralAPIError(response)
        if response.status_code is 503:
            raise delighted.errors.ServiceUnavailableError(response)
