import delighted
from delighted.util import aware_datetime_to_epoch_seconds, \
    naive_date_to_datetime
from . import get_headers, post_headers, DelightedTestCase
from delighted.errors import TooManyRequestsError
import datetime
import pytz
import tzlocal
from base64 import b64encode
from mock import patch
from six import b
import sys


class TestResource(DelightedTestCase):
    def setUp(self):
        super(TestResource, self).setUp()

    def check_retrieving_metrics(self, client=None):
        data = {'nps': 10}
        url = 'https://api.delightedapp.com/v1/metrics'
        self.mock_response(200, {}, data)

        expected_headers = get_headers.copy()
        retrieve_kwargs = {}
        if client:
            retrieve_kwargs['client'] = client
            expected_headers['Authorization'] = 'Basic %s' % b64encode(b(client.api_key)).decode('ascii')

        metrics = delighted.Metrics.retrieve(**retrieve_kwargs)
        self.check_call('get', url, expected_headers, {}, None)
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def test_retrieving_metrics(self):
        self.check_retrieving_metrics()

    def test_retrieving_metrics_other_client(self):
        client = delighted.Client(api_key='example')
        self.check_retrieving_metrics(client=client)

    def test_retrieving_metrics_range_unixtimestamp(self):
        data = {'nps': 10}
        self.mock_response(200, {}, data)
        since = 1425168000
        until = 1430348400
        url = 'https://api.delightedapp.com/v1/metrics'

        metrics = delighted.Metrics.retrieve(since=since, until=until)
        self.check_call('get', url, get_headers, None,
                        {'since': 1425168000, 'until': 1430348400})
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def test_retrieving_metrics_range_date_object(self):
        data = {'nps': 10}
        self.mock_response(200, {}, data)
        since = datetime.date(2013, 10, 1)
        until = datetime.date(2013, 11, 1)
        timezone = tzlocal.get_localzone()
        since_seconds = self._naive_date_to_epoch_seconds(since, timezone)
        until_seconds = self._naive_date_to_epoch_seconds(until, timezone)
        url = 'https://api.delightedapp.com/v1/metrics'

        metrics = delighted.Metrics.retrieve(since=since, until=until)
        self.check_call('get', url, get_headers, None,
                        {'since': since_seconds, 'until': until_seconds})
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def test_retrieving_metrics_range_datetime_object(self):
        data = {'nps': 10}
        self.mock_response(200, {}, data)
        timezone = pytz.timezone('America/Chicago')
        since = timezone.localize(datetime.datetime(2013, 10, 1))
        until = timezone.localize(datetime.datetime(2013, 11, 1))
        url = 'https://api.delightedapp.com/v1/metrics'

        metrics = delighted.Metrics.retrieve(since=since, until=until)
        self.check_call('get', url, get_headers, None,
                        {'since': 1380603600, 'until': 1383282000})
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def check_creating_or_updating_a_person(self, client=None):
        email = 'foo@bar.com'
        data = {'id': '123', 'email': email}
        url = 'https://api.delightedapp.com/v1/people'
        self.mock_response(200, {}, data)

        expected_headers = post_headers.copy()
        create_kwargs = {'email': email}
        if client:
            create_kwargs['client'] = client
            expected_headers['Authorization'] = 'Basic %s' % b64encode(b(client.api_key)).decode('ascii')

        person = delighted.Person.create(**create_kwargs)
        self.assertTrue(delighted.Person is type(person))
        self.assertEqual(person, {'id': '123', 'email': email})
        self.assertEqual(person.email, email)
        self.assertEqual('123', person.id)
        self.check_call('post', url, expected_headers, {'email': email}, None)

    def test_creating_or_updating_a_person(self):
        self.check_creating_or_updating_a_person()

    def test_creating_or_updating_a_person_other_client(self):
        client = delighted.Client(api_key='example')
        self.check_creating_or_updating_a_person(client=client)

    def test_unsubscribing_a_person(self):
        email = 'person@example.com'
        data = {'person_email': email}
        url = 'https://api.delightedapp.com/v1/unsubscribes'
        self.mock_response(200, {}, {'ok': True})

        delighted.Unsubscribe.create(person_email=email)
        self.check_call('post', url, post_headers, data, None)

    def test_deleting_a_person_by_multiple_identifiers(self):
        self.assertRaises(ValueError, lambda: delighted.Person.delete(id=42, email="foo@example.com"))

    def test_deleting_a_person_by_id(self):
        url = 'https://api.delightedapp.com/v1/people/42'
        self.mock_response(202, {}, {'ok': True})

        delighted.Person.delete(id=42)
        self.check_call('delete', url, post_headers, {}, None)

    def test_deleting_a_person_by_email(self):
        url = 'https://api.delightedapp.com/v1/people/email%3Afoo%40example.com'
        self.mock_response(202, {}, {'ok': True})

        delighted.Person.delete(email='foo@example.com')
        self.check_call('delete', url, post_headers, {}, None)

    def test_deleting_a_person_by_phone_number(self):
        url = 'https://api.delightedapp.com/v1/people/phone_number%3A%2B14155551212'
        self.mock_response(202, {}, {'ok': True})

        delighted.Person.delete(phone_number='+14155551212')
        self.check_call('delete', url, post_headers, {}, None)


    def test_deleting_pending_survey_requests_for_a_person(self):
        email = 'foo@bar.com'
        url = 'https://api.delightedapp.com/v1/people/foo%40bar.com' + \
              '/survey_requests/pending'
        self.mock_response(200, {}, {'ok': True})

        result = delighted.SurveyRequest.delete_pending(person_email=email)
        self.assertTrue(dict is type(result))
        self.assertEqual({'ok': True}, result)
        self.check_call('delete', url, post_headers, {}, None)

    def test_creating_a_survey_response(self):
        url = 'https://api.delightedapp.com/v1/survey_responses'
        data = {'id': '456', 'person': '123', 'score': 10}
        self.mock_response(200, {}, data)
        survey_response = delighted.SurveyResponse.create(person='123',
                                                          score=10)
        self.assertTrue(delighted.SurveyResponse is type(survey_response))
        self.assertEqual({'id': '456', 'person': '123', 'score': 10}, survey_response)
        self.assertEqual('123', survey_response.person)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)
        resp = {'person': '123', 'score': 10}
        self.check_call('post', url, post_headers, resp, None)

    def test_retrieving_a_survey_response_expand_person(self):
        url = 'https://api.delightedapp.com/v1/survey_responses/456'
        resp = {'id': '456',
                'person': {'id': '123', 'email': 'foo@bar.com', 'type': 'aaa'},
                'score': 10}
        self.mock_response(200, {}, resp)

        survey_response = delighted.SurveyResponse.retrieve('456',
                                                            expand=['person'])
        self.check_call('get', url, get_headers, None, {'expand[]': 'person'})
        self.assertTrue(delighted.SurveyResponse is type(survey_response))
        self.assertTrue(delighted.Person is type(survey_response.person))
        self.assertEqual(resp, survey_response)
        self.assertEqual(
            {'id': '123', 'email': 'foo@bar.com', 'type': 'aaa'},
            survey_response.person
        )
        self.assertEqual('123', survey_response.person.id)
        self.assertEqual('foo@bar.com', survey_response.person.email)
        self.assertEqual('aaa', survey_response.person.type)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)

    def test_updating_a_survey_response(self):
        url = 'https://api.delightedapp.com/v1/survey_responses/456'
        data = {'person': '123', 'score': 10}
        resp = {'id': '456', 'person': '123', 'score': 10}
        self.mock_response(200, {}, resp)

        old = {'id': '456', 'person': '321', 'score': 1}
        survey_response = delighted.SurveyResponse(old)
        survey_response.person = '123'
        survey_response.score = 10
        self.assertTrue(delighted.SurveyResponse is type(survey_response.save()))
        self.check_call('put', url, post_headers, resp, None)
        self.assertEqual(resp, survey_response)
        self.assertEqual('123', survey_response.person)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)

    def test_listing_all_survey_responses(self):
        url = 'https://api.delightedapp.com/v1/survey_responses'
        resp1 = {'id': '123', 'comment': 'One'}
        resp2 = {'id': '456', 'comment': 'Two'}
        self.mock_response(200, {}, [resp1, resp2])

        survey_responses = delighted.SurveyResponse.all(order='desc')
        self.check_call('get', url, get_headers, None, {'order': 'desc'})
        self.assertTrue(list is type(survey_responses))
        self.assertTrue(delighted.SurveyResponse is type(survey_responses[0]))
        self.assertEqual({'id': '123', 'comment': 'One'}, survey_responses[0])
        self.assertEqual('One', survey_responses[0].comment)
        self.assertEqual('123', survey_responses[0].id)
        self.assertTrue(delighted.SurveyResponse is type(survey_responses[1]))
        self.assertEqual({'id': '456', 'comment': 'Two'}, survey_responses[1])
        self.assertEqual('Two', survey_responses[1].comment)
        self.assertEqual('456', survey_responses[1].id)

    def test_listing_all_survey_responses_expand_person(self):
        url = 'https://api.delightedapp.com/v1/survey_responses'
        resp1 = {'id': '123', 'comment': 'One',
                 'person': {'id': '456', 'email': 'foo@bar.com', 'type': 'aaa'}}
        resp2 = {'id': '789', 'comment': 'Two',
                 'person': {'id': '012', 'email': 'koo@bar.com', 'type': 'bbb'}}
        self.mock_response(200, {}, [resp1, resp2])

        survey_responses = delighted.SurveyResponse.all(expand=['person'])
        self.check_call('get', url, get_headers, None, {'expand[]': 'person'})
        self.assertTrue(list is type(survey_responses))

        self.assertTrue(delighted.SurveyResponse is type(survey_responses[0]))
        self.assertEqual(resp1, survey_responses[0])
        self.assertEqual('One', survey_responses[0].comment)
        self.assertEqual('123', survey_responses[0].id)
        self.assertEqual(delighted.Person, type(survey_responses[0].person))
        self.assertEqual(
            {'id': '456', 'email': 'foo@bar.com', 'type': 'aaa'},
            survey_responses[0].person
        )
        self.assertEqual('456', survey_responses[0].person.id)
        self.assertEqual('foo@bar.com', survey_responses[0].person.email)
        self.assertEqual('aaa', survey_responses[0].person.type)

        self.assertTrue(delighted.SurveyResponse is type(survey_responses[1]))
        self.assertEqual(resp2, survey_responses[1])
        self.assertEqual('Two', survey_responses[1].comment)
        self.assertEqual('789', survey_responses[1].id)
        self.assertEqual(delighted.Person, type(survey_responses[1].person))
        self.assertEqual(
            {'id': '012', 'email': 'koo@bar.com', 'type': 'bbb'},
            survey_responses[1].person
        )
        self.assertEqual('012', survey_responses[1].person.id)
        self.assertEqual('koo@bar.com', survey_responses[1].person.email)
        self.assertEqual('bbb', survey_responses[1].person.type)

    def test_listing_all_people(self):
        url = 'https://api.delightedapp.com/v1/people'
        person1 = {'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}
        person2 = {'id': '456', 'email': 'bar@example.com', 'name': 'Bar Kim'}
        self.mock_response(200, {}, [person1, person2])

        people = delighted.Person.all()
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(list is type(people))
        self.assertTrue(delighted.Person is type(people[0]))
        self.assertEqual({'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}, people[0])
        self.assertEqual('foo@example.com', people[0].email)
        self.assertEqual('Foo Smith', people[0].name)
        self.assertEqual('123', people[0].id)
        self.assertTrue(delighted.Person is type(people[1]))
        self.assertEqual({'id': '456', 'email': 'bar@example.com', 'name': 'Bar Kim'}, people[1])
        self.assertEqual('Bar Kim', people[1].name)
        self.assertEqual('bar@example.com', people[1].email)
        self.assertEqual('456', people[1].id)

    def test_listing_all_people_pagination(self):
        url = 'https://api.delightedapp.com/v1/people'
        url_next = 'http://api.delightedapp.com/v1/people?nextlink123'
        person1 = {'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}
        person2 = {'id': '456', 'email': 'bar@example.com', 'name': 'Bar Kim'}
        person3 = {'id': '789', 'email': 'foos@ball.com', 'name': 'Foos Ball'}
        mock_response = delighted.http_response.HTTPResponse(200, {}, [person1, person2], {'next': {'url': url_next}})
        mock_response_next = delighted.http_response.HTTPResponse(200, {}, [person3], {})
        self.mock_multiple_responses([mock_response, mock_response_next])

        people = []
        for person in delighted.Person.list().auto_paging_iter():
            people.append(person)
        call_1 = {'meth': 'get', 'url': url, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        call_2 = {'meth': 'get', 'url': url_next, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        self.check_multiple_call([call_1, call_2])
        self.assertEqual(len(people), 3)
        self.assertTrue(delighted.Person is type(people[0]))
        self.assertEqual(person1, people[0])
        self.assertTrue(delighted.Person is type(people[1]))
        self.assertEqual(person2, people[1])
        self.assertTrue(delighted.Person is type(people[2]))
        self.assertEqual(person3, people[2])

    def test_listing_all_people_pagination_rate_limited(self):
        url = 'https://api.delightedapp.com/v1/people'
        url_next = 'http://api.delightedapp.com/v1/people?nextlink123'
        person1 = {'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}
        mock_response = delighted.http_response.HTTPResponse(200, {}, [person1], {'next': {'url': url_next}})
        mock_response_rate_limited = delighted.http_response.HTTPResponse(429, {'Retry-After': '10'}, [], {})
        self.mock_multiple_responses([mock_response, mock_response_rate_limited])

        people = []
        with self.assertRaises(TooManyRequestsError) as context:
            for person in delighted.Person.list().auto_paging_iter(auto_handle_rate_limits=False):
                people.append(person)

        self.assertEqual(context.exception.response.headers['Retry-After'], '10')
        call_1 = {'meth': 'get', 'url': url, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        call_2 = {'meth': 'get', 'url': url_next, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        self.check_multiple_call([call_1, call_2])
        self.assertEqual(len(people), 1)
        self.assertTrue(delighted.Person is type(people[0]))
        self.assertEqual(person1, people[0])

    def test_listing_all_people_pagination_auto_handle_rate_limit(self):
        url = 'https://api.delightedapp.com/v1/people'
        url_next = 'http://api.delightedapp.com/v1/people?nextlink123'
        person1 = {'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}
        person_next = {'id': '456', 'email': 'next@example.com', 'name': 'Next Person'}
        mock_response = delighted.http_response.HTTPResponse(200, {}, [person1], {'next': {'url': url_next}})
        mock_response_rate_limited = delighted.http_response.HTTPResponse(429, {'Retry-After': '3'}, [], {})
        mock_response_accepted = delighted.http_response.HTTPResponse(200, {}, [person_next], {})
        self.mock_multiple_responses([mock_response, mock_response_rate_limited, mock_response_accepted])

        people = []
        with patch('time.sleep', return_value=None) as patched_time_sleep:
            for person in delighted.Person.list().auto_paging_iter(auto_handle_rate_limits=True):
                people.append(person)

        patched_time_sleep.assert_called_once_with(3)

        call_1 = {'meth': 'get', 'url': url, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        call_rejected = {'meth': 'get', 'url': url_next, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        call_accepted = {'meth': 'get', 'url': url_next, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        self.check_multiple_call([call_1, call_rejected, call_accepted])
        self.assertEqual(len(people), 2)
        self.assertTrue(delighted.Person is type(people[0]))
        self.assertEqual(person1, people[0])
        self.assertTrue(delighted.Person is type(people[1]))
        self.assertEqual(person_next, people[1])

    def test_listing_all_unsubscribes(self):
        url = 'https://api.delightedapp.com/v1/unsubscribes'
        resp1 = {'person_id': '123', 'email': 'foo@bar.com', 'name': 'Foo', 'unsubscribed_at': 1440621400}
        self.mock_response(200, {}, [resp1])

        unsubscribes = delighted.Unsubscribe.all()
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(list is type(unsubscribes))
        self.assertTrue(delighted.Unsubscribe is type(unsubscribes[0]))
        self.assertEqual(resp1, dict(unsubscribes[0]))

    def test_listing_all_bounces(self):
        url = 'https://api.delightedapp.com/v1/bounces'
        resp1 = {'person_id': '123', 'email': 'foo@bar.com', 'name': 'Foo', 'bounced_at': 1440621400}
        self.mock_response(200, {}, [resp1])

        bounces = delighted.Bounce.all()
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(list is type(bounces))
        self.assertTrue(delighted.Bounce is type(bounces[0]))
        self.assertEqual(resp1, dict(bounces[0]))

    def test_retrieving_autopilot_configuration(self):
        mock_response = {
          'platform_id': 'email',
          'active': True,
          'frequency': 7776000,
          'created_at': 1611431275,
          'updated_at': 1618598875
        }
        url = 'https://api.delightedapp.com/v1/autopilot/email'
        self.mock_response(200, {}, mock_response)

        autopilot = delighted.AutopilotConfiguration.retrieve('email')
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(delighted.AutopilotConfiguration is type(autopilot))
        self.assertEqual(dict(autopilot), mock_response)
        self.assertEqual(autopilot.platform_id, 'email')
        self.assertEqual(autopilot.active, True)
        self.assertRaises(AttributeError, lambda: autopilot.id)


    def test_add_person_to_autopilot(self):
        email = 'foo@bar.com'
        mock_response = {'person': {'id': 123}}
        url = 'https://api.delightedapp.com/v1/autopilot/email/memberships'
        self.mock_response(200, {}, mock_response)

        expected_headers = post_headers.copy()
        create_kwargs = {'person_id': '123', 'person_email': email}

        autopilot = delighted.AutopilotMembership.forEmail().create(**create_kwargs)
        self.assertTrue(delighted.AutopilotMembershipForEmail is type(autopilot))
        self.assertEqual(autopilot, {'person': {'id': 123}})
        self.assertEqual(123, autopilot.person['id'])
        self.check_call('post', url, expected_headers, create_kwargs, None)


    def test_delete_person_from_autopilot(self):
        phone_number = '+14155551212'
        mock_response = {'person': {'id': 123}}
        url = 'https://api.delightedapp.com/v1/autopilot/sms/memberships'
        self.mock_response(202, {}, mock_response)

        expected_headers = post_headers.copy()
        delete_kwargs = {'person_phone_number': phone_number}

        delighted.AutopilotMembership.forSms().delete(**delete_kwargs)
        self.check_call('delete', url, expected_headers, delete_kwargs, None)


    def test_list_autopilot_memberships(self):
        url = 'https://api.delightedapp.com/v1/autopilot/email/memberships'
        url_next = 'http://api.delightedapp.com/v1/autopilot/email/memberships?nextlink123'
        person_1 = {
            'created_at': 1614041806,
            'updated_at': 1618012606,
            'person': {
                'id': '1',
                'name': None,
                'email': 'foo@example.com',
                'created_at': 1611363406,
                'phone_number': '+1555555112',
                'last_sent_at': None
            },
            'next_survey_request': {
                'id': '4',
                'created_at': 1614041806,
                'survey_scheduled_at': 1620086206,
                'properties': {
                    'Purchase Experience': 'Mobile App',
                    'State': 'CA'
                }
            }
        }
        person_2 = {
            'created_at': 1614041806,
            'updated_at': 1618012606,
            'person': {
                'id': '2',
                'name': None,
                'email': 'bar@example.com',
                'created_at': 1611363406,
                'phone_number': '+1555555113',
                'last_sent_at': None
            },
            'next_survey_request': {
                'id': '5',
                'created_at': 1614041806,
                'survey_scheduled_at': 1620086206,
                'properties': {
                    'Purchase Experience': 'Web',
                    'State': 'WA'
                }
            }
        }
        mock_response = delighted.http_response.HTTPResponse(200, {}, [person_1], {'next': {'url': url_next}})
        mock_response_2 = delighted.http_response.HTTPResponse(200, {}, [person_2], {})
        self.mock_multiple_responses([mock_response, mock_response_2])

        autopilot_people = []
        for autopilot_person in delighted.AutopilotMembership.forEmail().list().auto_paging_iter():
            autopilot_people.append(autopilot_person)
        call_1 = {'meth': 'get', 'url': url, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        call_2 = {'meth': 'get', 'url': url_next, 'kwargs': {'headers': get_headers, 'data': {}, 'params': None}}
        self.check_multiple_call([call_1, call_2])
        self.assertEqual(len(autopilot_people), 2)
        self.assertTrue(delighted.AutopilotMembershipForEmail is type(autopilot_people[0]))
        self.assertEqual(person_1, autopilot_people[0])
        self.assertTrue(delighted.AutopilotMembershipForEmail is type(autopilot_people[1]))
        self.assertEqual(person_2, autopilot_people[1])

    def test_rate_limit_response(self, client=None):
        self.mock_response(429, {'Retry-After': '5'}, {})

        # https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertRaises
        # Ability to use assertRaises() as a context manager was added in 2.7
        if sys.version_info < (2, 7):
            self.assertRaises(delighted.errors.TooManyRequestsError, lambda: delighted.Metrics.retrieve(client=client))
        else:
            with self.assertRaises(delighted.errors.TooManyRequestsError) as context:
                delighted.Metrics.retrieve(client=client)

            self.assertEqual(5, context.exception.retry_after)

    @classmethod
    def _naive_date_to_epoch_seconds(cls, date_obj, timezone):
        datetime_obj = timezone.localize(naive_date_to_datetime(date_obj))
        return aware_datetime_to_epoch_seconds(datetime_obj)
