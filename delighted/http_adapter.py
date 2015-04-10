import requests


class HTTPAdapter(object):
    """Wraps the logic around HTTP."""

    def request(self, method, uri, headers={}, data=None):
        response = requests.request(method, uri, headers=headers, data=data)

        return response.json()
