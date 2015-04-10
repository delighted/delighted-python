from base64 import b64encode
import json

import delighted
from delighted.http_adapter import HTTPAdapter


class Client(object):

    def __init__(self, api_key=None, api_base_url=delighted.api_base_url, http_adapter=HTTPAdapter()):
        if api_key is None:
            raise ValueError("You must provide an API key by setting \
                    delighted.api_key = '123abc' or passing api_key='abc123' \
                    when instantiating Client.")

        self.api_key = api_key
        self.api_base_url = api_base_url
        self.http_adapter = http_adapter

    def request(self, resource, url, params=None, headers=None):
        headers['Authorization'] = 'Basic %s' % (b64encode(delighted.api_key))
        headers['User-Agent'] = "Delighted Python %s" % delighted.VERSION

        url = "%s/%s" % (delighted.api_base_url, resource)

        if method == 'post':
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        data = json.dumps(params)

        return self.http_adapter.request(method, url, headers, data)
