from ._version import __VERSION__


# ==============================================================================


def includeme(config):
    """
    Pyramid hook to install this debugtoolbar plugin.

    Update your ENVIRONMENT.ini file

        debugtoolbar.includes = pyramid_debugtoolbar_api_sqlalchemy
    """
    # Legacy setuptools imports this package to discover the version.
    from .panels import SqlalchemyCsvDebugPanel

    config.add_debugtoolbar_panel(SqlalchemyCsvDebugPanel)
    config.add_route(
        "debugtoolbar.api_sqlalchemy.queries.csv",
        "/api-sqlalchemy/sqlalchemy-{request_id}.csv",
    )
    config.scan("pyramid_debugtoolbar_api_sqlalchemy.views")
    config.commit()


# ==============================================================================
