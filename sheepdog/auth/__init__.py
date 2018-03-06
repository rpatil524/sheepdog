"""
This module will depend on the downstream authutils dependency.

eg:
``pip install git+https://git@github.com/NCI-GDC/authutils.git@1.2.3#egg=authutils``
or
``pip install git+https://git@github.com/uc-cdis/authutils.git@1.2.3#egg=authutils``
"""

from cdislogging import get_logger

from authutils import (
    admin_auth,
    authorize_for_project,
    dbgap,
    roles,
    require_admin_auth_header
)
from authutils.auth_driver import AuthDriver
from authutils.federated_user import  FederatedUser

LOGGER = get_logger('sheepdog_auth')
def _log_import_error(module_name):
    """Log which module cannot be imported.

    Just in case this currently short list grows, make it a function.
    """

    LOGGER.info('Unable to import %s, assuming it is not there', module_name)

# planx only modules (for now)

# Separate try blocks in case one gets brought into gdc authutils.
# This is done with try blocks because when sheepdog.api imports
# sheepdog.auth you can't use flask.current_app. It hasn't been
# instantiated yet (application out of context error)

try:
    from authutils import require_auth
except ImportError:
    _log_import_error('require_auth')
