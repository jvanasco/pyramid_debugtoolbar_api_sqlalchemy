pyramid_debugtoolbar_api_sqlalchemy
===================================

Build Status: ![Python package](https://github.com/jvanasco/pyramid_debugtoolbar_api_sqlalchemy/workflows/Python%20package/badge.svg)

This package extends the existing `pyramid_debugtoolbar` SQLAlchemy Panel to
support downloadable CSV files of profiling data.

This package does not replace the default panel, and requires it to be active.

This package is designed for application profile and to be a useful part of test
suites, allowing developers to run a series of tests and log the SQLAlchemy
performance.

If you are using the debugtoolbar directly:

* If SQLAlchemy queries exist on the request, a "SQLAlchemy CSV" tab will appear.
  That will prompt you for queries.

If you are scripting:

* The urls are generated in a machine-friendly format, so you can regex the
  `request_id` off a page and pull it from the API.  this is explained below:


NOTES:
======

This packages requires pyramid_debugtoolbar 4.0 or newer


How to use this package
=======================


Update your ENVIRONMENT.ini file

    debugtoolbar.includes = pyramid_debugtoolbar_api_sqlalchemy

You MUST be using `pyramid_debugtoolbar` with the SQLAlchemy panel enabled.
This just piggybacks on the existing module's work to log queries.

You MUST use `debugtoolbar.includes`.  This will not work properly via `pyramid.includes`

You can access a csv of the SQLAlchemy report via the following url hack:

    url_html = '/_debug_toolbar/{request_id}'
    url_api =  '/_debug_toolbar/api-sqlalchemy/sqlalchemy-{request_id}.csv'
    
The file will be downloaded and offer a content-disposition as:

    sqlalchemy-{request_id}.csv

The CSV columns are:

* execution timing
* SQLAlchemy query
* query params (json encoded)


Configuration
=======================

By default, this package writes CSV files using "UTF-8" encoding.

To change this, use the environment variable `pyramid_debugtoolbar_api_sqlalchemy_encoding`

	export pyramid_debugtoolbar_api_sqlalchemy_encoding=ascii




