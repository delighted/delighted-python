from delighted import shared_client


class Resource(object):
    """Resource"""

    @classmethod
    def class_url(cls):
        return "/v1/%s" % (cls.path,)


class CreateableResource(Resource):

    @classmethod
    def create(cls, api_key=None, idempotency_key=None, **params):
        url = cls.class_url()
        headers = {}

        return shared_client().request('post', url, params, headers)


class UpdatableResource(Resource):
    def save(self):
        pass


class DeletableResource(Resource):
    def delete(self):
        pass


class Metrics(UpdatableResource, DeletableResource):
    path = '/metrics'

    @classmethod
    def retrieve(cls, **params):
        headers = {}
        response = shared_client().request('get', cls.path, params, headers)

        return response
