# stdlib

# pyramid_debugtoolbar

# local
from .panels import SqlalchemyCsvDebugPanel


# ==============================================================================


def includeme(config):
    """
    an earlier version used things like this
        altconfig = config.with_package('pyramid_debugtoolbar')
        altconfig.add_route('debugtoolbar_api_sqla.sqlalchemy_csv', '/_debug_toolbar-api/{request_id}/sqlalchemy.csv')
        altconfig.scan('pyramid_debugtoolbar_api_sqla.views')
        altconfig.commit()
    now we are included within the debugtoolbar , so are under it's prefix (note the routing below)
    this keeps our routes from appearing in the debugtoolbar
    """
    config.registry.settings['debugtoolbar.extra_panels'].append(SqlalchemyCsvDebugPanel)
    config.add_route('debugtoolbar.sqlalchemy_api_csv', '/sqlalchemy-api/sqlalchemy-{request_id}.csv')
    config.scan('pyramid_debugtoolbar_api_sqla.views')
    config.commit()


# ==============================================================================

