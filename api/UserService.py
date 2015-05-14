from .restservice import RestService

from . import SERVICE_URL

class UserService(RestService):
    @staticmethod
    def Info(id_or_name):
        if isinstance(id_or_name, int):
            return RestService._get(SERVICE_URL.USER + "/%d/info" % id_or_name)
        else:
            assert isinstance(id_or_name, str)
            return RestService._get(SERVICE_URL.USER + "/byname/%s" % id_or_name)

import logging
logger = logging.getLogger(__name__)

from PyQt5.QtCore import *

class Avatar:
    def __init__(self, name, tooltip, url):
        self.name = name
        self.tooltip = tooltip
        self.url = url

class League:
    def __init__(self, league, division):
        self.league = league
        self.division = division

class Rating:
    def __init__(self, mean, deviation):
        self.mean = mean
        self.deviation = deviation

    def readable(self):
        '''
        :return: Human readable rating (int)
        '''
        return max(0, int(round(self.mean - 3*self.deviation, -2)))

class UserInfo(QObject):

    updated = pyqtSignal(object)

    def __init__(self, id_or_name):
        super(UserInfo, self).__init__()

        if isinstance(id_or_name, int):
            self.id = id_or_name
            self.username = None
        else:
            assert isinstance(id_or_name, str)
            self.id = None
            self.username = id_or_name

        self.avatar = None
        self.clan = None
        self.country = None
        self.league = None
        self.rating = None

    def update(self):
        id_or_name = self.id if self.id else self.username

        def _onError(err_code, resp):
            logger.warning('Failed to get info for user "%s": %s', id_or_name, err_code)

        def _onSuccess(resp):

            if not self.id:
                self.id = resp["id"]

            if not self.username:
                self.username = resp['username']
            elif resp['name'] != self.username:
                # Username changed.
                self.username = resp['name']

            for attr in ['clan', 'country']:
                self.__dict__[attr] = resp[attr]

            self.avatar = Avatar(resp['avatar']['name'], resp['avatar']['tooltip'],
                                 resp['avatar']['url'])
            self.league = League(resp['league']['league'], resp['league']['division'])
            self.rating = Rating(resp['rating']['mean'], resp['rating']['deviation'])

            self.updated.emit(self)

        reply = UserService.Info(id_or_name)

        reply.error.connect(_onError)
        reply.done.connect(_onSuccess)
