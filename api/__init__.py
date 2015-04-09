
_networkAccessManager = None

def initialize_faftools_api(networkAccessManager):
    global _networkAccessManager
    _networkAccessManager = networkAccessManager

def _get_NAM():
    """
    Get the NetworkAccessManager. Use this function instead of just using the object by reference.

    If you grab the NAM by reference, you might very well grab it as a reference to None,
    before <i>initialize_faftools_api</i> is called.
    """
    return _networkAccessManager

VERSION_SERVICE_URL = "http://api.dev.faforever.com/version"
PATCH_SERVICE_URL = "http://api.dev.faforever.com/patch"

from .restservice import RestService