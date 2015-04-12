
from .restservice import RestService

from . import SERVICE_URL

class GamesService(RestService):
    @staticmethod
    def Current():
        return RestService._get(SERVICE_URL.GAMES + "/current")

    @staticmethod
    def Info(game_id):
        return RestService._get(SERVICE_URL.GAMES + "/%d/info" % game_id)

    @staticmethod
    def LiveReplay(game_id):
        return RestService._get(SERVICE_URL.GAMES + "/%d/livereplay" % game_id)

    @staticmethod
    def OpenGame(port, game_params):
        return RestService._post(SERVICE_URL.GAMES + "/open", { 'port': port, 'game_params': game_params })