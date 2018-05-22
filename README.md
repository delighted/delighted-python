[![Build Status](https://travis-ci.org/delighted/delighted-python.svg?branch=master)](https://travis-ci.org/delighted/delighted-python)

# Delighted API Python Client

Official Python client for the [Delighted API](https://delighted.com/docs/api).

## Installation

```
pip install --upgrade delighted
```

or

```
easy_install --upgrade delighted
```

### Upgrading from delighted-python

If you previously used the python package named `delighted-python`, please note that the package name is now just `delighted`.

## Configuration

To get started, you need to configure the client with your secret API key.

```python
import delighted
delighted.api_key = 'YOUR_API_KEY'
```

For further options, read the [advanced configuration section](#advanced-configuration).

**Note:** Your API key is secret, and you should treat it like a password. You can find your API key in your Delighted account, under *Settings* > *API*.

## Usage

Adding/updating people and scheduling surveys:

```python
# Add a new person, and schedule a survey immediately
person1 = delighted.Person.create(email='foo+test1@delighted.com')

# Add a new person, and schedule a survey after 1 minute (60 seconds)
person2 = delighted.Person.create(email='foo+test2@delighted.com', delay=60)

# Add a new person, but do not schedule a survey
person3 = delighted.Person.create(email='foo+test3@delighted.com', send=False)

# Add a new person with full set of attributes, including a custom question
# product name, and schedule a survey with a 30 second delay
person4 = delighted.Person.create(
        email='foo+test4@delighted.com',
        name='Joe Bloggs',
        properties={'customer_id': 123, 'country': 'USA',
                    'question_product_name': 'The London Trench'},
        delay=30)

# Update an existing person (identified by email), adding a name, without
# scheduling a survey
updated_person1 = delighted.Person.create(email='foo+test1@delighted.com',
                                          name='James Scott', send=False)
```

Unsubscribing people:

```python
# Unsubscribe an existing person
delighted.Unsubscribe.create(person_email='foo+test1@delighted.com')
```

Listing people:

```python
# List all people, 20 per page, first 2 pages
delighted.Person.all()
delighted.Person.all(page=2)
```

Listing people who have unsubscribed:

```python
# List all people who have unsubscribed, 20 per page, first 2 pages
delighted.Unsubscribe.all()
delighted.Unsubscribe.all(page=2)
```

Listing people whose emails have bounced:

```python
# List all people whose emails have bounced, 20 per page, first 2 pages
delighted.Bounce.all()
delighted.Bounce.all(page=2)
```

Deleting a person and all of the data associated with them:

```python
# Delete by person id
delighted.Person.delete(id=42)
# Delete by email address
delighted.Person.delete(email='test@example.com')
# Delete by phone number (must be E.164 format)
delighted.Person.delete(phone_number='+14155551212')
```

Deleting pending survey requests

```python
# Delete all pending (scheduled but unsent) survey requests for a person, by email.
delighted.SurveyRequest.delete_pending(person_email='foo+test1@delighted.com')
```

Adding survey responses:

```python
# Add a survey response, score only
survey_response1 = delighted.SurveyResponse.create(person=person1.id,
                                                   score=10)

# Add *another* survey response (for the same person), score and comment
survey_response2 = delighted.SurveyResponse.create(person=person1.id,
                                                   score=5,
                                                   comment='Really nice.')
```

Retrieving a survey response:

```python
# Retrieve an existing survey response
survey_response3 = delighted.SurveyResponse.retrieve('123')
```

Updating survey responses:

```python
# Update a survey response score
survey_response4 = delighted.SurveyResponse.retrieve('234')
survey_response4.score = 10
survey_response4.save
# <delighted.SurveyResponse object at 0xabc123>

# Update (or add) survey response properties
survey_response4.person_properties = {'segment': 'Online'}
survey_response4.save
# <delighted.SurveyResponse object at 0xabc123>

# Update person who recorded the survey response
survey_response4.person = '321'
survey_response4.save
# <delighted.SurveyResponse object at 0xabc123>
```

Listing survey responses:

```python
# List all survey responses, 20 per page, first 2 pages
survey_responses_page1 = delighted.SurveyResponse.all()
survey_responses_page2 = delighted.SurveyResponse.all(page=2)

# List all survey responses, 20 per page, expanding person object
survey_responses_page1_expanded = delighted.SurveyResponse.all(expand=['person'])
survey_responses_page1_expanded[0].person
# <delighted.Person object at 0xabc123>

# List all survey responses, 20 per page, for a specific trend (ID: 123)
survey_responses_page1_trend = delighted.SurveyResponse.all(trend='123')

# List all survey responses, 20 per page, in reverse chronological order (newest first)
survey_responses_page1_desc = delighted.SurveyResponse.all(order='desc')

# List all survey responses, 100 per page, page 5, with a time range
import pytz
timezone = pytz.timezone('America/Chicago')
filtered_survey_responses = delighted.SurveyResponse.all(
    page=5,
    per_page=100,
    since=timezone.localize(datetime.datetime(2014, 3, 1)),
    until=timezone.localize(datetime.datetime(2014, 4, 30))
)
```

Retrieving metrics:

```python
# Get current metrics, 30-day simple moving average, from most recent response
metrics = delighted.Metrics.retrieve()

# Get current metrics, 30-day simple moving average, from most recent response,
# for a specific trend (ID: 123)
metrics = delighted.Metrics.retrieve(trend='123')

# Get metrics, for given time range
import pytz
timezone = pytz.timezone('America/Chicago')
metrics = delighted.Metrics.retrieve(
    since=timezone.localize(datetime.datetime(2013, 10, 1)),
    until=timezone.localize(datetime.datetime(2013, 11, 1))
)
```

## Rate limits

If a request is rate limited, a `TooManyRequestsError` exception is raised. You can rescue that exception to implement exponential backoff or retry strategies. The exception provides a `retry_after` attribute to tell you how many seconds you should wait before retrying. For example:

```python
try:
    metrics = delighted.Metrics.retrieve()
except delighted.errors.TooManyRequestsError as err:
    retry_after_seconds = err.retry_after
    # wait for retry_after_seconds before retrying
    # add your retry strategy here ...
```

## <a name="advanced-configuration"></a> Advanced configuration & testing

The following options are configurable for the client:

```python
delighted.api_key
delighted.api_base_url # default: 'https://api.delighted.com/v1/'
delighted.http_adapter # default: delighted.HTTPAdapter
```

By default, a shared instance of `delighted.Client` is created lazily in `delighted.get_shared_client()`. If you want to create your own client, perhaps for test or if you have multiple API keys, you can:

```python
# Create an custom client instance, and pass as last argument to resource actions
import delighted
from delighted import Client
client = Client(api_key='API_KEY',
                api_base_url='https://api.delighted.com/v1/',
                http_adapter=HTTPAdapter())
metrics_from_custom_client = delighted.Metrics.retrieve(client=client)

# Or, you can set Delighted.shared_client yourself
delighted.shared_client = delighted.Client(
    api_key='API_KEY',
    api_base_url='https://api.delighted.com/v1/',
    http_adapter=delighted.HTTPAdapter()
)
metrics_from_custom_shared_client = delighted.Metrics.retrieve()
```

## Supported versions

- 2.6+, 3.3+ (PyPy supported)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Run the tests (`tox`)
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request

## Releasing

1. Bump the version in `delighted/__init__.py`.
2. Update the README and CHANGELOG as needed.
3. Tag the commit for release.
4. Update the package against PyPI's test server with  `python setup.py sdist upload -r pypitest`.
5. If (4) works, push to PyPI's live servers with `python setup.py sdist upload -r pypi`.

## Author

Originally by [Jason Pearson](https://github.com/kaeawc). Graciously transfered and now officially maintained by Delighted.
