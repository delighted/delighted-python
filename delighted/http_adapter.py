import requests

from delighted.http_response import HTTPResponse


class HTTPAdapter(object):

    def request(self, method, uri, headers={}, data=None, params=None):
        resp = requests.request(method, uri, headers=headers, data=data,
                                params=params)

        return HTTPResponse(resp.status_code, resp.headers, resp.text)
