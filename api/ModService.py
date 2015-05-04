
from .restservice import RestService

from . import SERVICE_URL

class ModService(RestService):
    @staticmethod
    def Info(id):
        return RestService._get(SERVICE_URL.MOD + "/%d/info" % id)

    @staticmethod
    def Icon(id):
        return RestService._get(SERVICE_URL.MOD + "/%d/icon" % id)

    @staticmethod
    def Search(query, limit=20):
        return RestService._get(SERVICE_URL.MOD + "/search", q=query, l=limit)

