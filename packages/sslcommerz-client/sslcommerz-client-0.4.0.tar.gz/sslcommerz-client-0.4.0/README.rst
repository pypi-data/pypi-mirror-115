========
Overview
========

A Sane SSLCommerz Client for Python.

* Free software: MIT license

Warning
=======
Under development. Is not usable. At all.

Why?
====

There are at least 5 sdk/library/client for SSLCommerz in PyPI right now including an official one. However, we wanted to create an API client that will take care of a major part of validation (thanks to :code:`pydantic`), will feel intuitive, and allow you to access and inspect data in ease.

Features
=========
* Pydantic powered dataclasses for every request (in request one can also use :code:`dict` that will be converted to a `dataclass`) and response.
* IPN validation.
* Methods for all official endpoints.

Installation
============

::

    pip install sslcommerz-client

You can also install the in-development version with::

    pip install https://gitlab.com/codesigntheory/python-sslcommerz-client/-/archive/master/python-sslcommerz-client-master.zip


Documentation
=============


https://python-sslcommerz-client.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
