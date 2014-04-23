from test import email, delighted, person, person_with_email, score, comment
from test import properties, location, operating_system
from time import mktime


class TestCreateSurvey(object):

    def now(self):

        from datetime import datetime

        return datetime.now()

    def addSeconds(self, date_time, seconds):

        from datetime import timedelta

        return date_time + timedelta(seconds=seconds)

    def test_create_survey_with_properties(
            self,
            delighted,
            person_with_email,
            score,
            properties):

        start = self.now()
        person_id = person_with_email['id']
        person_email = person_with_email['email']

        response = delighted.survey_response.create(
            person=person_id,
            score=score,
            person_properties=properties)

        assert response['id']
        assert response['person'] == person_id
        assert response['score'] == score
        assert response['created_at'] >= mktime(start.timetuple())

        import time

        time.sleep(1)

        responses = delighted.survey_response.get(person_email=person_email)

        assert len(responses) > 0

        for survey in responses:
            assert survey['person'] == person_id

    def test_create_survey_with_comment(
            self,
            delighted,
            person,
            score,
            comment):

        start = self.now()

        response = delighted.survey_response.create(
            person=person,
            score=score,
            comment=comment)

        assert response['id']
        assert response['person']
        assert response['score'] == score
        assert response['comment'] == comment
        assert response['created_at'] >= mktime(start.timetuple())

    def test_create_survey_only_score(
            self,
            delighted,
            person,
            score):

        start = self.now()

        response = delighted.survey_response.create(
            person=person,
            score=score)

        assert response['id']
        assert response['person']
        assert response['score'] == score
        assert response['comment'] is None
        assert response['created_at'] >= mktime(start.timetuple())


class TestGetSurveys(object):

    def test_get_surveys(self, delighted):

        responses = delighted.survey_response.get()

        assert len(responses) > 0

        for response in responses:
            assert response['id']
            assert response['person']
            assert isinstance(response['score'], int)
            assert isinstance(response['created_at'], int)
            assert isinstance(response['notes'], list)
