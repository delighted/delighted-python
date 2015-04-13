from collections import MutableMapping
from copy import deepcopy
from itertools import combinations
from urllib import quote

from delighted import shared_client


class Resource(dict):

    def __init__(self, attrs={}):
        super(Resource, self).__init__()

        if 'id' in attrs:
            self.id = attrs['id']
            del attrs['id']

        self._attrs = attrs

        for k, v in self._attrs.iteritems():
            super(Resource, self).__setitem__(k, v)

        if hasattr(self.__class__, 'expandable_attributes'):
            for attr, klass in self.expandable_attributes.items():
                if attr in self._attrs and dict == type(self._attrs[attr]):
                    expandable_attrs = self._attrs.pop(attr)
                    object.__setattr__(self, attr, klass(expandable_attrs))

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(Resource, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_' and k is not '_attrs':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError, err:
            raise AttributeError(*err.args)

    @classmethod
    def _set_client(self, params):
        if 'client' in params:
            self.client = params['client']
        else:
            self.client = shared_client()

class AllResource(Resource):
    pass


class CreateableResource(Resource):

    @classmethod
    def create(self, **params):
        self._set_client(params)
        json = self.client.request('post', self.path, {}, params)
        return self(json)


class RetrievableResource(Resource):

    @classmethod
    def retrieve(self, *args, **params):
        self._set_client(params)
        path = '%s/%s' % (self.path, args[0]) if len(args) > 0 else self.path
        json = self.client.request('get', path, {}, params)
        return self(json)


class UpdateableResource(Resource):

    @classmethod
    def update(self, **params):
        pass


class Metrics(RetrievableResource):
    path = 'metrics'
    singleton_resource = True


class Person(CreateableResource):
    path = 'people'


class SurveyRequest(Resource):
    path = 'people/%s/survey_requests/pending'

    @classmethod
    def delete_pending(self, **params):
        if 'person_email' not in params:
            raise ValueError("You must pass person_email")

        self._set_client(params)

        escaped_email = quote(params['person_email'])
        url = self.path % escaped_email

        return self.client.request('delete', url)


class SurveyResponse(AllResource, CreateableResource,
                     RetrievableResource, UpdateableResource):
    expandable_attributes = { 'person': Person }
    path = 'survey_responses'


class Unsubscribe(CreateableResource):
    path = 'unsubscribes'
