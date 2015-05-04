
_networkAccessManager = None

class __SERVICE_URL:
    "Shall hold service urls as attributes, because it looks pretty."
    def _init(self, domain):
        "Add service url bases in this function definition."

        url_bases = dict(
            AUTH='https://{domain}/',
            VERSION='http://{domain}/version',
            PATCH='http://{domain}/patch',
            GAMES='http://{domain}/games',
            USER='http://{domain}/user',
            MOD='http://{domain}/mod'
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

from .AuthService import AuthService
__all__ = ['AuthService','GamesService','UserService','VersionService']

class FAF_API:
    """
    Should probably be used for all services.

    I am going to use it to implement oauth-ed services.
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self.oauth_token = None

    def Login(self, username, password):
        self.oauth_token = AuthService.Login(self.client_id, username, password)

        return self.oauth_token

__all__ += ['FAF_API']