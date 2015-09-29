import delighted
from . import get_headers, post_headers, DelightedTestCase


class TestResource(DelightedTestCase):
    def setUp(self):
        super(TestResource, self).setUp()

    def test_retrieving_metrics(self):
        data = {'nps': 10}
        url = 'https://api.delightedapp.com/v1/metrics'
        self.mock_response(200, {}, data)

        metrics = delighted.Metrics.retrieve()
        self.check_call('get', url, get_headers, {}, None)
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def test_retrieving_metrics_range(self):
        data = {'nps': 10}
        self.mock_response(200, {}, data)
        since = 1425168000
        until = 1430348400
        url = 'https://api.delightedapp.com/v1/metrics'

        metrics = delighted.Metrics.retrieve(since=since, until=until)
        self.check_call('get', url, get_headers, None, \
            {'since': 1425168000, 'until': 1430348400})
        self.assertTrue(delighted.Metrics is type(metrics))
        self.assertEqual(dict(metrics), data)
        self.assertEqual(metrics.nps, 10)
        self.assertRaises(AttributeError, lambda: metrics.id)

    def test_creating_or_updating_a_person(self):
        email = 'foo@bar.com'
        data = {'id': '123', 'email': email}
        url = 'https://api.delightedapp.com/v1/people'
        self.mock_response(200, {}, data)

        person = delighted.Person.create(email=email)
        self.assertTrue(delighted.Person is type(person))
        self.assertEqual(dict(person), {'email': email})
        self.assertEqual(person.email, email)
        self.assertEqual('123', person.id)
        self.check_call('post', url, post_headers, {'email': email}, None)

    def test_unsubscribing_a_person(self):
        email = 'person@example.com'
        data = {'person_email': email}
        url = 'https://api.delightedapp.com/v1/unsubscribes'
        self.mock_response(200, {}, {'ok': True})

        delighted.Unsubscribe.create(person_email=email)
        self.check_call('post', url, post_headers, data, None)

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
