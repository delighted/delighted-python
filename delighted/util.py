import calendar
import datetime
import time

import six


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        time_tuple = dttime.timetuple()
        if len(time_tuple) == 6:
            time_tuple += (0, 0, 0)
        epoch = time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
        utc_timestamp = time.mktime(time_tuple) - epoch

    return int(utc_timestamp)


def encode(data):
    for key, value in six.iteritems(data):
        if value is None:
            continue
        elif isinstance(value, list) or isinstance(value, tuple):
            for subvalue in value:
                yield ("%s[]" % (key,), subvalue)
        elif isinstance(value, dict):
            subdict = dict(('%s[%s]' % (key, subkey), subvalue) for
                           subkey, subvalue in six.iteritems(value))
            for subkey, subvalue in encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, value)
