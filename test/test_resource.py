import json

import delighted
from delighted.http_response import HTTPResponse
from delighted.resource import (Metrics, Person, SurveyRequest,
                                SurveyResponse, Unsubscribe)
from . import get_headers, post_headers, DelightedTestCase


class TestResource(DelightedTestCase):
    def setUp(self):
        super(TestResource, self).setUp()

        delighted.api_key = 'abc123'

    def test_retrieving_metrics(self):
        data = {'nps': 10}
        url = 'https://api.delightedapp.com/v1/metrics'
        self.mock_response(200, {}, data)

        metrics = delighted.metrics.retrieve()
        self.check_call('get', url, get_headers, {})
        self.assertIs(type(metrics), Metrics)
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        with self.assertRaises(AttributeError):
            metrics.id

    def test_creating_or_updating_a_person(self):
        email = 'foo@bar.com'
        data = {'id': '123', 'email': email}
        url = 'https://api.delightedapp.com/v1/people'
        self.mock_response(200, {}, data)

        person = delighted.person.create(email=email)
        self.assertIs(type(person), Person)
        self.assertEqual(dict(person), data)
        self.assertEqual(person.email, email)
        self.assertEqual('123', person.id)
        self.check_call('post', url, post_headers, {'email': email})

    def test_unsubscribing_a_person(self):
        email = 'person@example.com'
        data = {'person_email': email}
        url = 'https://api.delightedapp.com/v1/unsubscribes'
        self.mock_response(200, {}, {'ok': True})

        survey_response = delighted.unsubscribe.create(person_email=email)
        self.check_call('post', url, post_headers, data)

    def test_deleting_pending_survey_requests_for_a_person(self):
        url ='https://api.delightedapp.com/v1/people/foo%40bar.com/survey_requests/pending'
        self.mock_response(200, {}, {'ok': True})

        result = delighted.survey_request.delete_pending(person_email='foo@bar.com')
        self.assertIs(dict, type(result))
        self.assertEqual({'ok': True }, result)
        self.check_call('delete', url, post_headers, {})

    def test_creating_a_survey_response(self):
        url ='https://api.delightedapp.com/v1/survey_responses'
        data = {'id': '456', 'person': '123', 'score': 10 }
        self.mock_response(200, {}, data)
        survey_response = delighted.survey_response.create(person='123',
                                                           score=10)
        self.assertIs(SurveyResponse, type(survey_response))
        self.assertEqual({'id': '456', 'person': '123', 'score': 10}, dict(survey_response))
        self.assertEqual('123', survey_response.person)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)
        self.check_call('post', url, post_headers, {'person': '123', 'score': 10})

    def test_retrieving_a_survey_response_expand_person(self):
        url = 'https://api.delightedapp.com/v1/survey_responses/456?expand%5B%5D=person'
        data = { 'id': '456',
                 'person': { 'id': '123', 'email': 'foo@bar.com' },
                 'score': 10 }
        self.mock_response(200, {}, data)

        survey_response = delighted.survey_response.retrieve('456', expand=['person'])
        self.assertIs(SurveyResponse, type(survey_response))
        self.assertIs(Person, type(survey_response.person))
        # self.assertEqual({'id': '456', 'person': '123', 'score': 10 }, dir(survey_response))
        self.assertEqual('123', survey_response.person.id)
        # assert_equal({ :email => 'foo@bar.com' }, survey_response.person.to_hash)
        self.assertEqual(10, survey_response.score)
        self.assertEqual('456', survey_response.id)

    def test_updating_a_survey_response(self):
        pass
