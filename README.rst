A Python client for `the delighted API <https://delightedapp.com/docs/api>`_.

Install
-------

This can be installed via the `pypi package <https://pypi.python.org/pypi/delighted>`_ using::

    $ pip install delighted

Usage
-----

Once you have your API key from Delighted you can quickly use this library from the console::

    $ export DELIGHTED_APIKEY="your api key here"
    $ python
    >>> from delighted import Delighted
    >>> delighted = Delighted()
    >>> delighted.metrics.get()
    {u'passive_count': 4, u'promoter_percent': 40.74074074074074, ... }

Run Tests
---------

You can use `pytest <https://pytest.org/latest/>`_ to run tests from the console::

    $ py.test
