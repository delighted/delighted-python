import requests
from requests.auth import HTTPBasicAuth
import os.path
import logging
import sys
import time

from .errors import DelightedError, APIKeyMissing, API_ERRORS

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

logger = logging.getLogger('delighted')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

ROOT = 'https://api.delightedapp.com/v1/'


class Delighted(object):
    def __init__(self, apikey=None, debug=False):
        '''Initialize the API client

        Args:
           apikey (str|None): provide your Delighted API key.  If this is left
           as None, we will attempt to get the API key from the following
           locations::
               - DELIGHTED_APIKEY in the environment vars
               - ~/.delighted.key for the user executing the script
               - /etc/delighted.key
           debug (bool): set to True to log all the request and response
           information to the "delighted" logger at the INFO level.  When
           set to false, it will log at the DEBUG level.  By default it will
           write log entries to STDERR
       '''

        self.session = requests.session()

        if debug:
            self.level = logging.INFO
        else:
            self.level = logging.DEBUG
        self.last_request = None

        if apikey is None:
            if 'DELIGHTED_APIKEY' in os.environ:
                apikey = os.environ['DELIGHTED_APIKEY']
            else:
                apikey = self.read_configs()

        if apikey is None:
            raise APIKeyMissing('You must provide an API key from Delighted')

        self.apikey = apikey

        from .people import People
        from .metrics import Metrics
        from .survey_response import SurveyResponse

        self.people = People(self)
        self.metrics = Metrics(self)
        self.survey_response = SurveyResponse(self)

    def get(self, url, params={}):
        '''Actually make the API call with the given params - this should
        only be called by the namespace methods'''

        url = ('%s%s' % (ROOT, url))
        msg = 'GET from %s: %s' % (url, params)

        self.log(msg)
        start = time.time()

        r = requests.get(
            url,
            data=params,
            auth=HTTPBasicAuth('auth', self.apikey))

        return self.get_response(r, url, params, start)

    def post(self, url, params={}):
        '''Actually make the API call with the given params - this should
        only be called by the namespace methods'''

        url = ('%s%s' % (ROOT, url))
        msg = 'POST to %s: %s' % (url, params)

        self.log(msg)
        start = time.time()

        r = requests.post(
            url,
            data=params,
            auth=HTTPBasicAuth('auth', self.apikey))

        return self.get_response(r, url, params, start)

    def delete(self, url, params={}):
        '''Actually make the API call with the given params - this should
        only be called by the namespace methods'''

        url = ('%s%s' % (ROOT, url))
        msg = 'DELETE from %s: %s' % (url, params)

        self.log(msg)
        start = time.time()

        r = requests.delete(
            url,
            data=params,
            auth=HTTPBasicAuth('auth', self.apikey))

        return self.get_response(r, url, params, start)

    def get_response(self, r, url, params, start=time.time()):
        '''Take the result and see if it is an error'''

        try:
            # grab the remote_addr before grabbing the text since the socket
            # will go away
            remote_addr = r.raw._original_response.fp._sock.getpeername()
        except:
            # we use two private fields when getting the remote_addr, to be a
            # little robust against errors
            remote_addr = (None, None)

        response_body = r.text
        complete_time = time.time() - start

        status = r.status_code

        self.log('Received %s in %.2fms: %s' % (
            status,
            complete_time * 1000,
            r.text))

        self.last_request = {
            'url': url,
            'request_body': params,
            'response_body': r.text,
            'remote_addr': remote_addr,
            'response': r,
            'time': complete_time
        }

        try:
            json_result = json.loads(response_body)
        except:
            json_result = {'errors': 'Data Not Found'}

        if status != requests.codes.ok and \
                status != requests.codes.created:
            raise self.cast_error(status, str(json_result['errors']))

        return json_result

    def cast_error(self, status_code, result):
        '''Take a result representing an error and cast it to a specific
        exception if possible (use a generic delighted.errors.DelightedError exception
        for unknown cases)'''

        if status_code in API_ERRORS:
            return API_ERRORS[status_code](result)
        else:
            msg = 'We received an unexpected error: %r' % result['errors']
            return DelightedError(msg)

    def read_configs(self):
        '''Try to read the API key from a series of files if it's not provided
        in code'''
        paths = [os.path.expanduser('~/.mailchimp.key'), '/etc/mailchimp.key']
        for path in paths:
            try:
                f = open(path, 'r')
                apikey = f.read().strip()
                f.close()
                if apikey != '':
                    return apikey
            except:
                pass

        return None

    def log(self, *args, **kwargs):
        '''Proxy access to the mailchimp logger, changing the level based on
        the debug setting'''
        logger.log(self.level, *args, **kwargs)

    def __repr__(self):
        return '<Mailchimp %s>' % self.apikey
