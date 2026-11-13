import csv
import os
import re

from pyramid.exceptions import NotFound
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from six import PY2, StringIO, binary_type, text_type

from .spreadsheet_utils import sanitize_spreadsheet_cell
from .utils import get_sqlalchemy_panel


ENCODING = os.environ.get("pyramid_debugtoolbar_api_sqlalchemy_encoding", "utf-8")


@view_config(route_name="debugtoolbar.api_sqlalchemy.queries.csv")
def queries_api_csv(request):
    # type: (Request) -> Response
    """Export the recorded SQL queries for the requested toolbar entry."""
    request_id = request.matchdict["request_id"]
    toolbar = request.pdtb_history.get(request_id, None)
    if toolbar is None:
        raise NotFound

    panel = get_sqlalchemy_panel(toolbar.panels)
    if panel is None:
        raise NotFound

    spreadsheet = request.GET.get("spreadsheet") == "1"
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    for query in panel.data.get("queries", ()):
        sql = query["raw_sql"]
        parameters = query["parameters"]
        if spreadsheet:
            sql = sanitize_spreadsheet_cell(sql)
            if parameters is not None:
                if isinstance(parameters, binary_type):
                    parameters = parameters.decode(ENCODING, "replace")
                else:
                    parameters = text_type(parameters)
                parameters = sanitize_spreadsheet_cell(parameters)
                if PY2:
                    parameters = parameters.encode(ENCODING)
        if PY2:
            sql = sql.encode(ENCODING)
        writer.writerow((query["duration"], sql, parameters))

    response = Response(
        content_type="text/csv", body=csvfile.getvalue(), charset=ENCODING
    )
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", request_id)
    suffix = "-spreadsheet" if spreadsheet else ""
    response.headers["Content-Disposition"] = str(
        'attachment; filename="sqlalchemy-%s%s.csv"' % (safe_id, suffix)
    )
    response.cache_control.no_store = True
    return response
