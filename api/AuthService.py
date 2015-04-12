
from .restservice import RestService
from . import SERVICE_URL

class AuthService(RestService):
    @staticmethod
    def Register(email, username, password):
        postData = {'email': email,
                    'username': username,
                    'password': password}

        return RestService._post(SERVICE_URL.AUTH + "/register", postData)

    @staticmethod
    def Login(username, password):
        postData = {'username': username,
                    'password': password}

        return RestService._post(SERVICE_URL.AUTH + "/login", postData)