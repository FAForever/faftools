
from .restservice import RestService
from . import SERVICE_URL

class AuthService(RestService):
    @staticmethod
    def Register(email, username, password):
        postData = {'email': email,
                    'username': username,
                    'password': password}

        return RestService._post(SERVICE_URL.AUTH + "auth/register", postData)

    @staticmethod
    def Login(client_id, username, password):
        postData = dict(grant_type='password',
                        username = username,
                        password = password,
                        client_id=client_id)

        return RestService._get(SERVICE_URL.AUTH + "oauth/token", **postData)