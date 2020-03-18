class HTTPResponse(object):

    def __init__(self, status_code, headers, body, links={}):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.links = links
