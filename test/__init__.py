import pytest
import uuid
import random


@pytest.fixture(scope='module')
def location():
    choices = [
        "New York, NY",
        "Austin, TX",
        "San Francisco, CA",
        "Washington, DC"]

    return random.choice(choices)


@pytest.fixture(scope='module')
def operating_system():
    choices = [
        "Android",
        "iOS",
        "Windows",
        "Mac",
        "Linux"]

    return random.choice(choices)


@pytest.fixture(scope='module')
def properties(location, operating_system):
    return {
        'operating_system': operating_system,
        'location': location
    }


@pytest.fixture(scope='module')
def comment():
    choices = [
        "Its's cool",
        "I'm not sure",
        "Can I keep it?"]

    return random.choice(choices)


@pytest.fixture(scope='module')
def person(delighted):

    responses = delighted.survey_response.get()

    warning_msg = "You haven't sent any surveys through Delighted's API, \
        can't get real Person object ids"

    assert len(responses) > 0, warning_msg

    people = []

    for response in responses:
        people.append(response['person'])

    return random.choice(people)


@pytest.fixture(scope='module')
def person_with_email(delighted, email):

    created = delighted.people.create(email)

    return {'id': created['id'], 'email': email }


@pytest.fixture(scope='module')
def score():
    return random.choice(range(1, 11))


@pytest.fixture(scope='module')
def email():
    return 'test@example.com' # % uuid.uuid4()


@pytest.fixture(scope='module')
def delighted():
    from delighted import Delighted

    return Delighted()
