import delighted
from delighted.util import aware_datetime_to_epoch_seconds, \
    naive_date_to_datetime
from . import get_headers, post_headers, DelightedTestCase
import datetime
import pytz
import tzlocal
from base64 import b64encode
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
        self.assertEqual(dict(person), {'email': email})
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
        self.assertEqual({'person': '123', 'score': 10}, dict(survey_response))
        self.assertEqual('123', survey_response.person)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)
        resp = {'person': '123', 'score': 10}
        self.check_call('post', url, post_headers, resp, None)

    def test_retrieving_a_survey_response_expand_person(self):
        url = 'https://api.delightedapp.com/v1/survey_responses/456'
        data = {'id': '456',
                'person': {'id': '123', 'email': 'foo@bar.com'},
                'score': 10}
        self.mock_response(200, {}, data)

        survey_response = delighted.SurveyResponse.retrieve('456',
                                                            expand=['person'])
        self.check_call('get', url, get_headers, None, {'expand[]': 'person'})
        self.assertTrue(delighted.SurveyResponse is type(survey_response))
        self.assertTrue(delighted.Person is type(survey_response.person))
        self.assertEqual({'person': '123', 'score': 10}, dict(survey_response))
        self.assertEqual('123', survey_response.person.id)
        resp_person = {'email': 'foo@bar.com'}
        self.assertEqual(resp_person, dict(survey_response.person))
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)

    def test_updating_a_survey_response(self):
        url = 'https://api.delightedapp.com/v1/survey_responses/456'
        data = {'person': '123', 'score': 10}
        resp = {'id': '456', 'person': '123', 'score': 10}
        self.mock_response(200, {}, resp)

        resp = {'id': '456', 'person': '321', 'score': 1}
        survey_response = delighted.SurveyResponse(resp)
        survey_response.person = '123'
        survey_response.score = 10
        self.assertTrue(delighted.SurveyResponse is type(survey_response.save()))
        self.check_call('put', url, post_headers, data, None)
        resp = {'person': '123', 'score': 10}
        self.assertEqual(resp, dict(survey_response))
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
        self.assertEqual({'comment': 'One'}, dict(survey_responses[0]))
        self.assertEqual('One', survey_responses[0].comment)
        self.assertEqual('123', survey_responses[0].id)
        self.assertTrue(delighted.SurveyResponse is type(survey_responses[1]))
        self.assertEqual({'comment': 'Two'}, dict(survey_responses[1]))
        self.assertEqual('Two', survey_responses[1].comment)
        self.assertEqual('456', survey_responses[1].id)

    def test_listing_all_survey_responses_expand_person(self):
        url = 'https://api.delightedapp.com/v1/survey_responses'
        resp1 = {'id': '123', 'comment': 'One',
                 'person': {'id': '123', 'email': 'foo@bar.com'}}
        resp2 = {'id': '456', 'comment': 'Two',
                 'person': {'id': '123', 'email': 'foo@bar.com'}}
        self.mock_response(200, {}, [resp1, resp2])

        survey_responses = delighted.SurveyResponse.all(expand=['person'])
        resp1 = {'person': '123', 'comment': 'One'}
        self.check_call('get', url, get_headers, None, {'expand[]': 'person'})
        self.assertTrue(list is type(survey_responses))
        self.assertTrue(delighted.SurveyResponse is type(survey_responses[0]))
        self.assertEqual(resp1, dict(survey_responses[0]))
        self.assertEqual('One', survey_responses[0].comment)
        self.assertEqual('123', survey_responses[0].id)
        self.assertEqual(delighted.Person, type(survey_responses[0].person))
        self.assertEqual({'email': 'foo@bar.com'}, survey_responses[0].person)
        resp2 = {'person': '123', 'comment': 'Two'}
        self.assertTrue(delighted.SurveyResponse is type(survey_responses[1]))
        self.assertEqual(resp2, dict(survey_responses[1]))
        self.assertEqual('One', survey_responses[0].comment)
        self.assertEqual('123', survey_responses[0].id)
        self.assertEqual(delighted.Person, type(survey_responses[1].person))
        resp2_person = {'email': 'foo@bar.com'}
        self.assertEqual(resp2_person, dict(survey_responses[1].person))

    def test_listing_all_people(self):
        url = 'https://api.delightedapp.com/v1/people'
        person1 = {'id': '123', 'email': 'foo@example.com', 'name': 'Foo Smith'}
        person2 = {'id': '456', 'email': 'bar@example.com', 'name': 'Bar Kim'}
        self.mock_response(200, {}, [person1, person2])

        people = delighted.Person.all()
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(list is type(people))
        self.assertTrue(delighted.Person is type(people[0]))
        self.assertEqual({'email': 'foo@example.com', 'name': 'Foo Smith'}, dict(people[0]))
        self.assertEqual('foo@example.com', people[0].email)
        self.assertEqual('Foo Smith', people[0].name)
        self.assertEqual('123', people[0].id)
        self.assertTrue(delighted.Person is type(people[1]))
        self.assertEqual({'email': 'bar@example.com', 'name': 'Bar Kim'}, dict(people[1]))
        self.assertEqual('Bar Kim', people[1].name)
        self.assertEqual('bar@example.com', people[1].email)
        self.assertEqual('456', people[1].id)

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
