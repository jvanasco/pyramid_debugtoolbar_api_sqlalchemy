pyramid_debugtoolbar_api_sqla
=============================

This allows for .csv output of sqlalchemy logging

how to use this
===============


1. update your ENVIRONMENT.ini file

	pyramid.includes = ... pyramid_debugtoolbar_api_sqla

You MUST be using  pyramid_debugtoolbar with the SqlAlchemy panel enabled.  This just piggybacks on the existing module.

2. you can access a csv of the SqlAlchemy report via the following url hack:

	url_html = '/_debug_toolbar/34343436383237303838'
	url_api = '/_debug_toolbar_api/34343436383237303838/sqla.csv'

notice these 2 changes on the url

* `/_debug_toolbar` -> `/_debug_toolbar_api`
* `{request_id}` -> `{request_id}/sqla.csv`