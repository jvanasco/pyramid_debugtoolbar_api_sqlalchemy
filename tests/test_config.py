# coding=utf-8
from __future__ import print_function
from __future__ import unicode_literals

# stdlib
import re
import unittest

# pyramid testing requirements
from pyramid import testing
from pyramid.exceptions import ConfigurationError
from pyramid.response import Response
from pyramid.request import Request

import sqlalchemy


# ------------------------------------------------------------------------------


# used to ensure the toolbar link is injected into requests
re_toolbar_link = re.compile(r'(?:href="http://localhost)(/_debug_toolbar/[\d]+)"')
re_csv_link = re.compile(
    r'href="(/_debug_toolbar/api-sqlalchemy/sqlalchemy-([\d]+).csv)"'
)


class TestDebugtoolbarPanel_NoSqlAlchemy(unittest.TestCase):
    def setUp(self):
        def view_no_sqlalchemy(request):
            return Response(
                "<html><head></head><body>OK</body></html>", content_type="text/html"
            )

        self.config = config = testing.setUp()
        config.add_settings(
            {"debugtoolbar.includes": ["pyramid_debugtoolbar_api_sqlalchemy"]}
        )
        config.include("pyramid_debugtoolbar")
        self.settings = config.registry.settings

        config.add_view(view_no_sqlalchemy)

    def tearDown(self):
        testing.tearDown()

    def test_panel_injected(self):

        # make the app
        app = self.config.make_wsgi_app()
        # make a request
        req1 = Request.blank("/")
        req1.remote_addr = "127.0.0.1"
        resp1 = req1.get_response(app)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("http://localhost/_debug_toolbar/", resp1.text)

        # check the toolbar
        links = re_toolbar_link.findall(resp1.text)
        self.assertIsNotNone(links)
        self.assertIsInstance(links, list)
        self.assertEqual(len(links), 1)
        toolbar_link = links[0]

        req2 = Request.blank(toolbar_link)
        req2.remote_addr = "127.0.0.1"
        resp2 = req2.get_response(app)
        self.assertEqual(resp2.status_code, 200)

        self.assertIn(
            '<li class="disabled" id="pDebugPanel-sqlalchemy-csv">', resp2.text
        )
        self.assertNotIn(
            '<div id="pDebugPanel-sqlalchemy-csv-content"',
            resp2.text,
        )


class TestDebugtoolbarPanel_HasSqlAlchemy(unittest.TestCase):
    def setUp(self):
        def view_has_sqlalchemy(request):

            engine = sqlalchemy.create_engine("sqlite://")
            conn = engine.connect()
            result = conn.execute(sqlalchemy.sql.text("SELECT NULL;"))
            # toss in another select statement with a unicode party hat
            result = conn.execute(sqlalchemy.sql.text("SELECT NULL; -- 🎉"))
            # make sure we encode bindparams correctly
            stmt = sqlalchemy.sql.text(
                "SELECT NULL = :party_hat or :int or :float or :text or :bool;"
            )
            stmt = stmt.bindparams(
                party_hat="🎉",
                int=1,
                float=1.0,
                text="text",
                bool=False,
            )
            result = conn.execute(stmt)
            return Response(
                "<html><head></head><body>OK</body></html>", content_type="text/html"
            )

        self.config = config = testing.setUp()
        config.add_settings(
            {"debugtoolbar.includes": ["pyramid_debugtoolbar_api_sqlalchemy"]}
        )
        config.include("pyramid_debugtoolbar")
        self.settings = config.registry.settings

        config.add_view(view_has_sqlalchemy)

    def tearDown(self):
        testing.tearDown()

    def test_panel_injected(self):

        # make the app
        app = self.config.make_wsgi_app()
        # make a request
        req1 = Request.blank("/")
        req1.remote_addr = "127.0.0.1"
        resp1 = req1.get_response(app)
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("http://localhost/_debug_toolbar/", resp1.text)

        # check the toolbar
        links = re_toolbar_link.findall(resp1.text)
        self.assertIsNotNone(links)
        self.assertIsInstance(links, list)
        self.assertEqual(len(links), 1)
        toolbar_link = links[0]

        req2 = Request.blank(toolbar_link)
        req2.remote_addr = "127.0.0.1"
        resp2 = req2.get_response(app)
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('<li class="" id="pDebugPanel-sqlalchemy-csv">', resp2.text)
        self.assertIn(
            '<div id="pDebugPanel-sqlalchemy-csv-content"',
            resp2.text,
        )
        self.assertIn(
            "SqlAclhemy queries are available for this request as a CSV via the link below:",
            resp2.text,
        )

        # csv
        match = re_csv_link.search(resp2.text)
        self.assertTrue(match)
        (_csv_link, _id) = match.groups()
        req3 = Request.blank(_csv_link)
        req3.remote_addr = "127.0.0.1"
        resp3 = req3.get_response(app)
        self.assertEqual(resp3.status_code, 200)
        self.assertIn("SELECT NULL;", resp3.text)
