
_networkAccessManager = None

class __SERVICE_URL:
    "Shall hold service urls as attributes, because it looks pretty."
    def _init(self, domain):
        "Add service url bases in this function definition."

        url_bases = dict(
            AUTH='https://{domain}/auth',
            VERSION='http://{domain}/version',
            PATCH='http://{domain}/patch',
            GAMES='http://{domain}/games',
            USER='http://{domain}/user'
        )

        for name, furl in url_bases.items():
            self.__dict__[name] = furl.format(domain=domain)

SERVICE_URL = __SERVICE_URL()

def initialize_faftools_api(networkAccessManager, api_domain):
    if _networkAccessManager is not None:
        raise RuntimeError('Reinitialization of faftools api.')

    global _networkAccessManager
    _networkAccessManager = networkAccessManager

    SERVICE_URL._init(api_domain)

def _get_NAM():
    """
    Get the NetworkAccessManager. Use this function instead of just using the object by reference.

    If you grab the NAM by reference, you might very well grab it as a reference to None,
    before <i>initialize_faftools_api</i> is called.
    """
    return _networkAccessManager