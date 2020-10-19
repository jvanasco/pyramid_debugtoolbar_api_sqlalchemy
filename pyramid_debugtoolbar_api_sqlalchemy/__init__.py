# local
from .panels import SqlalchemyCsvDebugPanel


__VERSION__ = "0.3.0"


# ==============================================================================


def includeme(config):
    """
    Pyramid hook to install this debugtoolbar plugin.

    Update your ENVIRONMENT.ini file

        debugtoolbar.includes = pyramid_debugtoolbar_api_sqlalchemy
    """
    config.add_debugtoolbar_panel(SqlalchemyCsvDebugPanel)
    config.add_route(
        "debugtoolbar.api_sqlalchemy.queries.csv",
        "/api-sqlalchemy/sqlalchemy-{request_id}.csv",
    )
    config.scan("pyramid_debugtoolbar_api_sqlalchemy.views")
    config.commit()


# ==============================================================================
