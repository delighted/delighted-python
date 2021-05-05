import six
import time
from six.moves.urllib_parse import quote

from delighted import get_shared_client
from delighted.errors import TooManyRequestsError


class Resource(dict):

    def __init__(self, attrs={}):
        super(Resource, self).__init__()

        if 'id' in attrs:
            object.__setattr__(self, 'id', attrs['id'])

        if hasattr(self.__class__, 'expandable_attributes'):
            for attr, klass in six.iteritems(self.expandable_attributes):
                if attr in attrs and isinstance(attrs[attr], dict):
                    expandable_attrs = attrs.pop(attr)
                    item_id = expandable_attrs['id']
                    super(Resource, self).__setitem__(attr, klass(expandable_attrs))

        for k, v in six.iteritems(attrs):
            super(Resource, self).__setitem__(k, v)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(Resource, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_' and k != '_attrs':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    @classmethod
    def _set_client(self, params):
        self.client = params.pop('client', None) or get_shared_client()

    @classmethod
    def _identifier_string(self, **identifier_dict):
        if len(identifier_dict) != 1:
            raise ValueError('You must pass exactly one identifier name and value')

        identifier_key = list(identifier_dict.keys())[0]
        identifier_value = list(identifier_dict.values())[0]

        if 'id' == str(identifier_key):
            return str(identifier_value)
        else:
            return '%s:%s' % (identifier_key, identifier_value)


class AllResource(Resource):
    @classmethod
    def all(self, **params):
        self._set_client(params)
        j = self.client.request_json('get', self.path, {}, params)
        return [self(i) for i in j]


class ListResource(Resource):
    @classmethod
    def list(self, **params):
        self._set_client(params)
        return ListObject(self, self.path, params, self.client)


class CreateableResource(Resource):

    @classmethod
    def create(self, **params):
        self._set_client(params)
        j = self.client.request_json('post', self.path, {}, params)
        return self(j)


class RetrievableResource(Resource):

    @classmethod
    def retrieve(self, *args, **params):
        self._set_client(params)
        path = '%s/%s' % (self.path, args[0]) if len(args) > 0 else self.path
        j = self.client.request_json('get', path, {}, params)
        return self(j)


class UpdateableResource(Resource):
    def save(self, **params):
        self._set_client(params)
        if hasattr(self.__class__, 'expandable_attributes'):
            expand_attrs = list(self.__class__.expandable_attributes.keys())
            params.update({'expand': expand_attrs})
        path = '%s/%s' % (self.path, self.id) if self.id else self.path
        j = self.client.request_json('put', path, {}, dict(self))
        return type(self)(j)


class DeleteableResource(Resource):
    @classmethod
    def delete(self, **params):
        self._set_client(params)
        identifier = self._identifier_string(**params)
        path = '%s/%s' % (self.path, quote(identifier, ''))
        return self.client.request_json('delete', path, {}, {})


class Metrics(RetrievableResource):
    path = 'metrics'
    singleton_resource = True


class Person(ListResource, AllResource, CreateableResource, DeleteableResource):
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

        return self.client.request_json('delete', url)


class SurveyResponse(AllResource, CreateableResource,
                     RetrievableResource, UpdateableResource):
    expandable_attributes = {'person': Person}
    path = 'survey_responses'


class Unsubscribe(AllResource, CreateableResource):
    path = 'unsubscribes'


class Bounce(AllResource):
    path = 'bounces'


class AutopilotConfiguration(RetrievableResource):
    path = 'autopilot'


class AutopilotMembership:

    @classmethod
    def forEmail(self):
        return AutopilotMembershipForEmail

    @classmethod
    def forSms(self):
        return AutopilotMembershipForSms

    @classmethod
    def delete(self, **params):
        try:
            self._set_client(params)
            return self.client.request_json('delete', self.path, {}, params)
        except AttributeError:
            print('You must first call a platform-specific method (e.g. forEmail())')
            raise


class AutopilotMembershipForEmail(AutopilotMembership, CreateableResource, ListResource):
    path = 'autopilot/email/memberships'


class AutopilotMembershipForSms(AutopilotMembership, CreateableResource, ListResource):
    path = 'autopilot/sms/memberships'


class ListObject:
    def __init__(self, klass, path, params, client):
        self.klass = klass
        self.path = path
        self.params = params
        self.client = client
        self.iteration_count = 0

    def auto_paging_iter(self, auto_handle_rate_limits=False):
        while True:
            try:
                # Get next (or first) page
                if self.iteration_count == 0:
                    result = self.client.request('get', self.path, {}, self.params)
                else:
                    result = self.client.request('get', self.next_link, full_url=True)
            except TooManyRequestsError as e:
                if auto_handle_rate_limits:
                    # Sleep and retry call
                    time.sleep(e.retry_after)
                    continue
                else:
                    raise

            self.iteration_count += 1
            if 'next' in result.response.links:
                self.next_link = result.response.links['next']['url']
            else:
                self.next_link = None

            for item in result.json:
                yield self.klass(item)

            if not self.next_link:
                break
