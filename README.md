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
    {u'passive_count': 4, u'promoter_percent': 40.74074074074074, ... }

### Run Tests

    $ py.test
