# stdlib
import csv

# pyramid
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import NotFound

# pypi
import six
from six import BytesIO, StringIO

import os

# lcoal
from .utils import get_sqlalchemy_panel


ENCODING = os.environ.get("pyramid_debugtoolbar_api_sqlalchemy_ecnoding", "utf-8")

# ==============================================================================


@view_config(route_name="debugtoolbar.api_sqlalchemy.queries.csv")
def queries_api_csv(request):

    history = request.pdtb_history
    try:
        last_request_pair = history.last(1)[0]
    except IndexError:
        last_request_pair = None
        last_request_id = None
    else:
        last_request_id = last_request_pair[0]

    request_id = request.matchdict.get("request_id", last_request_id)
    toolbar = history.get(request_id, None)

    if not toolbar:
        raise NotFound

    sqla_panel = get_sqlalchemy_panel(toolbar.panels)
    if not sqla_panel:
        raise NotFound

    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    for query in sqla_panel.data["queries"]:
        # we need to encode the query in Python2 if we use StringIO
        # we need to encode them in Python3 if we use BytesIO
        csvwriter.writerow(
            (query["duration"], query["raw_sql"].encode(ENCODING), query["parameters"])
        )
    csvfile.seek(0)
    if six.PY3:
        csvfile = BytesIO(csvfile.read().encode(ENCODING))
        csvfile.seek(0)
    as_csv = Response(content_type="text/csv", body_file=csvfile, status=200)
    as_csv.headers["Content-Disposition"] = str(
        "attachment; filename= sqlalchemy-%s.csv" % request_id
    )
    return as_csv
