# delighted-python

A CLI client and Python API library for [the delighted platform](https://delightedapp.com/docs/api).

### Install

This can be installed via the [pypi package](https://pypi.python.org/pypi/delighted) using:

    $ pip install delighted

### Usage

    $ export DELIGHTED_APIKEY="your api key here"
    $ python
    >>> from delighted import Delighted
    >>> delighted = Delighted()
    >>> delighted.metrics.get()
    {u'passive_count': 4, u'promoter_percent': 40.74074074074074, u'detractor_percent': 51.85185185185185, u'response_count': 54, u'passive_percent': 7.4074074074074066, u'promoter_count': 22, u'detractor_count': 28, u'nps': -11}

### Run Tests

    $ pytest test